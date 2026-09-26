# Workflow evidence policy review — 2026-09-26

Historical change evidence; not an additional instruction surface.

## Basis and plan

The user requested applying a retrospective of May Web's first milestone to global/repository guidance, after checking official OpenAI guidance. Read the official [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Build skills](https://learn.chatgpt.com/docs/build-skills), and [Best practices](https://learn.chatgpt.com/guides/best-practices). They support scoped layered guidance, concise task-specific skills, progressive disclosure, clear completion criteria, and representative validation. The failure classification and evidence rules below are our adaptation, not a prescribed OpenAI template.

Plan: make two bounded global edits, validate, then deploy only the two changed selected files. Repository-specific changes stay in May Web; no host-root migration, new skill, invocation-policy change, or config/security change.

## Changes and ownership

- `global/AGENTS.md`: scope uses agreed user outcomes rather than inheriting a predecessor feature inventory; completion evidence stays bounded to verified starting states, entries and results. Existing initiative, authority, reuse and proportional verification rules remain.
- `skills/agent-policy-maintenance/SKILL.md`: distinguish absent rules, unapplied rules, conflicting rules and missing deterministic checks before choosing an edit. Preserve official guidance vs observation vs adaptation distinctions. Improve the existing owner rather than appending duplicate instructions.
- The initiating project's detailed completion mapping, shared UI/navigation review, family-fact readback, and deployment receipt policy remain in its repository Skills/Canonical/runbook. Global policy contains no May Web domain rules.

## Rollout boundary

Source and installed files matched before editing; the worktree was clean. `deployment/desktop.json` selects agent-policy-maintenance. Retain `~/.codex/skills`, as supported by the existing deployment record and this conversation's available-skill path; do not install a duplicate under the documented `~/.agents/skills` path. The latter is absent. No global override exists and CODEX_HOME is unset. File equality and currently advertised paths do not prove new-session loading or behavioral reliability.

Rollback: revert this scoped source change and copy only these same two files to their original runtime locations. Preserve unrelated skills, explicit-only settings and intentional absences.

## Validation and limits

- Installed skill-creator `quick_validate.py`: changed policy Skill PASS, using temporary `uv --with pyyaml` because the default Python lacks PyYAML. No system dependency/config change.
- `python3 scripts/validate_harness.py`: PASS. After copying only the two changed selected files, `--runtime-home ~/.codex`: PASS, including selected-file equality and preserved intentional absences/invocation metadata.
- Static scenario review: an unneeded predecessor-only capability does not become mandatory; a passing pre-existing-record linkage test does not close a missing first-use creation path; an ordinary product edit does not invoke policy maintenance; an existing valid but unapplied rule calls for better evidence/routing rather than duplicate rules. These outcomes are document review, not independent model-run evidence.
- Global working agreements were refreshed into the current conversation after the file update. No new-session host probe or activation reliability claim. Existing deployment root and all other installed Skills remain unchanged.
- Diff review/check PASS. Local commit only; no remote push, product deployment or policy-root migration in this task.
