# Quick start — teamver-agent-sdk

## 1. Set identity + tokens

```bash
export TEAMVER_WORKSPACE_ID="W-…"
export TEAMVER_AGENT_ID="AG2-…"
export TEAMVER_AGENT_TOKEN="tv_ak_…"          # channel / DM / Drive / jobs
# optional mail:
export TEAMVER_MAIL_AGENT_TOKEN="tv_agent_…"
```

API hosts default to production when unset (see [configuration.md](./configuration.md)).

## 2. Run

```python
import asyncio
from teamver_agent_sdk import TeamverAgent

async def main():
    agent = TeamverAgent()  # TeamverAgentConfig.from_env()

    # Channel report
    await agent.report(text="Hello from agent", channel_id="CH-…")

    # Drive / DM (same tv_ak_* token)
    files = await agent.drive.list_files(drive_id="personal", limit=20)
    threads = await agent.dm.list_threads(limit=10)

    await agent.aclose()

asyncio.run(main())
```

Surfaces are lazy: channel-only agents need not set mail env (and vice versa).

### Function-calling / OpenClaw tools

Install [`teamver-agent-skills`](../agent-skills/) (not a Codex `SKILL.md`):

```python
from teamver_agent_skills import AgentToolAdapter
# or OpenClaw: from teamver_openclaw_adapter import OpenClawToolBridge

adapter = AgentToolAdapter(agent)
tools = adapter.list_tools()
await adapter.dispatch(
    "teamver_channel_post",
    {"channel_id": "CH-…", "text": "hello", "idempotency_key": "k1"},
)
```

## 3. More

- [API reference](./api-reference.md)
- [Agent guide](./guide.md)
- [agent-skills](../agent-skills/) — registry · OpenClaw/Hermes
- [Examples](../examples/agent-sdk/)
