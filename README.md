# Teamver SDK Docs

Public documentation for Teamver **agent** Python SDKs published on PyPI.

> Scope: agent 런타임에 필요한 공개 패키지 (`agent-sdk` · `mail-agent` · `sdk-core` · **agent-skills** · OpenClaw/Hermes adapters).  
> App/BE용 SDK(`teamver-app-sdk` 등)는 PyPI·문서 공개 대상이 아닙니다.

Publisher: [pypi.org/user/neuralstudio.kr](https://pypi.org/user/neuralstudio.kr/)

| PyPI package | Docs | Latest |
|--------------|------|--------|
| [`teamver-agent-sdk`](https://pypi.org/project/teamver-agent-sdk/) | [agent-sdk/](./agent-sdk/) | 0.6.5 |
| [`teamver-mail-agent`](https://pypi.org/project/teamver-mail-agent/) | [mail-agent/](./mail-agent/) | 0.3.1 |
| [`teamver-sdk-core`](https://pypi.org/project/teamver-sdk-core/) | [sdk-core/](./sdk-core/) | 0.1.2 |
| [`teamver-agent-skills`](https://pypi.org/project/teamver-agent-skills/) | [agent-skills/](./agent-skills/) | 0.1.0 |
| [`teamver-openclaw-adapter`](https://pypi.org/project/teamver-openclaw-adapter/) | [agent-skills/openclaw-adapter.md](./agent-skills/openclaw-adapter.md) | 0.1.0 |
| [`teamver-hermes-adapter`](https://pypi.org/project/teamver-hermes-adapter/) | [agent-skills/hermes-adapter.md](./agent-skills/hermes-adapter.md) | 0.1.0 |

**Start here if someone said “skill 설치”:** [terminology.md](./terminology.md) — Teamver Python skills ≠ OpenClaw/Codex `SKILL.md`.

## Repository layout

```text
terminology.md   # Teamver skills vs OpenClaw/Codex skills
agent-sdk/       # Unified agent runtime SDK (channel, DM, Drive, mail, jobs)
agent-skills/    # Engine-neutral skills + OpenClaw/Hermes adapters
mail-agent/      # Mail BE agent client
sdk-core/        # Shared HTTP transport / errors
examples/        # Runnable snippets (install from PyPI)
```

## Quick links

- Issues: [github.com/NeuralStudioKr/teamver-sdk-docs/issues](https://github.com/NeuralStudioKr/teamver-sdk-docs/issues)
- Website: [teamver.com](https://teamver.com)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

Documentation and examples in this repository are licensed under the MIT License.
See [LICENSE](./LICENSE).
