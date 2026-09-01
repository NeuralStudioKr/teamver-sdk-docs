# Changelog — teamver-agent-skills (+ adapters)

Public docs mirror. Package changelogs may also ship on PyPI / in the source repo.

## teamver-agent-skills

### [0.1.1] - 2026-09-02

- `teamver_whoami` — discover workspace/agent/channels/drives from `tv_ak_*`.
- `teamver_report` — post to the default report channel (optional `channel_id`).
- Catalog 24 → 26 tools. Call `teamver_whoami` before asking a human for W-/AG2-/CH- ids.

### [0.1.0] - 2026-08-04

- Initial release: SkillRegistry, SkillExecutor, default skill catalog.
- `AgentToolAdapter` compat for `teamver-agent-sdk`.

## teamver-openclaw-adapter

### [0.1.0] - 2026-08-04

- Initial `OpenClawToolBridge` over teamver-agent-skills.

## teamver-hermes-adapter

### [0.1.0] - 2026-08-04

- Initial Hermes adapter over the same registry.
