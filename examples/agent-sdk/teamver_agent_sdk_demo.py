#!/usr/bin/env python3
"""TeamverAgent facade 예시 (teamver-agent-sdk-python).

  python teamver_agent_sdk_demo.py --help
  python teamver_agent_sdk_demo.py dry-run
  python teamver_agent_sdk_demo.py surfaces
"""

from __future__ import annotations

import argparse
import asyncio
import json

from _demo_help import DESIGN_EPILOG

from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


async def cmd_dry_run(_: argparse.Namespace) -> None:
    try:
        cfg = TeamverAgentConfig.from_env()
    except Exception as exc:  # noqa: BLE001 — demo
        _print_json({"TeamverAgentConfig.from_env": "failed", "error": str(exc)})
        return
    _print_json(
        {
            "workspace_id": cfg.workspace_id,
            "agent_id": cfg.agent_id,
            "main_api_base": cfg.main_api_base,
            "mail_api_base": cfg.mail_api_base,
            "agent_api_base": cfg.agent_api_base,
            "channel_token_set": bool(cfg.channel_token),
            "mail_agent_token_set": bool(cfg.mail_agent_token),
        }
    )


async def cmd_surfaces(_: argparse.Namespace) -> None:
    agent = TeamverAgent()
    _print_json(
        {
            "facade": "TeamverAgent",
            "lazy_surfaces": ["inbox", "channel", "dm", "drive", "events", "mail", "jobs", "runtime"],
            "config_workspace": agent.config.workspace_id,
            "config_agent": agent.config.agent_id,
        }
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="teamver_agent_sdk_demo.py",
        description="teamver-agent-sdk — Agent unified client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=DESIGN_EPILOG + "\nWorker example: packages/python/teamver-agent-sdk-python/examples/unified_worker.py",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("dry-run", help="Load TeamverAgentConfig.from_env (masked tokens)")
    p.set_defaults(func=cmd_dry_run)

    p = sub.add_parser("surfaces", help="Show TeamverAgent lazy surface names")
    p.set_defaults(func=cmd_surfaces)

    args = parser.parse_args()
    asyncio.run(args.func(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
