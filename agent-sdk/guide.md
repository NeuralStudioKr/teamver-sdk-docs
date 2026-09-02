# Teamver Agent SDK — AI Agent Guide

**Audience:** agent runtimes, VM-hosted agents, and LLM automation that **report to Teamver channels** and/or **reply via Teamver Mail** with one config surface.  
**Package:** `teamver-agent-sdk` v0.6.12 — async `httpx` on Main (inbox/channel/DM/drive + event webhook); mail via **`teamver-mail-agent`**. Token-only identity (`GET /api/v2/ai-agents/me`). OpenClaw sentinels (`oc-sent-v….end`) are first-class.  
**Drive/DM/inbox:** see [API reference](./api-reference.md).

## 변경 이력

| 일시 (KST) | 변경 내용 |
|---|-----|
| 2026-09-02 | 0.6.12: `handle_webhook` → InboxItem · OpenClaw adapter 0.1.2 ingress |
| 2026-09-02 | 0.6.11: inbox / `reply()` / typed messages / `doctor --probe` / sentinel gateway_exec |
| 2026-09-02 | 0.6.10: DM `/ai-agents/me/dm` · channel POST `body` · CLI `dm`/`drive-list` |
| 2026-09-02 | 0.6.9: Drive files via `/ai-agents/me/drives/…` · CLI `files` |
| 2026-09-02 | 0.6.8: OpenClaw managed secret sentinel · CLI `channels` · staging host `stg-api.teamver.com` |
| 2026-09-02 | 0.6.7: engine channel list never uses `/collab/channels` |
| 2026-09-02 | 0.6.6: token-only identity; do not ask humans for W-/AG2- |
| 2026-08-28 | Bible 정합: `W-`/`AG2-`, ACL≠`tv_ak_`, `TEAMVER_AGENTS_API_BASE`, `tv_cp_` 비사용 |

---

## 1. When to use this SDK vs others

| Client | Target | Typical token |
|--------|--------|----------------|
| **teamver-agent-sdk** (this) | Unified facade: channel + DM + Drive + SSE + mail + jobs | `tv_ak_*` + `tv_agent_*` |
| **teamver-mail-agent** | Mail BE only (inbox loop, processing, reply) | `tv_agent_*` |
| **teamver-sdk-core** | Shared HTTP transport / errors (dependency) | — |

Use **this SDK** when the runtime has `TEAMVER_AGENT_TOKEN` (`tv_ak_*`). Workspace and agent ids are optional. Use **teamver-mail-agent** directly if you only need mail and want fewer layers.

---

## 2. Environment

Required for any use:

```bash
export TEAMVER_AGENT_TOKEN="tv_ak_…"
# optional — discovered from the token if omitted:
# export TEAMVER_WORKSPACE_ID="W-…"
# export TEAMVER_AGENT_ID="AG2-…"
```

Channel surface (collab + SSE events). API hosts default when unset:

| env | default |
|-----|---------|
| `TEAMVER_MAIN_API_BASE` | `https://api.teamver.com` (no `/api`) |
| `TEAMVER_AGENT_API_BASE` | `https://agent-api.teamver.com` |
| `TEAMVER_MAIL_API_BASE` | `https://mail-api.teamver.com` (no `/v1`) |

```bash
export TEAMVER_AGENT_TOKEN="tv_ak_…"                        # access grant, messages:write/read + events
# optional override:
# export TEAMVER_MAIN_API_BASE="https://api.teamver.com"
# export TEAMVER_AGENT_API_BASE="https://agent-api.teamver.com"
```

Mail surface (inbox / reply — delegated to `teamver-mail-agent`):

```bash
export TEAMVER_MAIL_AGENT_TOKEN="tv_agent_…"
# optional override:
# export TEAMVER_MAIL_API_BASE="https://mail-api.teamver.com"
```

Optional tuning (constructor on `TeamverAgentConfig`):

- `timeout_seconds` (default 30)
- `max_retries` / `retry_backoff_seconds` — HTTP 429, 502, 503, 504 and transport errors on **Main** `AgentHTTP` only

```python
from teamver_agent_sdk import TeamverAgent

agent = await TeamverAgent.connect()
# or, if ids are already in env:
# agent = TeamverAgent()
```

Always close when done:

```python
await agent.aclose()
```

---

## 3. Authentication

