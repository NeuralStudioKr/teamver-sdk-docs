# Changelog — teamver-agent-sdk

Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [0.6.7] - 2026-09-02

### Changed
- `ChannelClient.list_channels()` never calls `/collab/channels` (human JWT). ACL only: `/ai-agents/me/accessible-channels`, then workspace accessible-channels on 404.
- Source of truth is this PyPI package (`ns-teamver-packages`). OpenClaw images `pip install` a pin; there is no second tree in `ns-teamver-agents`.

## [0.6.6] - 2026-09-02

### Added
- Token-only setup: `TEAMVER_AGENT_TOKEN` is the only required human secret. Workspace/agent ids come from `GET /api/v2/ai-agents/me`.
- `TeamverAgent.connect()`, `whoami()`, `describe_setup()`, CLI `python -m teamver_agent_sdk required-env|whoami|doctor`.
- Channel list uses ACL `accessible-channels`. `report()` can omit `channel_id` after identity is resolved.
- Tools: `teamver_whoami`, `teamver_report` (`teamver-agent-skills` 0.1.1).
- Docs: [openclaw.md](./openclaw.md).

## [0.6.5] - 2026-08-28

### Changed
- `from_env()` reads **`TEAMVER_AGENTS_API_BASE`** when `TEAMVER_AGENT_API_BASE` is unset (OpenClaw `openclaw.env`).
- Docs: identity examples **`W-…` / `AG2-…`**. ACL (policy) is not a substitute for `tv_ak_*` in the runtime.

