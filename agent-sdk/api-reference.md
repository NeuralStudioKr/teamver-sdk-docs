# Teamver Agent SDK — API quick reference

**Package:** `teamver-agent-sdk` (0.6.11+ inbox/`reply()`/`doctor --probe`; 0.6.10+ DM `/me/dm` + channel `body`; 0.6.9+ Drive `/me/drives`; 0.6.8+ OpenClaw sentinels; 0.6.6+ token-only identity via `/ai-agents/me`)  
**Mail API:** [mail-agent/api-reference.md](../mail-agent/api-reference.md)

Paths below for **Main** are suffixes after `{TEAMVER_MAIN_API_BASE}/api/v2`.

---

## Facade — `TeamverAgent`

| Member | Type | Notes |
|--------|------|--------|
| `config` | `TeamverAgentConfig` | ids may be empty until `connect()` / `ensure_identity()` |
| `connect()` | classmethod async | `from_env` + `GET /ai-agents/me` |
| `whoami()` | async → dict | workspace, agent, ACL channels/drives |
| `channel` | `ChannelClient` | lazy; requires channel env |
| `dm` | `DmClient` | lazy; same token as channel |
| `drive` | `DriveClient` | lazy; same token as channel |
| `inbox` | `InboxClient` | lazy; `poll` / `reply` / `ack` (0.6.11+) |
| `events` | `EventStream` | lazy; same token as channel |
| `mail` | `TeamverMailAgentClient` | lazy; requires mail env |
| `report(...)` | async → `ReportResult` | channel post and/or mail reply |
| `aclose()` | async | close all opened HTTP clients |

### `TeamverAgent.report`

| Parameter | Required | Effect |
|-----------|----------|--------|
| `text` | yes | Message body (channel) / `body_text` (mail) |
| `channel_id` | no after `connect()` | default report channel from `/me`; else required |
| `reply_to_message_id` | one of channel / mail | `mail.reply` |
| `subject` | yes if mail reply | mail subject |
| `cc` | no | mail CC list |

### `ReportResult`

| Field | Content |
|-------|---------|
| `channel_message` | dict from Main post (or None) |
| `mail_reply` | dict from Mail reply (or None) |
| `delivered` | property: any surface succeeded |

---

## Config — `TeamverAgentConfig`

| Field / env | Description |
|-------------|-------------|
| `workspace_id` / `TEAMVER_WORKSPACE_ID` | Optional. Discovered from token (`W-…`) |
| `agent_id` / `TEAMVER_AGENT_ID` | Optional. Discovered from token (`AG2-…`) |
| `main_api_base` / `TEAMVER_MAIN_API_BASE` | Main host (no `/api`) |
| `channel_token` / `TEAMVER_AGENT_TOKEN` | **Required** `tv_ak_*` |
| `agent_api_base` / `TEAMVER_AGENT_API_BASE` | Agents BE. Fallback `TEAMVER_AGENTS_API_BASE` (0.6.5+) |
| `mail_api_base` / `TEAMVER_MAIL_API_BASE` | Mail BE host |
| `mail_agent_token` / `TEAMVER_MAIL_AGENT_TOKEN` | `tv_agent_*` |
| `control_plane_token` / `TEAMVER_CONTROL_PLANE_TOKEN` | Identity fallback (`tv_cp_*`) |
| `channel_enabled` | property: base + token set |
| `mail_enabled` | property: mail base + token set |
| `from_env()` / `from_token()` | load token; ids optional |
| `ensure_identity()` | `GET /api/v2/ai-agents/me` |

---

## Identity — `GET /ai-agents/me` (Main BE)

This is **not** an ns-teamver-agents route. Agents fallback is `GET /api/v2/engine/whoami` (`tv_cp_`, ids only). N33 adds `GET /api/v2/engine/main-me` and `GET /api/v2/engine/report-policy` (same `tv_cp_`, wrap Main `/me`; no ACL recompute).

| Field | Meaning |
|-------|---------|
| `workspace_id` / `agent_id` | Principal from `tv_ak_*` |
| `name` / `handle` / `scopes` | Display + credential scopes |
| `channels.items` | Read-effective ACL (same as `/ai-agents/me/accessible-channels`) |
| `drives.items` | Enabled drives with read |
| `dm` | `{applied_enabled}` |
| `report_channel_id` | Default report channel, or `null` |

