# operating-envelope

`operating-envelope` is the version-controlled canonical source for the user's agent harness: shared execution policy, reusable Skills, memory/recall architecture, and migration designs for repository-local agent environments.

Runtime locations such as `~/.codex/AGENTS.md` and `~/.codex/skills/` are deployment surfaces, not the canonical design source. Repository-local projects keep their own invariants, domain truth, and task-specific Skills rather than copying this repository's full policy surface.

`~/.codex/skills/` is the verified deployment on this desktop host, not a universal discovery rule for every Codex host. See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for host selection and optional runtime equality checks.

## Current Direction

The current redesign targets GPT-6 Astra and follows OpenAI's guidance on instruction sensitivity, initiative and follow-through, explicit delegation policy, and proportional testing. The governing migration design is [`docs/ASTRA_AGENT_HARNESS_V2.md`](docs/ASTRA_AGENT_HARNESS_V2.md).

The intended layers are:

- global `AGENTS.md`: small, always-on execution posture shared across repositories
- global Skills: reusable workflows that should load only when relevant
- repository `AGENTS.md`: repository-specific invariants and routing
- repository Skills: task-specific workflows unique to that repository
- project knowledge: architecture, validation, decisions, failures, current state, and compact recall indexes
- historical evidence: logs, retired designs, result records, and diagnostics that should not act as current instructions


## Canonical Sources

- `docs/ASTRA_AGENT_HARNESS_V2.md`: shared architecture and migration baseline
- `docs/GLOBAL_AGENTS_DESIGN.md`: admission, ownership, and validation rules for the global instruction layer
- `global/AGENTS.md`: canonical content deployed to `~/.codex/AGENTS.md`

- `skills/soluna/`: explicit-only multi-agent delivery workflow
- `skills/grill-me/`: upstream-derived design interrogation/stress-test workflow with guarded implicit invocation
- `skills/desktop-table-ui/`: reusable desktop table interaction contract
- `skills/desktop-window-lifecycle/`: reusable desktop window/dialog/page lifecycle contract
- `skills/python-test-portability/`: reusable Python test portability contract
