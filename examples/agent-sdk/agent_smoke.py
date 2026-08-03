#!/usr/bin/env python3
"""Host-built agent wheels → Docker pip install 예시 시나리오.

1) env / capability 확인
2) AgentToolAdapter 도구 스키마 로드
3) (channel) 채널 목록 · 선택적 테스트 post
4) (mail) inbox 목록
5) (jobs) active jobs 목록
6) heartbeat

단계 사이에 TEAMVER_STEP_SLEEP_SEC(기본 2초) sleep.
토큰 값은 로그에 출력하지 않는다.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from typing import Any


def _env(name: str, default: str = "") -> str:
    raw = (os.getenv(name) or default).strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        raw = raw[1:-1]
    return raw


def _debug_enabled() -> bool:
    return _env("TEAMVER_DEBUG", "0").lower() in ("1", "true", "yes", "on")


_SCENARIO_ENV_KEYS = (
    "TEAMVER_WORKSPACE_ID",
    "TEAMVER_AGENT_ID",
    "TEAMVER_MAIN_API_BASE",
    "TEAMVER_AGENT_TOKEN",
    "TEAMVER_AGENT_API_BASE",
    "TEAMVER_MAIL_API_BASE",
    "TEAMVER_MAIL_AGENT_TOKEN",
    "TEAMVER_SMOKE_CHANNEL_ID",
    "TEAMVER_MAIL_INBOX_STATUS",
    "TEAMVER_STEP_SLEEP_SEC",
    "TEAMVER_DEBUG",
)

_SECRET_KEYS = frozenset({"TEAMVER_AGENT_TOKEN", "TEAMVER_MAIL_AGENT_TOKEN"})


def _format_env_value(name: str, effective: str) -> str:
    if name in _SECRET_KEYS:
        if not effective:
            return "(unset)"
        prefix = effective[:8] if len(effective) >= 8 else effective[:3]
        return f"<set, len={len(effective)}, prefix={prefix}…>"
    if not effective:
        return "(unset)"
    return effective


def _print_effective_env(*, command: str) -> None:
    print("=== 환경 변수 (프로세스에 실제 적용된 값) ===")
    print(
        "  env 주입: `bash run.sh` → 같은 디렉터리 `.env` 가 있으면 "
        "`docker run --env-file .env` 로 컨테이너에 전달됩니다."
    )
    print(f"  command={command}")
    for key in _SCENARIO_ENV_KEYS:
        raw = (os.getenv(key) or "").strip()
        default = "2" if key == "TEAMVER_STEP_SLEEP_SEC" else ""
        if key == "TEAMVER_MAIL_INBOX_STATUS":
            default = "queued"
        effective = _env(key, default)
        print(f"  {key}={_format_env_value(key, effective)}")
        if raw and key not in _SECRET_KEYS and effective != raw:
            print(f"    (raw had outer quotes — stripped)")
    print()


def _step_sleep_sec() -> float:
    raw = _env("TEAMVER_STEP_SLEEP_SEC", "2")
    try:
        return max(0.0, float(raw))
    except ValueError:
        return 2.0


async def _pause(label: str) -> None:
    sec = _step_sleep_sec()
    if sec <= 0:
        return
    print(f"… {label} 후 {sec:g}초 대기")
    await asyncio.sleep(sec)


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def _as_list(payload: Any) -> list[Any]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("items", "results", "channels", "events", "jobs", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


async def cmd_dry_run(_: argparse.Namespace) -> int:
    _print_effective_env(command="dry-run")
    from teamver_agent_sdk import AgentToolAdapter, TeamverAgent, TeamverAgentConfig

    cfg_ok: dict[str, Any]
    try:
        cfg = TeamverAgentConfig.from_env()
        cfg_ok = {
            "workspace_id": cfg.workspace_id,
            "agent_id": cfg.agent_id,
            "channel_enabled": cfg.channel_enabled,
            "mail_enabled": cfg.mail_enabled,
            "jobs_enabled": cfg.jobs_enabled,
            "main_api_base": cfg.main_api_base,
            "mail_api_base": cfg.mail_api_base,
            "agent_api_base": cfg.agent_api_base,
            "channel_token_set": bool(cfg.channel_token),
            "mail_agent_token_set": bool(cfg.mail_agent_token),
        }
    except Exception as exc:  # noqa: BLE001 — demo
        cfg_ok = {"TeamverAgentConfig.from_env": "failed", "error": str(exc)}

    tools: list[str] = []
    try:
        # dry-run: config 실패해도 도구 이름 목록은 정적 스키마로 표시
        from teamver_agent_sdk import tool_json_schemas

        tools = [t.get("name", "?") for t in tool_json_schemas()]
    except Exception as exc:  # noqa: BLE001
        tools = [f"error:{exc}"]

    _print_json(
        {
            "mode": "dry-run",
            "config": cfg_ok,
            "scenario": [
                "load TeamverAgent + AgentToolAdapter",
                "list agent tool schemas",
                "channel.list_channels (if channel_enabled)",
                "optional channel.post_message (TEAMVER_SMOKE_CHANNEL_ID)",
                "dm.list_threads (if channel_enabled)",
                "drive.list_files personal (if channel_enabled)",
                "mail.list_inbox (if mail_enabled)",
                "jobs.list active (if jobs_enabled)",
                "runtime.heartbeat (if jobs_enabled)",
            ],
            "agent_tools": tools,
            "step_sleep_sec": _step_sleep_sec(),
            "packages": [
                "teamver-sdk-core (host wheel)",
                "teamver-mail-agent (host wheel)",
                "teamver-agent-sdk (host wheel)",
            ],
            "docs": [
                "docs_reference/agent/01_개발자_Teamver_연동_가이드.md",
                "docs_reference/agent/02_Agent_Teamver_연동_가이드.md",
            ],
            "note": "Live: python agent_smoke.py run (needs TEAMVER_* tokens)",
        }
    )
    # silence unused import warning for dry-run path clarity
    _ = (TeamverAgent, AgentToolAdapter)
    return 0


async def run_scenario(_: argparse.Namespace) -> int:
    from teamver_agent_sdk import (
        AgentToolAdapter,
        TeamverAgent,
        TeamverAgentAPIError,
        TeamverAgentConfigError,
    )
    from teamver_mail_agent.errors import MailAgentAPIError

    _print_effective_env(command="run")

    try:
        agent = TeamverAgent()
    except TeamverAgentConfigError as exc:
        print(f"CONFIG_ERROR: {exc}", file=sys.stderr)
        print("  → TEAMVER_WORKSPACE_ID / TEAMVER_AGENT_ID 및 surface env를 확인하세요.", file=sys.stderr)
        return 2

    adapter = AgentToolAdapter(agent)
    exit_code = 0

    try:
        # 1) capability + tools
        print("=== 1) capability · agent tools ===")
        caps = {
            "workspace_id": agent.config.workspace_id,
            "agent_id": agent.config.agent_id,
            "channel_enabled": agent.config.channel_enabled,
            "mail_enabled": agent.config.mail_enabled,
            "jobs_enabled": agent.config.jobs_enabled,
        }
        _print_json(caps)
        tools = adapter.list_tools()
        print(f"agent tools: {len(tools)}")
        for t in tools:
            print(f"  - {t.get('name')}: {t.get('description')}")
        if _debug_enabled() and tools:
            print("--- sample tool schema (first) ---")
            _print_json(tools[0])
        await _pause("capability")

        # 2) channel list (+ optional post)
        print("=== 2) channel ===")
        if agent.config.channel_enabled:
            try:
                channels = await adapter.dispatch("teamver_channel_list", {})
                items = _as_list(channels) if not isinstance(channels, dict) else (
                    _as_list(channels) or [channels]
                )
                print(f"channels payload keys/type: {type(channels).__name__}")
                if isinstance(channels, dict):
                    print(f"  top-level keys: {list(channels.keys())[:20]}")
                for i, ch in enumerate(items[:15], start=1):
                    if isinstance(ch, dict):
                        cid = ch.get("id") or ch.get("channel_id")
                        name = ch.get("name") or ch.get("title") or ""
                        print(f"  [{i}] id={cid!r} name={name!r}")
                    else:
                        print(f"  [{i}] {ch!r}")

                smoke_ch = _env("TEAMVER_SMOKE_CHANNEL_ID")
                if smoke_ch:
                    print(f"→ TEAMVER_SMOKE_CHANNEL_ID={smoke_ch} 테스트 post")
                    posted = await adapter.dispatch(
                        "teamver_channel_post",
                        {
                            "channel_id": smoke_ch,
                            "text": "[agent_smoke] Docker host-wheel smoke OK",
                            "idempotency_key": "agent-docker-smoke-1",
                        },
                    )
                    _print_json(posted if isinstance(posted, dict) else {"result": posted})
                else:
                    print("  (TEAMVER_SMOKE_CHANNEL_ID 비움 — post 생략)")
            except (TeamverAgentAPIError, Exception) as exc:
                print(f"channel 오류: {type(exc).__name__}: {exc}", file=sys.stderr)
                exit_code = 1
        else:
            print("  channel_enabled=false — skip")
        await _pause("channel")

        # 2b) dm + drive (same tv_ak_*)
        print("=== 2b) dm · drive ===")
        if agent.config.channel_enabled:
            try:
                threads = await adapter.dispatch("teamver_dm_list_threads", {"limit": 5})
                if isinstance(threads, dict):
                    print(f"dm threads keys: {list(threads.keys())[:12]}")
                    print(f"dm items: {len(_as_list(threads))}")
                drives = await adapter.dispatch("teamver_drive_list_drives", {})
                print(f"shared drives: {len(_as_list(drives) if isinstance(drives, dict) else drives)}")
                files = await adapter.dispatch(
                    "teamver_drive_list_files",
                    {"drive_id": "personal", "limit": 5},
                )
                print(f"personal files: {len(_as_list(files) if isinstance(files, dict) else files)}")
            except Exception as exc:  # noqa: BLE001
                print(f"dm/drive 오류: {type(exc).__name__}: {exc}", file=sys.stderr)
                exit_code = 1
        else:
            print("  channel_enabled=false — dm/drive skip")
        await _pause("dm/drive")

        # 3) mail inbox
        print("=== 3) mail inbox ===")
        if agent.config.mail_enabled:
            try:
                status = _env("TEAMVER_MAIL_INBOX_STATUS", "queued") or "queued"
                inbox = await adapter.dispatch(
                    "teamver_mail_list_inbox",
                    {"status": status, "limit": 10},
                )
                if hasattr(inbox, "model_dump"):
                    inbox = inbox.model_dump()
                items = []
                if isinstance(inbox, dict):
                    items = _as_list(inbox)
                    print(f"inbox keys: {list(inbox.keys())[:20]}")
                elif isinstance(inbox, list):
                    items = inbox
                print(f"inbox items (status={status}): {len(items)}")
                for i, item in enumerate(items[:10], start=1):
                    if isinstance(item, dict):
                        mid = item.get("message_id") or item.get("id")
                        subj = item.get("subject") or ""
                        print(f"  [{i}] message_id={mid!r} subject={subj!r}")
                    else:
                        print(f"  [{i}] {item!r}")
            except (MailAgentAPIError, TeamverAgentAPIError, Exception) as exc:
                print(f"mail 오류: {type(exc).__name__}: {exc}", file=sys.stderr)
                exit_code = 1
        else:
            print("  mail_enabled=false — skip")
        await _pause("mail")

        # 4) jobs
        print("=== 4) jobs (active) ===")
        if agent.config.jobs_enabled:
            try:
                jobs = await adapter.dispatch("teamver_jobs_list_active", {"limit": 10})
                if isinstance(jobs, dict):
                    print(f"jobs keys: {list(jobs.keys())[:20]}")
                    job_items = _as_list(jobs)
                elif isinstance(jobs, list):
                    job_items = jobs
                else:
                    job_items = []
                print(f"active jobs: {len(job_items)}")
                for i, job in enumerate(job_items[:10], start=1):
                    if isinstance(job, dict):
                        print(
                            f"  [{i}] id={job.get('id')!r} "
                            f"title={job.get('title')!r} status={job.get('status')!r}"
                        )
                    else:
                        print(f"  [{i}] {job!r}")
            except (TeamverAgentAPIError, Exception) as exc:
                print(f"jobs 오류: {type(exc).__name__}: {exc}", file=sys.stderr)
                exit_code = 1
        else:
            print("  jobs_enabled=false — skip (TEAMVER_AGENT_API_BASE 필요)")
        await _pause("jobs")

        # 5) heartbeat
        print("=== 5) heartbeat ===")
        if agent.config.jobs_enabled:
            try:
                await adapter.dispatch(
                    "teamver_heartbeat",
                    {
                        "operational_status": "idle",
                        "active_job_count": 0,
                        "version": "agent-docker-smoke",
                    },
                )
                print("OK heartbeat")
            except (TeamverAgentAPIError, Exception) as exc:
                print(f"heartbeat 오류: {type(exc).__name__}: {exc}", file=sys.stderr)
                exit_code = 1
        else:
            print("  jobs_enabled=false — heartbeat skip")
        await _pause("heartbeat")

        print("=== 시나리오 완료 ===")
        return exit_code
    finally:
        await agent.aclose()


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="agent_smoke.py",
        description=(
            "Host에서 빌드한 teamver agent wheel을 Docker에 복사·pip install 한 뒤 "
            "capability → tools → channel → mail → jobs → heartbeat 시나리오를 실행합니다."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "빌드: bash build_wheels.sh\n"
            "실행: bash run.sh   또는  bash run.sh dry-run\n"
            "문서: README.md · docs_reference/agent/"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("dry-run", help="네트워크 없이 설정·시나리오·도구 목록만 출력")
    p.set_defaults(func=cmd_dry_run)

    p = sub.add_parser("run", help="live Teamver agent 시나리오 실행")
    p.set_defaults(func=run_scenario)

    args = parser.parse_args()
    return asyncio.run(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
