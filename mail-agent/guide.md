# Teamver Mail SDK — AI Agent Guide

**Audience:** agent, autonomous workers, and LLM agents that **read and reply to mail** via Teamver Mail BE.  
**Package:** `teamver-mail-agent` v0.3.1 — async `httpx`, not OpenAPI codegen.

## 변경 이력

| 일시 (KST) | 변경 내용 |
|---|-----|
| 2026-08-02 22:55 | 디폴트 Mail host `https://mail-api.teamver.com` |

---

## 1. When to use this SDK vs others

| Client | Target | Base URL |
|--------|--------|----------|
| **teamver-mail-agent** (this) | Mail BE agent inbox / events / reply | `{MAIL_HOST}` — **no** `/api` prefix |
| **teamver-be-sdk** | Main BE — workspace, AI agents, drive | `{HOST}/api`, `/api/v2` |
| **teamver-agent-sdk** | Unified agent config → wraps this client for mail | Same as mail when env set |
| **teamver-app-sdk** | Per-app user JWT flows | App-specific paths |

Your runtime token is **`tv_agent_…`** issued for a **mail agent mailbox**, not a user JWT.

---

## 2. Environment

```bash
# Optional — default https://mail-api.teamver.com (no /v1)
# export TEAMVER_MAIL_API_BASE_URL="https://mail-api.teamver.com"
export TEAMVER_MAIL_AGENT_TOKEN="tv_agent_…"
export TEAMVER_HTTP_TIMEOUT=60   # optional

# Only if you provision mailboxes from Main BE / workers:
export TEAMVER_INTERNAL_API_KEY="…"
```

```python
from teamver_mail_agent import TeamverMailAgentClient

async with TeamverMailAgentClient.from_env() as client:
    ...
```

agent unified config also accepts `TEAMVER_MAIL_API_BASE` (alias).

---

## 3. Scopes

| Scope | Routes |
|-------|--------|
| `agent:read` | inbox, message, attachment URL, processing start/complete/fail |
| `agent:events` | poll/stream events, ack |
| `agent:reply` | POST reply |

Token issuance: Admin console or M2M `internal_m2m.issue_agent_token` (platform ops).

---

## 4. Recommended processing loop

```text
1. GET /v1/agent/events  OR  GET /v1/agent/events/stream (SSE)
2. POST /v1/agent/events/{event_id}/ack
3. GET /v1/agent/messages/{message_id}   # sets content_fetched_at on server
4. POST .../processing/start  (job_id = your correlation id)
5. Your LLM / tools handle the message
6. POST .../reply  (use Idempotency-Key = job_id)
7. POST .../processing/complete  (response_message_id from reply)
```

On failure: `processing_fail` with `failure_code` and `retryable`.

### SDK helper

```python
from teamver_mail_agent import run_standard_inbound_loop

async def handle(msg):
    # return (subject, body_text)
    return f"Re: {msg.subject}", "Thanks, I received your email."

await run_standard_inbound_loop(client, event, handle_message=handle)
```

---

## 5. Code patterns

### Poll inbox (batch worker)

```python
inbox = await client.list_inbox(status="queued", limit=20)
for item in inbox.items:
    msg = await client.get_message(item.message_id)
    ...
```

### Events + SSE

```python
page = await client.list_events(limit=100, after=cursor)
for ev in page.events:
    ...

from teamver_mail_agent import parse_sse_buffer

buf = ""
async for chunk in client.iter_events_sse(last_event_id=last_id):
    buf += chunk
    if "\n\n" in buf:
        for parsed in parse_sse_buffer(buf):
            ...
```

### Attachments

```python
for att in msg.attachments:
    presign = await client.attachment_download_url(msg.message_id, att.attachment_id)
    # GET presign.url with httpx (short-lived)
```

### Reply with idempotency

```python
job_id = "job-uuid-…"
out = await client.reply(
    message_id,
    subject="Re: …",
    body_text="…",
    idempotency_key=job_id,
)
```

---

## 6. Category facades (preferred for new code)

```python
await client.agent_api.get_message(message_id)
await client.agent_processing.start(message_id, job_id)
await client.agent_events.list(limit=50)
await client.agent_reply.send(message_id, subject="…", body_text="…")
await client.ops.health()
```

Flat methods (`client.get_message`, etc.) remain equivalent.

---

## 7. M2M provisioning (not typical agent VM)

Use only from **trusted Main BE workers** with internal key:

```python
config = TeamverMailAgentConfig(
    api_base_url="https://mail-api.teamver.com",
    agent_token="tv_agent_placeholder",  # still required by config validator
    internal_api_key=os.environ["TEAMVER_INTERNAL_API_KEY"],
)
# Or set internal_api_key on from_env() config after construction.

await client.internal_m2m.provision_agent_mailbox(
    platform_workspace_id,
    {"external_agent_id": "…", "issue_token": True},
)
```

Agent runtimes on the edge should **only** use `TEAMVER_MAIL_AGENT_TOKEN`, not the internal key.

---

## 8. Errors and retries

- Raised as **`MailAgentAPIError`** (`status_code`, `code`, `response_body`).
- Transient **429 / 502 / 503 / 504** retried with backoff (`max_retries` on config).
- **404** `message_not_found` — wrong id or not your agent's inbound message.
- **501** on reply attachments — not supported yet.

---

## 9. Escape hatch

```python
raw = await client.request("GET", "/v1/agent/inbox", params={"status": "received"})
```

---

## 10. Related docs

- [API reference](./api-reference.md) — route table
- [README](./README.md) — install & overview
- [Changelog](./changelog.md)
