# Teamver Agent SDK — API quick reference

**Package:** `teamver-agent-sdk` v0.6.2  
**Mail API:** [mail-agent/api-reference.md](../mail-agent/api-reference.md)

Paths below for **Main** are suffixes after `{TEAMVER_CHANNEL_API_BASE}/api/v2`.

---

## Facade — `TeamverAgent`

| Member | Type | Notes |
|--------|------|--------|
| `config` | `TeamverAgentConfig` | workspace_id, agent_id, tokens |
| `channel` | `ChannelClient` | lazy; requires channel env |
| `dm` | `DmClient` | lazy; same token as channel |
| `drive` | `DriveClient` | lazy; same token as channel |
| `events` | `EventStream` | lazy; same token as channel |
| `mail` | `TeamverMailAgentClient` | lazy; requires mail env |
| `report(...)` | async → `ReportResult` | channel post and/or mail reply |
| `aclose()` | async | close all opened HTTP clients |

### `TeamverAgent.report`

| Parameter | Required | Effect |
|-----------|----------|--------|
| `text` | yes | Message body (channel) / `body_text` (mail) |
| `channel_id` | one of channel / mail | `channel.post_message` |
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
| `workspace_id` / `TEAMVER_WORKSPACE_ID` | Workspace id in channel paths |
| `agent_id` / `TEAMVER_AGENT_ID` | Agent id for SSE + ack paths |
| `channel_api_base` / `TEAMVER_CHANNEL_API_BASE` | Main host (no `/api`) |
| `channel_token` / `TEAMVER_AGENT_TOKEN` | `tv_ak_*` |
| `mail_api_base` / `TEAMVER_MAIL_API_BASE` | Mail BE host |
| `mail_agent_token` / `TEAMVER_MAIL_AGENT_TOKEN` | `tv_agent_*` |
| `channel_enabled` | property: base + token set |
| `mail_enabled` | property: mail base + token set |
| `from_env()` | load required ids + optional tokens |

---

## Channel — `ChannelClient`

| SDK method | HTTP | Body / query |
|------------|------|----------------|
| `post_message(channel_id, text, mentions=, reply_to_message_id=)` | POST `/workspace/{ws}/channels/{id}/messages` | JSON `{text, mentions?, reply_to_message_id?}` |
| `read_messages(channel_id, limit=50, cursor=)` | GET same path | `limit`, `cursor` |
| `react(channel_id, message_id, emoji)` | POST `…/messages/{message_id}/reactions` | `{emoji}` |

Auth: Bearer `tv_ak_*`.

Agent tools: `teamver_channel_list` / `post` / `read` / `react`.

---

## DM — `DmClient`

| SDK method | HTTP |
|------------|------|
| `list_threads(limit=, cursor=)` | GET `/workspace/{ws}/dm/threads` |
| `open_thread(peer_user_id)` | POST `/workspace/{ws}/dm/threads` `{peer_user_id}` |
| `read_messages(thread_id, …)` | GET `…/dm/threads/{id}/messages` |
| `post_message(thread_id, text, …)` | POST same path `{text}` |

Agent tools: `teamver_dm_list_threads` / `open_thread` / `read_messages` / `post_message`.

---

## Drive — `DriveClient`

| SDK method | HTTP / 동작 |
|------------|-------------|
| `list_shared_drives()` | GET `/api/v2/shared-drive` |
| `list_files(drive_id=, …)` | GET `/api/drive/list` (+ personal recent 폴백) |
| `download_url(asset_id, …)` | GET `/api/drive/asset/{id}/download-url` |
| `download(asset_id, dest_path, …)` | URL fetch → 로컬 파일 |
| `upload(local_path=, …)` | upload-request → PUT → confirm |

Agent tools: `teamver_drive_list_drives` / `list_files` / `download_url` / `download` / `upload`.

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
| `TeamverAgentError` | Base class |
