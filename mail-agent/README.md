# teamver-mail-agent

Async Python client for the **Teamver Mail BE** Agent API (`/v1/agent/*`).

PyPI: [teamver-mail-agent](https://pypi.org/project/teamver-mail-agent/)

For channel + DM + Drive + mail in one facade, use [`teamver-agent-sdk`](../agent-sdk/) instead.

## Docs

- [Installation](./installation.md)
- [Quick start](./quickstart.md)
- [API reference](./api-reference.md)
- [Agent guide](./guide.md)
- [Changelog](./changelog.md)
- [Examples](../examples/mail-agent/)

## Install

```bash
pip install teamver-mail-agent
```

## Minimal example

```python
import asyncio
from teamver_mail_agent import TeamverMailAgentClient

async def main():
    async with TeamverMailAgentClient.from_env() as client:
        events = await client.list_events(limit=10)
        for ev in events.events:
            if ev.message_id:
                await client.ack_event(ev.event_id)

asyncio.run(main())
```

## License

MIT — documentation in this repo; package license on PyPI.
