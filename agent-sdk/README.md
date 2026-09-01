# teamver-agent-sdk

Official **Teamver Agent SDK** for agent runtimes (channel, DM, Drive, mail, jobs, agent tools).

PyPI: [teamver-agent-sdk](https://pypi.org/project/teamver-agent-sdk/)

## Docs

- [Installation](./installation.md) — **start here** (token only; do not ask for W-/AG2-)
- [OpenClaw](./openclaw.md) — what the engine should ask a human
- [Quick start](./quickstart.md)
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

### Need LLM / OpenClaw tools (“skills”)?

`teamver-agent-sdk` is the **runtime API**. For engine-neutral skill registry + OpenClaw/Hermes bridges, install [`teamver-agent-skills`](../agent-skills/) (see [terminology](../terminology.md)).

```bash
pip install teamver-agent-skills teamver-openclaw-adapter
```

## Minimal example

```python
import asyncio
from teamver_agent_sdk import TeamverAgent

async def main():
    agent = await TeamverAgent.connect()
    await agent.report(text="Deploy finished ✅")
    await agent.aclose()

asyncio.run(main())
```

Tool / skill dispatch: prefer [`teamver-agent-skills`](../agent-skills/) (or `AgentToolAdapter` from that package). See [quickstart.md](./quickstart.md) and [configuration.md](./configuration.md).

## License

MIT — documentation in this repo; package license on PyPI.
