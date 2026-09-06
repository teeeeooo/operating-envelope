# Astra Agent Harness V2

Status: Governing migration baseline  
Date: 2026-09-06  
Owner: `operating-envelope`  
Scope: user-level agent harness, `predictor_v3`, and `oil_level_tracker`

## 1. Purpose

This document is the canonical design baseline for restructuring the user's agent environment around GPT-6 Astra. It governs the shared architecture and migration sequence; repository-local documents own only the project-specific application of this design.

The redesign is not a request to maximize policy or documentation. Its goal is to minimize instruction surface while preserving high-value engineering memory, domain truth, and project-specific safeguards.

Authoritative OpenAI guidance used by this design:

- GPT-6 Astra model guidance: <https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra>
- Codex `AGENTS.md` guidance: <https://developers.openai.com/codex/guides/agents-md>
- Codex Skills guidance: <https://developers.openai.com/codex/skills>
- Codex memory guidance: <https://learn.chatgpt.com/docs/customization/memories>

OpenAI guidance is external product guidance, not repository instruction. If it changes, re-audit this design before changing active policy.

## 2. Design Drivers
GPT-6 Astra is more instruction-sensitive than prior models. The harness therefore must avoid duplicated, stale, conflicting, or historical instructions on the active path.

The design adopts four model-specific operating assumptions from OpenAI guidance:

- bias toward action and complete authorized work instead of stopping at plans;
- make user instructions explicitly higher priority than Skill guidance;
- specify delegation behavior when a multi-agent workflow depends on it;
- calibrate verification to the actual change and avoid unjustified repeated broad testing.

The design also treats memory as auxiliary retrieval. Durable team/project truth belongs in version-controlled owners; memory exists to find that truth quickly, not to replace it.

## 3. Layer Model

The target architecture has six logical layers:

```text
L0  Global AGENTS        always-on shared execution posture
L1  Global Skills        reusable conditional workflows
L2  Repository AGENTS    repo invariants and routing only
L3  Repository Skills    repo-specific conditional workflows
L4  Project Knowledge    current state, architecture, validation, decisions, recall
L5  Historical Evidence  logs, retired designs, result records, diagnostics
```

A rule should live at the lowest layer that still covers every place where it is valid. Do not copy a global rule into repository policy merely for visibility.
## 4. Global `AGENTS.md`

Canonical source: [`global/AGENTS.md`](../global/AGENTS.md). Design contract: [`docs/GLOBAL_AGENTS_DESIGN.md`](GLOBAL_AGENTS_DESIGN.md). The deployed user copy will live at `~/.codex/AGENTS.md`.

The global file should remain small. It owns only behavior that is valid across repositories, including:

- act on clear requests rather than returning only a plan;
- infer routine, reversible details from available context and repository evidence;
- ask only when ambiguity can materially change the outcome, authority, or irreversible effect;
- do not request approval again when the user already granted it for the current scope;
- preserve unrelated user changes and avoid unsolicited scope expansion;
- treat user instructions as higher priority than reusable Skill guidance;
- use proportional verification and do not repeat already-sufficient checks without an invalidating reason;
- perform bounded recall before broad rediscovery when prior decisions, failures, paused work, or intentional existing mechanisms are materially relevant.

It must not contain product-domain rules, project-specific protected paths, milestone state, or detailed task procedures.

## 5. Global Skills

Global Skills own reusable workflows that should be loaded only for relevant tasks. Initial target set:

- `soluna`: explicit-only multi-agent allocation/orchestration workflow;
- `grill-me`: upstream-derived structured design interrogation with Codex-compatible questioning and guarded implicit invocation;
- `desktop-table-ui`: reusable desktop table interaction contract;
- `desktop-window-lifecycle`: reusable window/dialog/viewport/page lifecycle contract;
- `python-test-portability`: reusable Python test portability across OS/cwd/text/subprocess/logical-artifact boundaries.
`soluna` remains user-selected rather than implicitly triggered because it imposes a deliberate worker-allocation approval workflow. Its canonical source should move from legacy user Skill storage into this repository, then deploy to the current Codex user Skill location.

`desktop-table-ui` should own behavior such as selection, keyboard navigation, copy/paste, rectangular paste, clipboard representation, read-only/edit semantics, scrolling, batch editing, and selection preservation. It should be framework-neutral first; Qt/Tkinter details belong in optional references only when repeated need justifies them.

`desktop-window-lifecycle` should own window/dialog/viewport and dynamic page lifecycle behavior: modal/modeless commit semantics, open/close, geometry, resize, focus, dirty state, page activation/deactivation/disposal, and layout ownership.

