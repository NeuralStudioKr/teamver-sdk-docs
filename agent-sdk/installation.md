# Installation — teamver-agent-sdk

## What OpenClaw (or any agent) should ask a human

After `pip install teamver-agent-sdk`, run:

```bash
python -m teamver_agent_sdk required-env
```

**Required:** `TEAMVER_AGENT_TOKEN` — plaintext `tv_ak_*` **or** an OpenClaw Secret Store sentinel (`oc-sent-v….end`). The Gateway substitutes the real token at HTTPS egress. Do not reject the sentinel in the engine.

**Do not ask for** `TEAMVER_WORKSPACE_ID` or `TEAMVER_AGENT_ID`. The SDK discovers them with `GET /api/v2/ai-agents/me`. A Teamver web login is not a substitute for the agent token.

**Ask only if needed:**

- `TEAMVER_MAIN_API_BASE` — staging API host is **`https://stg-api.teamver.com`** (not the frontend `https://stg.teamver.com`). Production default is `https://api.teamver.com`.
- `TEAMVER_MAIL_AGENT_TOKEN` (`tv_agent_*` or the same kind of sentinel) — only if Mail is in scope
- `TEAMVER_ALLOW_SECRET_REF=1` — only if another secret manager uses a non-`oc-sent-` placeholder

**Never put in the engine:** `TEAMVER_INTERNAL_API_KEY`, user password, user JWT (`eyJ…`).

Then (inside OpenClaw **gateway exec** if the token is a sentinel):

```bash
python -m teamver_agent_sdk whoami
python -m teamver_agent_sdk doctor --probe
python -m teamver_agent_sdk channels
python -m teamver_agent_sdk files
python -m teamver_agent_sdk dm
```

A local shell that never hits the Gateway proxy will **not** turn `oc-sent-v….end` into `tv_ak_*`. Use `gateway_exec` or a real `tv_ak_*`.

## Requirements

- Python **3.11+**
- Network access to PyPI and Teamver APIs

## pip

```bash
pip install teamver-agent-sdk
```

Pin a version:

```bash
pip install 'teamver-agent-sdk==0.6.11'
```

Dependencies installed automatically:

- `teamver-mail-agent`
- `teamver-sdk-core`
- `teamver-agent-skills`
- `httpx`, `pydantic`

## Verify

```bash
python -c "import teamver_agent_sdk as m; print(m.__version__)"
python -m teamver_agent_sdk required-env
```

## Skills / OpenClaw tools

This package alone is **not** an OpenClaw/Codex `SKILL.md` install. For Teamver function-calling skills:

```bash
pip install teamver-agent-skills teamver-openclaw-adapter
```

Call `teamver_whoami` first so the model does not ask the human for workspace/channel ids.

See [agent-skills installation](../agent-skills/installation.md) and [terminology](../terminology.md).

## Next

1. [Configuration](./configuration.md) — env vars and tokens  
2. [Quick start](./quickstart.md)