> Published on PyPI as [teamver-agent-sdk 0.6.5](https://pypi.org/project/teamver-agent-sdk/0.6.5/). API behavior above 0.6.3 is unchanged except the env alias.

## [0.6.3] - 2026-08-03

### Changed
- **`TEAMVER_MAIN_API_BASE`** / config `main_api_base` is the canonical Main host (channel · DM · drive).
- Deprecated: `TEAMVER_CHANNEL_API_BASE`, config `channel_api_base` (alias only; legacy env still read if MAIN unset).

## [0.6.2] - 2026-08-02

### Changed
- `from_env()` defaults API hosts when unset:
  `TEAMVER_MAIN_API_BASE` → `https://api.teamver.com`,
  `TEAMVER_AGENT_API_BASE` → `https://agent-api.teamver.com`,
  `TEAMVER_MAIL_API_BASE` → `https://mail-api.teamver.com`
  (SSOT: `teamver-sdk-core` defaults).
- PyPI / README documentation URLs → public
  [teamver-sdk-docs/agent-sdk](https://github.com/NeuralStudioKr/teamver-sdk-docs/tree/main/agent-sdk)
  (private monorepo `Repository` link removed).
- PyPI author/maintainer → NeuralStudio `<dev@neuralstudio.kr>`.

## [0.6.1] - 2026-08-02

### Changed (OpenClaw → agent 용어)
- Prefer `teamver_agent_sdk.tools` / `AgentToolAdapter` (function-calling).
- `OpenClawAdapter` · `teamver_agent_sdk.openclaw` 는 하위 호환 alias/shim.

## [0.6.0] - 2026-08-02

### Added (Drive / DM for agent runtimes)
- `DmClient` — workspace DM list/open/read/post (`/api/v2/workspace/{ws}/dm/*`).
- `DriveClient` — shared-drive list, file list, download-url, local download, presigned 3-step upload.
- Agent tools: `teamver_channel_read` / `react`, `teamver_dm_*` (4), `teamver_drive_*` (5).
  Catalog **13 → 24**.
- Docs: `docs/11_agent_sdk_Drive_DM_확장_상위설계.md` + 구현설계·현황.
- Tests: `test_dm_client.py`, `test_drive_client.py`; adapter catalog assertions.

## [0.5.0] - 2026-07-23

### Added (15-1 §07.2-E — Engine 런타임 결선)
- `intent_runtime.py` — `JobIntentClassifier`: 주입된 `chat_fn`(동기/비동기)으로 판단 루프
  수행(규칙 선필터 → 구조화 출력 LLM → 계약 검증 → 선택적 apply). 잘못된 LLM 출력은 안전
  CLARIFY 로 폴백. `ChatCompletionFn` Protocol. 모델·프레임워크 무관(테스트는 가짜 chat_fn).
- `classify_and_apply()` — 판단 후 `AgentToolAdapter` 로 create/attach/NO_JOB 라우팅.
- 신규 export + `tests/test_intent_runtime.py`(5). 49 passed.

## [0.4.0] - 2026-07-23

### Added (15-1 §07.2 판단 위치·Engine 연동)
- `job_intent.py` — Job 의도 판단을 **Engine LLM** 이 하도록 돕는 계약/프롬프트:
  `JobCandidate`/`InboundMessage`/`JobDecisionContext`, `SYSTEM_PROMPT`+`FEW_SHOTS`,
  `render_context`/`build_job_decision_messages`(모델 무관), `job_decision_response_schema`
  (구조화 출력), `rule_prefilter`(명백한 잡담→NONE, LLM 생략).
- `AgentToolAdapter.build_job_decision_request()`(messages+schema+선필터) /
  `apply_job_decision()`(검증된 decision → create/attach/NO_JOB 라우팅).
- `jobs.create()` + `JobsCreateArgs` 에 `request_intent`/`related_job_id`/`link_type`/
  `confidence` 추가(서버 링크·SUPERSEDE 종료·confidence 가드 연동).
- 신규 export + `tests/test_job_intent_golden.py`(10). 44 passed.

## [0.3.0] - 2026-07-23

### Added (15-1 §07.1 요청 의도 분류 / Request Intent Classification)
- `AgentJobDecision` 확장: `request_intent`(AMEND/SUPERSEDE/FOLLOW_UP/NEW/NONE/
  CLARIFY), `related_job_id`, `link_type`(follow_up|supersedes), `clarification`.
- `effective_intent` — `request_intent` 미지정 시 `action` 에서 유도(ATTACH→AMEND,
  CREATE→NEW, NO_JOB→NONE).
- 검증 규칙: AMEND→existing_job_id, SUPERSEDE/FOLLOW_UP→related_job_id,
  link_type→related_job_id 정합. `contracts/schemas/job-decision.schema.json` 동기.
- 신규 export: `RequestIntent`, `LinkType`, `Clarification`.

## [0.2.0] - 2026-07-23

### Changed (16-1 §7, §13, §17)
- **BREAKING**: HTTP transport (channel/events/jobs/runtime) now delegates to
  `teamver-sdk-core` (`TeamverAsyncTransport`). Per-surface retry/error loops
  removed (§17). `AgentHTTP` builds the transport per request so a swapped
  underlying client is honored (test injection).
- Errors unified onto the core tree: `TeamverAgentError`→`TeamverSDKError`,
  `TeamverAgentConfigError`→`ConfigurationError`, `TeamverAgentAPIError`→root.

### Added
- **Agent Tool Adapter** (§8): `teamver_agent_sdk.tools` (`AgentToolAdapter`;
  legacy `openclaw`/`OpenClawAdapter` alias) with `ToolSpec`,
  `build_tool_specs`, `tool_json_schemas` (validate args → route to agent surface).
  13 tools; JSON Schema generated from Pydantic models.
- **Job decision** (§9): `AgentJobDecision` model + `JobsClient.decide()` — a
  local schema validator (no server decide API); conditional required fields for
  CREATE_JOB / ATTACH_JOB.
- `teamver-sdk-core>=0.1.0` dependency; bumped `teamver-mail-agent>=0.3.0`.

## [0.1.0] - previous

### Added
- Unified Teamver SDK for agent runtimes: channel reporting, event receive
  loop, and mail integration.
- Event checkpoint stores (`InMemoryCheckpointStore`, `FileCheckpointStore`) and
  `dedup_key` helper for idempotent event processing (15-1 §04).
