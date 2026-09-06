# Gate Contract

Read this for audit, repair, Main final review, exceptional Astra specialist review, commit, push, merge, or closeout.

## Protected baseline

Audit original goals and authoritative prior expectations as well as the current design. Inventory changed oracles, fixtures, cohorts, tolerances, golden values, skip/xfail, and validation options. Classify each as equivalent coverage, independently evidenced correction, explicitly approved behavior change, or regression.

Prior relevant completion obligations cannot silently disappear. Missing quality, performance, runtime-identity, or provenance evidence stays missing; test duration is not application performance.

## Identity gate

Directly verify repository, applicable instructions, branch/worktree, complete changed scope, base SHA, head SHA, and worktree state. Refresh identity after checkout, commit, rebase, reset, fetched remote movement, dirty worktree changes, another actor update, or repair.

Worker reports and remembered conversation are navigation only. Exact repository state is authority.

## Evidence reuse

Reuse evidence only while it still covers the same relevant source/contract/identity/environment/provenance and required acceptance area. After repair, rerun only invalidated evidence.

Use statuses precisely: `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, `NOT_AVAILABLE`, `UNVERIFIED`.

Verification must be proportional to changed behavior and risk. After required checks pass, broaden or repeat testing only for a concrete invalidation, failure, shared-owner risk, or unresolved acceptance question. Avoid tests that merely mirror implementation for reversible low-impact changes.

## Audit independence

The fresh Luna auditor directly reviews the exact head and materially adjacent owners. It does not repair findings. A repair creates a new head and returns to audit; preserve evidence the repair did not invalidate.

Audit findings must state material impact, affected owner, proof, required repair, and invalidated evidence. Do not block on optional style or unsupported hypothetical risk.

## Main final gate

Main reviews directly:

1. frozen outcome contract and protected baseline;
2. exact base/head and complete changed scope;
3. load-bearing implementation and high-risk adjacent owners;
4. Luna audit card and unresolved findings;
5. evidence provenance/invalidation; and
6. authority for the next external mutation.

Use an exceptional fresh Astra specialist only for one unresolved high-impact question. It must use `gpt-6-astra`; Main selects `low` or `medium`, and spawned Astra children may not exceed `medium`. It assists Main; it does not become a mandatory gate or own the final judgment.

Return `FINAL_GATE: PASS`, `FINAL_GATE: FAIL`, or `FINAL_GATE: BLOCKED`. Separate this gate status from outcome `COMPLETE`, `PARTIAL`, or `BLOCKED`.

## Commit and external-mutation gate

- Commit only within established authority and preserve logical units.
- Never amend, rebase, force-push, discard unrelated state, merge, deploy, or publish without authority that covers that action.
- Request missing authority at the latest practical point after producing the concrete reviewable state the user is being asked to authorize.
- Before push, verify expected branch/head, remote base, and ahead/behind state.
- After an authorized push, verify expected local HEAD equals the authoritative remote and the worktree is clean.

## Escalation

Escalate to Main for invariant changes, boundary crossings, high-severity ambiguity, or two failed repair rounds. Changes to the frozen outcome contract or approved worker allocation require the corresponding user approval before dependent dispatch.