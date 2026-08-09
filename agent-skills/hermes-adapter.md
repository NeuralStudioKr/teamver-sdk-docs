# teamver-hermes-adapter

Hermes-facing adapter over the same [`teamver-agent-skills`](./README.md) registry.

PyPI: [teamver-hermes-adapter](https://pypi.org/project/teamver-hermes-adapter/)

## Install

```bash
pip install teamver-hermes-adapter
# or
pip install "teamver-agent-skills[hermes]"
```

## Usage

```python
from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig
from teamver_hermes_adapter import HermesToolBridge

agent = TeamverAgent(TeamverAgentConfig.from_env())
bridge = HermesToolBridge(agent)
tools = bridge.list_tools()
# await bridge.dispatch("teamver_heartbeat", {"operational_status": "idle"})
```

Exact class/API mirrors the OpenClaw bridge pattern — see the package README on PyPI for the current export name if it differs after a minor release.

## Notes

- Same Teamver skill names as OpenClaw; only the engine tool JSON shape differs.  
- Not a Hermes “skill file” install — Python package only.
