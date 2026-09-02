# Changelog — teamver-agent-skills (+ adapters)

Public docs mirror. Package changelogs may also ship on PyPI / in the source repo.

## teamver-agent-skills

### [0.1.3] - 2026-09-02

- `teamver_inbox_poll` / `teamver_inbox_reply`. Catalog 26 → 28 tools. Needs `teamver-agent-sdk>=0.6.11`.

### [0.1.2] - 2026-09-02

- Preserve HTTP status on skill failure so OpenClaw can return 401 vs 404 as tool results.

### [0.1.1] - 2026-09-02

- `teamver_whoami` — discover workspace/agent/channels/drives from `tv_ak_*`.
- `teamver_report` — post to the default report channel (optional `channel_id`).
- Catalog 24 → 26 tools. Call `teamver_whoami` before asking a human for W-/AG2-/CH- ids.

### [0.1.0] - 2026-08-04

- Initial release: SkillRegistry, SkillExecutor, default skill catalog.
- `AgentToolAdapter` compat for `teamver-agent-sdk`.

## teamver-openclaw-adapter

### [0.1.1] - 2026-09-02

- OpenAI function envelopes, `TOOL_NAMES`, `from_env()`.
- Dispatch maps 401/403 → `MAIN_UNAUTHORIZED`, 404 → `MAIN_PATH_NOT_FOUND`.
- Bake SSOT is PyPI (not `ns-teamver-agents/packages`).

### [0.1.0] - 2026-08-04

- Initial `OpenClawToolBridge` over teamver-agent-skills.

## teamver-hermes-adapter

### [0.1.0] - 2026-08-04

- Initial Hermes adapter over the same registry.
