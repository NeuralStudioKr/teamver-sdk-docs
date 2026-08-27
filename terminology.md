# Terminology — Teamver “skills” vs OpenClaw/Codex skills

These names look similar but are **different layers**. Mixing them up is the most common install mistake.

| Term | What it is | How you install / use it |
|------|------------|---------------------------|
| **Teamver Agent SDK** (`teamver-agent-sdk`) | Python runtime facade: channel, DM, Drive, events, jobs, mail | `pip install teamver-agent-sdk` |
| **Teamver Agent Skills** (`teamver-agent-skills`) | Engine-neutral **skill registry + executor** over the SDK (JSON Schema tools) | `pip install teamver-agent-skills` |
| **OpenClaw / Hermes adapter** | Bridges Teamver skills → engine-specific tool registration | `pip install teamver-openclaw-adapter` or `teamver-hermes-adapter` |
| **OpenClaw / Codex Skill** (`SKILL.md`, plugin bundle) | Agent **prompt/ops recipe**, not a Python package | Engine skill install / `$skill-name` — **not** `pip install teamver-agent-sdk` |

## Decision guide

```text
Need Teamver APIs from Python?
  └─ pip install teamver-agent-sdk

Need LLM function-calling tools (channel/DM/drive/mail/jobs) from OpenClaw?
  └─ pip install teamver-agent-skills teamver-openclaw-adapter
       (tokens still come from openclaw.env — ACL + tv_ak_ / tv_agent_)

Need a Codex/OpenClaw “how to use Teamver” playbook?
  └─ That is a separate SKILL.md / plugin — not these PyPI packages.
```

## Related docs

- [agent-sdk/](./agent-sdk/) — runtime SDK  
- [agent-skills/](./agent-skills/) — registry, executor, adapters  
- PyPI publisher: [neuralstudio.kr](https://pypi.org/user/neuralstudio.kr/)
