# OpenClaw — connecting to Teamver with teamver-agent-sdk

This is the page an engine should follow after installing from PyPI.

## Install

```bash
pip install 'teamver-agent-sdk==0.6.8'
python -c "import teamver_agent_sdk as m; print(m.__version__)"
```

Need **0.6.8+** for OpenClaw Secret Store sentinels. 0.6.6+ is token-only identity. 0.6.7 drops `/collab/channels` for engines.

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
```

Do **not** copy a local `teamver_channels.py` that reimplements ACL fallbacks. Channel list lives in `ChannelClient.list_channels()`. Official script: [examples/openclaw/list_channels.py](https://github.com/NeuralStudioKr/ns-teamver-packages/blob/main/examples/openclaw/list_channels.py).

```python
from teamver_agent_sdk import TeamverAgent

agent = await TeamverAgent.connect()
await agent.channel.list_channels()
await agent.report(text="connected")
await agent.drive.list_files(limit=20)
```

## Bake / OpenClaw image

The OpenClaw engine image installs these packages from **PyPI** (`teamver-agent-sdk==0.6.8`, `teamver-openclaw-adapter==0.1.1`). There is no SDK source tree inside `ns-teamver-agents`.

Channel list is `GET /api/v2/ai-agents/me/accessible-channels` (ACL). Engines never call `/collab/channels`.
