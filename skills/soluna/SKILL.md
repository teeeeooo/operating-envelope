---
name: soluna
description: Deliver repository changes with Main-owned design and acceptance, bounded worker allocation approved by the user, Luna implementation, and independent review. Use for this explicit divided-authority workflow, not ordinary single-agent coding or editing this skill itself.
---

# Soluna

Main owns the user's goals, design, integration judgment, and final acceptance. Delegate bounded execution and independent review without transferring that ownership.

## Instruction priority

- Runtime system/developer policy and the user's current instructions outrank this skill.
- Previously established user authority persists unless the user narrows or withdraws it.
- Soluna adds workflow constraints only where this skill explicitly says so; do not infer extra approval requirements.
- If a Soluna rule itself forces a pause or approval request, identify the exact rule to the user.

## Role contract

- Main owns intake, original outcomes, protected acceptance, repository-backed design, worker allocation, evidence reconciliation, final judgment, and user reporting.
- Main may perform read-only intake and design before worker-allocation approval. It may also continue safe independent work while approved workers run.
- A Luna Explorer is optional and read-only. It maps code, documents, call relationships, tests, and impact boundaries without deciding architecture.
- Luna implementers own only their approved source/test/documentation scope and permitted commits.
- A fresh Luna auditor independently reviews the exact head and stays read-only through its audit decision.
- A fresh Astra specialist is exceptional: use it only for a named unresolved high-impact design or audit question where an independent context materially helps.

## Model and delegation contract

- Soluna does not constrain the current Main session's model or reasoning effort. The user owns that session-level choice.
- Any spawned Astra child must use `gpt-6-astra` with reasoning effort `low` or `medium`. `high`, `xhigh`, `max`, and `ultra` are prohibited for spawned Astra children.
- Spawn Luna workers with `gpt-5.6-luna`. Main chooses each Luna worker's supported reasoning effort according to the task; Soluna imposes no separate Luna effort floor, default, or ceiling.
- An exceptional Astra specialist uses a fresh context and an effort selected by Main from `low` or `medium`.
- Never silently substitute an approved child model or effort. If that combination is unavailable, report `BLOCKED` and request direction.
- Main owns delegation by default. Child agents must not spawn further agents unless the approved allocation explicitly grants one bounded child delegation to that stage.
- Auditors never delegate repair and never accept another agent's conclusion as audit evidence without direct verification.
- Default to one Luna implementer. Add a second only for genuinely independent work without shared-file or sequential dependency.

## Workflow

Use only the phases the task needs:

`INTAKE -> DESIGN_MAIN -> ALLOCATION_WAIT -> IMPLEMENT_LUNA -> AUDIT_LUNA -> FINAL_MAIN -> CLOSE_LUNA -> CLOSED`

Optional approved branches include `EXPLORE_LUNA`, `EVIDENCE_LUNA`, `SPECIALIST_ASTRA`, and bounded `REPAIR_LUNA -> AUDIT_LUNA`. Use `AUTHORITY_WAIT` only when a later external mutation needs authority not already present.

Main-only read-only work does not require allocation approval. If no child agent will be dispatched, do not invent an allocation approval unless the user explicitly asked to approve a Main-only plan.

## Worker-allocation approval

- Before the first child-agent dispatch, Main presents one concrete allocation and obtains explicit user approval. The original task request is not this allocation approval.
- The allocation names Main's responsibilities; each child worker's count, role, bounded scope, exact model/effort, dependencies, timing, and mutation authority; and any bounded repair or closeout reuse. Main's own model/effort is outside the allocation because the user selects the root session.
- Approval governs worker topology and delegated authority. It does not prevent Main from doing authorized read-only analysis, design, or integration work.
- Reapproval is required when worker count, role, model/effort, delegated scope, dependency structure, or mutation authority materially changes.
- Head movement, evidence updates, ordinary implementation choices, and editorial specification wording do not by themselves invalidate allocation approval.
- A change to the frozen outcome/acceptance contract is material. Record the revised contract and obtain fresh allocation approval before further child-agent dispatch.
- Read [references/execution-plan.md](references/execution-plan.md) before recording or approving an allocation.

## Outcomes, acceptance, and steering

- Freeze a compact outcome contract before implementation: original outcomes, observable acceptance, authoritative baseline references, relevant quality/runtime/provenance obligations, and named unknowns.
- Do not reduce outcomes, weaken protected criteria, invert negative tests, remove failing cohorts, or disable checks to manufacture PASS without explicit user approval of the lost guarantee.
- Treat user messages during active work as steering. Reconcile them against current scope, preserve unaffected completed work and valid evidence, and invalidate only what the steering actually changes.
- Steering alone does not reset the workflow or allocation approval. If it changes the contract or approved allocation, update that artifact and obtain the corresponding approval before dependent dispatch.

## State and handoff

Use [scripts/workflow_state.py](scripts/workflow_state.py) for compact state outside the repository. Store decisions, identities, artifact paths, findings, evidence references, steering revision, and next gate; keep raw logs and detailed reports elsewhere.

Before dispatch, read [references/handoff-contract.md](references/handoff-contract.md). Handoffs must be constraint-complete and method-light. Pass artifact references rather than conversation history.

## Dispatch, evidence, and gates

- Use native subagents. After dispatch, Main continues useful approved independent work without conflicting edits or redundant execution.
- When Main has nothing useful to do while an agent is still running, wait with the runtime's native wait/persistence mechanism instead of ending merely because the worker is pending.
- Never terminate an agent or declare failure solely because a wait interval elapsed. Investigate a concrete failure, blocker, user request, or meaningful event.
- Require a compact gate card from workers; detailed evidence belongs in an artifact.
- Before audit, repair, final review, commit, push, or closeout, read [references/gate-contract.md](references/gate-contract.md).
- Bind audit and validation to exact repository/base/head identity. Worker reports are navigation, not repository truth.
- Reuse valid evidence and rerun only checks invalidated by source, contract, identity, environment, provenance, or a concrete failure.
- Verification must be proportional to changed behavior and risk. Do not broaden or repeat passing tests without a concrete reason.
- Luna audit findings go to bounded Luna repair, then return to a fresh audit of the repaired head. After two failed repair rounds, stop at `BLOCKED` unless the user authorizes another round.
- Main final review compares the exact diff and audit evidence with the original outcome contract and protected baseline; a worker PASS is never sufficient by itself.

## Closeout

- Preserve unrelated user changes and logical commit boundaries.
- Commit, push, merge, deploy, or other external mutations only within authority already established by the user; request new authority at the latest practical point when it is actually needed.
- After an authorized push, verify expected local/remote equality and clean state.
- Report delivered and unmet outcomes, acceptance changes, decisive validation, runtime identity where relevant, and commit/push status.
- Separate gate status (`PASS`/`FAIL`/`BLOCKED`) from outcome status (`COMPLETE`/`PARTIAL`/`BLOCKED`).