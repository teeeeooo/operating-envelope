# operating-envelope

`operating-envelope` is the version-controlled canonical source for the user's agent harness: shared execution policy, reusable Skills, memory/recall architecture, and migration designs for repository-local agent environments.

Runtime locations such as `~/.codex/AGENTS.md` and `~/.agents/skills/` are deployment surfaces, not the canonical design source. Repository-local projects keep their own invariants, domain truth, and task-specific Skills rather than copying this repository's full policy surface.

## Current Direction

The current redesign targets GPT-6 Astra and follows OpenAI's guidance on instruction sensitivity, initiative and follow-through, explicit delegation policy, and proportional testing. The governing migration design will live under `docs/`.

The intended layers are:

- global `AGENTS.md`: small, always-on execution posture shared across repositories
- global Skills: reusable workflows that should load only when relevant
- repository `AGENTS.md`: repository-specific invariants and routing
- repository Skills: task-specific workflows unique to that repository
- project knowledge: architecture, validation, decisions, failures, current state, and compact recall indexes
- historical evidence: logs, retired designs, result records, and diagnostics that should not act as current instructions

## Existing Small Template

`templates/small/` is retained as migration input from the repository's previous purpose. It is not automatically authoritative for the new harness architecture.
