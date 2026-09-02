# Installation — teamver-agent-skills

## Requirements

- Python **3.11+**
- Network access to PyPI and Teamver APIs
- Tokens as for [`teamver-agent-sdk`](../agent-sdk/configuration.md)

## pip

Skills only:

```bash
pip install teamver-agent-skills
```

With OpenClaw adapter:

```bash
pip install teamver-agent-skills teamver-openclaw-adapter
# or
pip install "teamver-agent-skills[openclaw]"
```

With Hermes adapter:

```bash
pip install teamver-agent-skills teamver-hermes-adapter
# or
pip install "teamver-agent-skills[hermes]"
```

Pin versions (example):

```bash
pip install 'teamver-agent-skills==0.1.3' 'teamver-openclaw-adapter==0.1.1'
```

Dependencies installed automatically:

- `teamver-agent-sdk` (≥ 0.6.11 for inbox tools)
- `teamver-mail-agent`, `teamver-sdk-core` (via agent-sdk)
- `pydantic`

## Verify

```bash
python -c "import teamver_agent_skills as m; print(m.__version__)"
python -c "import teamver_openclaw_adapter as m; print(m.__version__)"
```

## Relationship to agent-sdk tools

`teamver-agent-sdk` may still expose `AgentToolAdapter` / tool helpers for compatibility.
**Prefer** installing `teamver-agent-skills` (and an adapter) for new OpenClaw/Hermes integrations.

If you only need Channel/DM/Drive/Mail APIs without function-calling tools, `pip install teamver-agent-sdk` is enough — see [terminology](../terminology.md).

## Next

1. [Quick start](./quickstart.md)  
2. [OpenClaw adapter](./openclaw-adapter.md) or [Hermes adapter](./hermes-adapter.md)
