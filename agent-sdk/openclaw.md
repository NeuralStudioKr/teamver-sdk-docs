# OpenClaw — connecting to Teamver with teamver-agent-sdk

This is the page an engine should follow after installing from PyPI.

## Install

```bash
pip install 'teamver-agent-sdk==0.6.9'
python -c "import teamver_agent_sdk as m; print(m.__version__)"
```

Need **0.6.9+** for Drive file list (`/ai-agents/me/drives/…`). 0.6.8+ for OpenClaw Secret Store sentinels. 0.6.6+ is token-only identity. 0.6.7 drops `/collab/channels` for engines.

## Ask the human for this (and only this)

```bash
python -m teamver_agent_sdk required-env
```

1. `TEAMVER_AGENT_TOKEN` — `tv_ak_*` **or** OpenClaw `oc-sent-v….end` (protected env). Do not treat the sentinel as a misconfigured token.
2. `TEAMVER_MAIN_API_BASE=https://stg-api.teamver.com` on staging (never `https://stg.teamver.com`, that is the website).
3. `TEAMVER_MAIL_AGENT_TOKEN` only if Mail is in scope.

Do **not** ask for `TEAMVER_WORKSPACE_ID` or `TEAMVER_AGENT_ID` unless `/ai-agents/me` is 404 on a stale staging deploy (temporary fallback).

Never request `TEAMVER_INTERNAL_API_KEY`, a user password, or a user JWT.

## Prove the link

Run these **via OpenClaw gateway exec** when the token is a sentinel, so egress can substitute `tv_ak_*`:

```bash
python -m teamver_agent_sdk whoami
python -m teamver_agent_sdk doctor
python -m teamver_agent_sdk channels
python -m teamver_agent_sdk files
```

### GET `/api/v2/ai-agents/me` response example

Main BE, not Agents. `Authorization: Bearer tv_ak_…` (or a sentinel that Gateway substitutes). Full field notes: [api-reference](./api-reference.md#identity--get-ai-agentsme-main-be).

**200**

```json
{
  "workspace_id": "W-1a2b3c",
  "agent_id": "AG2-9f8e7d",
  "name": "한돌",
  "handle": "handol",
  "scopes": ["messages:read", "messages:write", "channels:read"],
  "channels": {
    "items": [
      {"channel_id": "CH-aaa111", "name": "한돌ch2", "visibility": "public"},
      {"channel_id": "CH-bbb222", "name": "한돌ch1", "visibility": "public"}
    ],
    "total": 2
  },
  "drives": {
    "items": [
      {
        "shared_drive_id": "SD-ccc333",
        "name": "한돌 Drive",
        "can_read": true,
        "can_write": true
      }
    ],
    "total": 1
  },
  "dm": {"applied_enabled": true},
  "report_channel_id": "CH-bbb222"
}
```

**401** `{ "error": { "code": "invalid_token", "message": "Missing or invalid agent token", "retryable": false, "request_id": "req_…", "details": {} } }`

CLI `whoami` prints this object (plus SDK `source`). If staging returns **404**, the live Main container does not have the route yet.

Do **not** copy a local `teamver_channels.py` that reimplements ACL fallbacks. Channel list lives in `ChannelClient.list_channels()`. Official script: [examples/openclaw/list_channels.py](https://github.com/NeuralStudioKr/ns-teamver-packages/blob/main/examples/openclaw/list_channels.py).

```python
from teamver_agent_sdk import TeamverAgent

agent = await TeamverAgent.connect()
await agent.channel.list_channels()
await agent.report(text="connected")
await agent.drive.list_files(limit=20)
```

## Bake / OpenClaw image

The OpenClaw engine image installs these packages from **PyPI** (`teamver-agent-sdk==0.6.9`, `teamver-openclaw-adapter==0.1.1`). There is no SDK source tree inside `ns-teamver-agents`.

Channel list is `GET /api/v2/ai-agents/me/accessible-channels` (ACL). Engines never call `/collab/channels`.

Drive file list is `GET /api/v2/ai-agents/me/drives/{shared_drive_id}/files`. Engines never call human JWT `/api/drive/list`. Official script: [examples/openclaw/list_files.py](https://github.com/NeuralStudioKr/ns-teamver-packages/blob/main/examples/openclaw/list_files.py).
