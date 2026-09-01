# Installation — teamver-agent-sdk

## What OpenClaw (or any agent) should ask a human

After `pip install teamver-agent-sdk`, run:

```bash
python -m teamver_agent_sdk required-env
```

**Required:** `TEAMVER_AGENT_TOKEN` (`tv_ak_*`).

**Do not ask for** `TEAMVER_WORKSPACE_ID` or `TEAMVER_AGENT_ID`. The SDK discovers them with `GET /api/v2/ai-agents/me`. A Teamver web login is not a substitute for the agent token, and the human does not need to copy `W-…` from the UI.

**Ask only if needed:**

- `TEAMVER_MAIN_API_BASE` — staging or private Main host (production default is `https://api.teamver.com`)
- `TEAMVER_MAIL_AGENT_TOKEN` (`tv_agent_*`) — only if the agent should use Mail

**Never put in the engine:** `TEAMVER_INTERNAL_API_KEY`, user password, user JWT.

Then:

```bash
python -m teamver_agent_sdk whoami
```

## Requirements

- Python **3.11+**
- Network access to PyPI and Teamver APIs

## pip

```bash
pip install teamver-agent-sdk
```

Pin a version:

```bash
pip install 'teamver-agent-sdk==0.6.6'
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
