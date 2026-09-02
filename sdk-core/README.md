# teamver-sdk-core

Shared async HTTP core for Teamver Python SDKs.

PyPI: [teamver-sdk-core](https://pypi.org/project/teamver-sdk-core/)

- [Changelog](./changelog.md)

## Features

| Module | Role |
| --- | --- |
| `defaults` | Production API hosts: `https://api.teamver.com`, `https://agent-api.teamver.com`, `https://mail-api.teamver.com` |
| `transport` | `TeamverAsyncTransport` — httpx async requests, retry, error normalization |
| `errors` | `TeamverSDKError` tree + `error_for_status` / `parse_error_body` / `format_error` |
| `retry` | `RetryPolicy` — safe retries (non-idempotent POST needs `idempotency_key`) |
| `context` | `RequestContext` — `request_id` / `correlation_id` |
| `pagination` | cursor `iterate_pages` |
| `masking` | mask tokens / Bearer / internal keys in logs |

### Default API hosts (SSOT)

| Constant | Host | Used by |
| --- | --- | --- |
| `DEFAULT_MAIN_API_BASE` | `https://api.teamver.com` | channel/Drive/DM, agent-sdk |
| `DEFAULT_AGENT_API_BASE` | `https://agent-api.teamver.com` | agent-sdk jobs/heartbeat |
| `DEFAULT_MAIL_API_BASE` | `https://mail-api.teamver.com` | mail-agent, agent-sdk mail |

No path suffix (`/api`, `/v1`). Override per package via env.

## Error tree

```
TeamverSDKError
├─ ConfigurationError
├─ AuthenticationError        (401)
├─ AuthorizationError         (403)
├─ NotFoundError              (404)
├─ ConflictError              (409)
│  ├─ IdempotencyConflictError
│  └─ VersionConflictError
├─ RateLimitError             (429)
├─ TemporaryUnavailableError  (502/503/504)
└─ TransportError
```

`TeamverSDKError` carries `.status_code`, `.path`, `.request_id`, `.response_body`. Use `format_error(exc)` for a one-line ops log (no token). Requires **0.1.3+**.

## Retry rules

- Retried: transport failure, `429`, `502`, `503`, `504`
- `GET/HEAD/PUT/DELETE` — treated as idempotent
- `POST/PATCH` — retried only when `idempotency_key` is set

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](./LICENSE).
