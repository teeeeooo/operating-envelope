# operating-envelope Repository Instructions

This repository is the canonical source for the user-level Codex agent harness.

## Ownership

- `global/AGENTS.md` owns the canonical global working agreements deployed to `~/.codex/AGENTS.md`.
- `skills/<name>/` owns canonical reusable Skills deployed to `~/.codex/skills/<name>/`.
- `docs/ASTRA_AGENT_HARNESS_V2.md` owns the shared harness architecture and migration sequence.
- Focused design documents may refine one layer but must not silently contradict the governing architecture.

## Editing rules

- Keep global policy repository-agnostic and small.
- Keep conditional workflows in Skills rather than expanding always-on `AGENTS.md` surfaces.
- Do not copy repository-specific product or domain rules into global policy or global Skills.
- Treat runtime files under `~/.codex` as deployed projections, not canonical source.
- When a task includes runtime rollout, update canonical source first, then deploy and verify canonical/runtime equality.
- Validate changed Skills with the installed system `skill-creator` validator when available.
- Preserve explicit-only invocation policy for workflows that intentionally require direct user selection.