Missing/invalid Bearer → **401** `invalid_token`. A **404** on staging means the live container has not been redeployed (`deploy.sh --staging`), not that the token is wrong.

### Response example

`GET {TEAMVER_MAIN_API_BASE}/api/v2/ai-agents/me`  
`Authorization: Bearer tv_ak_…`

**200** — N27 (`ns-teamver-be` `ai_agent_me_service.build_agent_me_response`). `channels.items` is the read-effective list (same as `/ai-agents/me/accessible-channels`), not a raw ACL dump.

```json
{
  "workspace_id": "W-1a2b3c",
  "agent_id": "AG2-9f8e7d",
  "name": "한돌",
  "handle": "handol",
  "scopes": ["messages:read", "messages:write", "channels:read"],
  "channels": {
    "items": [
      {"channel_id": "CH-aaa111", "name": "한돌ch2", "visibility": "public"},
      {"channel_id": "CH-bbb222", "name": "한돌ch1", "visibility": "public"}
    ],
    "total": 2
  },
  "drives": {
    "items": [
      {
        "shared_drive_id": "SD-ccc333",
        "name": "한돌 Drive",
        "can_read": true,
        "can_write": true
      }
    ],
    "total": 1
  },
  "dm": {"applied_enabled": true},
  "report_channel_id": "CH-bbb222"
}
```

Empty ACL still returns ids. `report_channel_id` and `handle` may be `null`. `channels.items` / `drives.items` may be `[]`.

**401** — missing header, unknown/revoked token, user JWT. Not 404.

```json
{
  "error": {
    "code": "invalid_token",
    "message": "Missing or invalid agent token",
    "retryable": false,
    "request_id": "req_…",
    "details": {}
  }
}
```

Sibling **200** examples:

`GET /api/v2/ai-agents/me/accessible-channels`

```json
{
  "workspace_id": "W-1a2b3c",
  "agent_id": "AG2-9f8e7d",
  "items": [
    {"channel_id": "CH-aaa111", "name": "한돌ch2", "visibility": "public"},
    {"channel_id": "CH-bbb222", "name": "한돌ch1", "visibility": "public"}
  ],
  "total": 2
}
```

`GET /api/v2/ai-agents/me/report-channel`

```json
{
  "workspace_id": "W-1a2b3c",
  "agent_id": "AG2-9f8e7d",
  "channel_id": "CH-bbb222"
}
```

---

## Channel — `ChannelClient`

| SDK method | HTTP | Body / query |
|------------|------|----------------|
| `list_channels()` | GET `/ai-agents/me/accessible-channels` (404 → workspace `/ai-agents/{id}/accessible-channels`). **Never** `/collab/channels`. | — |
| `post_message(channel_id, text, mentions=, reply_to_message_id=, correlation_id=, task_id=)` | POST `/workspace/{ws}/channels/{id}/messages` | JSON `{body, text?, mentions?, parent_message_id?, correlation_id?, task_id?}` (`body` is required by Main) |
| `reply(message, text, …)` | same POST | infers `channel_id` + `reply_to_message_id` from `InboxItem` / `AgentMessage` / dict |
| `read_messages(channel_id, limit=50, cursor=, before=, after=)` | GET same path | `limit`, `before` (Main keyset; `cursor` is an alias), `after` |
| `react(channel_id, message_id, emoji)` | POST `…/messages/{message_id}/reactions` | `{emoji}` |

Auth: Bearer `tv_ak_*`.

Agent tools: `teamver_whoami` / `teamver_report` / `teamver_inbox_poll` / `teamver_inbox_reply` / `teamver_channel_list` / `post` / `read` / `react`.

---

## DM — `DmClient`

| SDK method | HTTP |
|------------|------|
| `list_threads(limit=, cursor=)` | GET `/ai-agents/me/dm/threads` |
| `open_thread(peer_user_id)` | POST `/ai-agents/me/dm/threads` `{peer_user_id}` |
| `search_users(q=)` | GET `/ai-agents/me/directory/users?q=` |
| `open_thread_by_email(email)` | search → exact email → `open_thread` |
| `read_messages(thread_id, …)` | GET `…/dm/threads/{id}/messages` |
| `post_message(thread_id, text, …)` | POST same path `{text, body, correlation_id?, task_id?}` |
| `reply(thread_id_or_item, text, …)` | alias of `post_message` |

