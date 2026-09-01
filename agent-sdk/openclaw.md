# OpenClaw — connecting to Teamver with teamver-agent-sdk

This is the page an engine should follow after installing from PyPI.

## Install

```bash
pip install teamver-agent-sdk
python -c "import teamver_agent_sdk as m; print(m.__version__)"
```

Need **0.6.6+**. 0.6.5 still required humans to paste workspace/agent ids.

## Ask the human for this (and only this)

```bash
python -m teamver_agent_sdk required-env
```

1. `TEAMVER_AGENT_TOKEN` starting with `tv_ak_`
2. `TEAMVER_MAIN_API_BASE` only if this is not production (`https://api.teamver.com`)
3. `TEAMVER_MAIL_AGENT_TOKEN` (`tv_agent_*`) only if Mail is in scope

Do **not** ask for `TEAMVER_WORKSPACE_ID` or `TEAMVER_AGENT_ID`. Those are not “login and copy from the website” values for the engine. The token is the identity; `GET /api/v2/ai-agents/me` returns workspace, agent id, ACL channels, and drives.

Never request `TEAMVER_INTERNAL_API_KEY`, a user password, or a user JWT.

## Prove the link

```bash
export TEAMVER_AGENT_TOKEN="tv_ak_…"
python -m teamver_agent_sdk whoami
```

Then in Python:

```python
from teamver_agent_sdk import TeamverAgent

agent = await TeamverAgent.connect()
await agent.channel.list_channels()
await agent.report(text="connected")
await agent.drive.list_files(limit=20)
```

Tools: `teamver_whoami` → `teamver_channel_list` → `teamver_report` / `teamver_drive_list_files`.
