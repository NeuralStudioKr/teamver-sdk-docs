# teamver-openclaw-adapter

Wraps [`teamver-agent-skills`](./README.md) for **OpenClaw** tool registration and dispatch so the engine can talk to **Teamver Main** (channel, Drive, DM) and **Teamver Mail**.

PyPI: [teamver-openclaw-adapter](https://pypi.org/project/teamver-openclaw-adapter/)

This is a **Python tool bridge**, not an OpenClaw/Codex `SKILL.md` package. See [terminology](../terminology.md).

Trust / tokens: Agents Console injects `openclaw.env`. **ACL is policy; `tv_ak_*` is the key.** Do not put `TEAMVER_INTERNAL_API_KEY` in the container. See [agent-sdk configuration](../agent-sdk/configuration.md).

## Install (inside the OpenClaw / agent image)

```bash
pip install teamver-openclaw-adapter
# pulls teamver-agent-skills → teamver-agent-sdk
```

## Env the engine must already have

Injected by VM Manager into `openclaw.env` (not hand-edited as the product path):

| env | prefix | Surface |
|-----|--------|---------|
| `TEAMVER_WORKSPACE_ID` | `W-…` | identity |
| `TEAMVER_AGENT_ID` | `AG2-…` | identity |
| `TEAMVER_AGENT_TOKEN` | `tv_ak_*` | channel / DM / Drive / jobs |
| `TEAMVER_MAIN_API_BASE` | URL | Main |
| `TEAMVER_MAIL_AGENT_TOKEN` | `tv_agent_*` | mail |
| `TEAMVER_MAIL_API_BASE` | URL | Mail |
| `TEAMVER_AGENT_API_BASE` or `TEAMVER_AGENTS_API_BASE` | URL | jobs / heartbeat (`0.6.5+` reads the plural name) |

`TEAMVER_CONTROL_PLANE_TOKEN` (`tv_cp_*`) may be present. **The adapter/SDK does not use it** for channel/Drive/DM/Mail.

## Register tools with OpenClaw

```python
import asyncio
from teamver_agent_sdk import TeamverAgent, TeamverAgentConfig
from teamver_openclaw_adapter import OpenClawToolBridge

async def main():
    agent = TeamverAgent(TeamverAgentConfig.from_env())
    bridge = OpenClawToolBridge(agent)

    tools = bridge.list_tools()          # JSON schemas for the LLM
    # Register `tools` with OpenClaw's tool list, then:
    out = await bridge.dispatch(
        "teamver_channel_post",
        {"channel_id": "CH-…", "text": "hello from OpenClaw"},
    )
    print(out)
    await agent.aclose()

asyncio.run(main())
```

Wire `bridge.list_tools()` / `bridge.dispatch(name, args)` to whatever OpenClaw plugin hook your image uses. The default catalog names:

| Goal | Tool name |
|------|-----------|
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