Visual design systems, business validation, domain schemas, and product-specific toolkit policies remain repository-local.

`python-test-portability` is now a global implicit Skill after predictor repo-root/cwd regressions and Oil portability rules established real cross-repository reuse. It owns only filesystem/path identity, UTF-8 text I/O, non-interactive subprocess behavior, cwd/repo-root independence, logical-artifact identity, and semantic assertion guidance; Qt/testkit-specific lifecycle rules remain repository-local.

## 6. Repository `AGENTS.md`

Repository `AGENTS.md` files become compact always-on overlays. They should contain only:

- repository-wide invariants that truly apply to most work;
- canonical-owner routing when the correct owner cannot be inferred from the task;
- repository-specific public or architectural boundaries that must always be visible;
- pointers to repository Skills for conditional procedures.

Generic autonomy, approval, editing discipline, and test-calibration prose should be removed after the global `AGENTS.md` is deployed and verified.

Historical procedures must not remain in an active `AGENTS.md` merely because they were once important.
## 7. Memory and Recall Architecture

The previous conclusion to retire project memory was incorrect for the user's actual goal. The compact memory layer is retained and redesigned.

The purpose is to reduce three recurring costs:

- repeating work or failed approaches that were already explored;
- reconstructing why a prior decision was made;
- broadly searching for an implementation or owner that was previously located.

Use three memory temperatures:

```text
Hot   compact project memory seed / summary
Warm  decision records and failure lessons
Cold  project log, Git history, result records, evidence, diagnostics
```

The hot layer is a routing index, not a second handbook or a duplicate current-state document. A useful entry contains only enough information to change future retrieval behavior: topic/keywords, one or two durable reminders, current owner, and a pointer to deeper detail.

Drift-prone facts such as current branch, current milestone status, or active runtime values remain owned by current-state documents/source and should not be copied into the seed except as a routing clue.

Codex-generated/local memory is auxiliary. Version-controlled project decisions and failure lessons remain authoritative for team/project engineering history.
## 8. Recall Gate and Memory Write Policy

The old memory workflow mixed reading and writing. V2 separates them.

### Recall Gate — read side

Perform a bounded recall pass before broad exploration when the task materially depends on prior decisions, previous failures, resumed work, unclear existing ownership, or an existing mechanism that appears intentionally non-obvious.

Expected path:

```text
compact memory seed
→ relevant decision/failure entry only
→ current canonical owner/source
→ stop recall and continue work
```

Recall should be search-driven and bounded rather than reading the full project log. The target is a small number of retrieval steps, not exhaustive historical review.

### Memory Write Review — write side

Do not require a memory update for every completed change. Write only when a new fact is likely to prevent meaningful future re-investigation or repeated failure, materially changes an architectural decision, records a counterintuitive constraint, or preserves a difficult-to-discover ownership relationship.

No high-leverage reusable learning means no memory update.

The old mandatory `Result Record → memory_review → seed update` chain is therefore not part of V2.
## 9. Decision, Failure, and Code-Topology Retrieval

Decision memory and code topology solve different problems and must not be conflated.

Decision/failure records answer `why`, `why not`, and `what should not be repeated`. They should capture the durable decision, rationale, rejected or failed alternative when relevant, current owner, supersession status, and the trigger for reconsideration.

Code search or a derived code graph answers `where`, `what calls this`, and `what is connected`. `ACTIVE_DOCUMENTS`, source search, symbol search, and the bounded Oil S11 Graphify pilot may serve this layer.

A generated wiki or code graph must remain a disposable projection unless separately promoted through evidence. It does not replace source, architecture owners, decision records, or validation contracts.

Recommended retrieval routing:

| Question | First owner |
| --- | --- |
| Why was this chosen? | memory seed → decision record |
| Did this fail before? | memory seed → failure lesson |
| Where is this implemented? | owner map → source/code topology |
| What may this change affect? | source/code topology + tests |
| What exactly happened last time? | cold evidence / Git / project log |
| What is current now? | work plan/current owner/source |

## 10. `predictor_v3` Migration
The predictor migration is performed only after the global layer is deployed and verified.

Target changes:

