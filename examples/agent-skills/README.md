# Agent skills examples

Install from PyPI:

```bash
pip install teamver-agent-skills teamver-openclaw-adapter
```

Set env vars as in [agent-sdk configuration](../../agent-sdk/configuration.md), then:

```bash
python minimal_skill_bridge.py
# optional live heartbeat:
TEAMVER_RUN_HEARTBEAT_TOOL=1 python minimal_skill_bridge.py
```

See [agent-skills docs](../../agent-skills/).
