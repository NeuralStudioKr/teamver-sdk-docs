# Quick start — teamver-agent-sdk

## 1. Set the token

```bash
export TEAMVER_AGENT_TOKEN="tv_ak_…"          # required — channel / DM / Drive / jobs
# staging / private Main only:
# export TEAMVER_MAIN_API_BASE="https://stg-api.example"
# optional mail:
# export TEAMVER_MAIL_AGENT_TOKEN="tv_agent_…"
```

`TEAMVER_WORKSPACE_ID` and `TEAMVER_AGENT_ID` are **optional**. If they are missing, `TeamverAgent.connect()` calls `GET /api/v2/ai-agents/me` and fills them. Do not ask a human to paste `W-…` / `AG2-…` from the web UI.

API hosts default to production when unset (see [configuration.md](./configuration.md)).

Check what you still need:

```bash
python -m teamver_agent_sdk required-env
python -m teamver_agent_sdk whoami
```

## 2. Run

```python
import asyncio
from teamver_agent_sdk import TeamverAgent

async def main():
    agent = await TeamverAgent.connect()  # token → identity + ACL

    who = await agent.whoami()
    print(who["workspace_id"], who["agent_id"])

    channels = await agent.channel.list_channels()  # ACL accessible-channels
    await agent.report(text="Hello from agent")     # default report channel

    files = await agent.drive.list_files(limit=20)
    threads = await agent.dm.list_threads(limit=10)

    await agent.aclose()

asyncio.run(main())
```

Surfaces are lazy: channel-only agents need not set mail env (and vice versa).

### Function-calling / OpenClaw tools

Install [`teamver-agent-skills`](../agent-skills/) (not a Codex `SKILL.md`):

```python
from teamver_agent_skills import AgentToolAdapter

adapter = AgentToolAdapter(agent)
await adapter.dispatch("teamver_whoami", {})
await adapter.dispatch("teamver_channel_list", {})
await adapter.dispatch("teamver_report", {"text": "hello"})
```

## 3. More

- [API reference](./api-reference.md)
- [Agent guide](./guide.md)
- [agent-skills](../agent-skills/) — registry · OpenClaw/Hermes
- [Examples](../examples/agent-sdk/)
