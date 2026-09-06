# Handoff Contract

Read this before dispatching a Luna Explorer, evidence worker, implementer, auditor, bounded repair, or exceptional Astra specialist. Verify the assignment against the approved worker allocation before spawning.

## Required sections

Keep each handoff concise and use these sections in order:

1. **Role and authority** — role, permitted mutations, prohibited actions, exact model/effort, and whether bounded child delegation is explicitly granted.
2. **Identity gate** — repository path, branch/worktree, expected base/head, clean/dirty expectations.
3. **Authoritative artifacts** — outcome contract, protected baseline, compact state, design/evidence, applicable instructions, and prior gate card. Link; do not copy.
4. **Objective and scope** — one bounded outcome, owned files or behavior, explicit non-goals.
5. **Invariants and acceptance** — only load-bearing constraints and observable success criteria.
6. **Validation and next gate** — checks owned by this role, reusable evidence, invalidation triggers, commit authority, next phase.
7. **Report contract** — compact gate card plus a path to detailed evidence.

Self-contained means the agent can start from identity, authority, artifacts, invariants, acceptance, and next gate. It does not mean copying repository or conversation history.

## Method-light rule

Specify what must remain true, not implementation details the worker can responsibly choose. Prescribe helper names, file splits, algorithms, thresholds, or test layout only when Main marked them load-bearing.

A worker stops on a new owner, public/persisted contract, runtime boundary, external mutation, or behavior outside approved acceptance.

## Delegation rule

Main owns delegation by default. A child agent must not spawn another agent unless its approved stage explicitly grants one bounded child delegation with a named purpose and scope. That child may not delegate further.

Auditors never delegate repair work. No agent may use another agent's conclusion as final evidence without directly checking the decisive repository state required by its own role.

## Role-specific clauses

### Luna Explorer

- Read only the assigned code/document scope and relevant boundaries.
- Report file/symbol references, call relationships, related tests, impact candidates, facts, hypotheses, and unknowns.
- Do not decide final architecture, implement, commit, or mutate validation state.

### Evidence Luna

- Inventory repository-owned authority, sibling implementations, local patterns, and supported official/upstream mechanisms relevant to the requested behavior.
- Use external maintained implementations only when repository and official sources do not resolve the question.
- Produce a compact reuse inventory; Main makes the architecture decision.

### Luna implementer

- Own only assigned source, tests, source-completing documentation, and authorized commits.
- Reuse compatible existing ownership instead of creating duplicate mechanisms.
- Stop with `NEEDS_DECISION` if implementation requires an unapproved owner, public contract change, acceptance reduction, or broader mechanism.
- Preserve unrelated user changes and report conflicts instead of overwriting them.

### Luna auditor

- Start fresh and verify exact identity, complete diff, applicable instructions, and load-bearing owners directly.
- Challenge implementation against original outcomes and protected old expectations, not merely the latest specification.
- Inspect changed oracles, omitted cohorts, real-path coverage, runtime identity, and claimed performance evidence when relevant.
- Stay read-only and do not repair findings.
- Return `AUDIT: PASS`, `AUDIT: FAIL`, or `AUDIT: BLOCKED`.

### Bounded repair

- Name each finding, affected owner, preserved evidence, invalidated evidence, and exact next audit gate.
- Change only the bounded finding. Do not broaden architecture or acceptance.

### Exceptional Astra specialist

- Use only `gpt-6-astra` in a fresh context. Main selects `low` or `medium`; higher reasoning efforts are prohibited for spawned Astra children.
- Answer one named unresolved high-impact design or audit question from the minimum evidence needed.
- Do not become a routine gate, implement source, or replace Main's final judgment.

## Gate card

```text
STATUS: PASS | FAIL | BLOCKED | NEEDS_DECISION
ROLE: <role>
BASE: <sha or N/A>
HEAD: <sha or N/A>
CHANGED_SCOPE: <paths/count or none>
FINDINGS: <none or concise severity-tagged list>
OUTCOMES: <covered and unmet original outcome IDs>
ACCEPTANCE_CHANGES: <old/new criteria and approval/evidence>
EVIDENCE_EXECUTED: <concise list>
EVIDENCE_REUSED: <concise list>
EVIDENCE_INVALIDATED: <concise list>
ARTIFACT: <path or N/A>
NEXT_GATE: <phase>
```

Do not paste full logs, diffs, or repeated passing criteria into the conversation.