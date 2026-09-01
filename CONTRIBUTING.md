# Contributing

Thanks for helping improve Teamver SDK documentation.

## Scope

This repository is **docs and examples only**. SDK source lives in [`ns-teamver-packages`](https://github.com/NeuralStudioKr/ns-teamver-packages) and is published to PyPI. Do not document a second copy under `ns-teamver-agents/packages`.

Please open issues or PRs for:

- Missing / unclear installation or configuration steps
- Broken links or outdated API tables
- Example bugs or improvements
- Typos and wording

## SDK labels

When filing an issue, pick the matching label (or mention the SDK in the title):

| Label | Package |
|-------|---------|
| `sdk: agent` | `teamver-agent-sdk` |
| `sdk: mail-agent` | `teamver-mail-agent` |
| `sdk: core` | `teamver-sdk-core` |
| `sdk: skills` | `teamver-agent-skills` · adapters |

이 저장소는 **agent 공개 SDK** 문서만 다룹니다 (`agent-sdk` · `mail-agent` · `sdk-core` · `agent-skills` · adapters). `teamver-app-sdk` 등 App/BE SDK는 범위 밖입니다.

Also use `type: bug`, `type: docs`, or `type: question` when applicable.

## Editing docs

1. Fork and branch from `main`.
2. Keep each SDK folder self-contained; prefer relative links (`./installation.md`).
3. Do not commit secrets, tokens, or private monorepo paths.
4. Open a PR describing what changed.

## Examples

Examples under `examples/` should install packages from **PyPI** (or a local wheel), not private git URLs.
