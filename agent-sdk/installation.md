# Installation — teamver-agent-sdk

## Requirements

- Python **3.11+**
- Network access to PyPI and Teamver APIs

## pip

```bash
pip install teamver-agent-sdk
```

Pin a version:

```bash
pip install 'teamver-agent-sdk==0.6.3'
```

Dependencies installed automatically:

- `teamver-mail-agent`
- `teamver-sdk-core`
- `httpx`, `pydantic`

## Verify

```bash
python -c "import teamver_agent_sdk as m; print(m.__version__)"
```

## Skills / OpenClaw tools

This package alone is **not** an OpenClaw/Codex `SKILL.md` install. For Teamver function-calling skills:

```bash
pip install teamver-agent-skills teamver-openclaw-adapter
```

See [agent-skills installation](../agent-skills/installation.md) and [terminology](../terminology.md).

## Next

1. [Configuration](./configuration.md) — env vars and tokens  
2. [Quick start](./quickstart.md)
