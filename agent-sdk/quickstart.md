# Quick start — teamver-agent-sdk

## 1. Set identity + tokens

```bash
export TEAMVER_WORKSPACE_ID="WS-…"
export TEAMVER_AGENT_ID="AGT-…"
export TEAMVER_AGENT_TOKEN="tv_ak_…"          # channel / DM / Drive / jobs
# optional mail:
export TEAMVER_MAIL_AGENT_TOKEN="tv_agent_…"
```

API hosts default to production when unset (see [configuration.md](./configuration.md)).

## 2. Run

```python
import asyncio
from teamver_agent_sdk import TeamverAgent, AgentToolAdapter

async def main():
    agent = TeamverAgent()  # TeamverAgentConfig.from_env()
    adapter = AgentToolAdapter(agent)

    # Function-calling schemas for your LLM runtime
    tools = adapter.list_tools()

    # Channel report
    await agent.report(text="Hello from agent", channel_id="CH-…")

    # Drive / DM (same tv_ak_* token)
    files = await agent.drive.list_files(drive_id="personal", limit=20)
    threads = await agent.dm.list_threads(limit=10)

    await adapter.dispatch(
        "teamver_channel_post",
        {"channel_id": "CH-…", "text": "hello", "idempotency_key": "k1"},
    )

    await agent.aclose()

asyncio.run(main())
```

Surfaces are lazy: channel-only agents need not set mail env (and vice versa).

## 3. More

- [API reference](./api-reference.md)
- [Agent guide](./guide.md)
- [Examples](../examples/agent-sdk/)
