# teamver-openclaw-adapter

Wraps [`teamver-agent-skills`](./README.md) for **OpenClaw** tool registration and dispatch so the engine can talk to **Teamver Main** (channel, Drive, DM) and **Teamver Mail**.

PyPI: [teamver-openclaw-adapter](https://pypi.org/project/teamver-openclaw-adapter/) **0.1.1** (needs `teamver-agent-sdk>=0.6.8` and `teamver-agent-skills>=0.1.2`).

This is a **Python tool bridge**, not an OpenClaw/Codex `SKILL.md` package. See [terminology](../terminology.md).

**Source of truth:** [`ns-teamver-packages`](https://github.com/NeuralStudioKr/ns-teamver-packages) → PyPI. `ns-teamver-agents` does not vendor a second SDK. OpenClaw images `pip install` pinned versions.

Trust / tokens: Agents Console injects `openclaw.env`. **ACL is policy; `tv_ak_*` is the key.** Do not put `TEAMVER_INTERNAL_API_KEY` in the container. See [agent-sdk configuration](../agent-sdk/configuration.md).

## Install (inside the OpenClaw / agent image)

```bash
pip install 'teamver-agent-sdk==0.6.8' 'teamver-openclaw-adapter==0.1.1'
```

## Env the engine should already have

Injected by VM Manager into `openclaw.env`. **A human only needs to supply `TEAMVER_AGENT_TOKEN` (`tv_ak_*` or OpenClaw `oc-sent-v….end`).** Workspace/agent ids come from `GET /api/v2/ai-agents/me`.

| env | prefix | Required |
|-----|--------|----------|
| `TEAMVER_AGENT_TOKEN` | `tv_ak_*` or `oc-sent-v….end` | **yes** — channel / DM / Drive / jobs |
| `TEAMVER_MAIN_API_BASE` | URL | staging/private only (prod default `https://api.teamver.com`) |
| `TEAMVER_MAIL_AGENT_TOKEN` | `tv_agent_*` | mail only |
| `TEAMVER_MAIL_API_BASE` | URL | mail only |
| `TEAMVER_AGENT_API_BASE` or `TEAMVER_AGENTS_API_BASE` | URL | jobs / heartbeat |
| `TEAMVER_WORKSPACE_ID` / `TEAMVER_AGENT_ID` | `W-…` / `AG2-…` | **optional** — discovered from the token |

`TEAMVER_CONTROL_PLANE_TOKEN` (`tv_cp_*`) may be present. **The adapter/SDK does not use it** for channel/Drive/DM/Mail.

Do **not** ask the human to paste `W-…` / `AG2-…` from the web UI.

## Register tools with OpenClaw

```python
import asyncio
from teamver_agent_sdk import TeamverAgent
from teamver_openclaw_adapter import OpenClawToolBridge

async def main():
    agent = await TeamverAgent.connect()
    bridge = OpenClawToolBridge(agent)

    tools = bridge.list_tools()  # OpenAI envelopes: {"type":"function","function":{...}}
    out = await bridge.dispatch("teamver_whoami", {})
    print(out)
    await agent.aclose()

asyncio.run(main())
```

`dispatch` returns a dict. HTTP **401/403** → `error_code=MAIN_UNAUTHORIZED`. HTTP **404** → `MAIN_PATH_NOT_FOUND` (engine list path is `/ai-agents/me/accessible-channels`, never `/collab/channels`).

Wire `bridge.list_tools()` / `bridge.dispatch(name, args)` to the OpenClaw plugin hook. Default catalog:

| Goal | Tool name |
|------|-----------|
| Who am I / default report | `teamver_whoami` · `teamver_report` |
| List / post / read / react on a **channel** | `teamver_channel_list` · `teamver_channel_post` · `teamver_channel_read` · `teamver_channel_react` |
| **DM** threads | `teamver_dm_list_threads` · `teamver_dm_open_thread` · `teamver_dm_read_messages` · `teamver_dm_post_message` |
| **Drive** list / download / upload | `teamver_drive_list_drives` · `teamver_drive_list_files` · `teamver_drive_download_url` · `teamver_drive_download` · `teamver_drive_upload` |
| **Mail** inbox / get / reply | `teamver_mail_list_inbox` · `teamver_mail_get_message` · `teamver_mail_reply` |
| Jobs / heartbeat | `teamver_jobs_*` · `teamver_heartbeat` |

Drive tool results must carry **path / URL / asset_id**, not raw file bytes.

## Console must be done first (or tools 403)

1. **Agent 권한** — channels / shared Drive R/W / DM allowed, apply status **applied**.
2. **Agent 프로필** — `tv_ak_` inject **주입됨** (and mail inject if using mail).
3. **Agent 메일** — `@teamver.com` provisioned if using mail.

How to verify end-to-end as a human: Agents `docs_specs` **22** (OpenClaw · Main channel · Drive · DM · Mail).

## Notes

- Runnable snippet: [../examples/agent-skills/minimal_skill_bridge.py](../examples/agent-skills/minimal_skill_bridge.py)
