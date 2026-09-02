# teamver-agent-skills (+ adapters)

Engine-neutral **Teamver agent skills**: registry, executor, and the default catalog
(inbox, channel, DM, Drive, jobs, mail, heartbeat) backed by [`teamver-agent-sdk`](../agent-sdk/).

Does **not** import OpenClaw or Hermes. Install an adapter for engine tool registration.

| PyPI package | Role |
|--------------|------|
| [`teamver-agent-skills`](https://pypi.org/project/teamver-agent-skills/) | Registry · executor · default catalog |
| [`teamver-openclaw-adapter`](https://pypi.org/project/teamver-openclaw-adapter/) | OpenClaw tool bridge |
| [`teamver-hermes-adapter`](https://pypi.org/project/teamver-hermes-adapter/) | Hermes tool bridge |

> **Not the same as** OpenClaw/Codex `SKILL.md` skills. See [terminology](../terminology.md).

## Docs

- [Installation](./installation.md)
- [Quick start](./quickstart.md)
- [OpenClaw adapter](./openclaw-adapter.md)
- [Hermes adapter](./hermes-adapter.md)
- [Changelog](./changelog.md)
- [Examples](../examples/agent-skills/)

## Install

```bash
# Skills only (engine-neutral)
pip install teamver-agent-skills

# Skills + OpenClaw bridge
pip install teamver-agent-skills teamver-openclaw-adapter
# or
pip install "teamver-agent-skills[openclaw]"
```

Python **≥ 3.11**. Pulls in `teamver-agent-sdk` (and its mail/core deps).

## Minimal example

```python
import asyncio
from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig
from teamver_agent_skills import SkillExecutor, SkillContext, build_default_registry

async def main():
    agent = TeamverAgent(TeamverAgentConfig.from_env())
    executor = SkillExecutor(build_default_registry(), SkillContext(agent=agent))
    result = await executor.execute("teamver_channel_list", {})
    print(result)
    await agent.aclose()

asyncio.run(main())
```

Legacy `AgentToolAdapter` (same idea as agent-sdk tools; prefer skills package):

```python
from teamver_agent_skills import AgentToolAdapter

adapter = AgentToolAdapter(agent)
await adapter.dispatch("teamver_channel_post", {"channel_id": "CH-1", "text": "hi"})
```

## License

MIT — documentation in this repo; package license on PyPI.
