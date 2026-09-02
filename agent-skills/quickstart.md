# Quick start — teamver-agent-skills

## 1. Env (same as agent-sdk)

```bash
export TEAMVER_AGENT_TOKEN="tv_ak_…"
# optional — discovered if omitted:
# export TEAMVER_WORKSPACE_ID="W-…"
# export TEAMVER_AGENT_ID="AG2-…"
# optional mail:
export TEAMVER_MAIL_AGENT_TOKEN="tv_agent_…"
```

## 2. Execute a skill by name

```python
import asyncio
from teamver_agent_sdk import TeamverAgent
from teamver_agent_skills import SkillExecutor, SkillContext, build_default_registry

async def main():
    agent = await TeamverAgent.connect()
    registry = build_default_registry()
    executor = SkillExecutor(registry, SkillContext(agent=agent))

    # List registered skill names
    print([s.name for s in registry.list_skills()])

    result = await executor.execute("teamver_whoami", {})
    result = await executor.execute("teamver_inbox_poll", {"limit": 20})
    result = await executor.execute("teamver_channel_list", {})
    print(result)

    await agent.aclose()

asyncio.run(main())
```

## 3. Adapter path (OpenClaw)

```python
from teamver_openclaw_adapter import OpenClawToolBridge

bridge = OpenClawToolBridge(agent)
tools = bridge.list_tools()          # JSON schemas for the engine
await bridge.dispatch("teamver_heartbeat", {"operational_status": "idle"})
```

See [openclaw-adapter.md](./openclaw-adapter.md).

## 4. Default catalog (overview)

The default registry covers Teamver surfaces such as:

- Channel: list / post / read / react  
- Inbox: poll new channel+DM instructions / reply on the originating surface  
- DM: threads / messages  
- Drive: drives / files  
- Jobs / heartbeat / mail tools  

Exact names and JSON Schema come from `build_default_registry()` / `tool_json_schemas()` at runtime.

## 5. More

- [Installation](./installation.md)
- [Examples](../examples/agent-skills/)
- [agent-sdk configuration](../agent-sdk/configuration.md)