Agent tools: `teamver_dm_list_threads` / `open_thread` / `read_messages` / `post_message`. Inbox: `teamver_inbox_poll` / `teamver_inbox_reply`.

---

## Drive — `DriveClient`

| SDK method | HTTP / 동작 |
|------------|-------------|
| `list_shared_drives()` | GET `/ai-agents/me` drives (ACL) |
| `list_files(drive_id=, …)` | GET `/ai-agents/me/drives/{id}/files` |
| `download_url(asset_id, …)` | GET `/ai-agents/me/drives/{id}/assets/{asset_id}/download-url` |
| `download(asset_id, dest_path, …)` | URL fetch → 로컬 파일 |
| `upload(local_path=, …)` | upload-request → PUT → confirm (human path until N29) |

Agent tools: `teamver_drive_list_drives` / `list_files` / `download_url` / `download` / `upload`.

---

## Inbox — `InboxClient` (0.6.11+)

Additive. Existing `channel` / `dm` / `events` clients stay.

| SDK method | HTTP | Notes |
|------------|------|--------|
| `poll(store=, limit=)` | GET `/ai-agents/me/inbox` | fallback: events poll, then compose ACL channels (max 8) + DM threads (max 12) |
| `reply(item, text, …)` | channel or DM POST | uses item surface (`reply_to_message_id` vs `thread_id`) |
| `ack(event_id)` | POST `/ai-agents/me/inbox/{id}/ack` | |
| checkpoint `get_cursor` / `save_cursor` | local JSON | last-seen per surface key (`channel:{id}`, `dm:{id}`, `inbox`) |

Typed: `AgentMessage.from_api` coalesces `id`/`message_id`, `body`/`text`. Dict-returning APIs are unchanged.

```python
from teamver_agent_sdk import FileCheckpointStore

store = FileCheckpointStore("/tmp/teamver-inbox.json")
for item in await agent.inbox.poll(store=store):
    await agent.inbox.reply(item, "received")
    if item.event_type:
        await agent.inbox.ack(item.id)
```

CLI: `python -m teamver_agent_sdk doctor --probe` (read) / `--probe-write`. Sentinel: run via OpenClaw **gateway exec**.

---

## Events — `EventStream`

| SDK method | HTTP | Notes |
|------------|------|--------|
| `listen(last_event_id=)` | GET `/ai-agents/{agent_id}/events/stream` | SSE; yields `AgentEvent` |
| `ack(event_id)` | POST `/ai-agents/{agent_id}/events/{event_id}/ack` | |

### `AgentEvent`

| Field | SSE source |
|-------|------------|
| `id` | `id:` line |
| `event` | `event:` line |
| `data` | parsed JSON from `data:` lines |

### `parse_sse_events(buffer) -> (events, remainder)`

Utility for incremental SSE parsing (used by `listen()`).

---

## Mail — `agent.mail` (`TeamverMailAgentClient`)

Not re-documented here. Use flat aliases on the mail client, e.g.:

| Common alias | Mail path (on mail host) |
|--------------|---------------------------|
| `list_inbox` | GET `/v1/agent/inbox` |
| `get_message` | GET `/v1/agent/messages/{id}` |
| `list_events` | GET `/v1/agent/events` |
| `ack_event` | POST `/v1/agent/events/{id}/ack` |
| `reply` | POST `/v1/agent/messages/{id}/reply` |
| `processing_start` / `complete` / `fail` | POST `…/processing/*` |

Full table: [teamver-mail-agent API_QUICKREF.md](../mail-agent/api-reference.md).

---

## HTTP transport — `AgentHTTP` (internal)

Used by channel + events only:

- Retries: 429, 502, 503, 504 + transport errors (`max_retries`, backoff)
- Headers: `Authorization`, `X-Teamver-Request-Id`, `User-Agent`

---

## Errors

| Class | Typical cause |
|-------|----------------|
| `TeamverAgentConfigError` | Invalid/missing config |
| `TeamverAgentAPIError` | Main API failure |
| `TeamverAgentError` | Base class; `.status_code` `.path` `.request_id` `.response_body` |
| `format_error(exc)` | one-line ops log (no token) |
