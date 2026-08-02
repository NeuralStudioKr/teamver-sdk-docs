# Changelog — teamver-mail-agent

Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [0.3.1] - 2026-08-02

### Changed
- `from_env()` defaults `TEAMVER_MAIL_API_BASE` / `TEAMVER_MAIL_API_BASE_URL`
  to `https://mail-api.teamver.com` when unset (token still required).
- PyPI / README documentation URLs → public
  [teamver-sdk-docs/mail-agent](https://github.com/NeuralStudioKr/teamver-sdk-docs/tree/main/mail-agent).

## [0.3.0] - 2026-07-23

### Changed (16-1 §6, §13, §17)
- **BREAKING**: HTTP transport now delegates to `teamver-sdk-core`
  (`TeamverAsyncTransport`). mail-agent no longer implements its own retry/error
  loop — duplicated transport removed (§17). SSE streaming keeps a dedicated
  httpx client (out of core transport scope).
- Errors unified onto the core tree: `MailAgentAPIError` aliases `TeamverSDKError`.
- Reply/processing `Idempotency-Key` header is now threaded into the core
  idempotency-safe retry policy (non-idempotent POST retried only with a key).

### Added
- `teamver-sdk-core>=0.1.0` dependency.

## [0.2.0] - previous

### Added
- Mail agent client for inbound task claim, processing status, and reply flows.
- Runtime-contract error envelope alignment (15-1 §06).
