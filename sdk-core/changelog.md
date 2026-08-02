# Changelog — teamver-sdk-core

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [0.1.1] - 2026-08-02

### Added
- `defaults.py`: production API host constants
  (`DEFAULT_CHANNEL_API_BASE` / `DEFAULT_MAIN_API_BASE` =
  `https://api.teamver.com`, `DEFAULT_AGENT_API_BASE` =
  `https://agent-api.teamver.com`, `DEFAULT_MAIL_API_BASE` =
  `https://mail-api.teamver.com`). Exported from package root.

### Changed
- PyPI documentation URLs → public
  [teamver-sdk-docs/sdk-core](https://github.com/NeuralStudioKr/teamver-sdk-docs/tree/main/sdk-core).
- PyPI author/maintainer → NeuralStudio `<dev@neuralstudio.kr>`.

## [0.1.0] - 2026-07-23

### Added
- Initial greenfield core shared by all Teamver SDKs (16-1 §4, §13).
- `TeamverAsyncTransport`: httpx-based async transport with retry, error
  normalization, and request-context header propagation.
- Unified exception tree rooted at `TeamverSDKError`
  (`Authentication`/`Authorization`/`NotFound`/`Conflict`/`RateLimit`/
  `TemporaryUnavailable`/`Transport` + idempotency/version conflict subtypes).
- `error_for_status` / `parse_error_body` normalize Main `error`, FastAPI
  `detail`, and legacy shapes into one model while preserving status/code/request_id.
- `RetryPolicy` with idempotency-aware retry (non-idempotent POST retried only
  when an `Idempotency-Key` is supplied).
- `RequestContext` for `request_id` / `correlation_id` propagation.
- `iterate_pages` cursor pagination helper and `extract_page`.
- `mask_secrets` / `mask_headers` for token/Bearer/internal-key redaction.
