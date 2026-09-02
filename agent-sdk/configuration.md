# Configuration — teamver-agent-sdk

Load with `TeamverAgentConfig.from_env()`, `TeamverAgentConfig.from_token("tv_ak_…")`, or `await TeamverAgent.connect()`.

Product tokens and trust boundaries: Agents Console injects secrets into OpenClaw `openclaw.env` (Desired → VM Manager). Do **not** put `TEAMVER_INTERNAL_API_KEY` or user JWTs in the engine. ACL in the Console is **policy**; `tv_ak_*` is the **runtime key**. Both are required to write to channels / Drive / DM.

## What a human must provide

| | |
|--|--|
| **Required** | `TEAMVER_AGENT_TOKEN` (`tv_ak_*` or OpenClaw `oc-sent-v….end`) |
| **Optional (staging)** | `TEAMVER_MAIN_API_BASE=https://stg-api.teamver.com` |
| **Optional (mail)** | `TEAMVER_MAIL_AGENT_TOKEN` (`tv_agent_*`) |
| **Auto-discovered** | `workspace_id`, `agent_id`, accessible channels, drives, default report channel |
| **Never send** | `TEAMVER_INTERNAL_API_KEY`, user password, user JWT |

Print the same contract without a network call:

```bash
python -m teamver_agent_sdk required-env
```

Python: `from teamver_agent_sdk import describe_setup`.

## Environment variables

| env | purpose | default |
|-----|---------|---------|
| `TEAMVER_AGENT_TOKEN` | channel/DM/drive/jobs grant (`tv_ak_*` or `oc-sent-v….end`) | **required** to talk to Main |
| `TEAMVER_ALLOW_SECRET_REF` | `1` skips prefix checks (JWT still rejected) | unset |
| `TEAMVER_WORKSPACE_ID` | workspace id (`W-…`; legacy `WS-…`) | *optional — `GET /api/v2/ai-agents/me`* |
| `TEAMVER_AGENT_ID` | agent id (`AG2-…`; legacy `AGT-…`) | *optional — same* |
| `TEAMVER_MAIN_API_BASE` | Main API host (**no** `/api`) | `https://api.teamver.com` |
| `TEAMVER_AGENT_API_BASE` | Agents BE host (jobs / heartbeat) | `https://agent-api.teamver.com` |
| `TEAMVER_AGENTS_API_BASE` | alias of Agents BE host | used if `TEAMVER_AGENT_API_BASE` is unset (OpenClaw CP inject) |
| `TEAMVER_MAIL_API_BASE` | Mail API host (**no** `/v1`) | `https://mail-api.teamver.com` |
| `TEAMVER_MAIL_AGENT_TOKEN` | mail agent token (`tv_agent_*`) | — |
| `TEAMVER_CONTROL_PLANE_TOKEN` | Agents whoami fallback (`tv_cp_*`) | — (identity only; not for channel/Drive) |
| `TEAMVER_HTTP_TIMEOUT` | HTTP timeout (seconds) | `30` |
| `TEAMVER_AGENT_LOG_LEVEL` | log level | `INFO` |
| `TEAMVER_RUNTIME_HEARTBEAT_INTERVAL` | heartbeat interval (seconds) | `30` |

Production API hosts are hardcoded in the SDK (`teamver-sdk-core` defaults). Override with env for staging.

If ids are already injected (VM `openclaw.env`), the SDK uses them and does not need `/me`. If they are missing, it discovers them. OpenClaw must **not** treat missing ids as a reason to block and ask the human.

## Token rules

| Token | Prefix | Used for |
|-------|--------|----------|
| Channel / DM / Drive / Jobs | `tv_ak_*` or OpenClaw `oc-sent-v….end` | Main collab + identity `/me` + Agents BE ops |
| Mail | `tv_agent_*` or the same sentinel form | Mail BE `/v1/agent/*` |
| Control plane | `tv_cp_*` | Identity fallback `GET /api/v2/engine/whoami` only |
| Other secret managers | `TEAMVER_ALLOW_SECRET_REF=1` | Skip prefix; **user JWT (`eyJ…`) is still rejected** |

OpenClaw Secret Store injects a process-local sentinel. The Gateway substitutes the real `tv_ak_*` only on outbound HTTPS. Run `whoami` / `doctor --probe` / `channels` / `files` / `dm` **via gateway exec**, not a local shell that never hits that proxy.

```bash
# Recommended (OpenClaw VM)
python -m teamver_agent_sdk doctor --probe
```

Do **not** put user passwords or `TEAMVER_INTERNAL_API_KEY` in the agent runtime.

## Capability flags

| Property | True when |
|----------|-----------|
| `channel_enabled` | Main base + `tv_ak_*` |
| `mail_enabled` | mail base + `tv_agent_*` |
| `jobs_enabled` | agent API base + `tv_ak_*` |
| `identity_deferred` | workspace or agent id still empty |

## Explicit config

```python
from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig

cfg = TeamverAgentConfig.from_token("tv_ak_…")
agent = await TeamverAgent.connect(cfg)
```

Ids in the constructor remain valid for tests and for VMs that already inject `W-` / `AG2-`.
