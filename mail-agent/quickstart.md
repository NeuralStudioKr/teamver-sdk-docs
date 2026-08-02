# Quick start — teamver-mail-agent

## Environment

| Field | Env | Default |
|-------|-----|---------|
| `api_base_url` | `TEAMVER_MAIL_API_BASE` or `TEAMVER_MAIL_API_BASE_URL` | `https://mail-api.teamver.com` |
| `agent_token` | `TEAMVER_MAIL_AGENT_TOKEN` | *(required)* `tv_agent_…` |

```bash
export TEAMVER_MAIL_AGENT_TOKEN="tv_agent_…"
# optional override:
# export TEAMVER_MAIL_API_BASE="https://mail-api.teamver.com"
```

## Recommended loop

```text
list/stream events → ack → get_message → processing_start
→ handle → reply (Idempotency-Key) → processing_complete
```

## Code

```python
import asyncio
from teamver_mail_agent import TeamverMailAgentClient

async def main():
    async with TeamverMailAgentClient.from_env() as client:
        events = await client.list_events(limit=10)
        for ev in events.events:
            if not ev.message_id:
                continue
            await client.ack_event(ev.event_id)
            msg = await client.get_message(ev.message_id)
            print(msg.subject, msg.body_text)

asyncio.run(main())
```

Scopes on the token: `agent:read`, `agent:events`, `agent:reply`.

See [API reference](./api-reference.md).
