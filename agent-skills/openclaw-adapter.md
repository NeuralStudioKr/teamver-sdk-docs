# teamver-openclaw-adapter

Wraps [`teamver-agent-skills`](./README.md) for **OpenClaw** tool registration and dispatch.

PyPI: [teamver-openclaw-adapter](https://pypi.org/project/teamver-openclaw-adapter/)

## Install

```bash
pip install teamver-openclaw-adapter
# pulls teamver-agent-skills → teamver-agent-sdk
```

## Usage

```python
import asyncio
from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig
from teamver_openclaw_adapter import OpenClawToolBridge

async def main():
    agent = TeamverAgent(TeamverAgentConfig.from_env())
    bridge = OpenClawToolBridge(agent)

    tools = bridge.list_tools()
    print(f"tools={len(tools)}")

    out = await bridge.dispatch(
        "teamver_heartbeat",
        {"operational_status": "idle", "active_job_count": 0},
    )
    print(out)
    await agent.aclose()

asyncio.run(main())
```

## Notes

- This is a **Python tool bridge**, not an OpenClaw/Codex `SKILL.md` package.  
- For terminology, see [../terminology.md](../terminology.md).  
- Runnable snippet: [../examples/agent-skills/minimal_skill_bridge.py](../examples/agent-skills/minimal_skill_bridge.py)
