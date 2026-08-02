# teamver-agent-sdk

Official **Teamver Agent SDK** for agent runtimes (channel, DM, Drive, mail, jobs, agent tools).

PyPI: [teamver-agent-sdk](https://pypi.org/project/teamver-agent-sdk/)

## Docs

- [Installation](./installation.md)
- [Quick start](./quickstart.md)
- [Configuration](./configuration.md)
- [API reference](./api-reference.md)
- [Agent guide](./guide.md)
- [Changelog](./changelog.md)
- [Examples](../examples/agent-sdk/)

## What it covers

| Surface | Token | Notes |
|---------|-------|-------|
| Channel / DM / Drive / SSE | `tv_ak_*` | Main API |
| Jobs / heartbeat | `tv_ak_*` | Agents BE |
| Mail | `tv_agent_*` | via `teamver-mail-agent` |

## Install

```bash
pip install teamver-agent-sdk
```

Python **≥ 3.11**. Pulls in `teamver-mail-agent` and `teamver-sdk-core`.

## Minimal example

```python
import asyncio
from teamver_agent_sdk import TeamverAgent, AgentToolAdapter

async def main():
    agent = TeamverAgent()  # from env
    adapter = AgentToolAdapter(agent)
    tools = adapter.list_tools()
    await agent.report(text="Deploy finished ✅", channel_id="CH-…")
    await agent.aclose()

asyncio.run(main())
```

See [quickstart.md](./quickstart.md) and [configuration.md](./configuration.md).

## License

MIT — documentation in this repo; package license on PyPI.