- shrink root `AGENTS.md` to predictor-wide invariants and owner/Skill routing;
- keep `calculator`, `ml-predictor`, and `packaging` repository Skills, removing duplicated global behavior;
- retire the repo-local `grill-me` and use the upstream-derived global `grill-me` with a minimal Codex compatibility adaptation;
- retire repo-local `ui-surface`; reusable table/window behavior is global while predictor-specific UI ownership remains under `docs/ui_ux/`;
- retain `ACTIVE_DOCUMENTS.md` as the compact current-owner router and repair stale/malformed routes;
- retain product/architecture truth in `PROJECT_CHARTER`, `project_brief`, `WORK_PLAN`, architecture docs, and source while removing duplicated harness prose;
- retain `project_log` as durable chronology, not as an always-read instruction source;
- redesign the project memory seed as the hot recall index;
- introduce small decision/failure memory only where it reduces future rediscovery.

The mandatory Result Record lifecycle is retired for new work. Existing records remain historical evidence.

The existing agent change checker must be decoupled from mandatory `memory_review`, `memory_reason`, report-index updates, and seed updates. Mechanical engineering safeguards should remain only where they protect a real repository contract.

The predictor migration resolves the 350-LOC hard gate as a warning/review signal rather than a failure threshold, avoiding artificial code splits.

Repository-specific migration record target:

`predictor_v3/docs/designs/2026-09-07-astra-agent-harness-v2-migration.md`
## 11. `oil_level_tracker` Migration

Oil migration should occur on a dedicated harness/policy branch rather than being mixed into the current R21 feature branch unless repository state makes a separate branch impossible.

Target changes:

- shrink root `AGENTS.md` after global policy is available;
- simplify `execution-policy.md` by removing ordinary DISCOVER/EXECUTE/VERIFY/CLOSE ceremony and V0-V5 taxonomy;
- retain exact-head review freeze and publication boundaries where they express real repository state transitions;
- distinguish Task COMPLETE from Milestone DONE;
- keep `work-plan`, `roadmap`, retained commitments, architecture, logic map, validation, and evidence as engineering truth;
- move the workflow half of S11 detector governance into a repo-local `s11-detector-change` Skill while retaining schema/checker rules in durable docs/code;
- keep the detector logic map and causal failure registry as project knowledge, not Skills;
- add a repo-local `windows-qualification` Skill;
- split the current Windows operations surface so R7-R12 procedures cannot masquerade as the current-candidate qualification procedure;
- add a revision-neutral current-candidate Windows qualification owner that resolves identity from the Work Plan, allowing a later R21 merge without pre-promoting unmerged feature-branch truth;
- relax `docs/README.md` mandatory-read behavior to document creation, move/rename/archive, owner changes, or unclear ownership.

Oil now uses a compact `docs/00-project/recall-index.md` only as a routing layer over the existing work-plan, logic map, failure registry, reviewed truth, and retained commitments; it is not a second memory SSOT.

Repository-specific migration record target:

`oil_level_tracker/docs/20-architecture/s11-agent-harness-v2-routing-design.md`

## 12. `operating-envelope` Target Structure
The repository becomes the canonical source for the user-level harness rather than a template-only project.

```text
operating-envelope/
├── README.md
├── AGENTS.md                    # repo-local rules for editing this repo
├── docs/
│   └── ASTRA_AGENT_HARNESS_V2.md
├── global/
│   └── AGENTS.md                # canonical deployed global policy
└── skills/
    ├── soluna/
    ├── grill-me/
    ├── desktop-table-ui/
    └── desktop-window-lifecycle/
```

Runtime locations such as `~/.codex/AGENTS.md` and `~/.codex/skills/*` are deployment surfaces. This repository owns their canonical source and migration history.

Do not introduce an independent authoritative wiki for this harness. If a generated wiki is later useful, it must be reproducible from canonical source and clearly marked as a projection.

## 13. Migration Sequence

Migration is deliberately staged so behavioral changes can be attributed to a specific layer.
### Phase A — Bootstrap and global foundation

1. Establish `operating-envelope` identity and governing design baseline.
2. Create canonical global `AGENTS.md` and a minimal repo-local `AGENTS.md` for this repository.
3. Migrate `soluna` canonical source and make invocation explicitly user-selected.
4. Canonicalize upstream-derived `grill-me`, plus `desktop-table-ui` and `desktop-window-lifecycle`.
5. Deploy global policy/Skills to the Codex runtime locations and verify discovery/trigger behavior.

### Phase B — predictor migration

1. Create the predictor-specific migration record.
2. Slim root policy and repository Skills against the verified global layer.
3. Retire mandatory Result Record and memory-write ceremony while preserving historical evidence.
4. Redesign bounded recall and decouple mechanical checkers.
5. Synchronize active owner maps and archive superseded harness designs.

### Phase C — Oil migration

