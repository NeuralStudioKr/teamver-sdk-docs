# Teamver Mail SDK — API quick reference

**Client:** `TeamverMailAgentClient` — categories + flat aliases.

---

## Agent runtime (`Bearer tv_agent_*`)

| Method | Path | Scope | SDK (category) | Flat alias |
|--------|------|-------|----------------|------------|
| GET | `/v1/agent/inbox` | `agent:read` | `agent_api.list_inbox` | `list_inbox` |
| GET | `/v1/agent/messages/{id}` | `agent:read` | `agent_api.get_message` | `get_message` |
| POST | `.../attachments/{aid}/download-url` | `agent:read` | `agent_api.attachment_download_url` | `attachment_download_url` |
| POST | `.../status` | `agent:read` | `agent_api.update_message_status` | `update_message_status` |
| GET | `/v1/agent/events` | `agent:events` | `agent_events.list` | `list_events` |
| GET | `/v1/agent/events/stream` | `agent:events` | `agent_events.iter_sse_raw` | `iter_events_sse` |
| POST | `/v1/agent/events/{id}/ack` | `agent:events` | `agent_processing.ack_event` | `ack_event` |
| POST | `.../processing/start` | `agent:read` | `agent_processing.start` | `processing_start` |
| POST | `.../processing/complete` | `agent:read` | `agent_processing.complete` | `processing_complete` |
| POST | `.../processing/fail` | `agent:read` | `agent_processing.fail` | `processing_fail` |
| POST | `.../reply` | `agent:reply` | `agent_reply.send` | `reply` |

Query params: inbox `status`, `limit`; events `after`, `limit`.  
Reply: optional header `Idempotency-Key`.

---

## Ops (no auth)

| GET | Path | SDK |
|-----|------|-----|
| `/health` | `ops.health` |
| `/health/db` | `ops.health_db` |
| `/health/s3` | `ops.health_s3` |
| `/health/ses` | `ops.health_ses` |

---

## Internal M2M (`X-Teamver-Internal-Api-Key`)

Requires `TeamverMailAgentConfig.internal_api_key` or `TEAMVER_INTERNAL_API_KEY`.

| Method | Path | SDK |
|--------|------|-----|
| GET | `/internal/m2m/workspaces/{ws}/mail-health` | `internal_m2m.workspace_mail_health` |
| POST | `/internal/m2m/workspaces/{ws}/agent-mailboxes` | `internal_m2m.provision_agent_mailbox` |
| POST | `.../agent-mailboxes/{ext}/tokens` | `internal_m2m.issue_agent_token` |
| GET | `.../agent-mailboxes/{ext}/health` | `internal_m2m.agent_mailbox_health` |

Other M2M routes: use `client.request(..., auth="internal")`.

---

## Errors

JSON shape: `{"error": {"code": "...", "message": "..."}}` → `MailAgentAPIError`.
