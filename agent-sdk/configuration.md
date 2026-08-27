# Configuration — teamver-agent-sdk

Load with `TeamverAgentConfig.from_env()` or `TeamverAgent()`.

Product tokens and trust boundaries: Agents Console injects secrets into OpenClaw `openclaw.env` (Desired → VM Manager). Do **not** put `TEAMVER_INTERNAL_API_KEY` or user JWTs in the engine. ACL in the Console is **policy**; `tv_ak_*` is the **runtime key**. Both are required to write to channels / Drive / DM.

## Environment variables

| env | purpose | default |
|-----|---------|---------|
| `TEAMVER_WORKSPACE_ID` | workspace id (`W-…`; legacy `WS-…` accepted) | *(required)* |
| `TEAMVER_AGENT_ID` | agent id (`AG2-…`; legacy `AGT-…` accepted) | *(required)* |
| `TEAMVER_MAIN_API_BASE` | Main API host (**no** `/api`) | `https://api.teamver.com` |
| `TEAMVER_AGENT_TOKEN` | channel/DM/drive/jobs grant (`tv_ak_*`) | — |
| `TEAMVER_AGENT_API_BASE` | Agents BE host (jobs / heartbeat) | `https://agent-api.teamver.com` |
| `TEAMVER_AGENTS_API_BASE` | alias of Agents BE host | used if `TEAMVER_AGENT_API_BASE` is unset (OpenClaw CP inject) |
| `TEAMVER_MAIL_API_BASE` | Mail API host (**no** `/v1`) | `https://mail-api.teamver.com` |
| `TEAMVER_MAIL_AGENT_TOKEN` | mail agent token (`tv_agent_*`) | — |
| `TEAMVER_HTTP_TIMEOUT` | HTTP timeout (seconds) | `30` |
| `TEAMVER_AGENT_LOG_LEVEL` | log level | `INFO` |
| `TEAMVER_RUNTIME_HEARTBEAT_INTERVAL` | heartbeat interval (seconds) | `30` |

Production API hosts are hardcoded in the SDK (`teamver-sdk-core` defaults). Override with env for staging.

OpenClaw may also have `TEAMVER_CONTROL_PLANE_TOKEN` (`tv_cp_*`). **This package does not read it.** Channel / DM / Drive / Mail go through `tv_ak_*` and `tv_agent_*`.

## Token rules

| Token | Prefix | Used for |
|-------|--------|----------|
| Channel / DM / Drive / Jobs | `tv_ak_*` | Main collab + Agents BE ops |
| Mail | `tv_agent_*` | Mail BE `/v1/agent/*` |
| Control plane | `tv_cp_*` | Engine → Agents CP only (not this SDK) |

Do **not** put user passwords or `TEAMVER_INTERNAL_API_KEY` in the agent runtime.

## Capability flags

| Property | True when |
|----------|-----------|
| `channel_enabled` | Main base + `tv_ak_*` |
| `mail_enabled` | mail base + `tv_agent_*` |
| `jobs_enabled` | agent API base + `tv_ak_*` |

## Explicit config

```python
from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig

cfg = TeamverAgentConfig(
    workspace_id="W-…",
    agent_id="AG2-…",
    channel_token="tv_ak_…",
    # main_api_base / agent_api_base / mail_api_base optional (defaults apply in from_env)
)
agent = TeamverAgent(cfg)
```
