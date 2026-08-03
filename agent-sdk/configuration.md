# Configuration — teamver-agent-sdk

Load with `TeamverAgentConfig.from_env()` or `TeamverAgent()`.

## Environment variables

| env | purpose | default |
|-----|---------|---------|
| `TEAMVER_WORKSPACE_ID` | workspace id (`WS-…`) | *(required)* |
| `TEAMVER_AGENT_ID` | agent id (`AGT-…`) | *(required)* |
| `TEAMVER_MAIN_API_BASE` | Main API host (**no** `/api`) | `https://api.teamver.com` |
| `TEAMVER_AGENT_TOKEN` | channel/DM/drive/jobs grant (`tv_ak_*`) | — |
| `TEAMVER_AGENT_API_BASE` | Agents BE host (jobs / heartbeat) | `https://agent-api.teamver.com` |
| `TEAMVER_MAIL_API_BASE` | Mail API host (**no** `/v1`) | `https://mail-api.teamver.com` |
| `TEAMVER_MAIL_AGENT_TOKEN` | mail agent token (`tv_agent_*`) | — |
| `TEAMVER_HTTP_TIMEOUT` | HTTP timeout (seconds) | `30` |
| `TEAMVER_AGENT_LOG_LEVEL` | log level | `INFO` |
| `TEAMVER_RUNTIME_HEARTBEAT_INTERVAL` | heartbeat interval (seconds) | `30` |

Production API hosts are hardcoded in the SDK (`teamver-sdk-core` defaults). Override with env for staging.

## Token rules

| Token | Prefix | Used for |
|-------|--------|----------|
| Channel / Jobs | `tv_ak_*` | Main collab + Agents BE ops |
| Mail | `tv_agent_*` | Mail BE `/v1/agent/*` |

Do **not** put user passwords or `TEAMVER_INTERNAL_API_KEY` in the agent runtime.

## Capability flags

| Property | True when |
|----------|-----------|
| `channel_enabled` | channel base + `tv_ak_*` |
| `mail_enabled` | mail base + `tv_agent_*` |
| `jobs_enabled` | agent API base + `tv_ak_*` |

## Explicit config

```python
from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig

cfg = TeamverAgentConfig(
    workspace_id="WS-…",
    agent_id="AGT-…",
    channel_token="tv_ak_…",
    # main_api_base / agent_api_base / mail_api_base optional (defaults apply in from_env)
)
agent = TeamverAgent(cfg)
```
