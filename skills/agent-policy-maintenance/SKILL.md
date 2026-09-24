---
name: agent-policy-maintenance
description: Audit or consolidate AGENTS.md, agent Skills, and instruction-owner maps; separate reusable guidance from repository contracts and reconcile canonical sources with selected runtime installations. Use for agent-policy maintenance, not ordinary product documentation or feature work.
---

# Agent Policy Maintenance

Keep useful instructions easy to discover without copying product truth into a global handbook. Respect the requested repositories and deployment scope; policy maintenance does not authorize product changes, publishing, or security-setting changes.

## Establish ownership

- Inspect the actual instruction chain, overrides, Skill roots, canonical source, deployment selection, and local changes before editing. A file's presence is not evidence that the host loaded it.
- When discovery or invocation behavior matters, consult current official documentation and the installed host. Preserve a working deployment root until a host check supports migration; do not duplicate same-name Skills across discovered roots.
- Treat user-requested opt-outs, explicit-only invocation, system-managed Skills, unrelated installed Skills, and existing security configuration as boundaries to preserve.

## Choose the smallest owner

- Global AGENTS: stable, broadly useful execution behavior only.
- Global Skill: a demonstrated cross-project conditional workflow with a discriminating trigger.
- Repository AGENTS: important repository invariants and routing; repository Skills: domain-specific procedures.
- Canonical project documents: product meaning, schemas, security, acceptance, and implementation ownership. Current-state files and historical evidence retain their distinct roles.
- Merge repeated rules into their existing owner before adding a new Skill. Keep toolkit choices, formulas, private-data rules, and platform acceptance local unless genuine reuse is established.

## Edit and reconcile

- Preserve each still-valid constraint when removing duplication; record a replacement owner before retiring an active contract. Do not rewrite historical evidence as current policy.
- Move substantial conditional detail to linked references only when that avoids irrelevant reads. Keep the activation boundary and essential constraints in SKILL.md; make required reference-reading conditions explicit.
- Update canonical source first. For authorized installation, copy only selected changed managed files after validation; do not install the entire canonical catalog or overwrite host configuration.

## Validate and report

- Check frontmatter, invocation policy, reference paths, ownership coverage, and representative matching/non-matching requests. Run changed helper tests and inspect the complete diff.
- Use the installed skill-creator validator when runnable. Report unavailable dependencies rather than calling a substitute an official validation pass.
- Check managed source/runtime equality, overrides, duplicate names, and intentional absences separately from actual host discovery and model behavior.
- Report applied changes, deliberately retained owners, verification limitations, and exact remaining work. Keep inventories, case evidence, and rollback material with the audit, not in always-on instructions.