| Surface | Header | Base URL used by SDK |
|---------|--------|----------------------|
| Channel + events | `Authorization: Bearer {tv_ak_*}` | `{TEAMVER_MAIN_API_BASE}/api/v2` |
| Mail | Bearer `tv_agent_*` (via `TeamverMailAgentClient`) | `{TEAMVER_MAIL_API_BASE}` |

Main requests also send `X-Teamver-Request-Id` (UUID) per call.

Token prefixes are validated at config time: `tv_ak_` for channel, `tv_agent_` for mail.

---

## 4. Unified `report()` workflow

Single helper for “tell the human” on channel and/or mail thread:

```python
from teamver_agent_sdk import TeamverAgent

agent = TeamverAgent()

# Channel only
result = await agent.report(
    text="Deploy finished ✅",
    channel_id="CH-…",
)

# Mail reply only (subject required)
result = await agent.report(
    text="Summary attached in body.",
    reply_to_message_id="MSG-uuid",
    subject="Re: Weekly report",
    cc=["ops@example.com"],  # optional, mail only
)

# Both in one call
result = await agent.report(
    text="Done — also replied by email.",
    channel_id="CH-…",
    reply_to_message_id="MSG-uuid",
    subject="Re: Task",
)

assert result.delivered
await agent.aclose()
```

Rules:

- At least one of `channel_id` or `reply_to_message_id` is required.
- Mail reply requires `subject`.
- `ReportResult.channel_message` / `.mail_reply` hold JSON dicts from the APIs.

### 4.1 Inbox (`agent.inbox`) — 0.6.11+

Prefer this for “new instruction → same-surface reply”. Channel and DM clients remain.

```python
from teamver_agent_sdk import FileCheckpointStore

agent = await TeamverAgent.connect()
store = FileCheckpointStore("/tmp/teamver-inbox.json")
for item in await agent.inbox.poll(store=store):
    await agent.inbox.reply(item, "received")
await agent.aclose()
```

- `poll` tries `GET /ai-agents/me/inbox`, then events poll, then ACL channel+DM compose.
- `reply` uses `reply_to_message_id` on channel and `thread_id` on DM.
- Cursor helpers: `store.get_cursor` / `save_cursor`.
- Typed: `AgentMessage.from_api` (`id`/`message_id`, `body`/`text`).

### 4.1.1 Event webhook (0.6.12+)

Main POSTs inbox-shaped JSON to your HTTPS URL. **Do not** persist HTTP `reply.body` as a channel message.

```python
result = await agent.inbox.handle_webhook(
    raw_body, headers, secret=os.environ.get("TEAMVER_WEBHOOK_SECRET"), store=store
)
if not result.ping and not result.duplicate:
    for item in result.items:
        await agent.inbox.reply(item, "received")
```

HMAC: `sha256=HMAC_SHA256(secret, timestamp + "." + raw_body)`. Ping is not an inbox item. OpenClaw: `python -m teamver_openclaw_adapter webhook`.

OpenClaw sentinel: `python -m teamver_agent_sdk doctor --probe` must run via **gateway exec**.

---

## 5. Channel client (`agent.channel`)

Lazy: needs `channel_enabled`. Scope on token must allow collab messages.

```python
# Post (docs/20 §5.3)
msg = await agent.channel.post_message(
    "CH-…",
    "Hello from agent",
    mentions=["USR-…"],           # optional
    reply_to_message_id="MSG-…",  # optional thread reply
)

# Read history (before = Main keyset; cursor is an alias)
page = await agent.channel.read_messages("CH-…", limit=50, before=None)
await agent.channel.reply(page["items"][0], "ack")  # or InboxItem / AgentMessage

# Reaction
await agent.channel.react("CH-…", message_id="MSG-…", emoji="✅")
```

HTTP mapping (Main BE):

- `POST /api/v2/workspace/{workspace_id}/channels/{channel_id}/messages`
- `GET` same path (list)
- `POST …/messages/{message_id}/reactions`

For admin-only collab extras beyond channel/DM use **teamver-be-sdk** `collab_v2`.

### 5.1 DM (`agent.dm`)

```python
threads = await agent.dm.list_threads(limit=20)
opened = await agent.dm.open_thread("USR-…")
# or: opened = await agent.dm.open_thread_by_email("user@example.com")
msgs = await agent.dm.read_messages(opened["id"], limit=50)
await agent.dm.post_message(opened["id"], "hello from agent")
```

