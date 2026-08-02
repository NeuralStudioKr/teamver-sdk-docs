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
pip install 'teamver-agent-sdk==0.6.2'
```

Dependencies installed automatically:

- `teamver-mail-agent`
- `teamver-sdk-core`
- `httpx`, `pydantic`

## Verify

```bash
python -c "import teamver_agent_sdk as m; print(m.__version__)"
```

## Next

1. [Configuration](./configuration.md) — env vars and tokens  
2. [Quick start](./quickstart.md)
