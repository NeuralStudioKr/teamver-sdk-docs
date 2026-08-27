# Examples — agent-sdk

Install from PyPI first:

```bash
pip install 'teamver-agent-sdk>=0.6.3'
cp .env.example .env   # fill tokens
```

| File | Description |
|------|-------------|
| `teamver_agent_sdk_demo.py` | Small demo / capability dump |
| `agent_smoke.py` | Multi-step smoke (channel · mail · jobs · heartbeat) |
| `.env.example` | Env template |

Run:

```bash
set -a && source .env && set +a
python teamver_agent_sdk_demo.py
# or
python agent_smoke.py
```

Docs: [../agent-sdk/](../../agent-sdk/)