1. Create the Oil-specific migration record on an isolated policy branch.
2. Slim root/execution policy.
3. Introduce S11 detector-change and Windows-qualification Skills.
4. Split current Windows procedure from historical revision procedures.
5. Verify current-candidate qualification routing and existing governance checkers.

### Phase D — optional retrieval improvements
After the core migration is stable:

- maintain the global `python-test-portability` Skill from genuinely shared rules only;
- pilot Graphify first in `oil_level_tracker` on the bounded S11 detector/application/publication topology; keep generated graph state local/disposable and use source/current owners as authority;
- evaluate generated/disposable project wiki views only if they reduce retrieval cost;
- consider moving Soluna role/model definitions into native Codex custom-agent configuration while keeping orchestration semantics in the Skill.

## 14. Validation Contract

The migration is not complete merely because files were moved. Validate actual model-facing behavior.

Global checks:

- Codex reports/uses the intended global `AGENTS.md` source;
- global Skills are discoverable from their deployed location;
- explicit-only workflows do not trigger implicitly;
- an ordinary clear bug-fix request proceeds without redundant approval questions;
- a small reversible change does not cause unjustified broad/repeated tests;
- explicit user instructions override a reusable Skill when they conflict.

Recall checks:

- a prior-decision query routes through the compact memory index rather than reading the full project log;
- retrieved historical guidance is checked against current owners/source when drift is possible;
- a task with no relevant prior decision does not pay unnecessary recall cost.

Repository checks follow in the next section.
Predictor checks:

- table work selects the global table Skill plus only the necessary predictor owner context;
- a calculator-only change does not load UI workflow unnecessarily;
- mandatory Result Record/memory-review coupling no longer blocks ordinary changes;
- relevant historical decisions are still quickly recallable;
- active owner documents contain no routes to retired workflow policy.

Oil checks:

- an S11 detector task loads only relevant logic-map/failure/validation owners;
- current-candidate Windows qualification cannot select R7-R12 historical procedure as current guidance;
- already-accepted local candidate evidence is reused unless an explicit invalidation condition is present;
- governance checkers continue protecting the durable detector contract after workflow prose moves to a Skill.

General repository checks:

- no stale links or duplicate active policy owners;
- no same-name duplicate global/local Skill exposure unless intentionally scoped;
- `git diff --check` passes;
- changed policy surfaces are reviewed for hidden approval pauses, stale authority, and over-testing triggers.

Hook/CI checks:

- `operating-envelope` runs a lightweight canonical harness/Skill CI on `main` and pull requests;
- predictor checkouts install `core.hooksPath=.githooks` via a repository script, while the generic repository-policy CI is separated from AHRI/Calculator validation;
- Oil keeps its existing `.githooks/pre-push` detector-governance check paired with the same CI checker;
- derived Graphify freshness never becomes a blocking correctness hook during the bounded pilot.

## 15. Post-Migration Decisions And Remaining Pilots

Post-migration evidence resolved the initial open questions:

- predictor repo-local `ui-surface` is retired; global table/window Skills plus `docs/ui_ux/` cover the remaining ownership cleanly;
- predictor's new-source 350-LOC rule is warning-first, not a hard failure gate;
- Oil uses a compact recall index rather than a second project-memory SSOT;
- Graphify is an active bounded pilot in `oil_level_tracker` S11. The pilot host uses local `graphifyy` tooling, but the repository does not require Graphify as a correctness dependency. Exact symbol/literal lookup remains source-search-first; Graphify is reserved for relational topology, affected callers/tests, and blast radius. Its graph is derived/disposable and never overrides source, logic-map, architecture, failure, or current-state owners;
- `python-test-portability` is implemented as an implicit global Skill for genuinely shared Python portability rules. Oil-specific Qt lifecycle/QPA rules stay local.

The Oil Graphify smoke/benchmark found useful transitive caller/test relationships but also showed that bounded scope can hide a real caller until the scope is corrected; five exact-symbol comparisons also showed literal `rg` is materially faster. Keep task-start incremental refresh and optional agent-managed watch, leave Graphify Git hooks uninstalled during the pilot, and decide long-term adoption only after repeated real S11 work. `python-test-portability` was promoted only after concrete predictor/Oil reuse evidence appeared.

## 16. Governance of This Design

This file owns the shared V2 architecture until superseded by a later design in `operating-envelope`. Runtime copies and repository-local migration records must not silently redefine global architecture.

When an implementation reveals that this design is wrong, update the design decision explicitly rather than accumulating a contradictory local exception. Historical versions remain available through Git.