HTTP: `GET/POST /api/v2/ai-agents/me/dm/threads` (not human `/workspace/{ws}/dm/threads`).

agent tools: `teamver_dm_list_threads` / `open_thread` / `read_messages` / `post_message`.

### 5.2 Drive (`agent.drive`)

```python
drives = await agent.drive.list_shared_drives()
files = await agent.drive.list_files(limit=50)  # sole ACL drive, or pass drive_id="SD-…"
await agent.drive.download(asset_id, "/tmp/file.bin")
```

agent tools: `teamver_drive_list_drives` / `list_files` / `download_url` / `download` / `upload`.  
Tool 결과에는 바이너리를 넣지 말고 **path / URL / asset_id** 만 사용.

---

## 6. Event stream (`agent.events`)

SSE consumer for agent triggers (mention, command, etc.):

```python
async for evt in agent.events.listen(last_event_id=None):
    # evt.id, evt.event, evt.data (dict)
    if evt.event == "mention":
        channel_id = evt.data.get("channel_id")
        if channel_id:
            await agent.report(text="On it.", channel_id=channel_id)
    if evt.id:
        await agent.events.ack(evt.id)
```

HTTP mapping:

- `GET /api/v2/ai-agents/{agent_id}/events/stream` (`Accept: text/event-stream`, optional `Last-Event-ID`)
- `POST /api/v2/ai-agents/{agent_id}/events/{event_id}/ack`

Parsing helper (tests / custom consumers):

```python
from teamver_agent_sdk import parse_sse_events

events, remainder = parse_sse_events(buffer)
```

Long-lived streams: handle reconnect with `last_event_id` from the last `evt.id`.

---

## 7. Mail client (`agent.mail`)

Lazy: needs `mail_enabled`. This is **`TeamverMailAgentClient`** from `teamver-mail-agent` (same types as installing that package alone).

Typical inbound loop (prefer mail-agent helper for full processing contract):

```python
events = await agent.mail.list_events(limit=10)
for ev in events:
    await agent.mail.ack_event(ev["id"])
    msg = await agent.mail.get_message(ev["message_id"])
    await agent.mail.processing_start(msg["id"], job_id="job-1")
    await agent.mail.reply(
        msg["id"],
        subject=f"Re: {msg.get('subject', '')}",
        body_text="Automated reply body.",
        idempotency_key="job-1",
    )
    await agent.mail.processing_complete(msg["id"], response_message_id="…")
```

Or use **`run_standard_inbound_loop`** from `teamver_mail_agent` — see [mail-agent guide](../mail-agent/guide.md).

Mail API paths, scopes, and M2M: [teamver-mail-agent API_QUICKREF.md](../mail-agent/api-reference.md).

---

## 8. Errors

| Exception | When |
|-----------|------|
| `TeamverAgentConfigError` | Missing token / wrong prefix / surface used without env |
| `TeamverAgentAPIError` | Main HTTP 4xx/5xx or transport failure; `.status_code`, `.path`, `.request_id`, `.response_body` |
| `format_error(exc)` | one-line ops log (no token) |
| `ImportError` | `teamver-mail-agent` not installed (required dependency) |

Mail errors from delegated client: `MailAgentAPIError` (`teamver_mail_agent.errors`).

Main error JSON may use `error.code` / `error.message` or FastAPI `detail` string — do not assume one schema.

---

## 9. agent / VM checklist

1. Agents Console: Access ACL applied **and** `tv_ak_*` injected into OpenClaw `openclaw.env` as `TEAMVER_AGENT_TOKEN`. Mail: provision + `tv_agent_*`.
2. Runtime env: `TEAMVER_*` from §2 (`W-…` / `AG2-…`). Never `TEAMVER_INTERNAL_API_KEY`.
3. Process: `inbox.poll()` and/or `handle_webhook` → `inbox.reply()` / `report()` / `mail.reply`.
4. On shutdown: `await agent.aclose()`.

---

## 10. Verification

```bash
pip install 'teamver-agent-sdk>=0.6.12'
python -c "import teamver_agent_sdk as m; print(m.__version__)"
```

See also [examples/agent-sdk](../examples/agent-sdk/).

---

## 11. Related docs

| Doc | Purpose |
|-----|---------|
| [API reference](./api-reference.md) | Facade methods + Main HTTP paths |
| [Configuration](./configuration.md) | Env vars and defaults |
| [mail-agent guide](../mail-agent/guide.md) | Full mail processing loop |
