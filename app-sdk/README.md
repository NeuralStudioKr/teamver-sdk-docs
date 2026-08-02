# teamver-app-sdk

Python client for **AI Apps** talking to Teamver Main BE (user JWT / bootstrap / drive helpers).

PyPI: [teamver-app-sdk](https://pypi.org/project/teamver-app-sdk/) (when published)

## Docs

- [Changelog](./changelog.md)
- [Examples](../examples/app-sdk/)

## Install

```bash
pip install teamver-app-sdk
```

Python **≥ 3.11**.

## Environment

| env | purpose | default |
|-----|---------|---------|
| `TEAMVER_API_BASE_URL` | Main host (**no** `/api`) | `https://api.teamver.com` |
| `TEAMVER_APP_KEY` | App key segment | `mail` |
| `TEAMVER_INTERNAL_API_KEY` | M2M (required for `TeamverM2MClient`) | — |
| `TEAMVER_HTTP_TIMEOUT_SECONDS` | timeout | `10` |

## Basic usage

```python
from teamver_app_sdk import TeamverAppClient

async with TeamverAppClient.from_env(app_key="docs") as teamver:
    ctx = await teamver.auth.resolve_context(
        access_token="<teamver access jwt>",
        workspace_id="WS-...",
    )
    asset = await teamver.drive.upload_bytes_to_personal_drive(
        access_token=ctx.access_token,
        filename="result.txt",
        content=b"hello",
        content_type="text/plain",
    )
```

## FastAPI helper

```python
from fastapi import Depends
from teamver_app_sdk import TeamverAppClient
from teamver_app_sdk.integrations.fastapi import create_teamver_context_dependency

teamver = TeamverAppClient.from_env(app_key="docs")
get_teamver_context = create_teamver_context_dependency(teamver)

@router.post("/api/documents")
async def create_document(ctx=Depends(get_teamver_context)):
    return {"user_id": ctx.user_id, "workspace_id": ctx.workspace_id}
```

## Related SDKs

- Agent runtimes → [agent-sdk](../agent-sdk/)
- Mail-only agents → [mail-agent](../mail-agent/)

## License

MIT — documentation in this repo; package license on PyPI.
