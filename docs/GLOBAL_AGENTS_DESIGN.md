# Global AGENTS Design

## Purpose

This document defines the design contract for the user-level global `AGENTS.md` used by Codex. The canonical runtime content is `global/AGENTS.md`; the deployed copy will live at `~/.codex/AGENTS.md`.

The global file is an always-on behavioral layer. It should contain only stable rules that are useful across repositories and across most non-trivial work.

## External basis

The design is aligned with current OpenAI guidance for GPT-6 Astra and Codex instruction discovery:

- Astra is more sensitive to instructions in Skills and `AGENTS.md`, so instruction surfaces should be audited for conflicts and unnecessary pauses.
- User instructions should take precedence over reusable Skill guidance when they conflict.
- Astra benefits from explicit initiative and follow-through guidance so routine ambiguity does not stop authorized work.
- Verification should be proportional; already-sufficient passing checks should not be repeated without an invalidating reason.
- Codex loads global guidance before repository-local guidance and has a finite combined project-instruction budget.

External documentation informs this design but is not itself an executable repository instruction surface.

References checked 2026-09-06:

- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra
- https://developers.openai.com/codex/guides/agents-md

## Admission rule

A rule belongs in global `AGENTS.md` only when all of the following are true:

1. it is valid across repositories;
2. it is useful for a broad class of tasks;
3. it is stable enough to justify always-on context;
4. it governs agent behavior rather than product/domain truth;
5. it cannot be better expressed as a conditional Skill.

## Owned behavior

The global contract owns five narrow concerns.

### 1. Initiative and completion

For clear action requests, proceed through the requested work and appropriate verification rather than stopping after planning. Resolve routine and reversible details from context, tools, and repository evidence. Ask only when missing information can materially change the outcome, authority, or an irreversible/external effect.

Do not request the same approval twice within an unchanged scope. Incorporate mid-task steering and continue from completed work where possible.

### 2. Scope discipline

Preserve unrelated user changes. Do not add cleanup, refactors, features, or policy changes outside the requested scope merely because they appear useful. Prefer the smallest sufficient change consistent with the repository's architecture and explicit user intent.

### 3. Instruction and Skill discipline

The user's explicit task intent takes precedence over reusable Skill guidance. Repository-local instructions may specialize the global defaults for their scope.

If a Skill is the reason work would pause, request extra approval, remain unfinished, or diverge from the user's intent, surface the exact Skill rule that caused the conflict instead of silently treating it as higher authority.

### 4. Bounded recall and evidence

When a task materially depends on a prior decision, known failure, paused effort, or an apparently intentional existing mechanism, perform a bounded recall pass before broad rediscovery. Use compact memory/index material to route to only the relevant decision, failure, owner, or evidence.

Memory is routing evidence, not automatic authority for drift-prone facts. Verify mutable or current claims against the present source/owner. Do not broadly scan historical logs when targeted recall is sufficient.

### 5. Verification calibration

Match verification depth to the size, risk, and boundary of the change. Prefer focused checks first. Do not repeat already-sufficient passing checks unless a later change, failure, explicit requirement, or unresolved concern invalidates that evidence.

## Side-effect boundary

Do not create commits, push, deploy, publish, delete remote data, or perform comparable external side effects unless the user requested them or the current scope clearly grants that authority. Once authority is granted, do not add a second approval ceremony for the same action.

Destructive or materially irreversible actions require clear authority even when nearby reversible work is authorized.

## Explicit non-owners

The global file must not own:

- project identities, product rules, formulas, schemas, or protected paths;
- repository milestone/current-state information;
- task-specific implementation procedures;
- framework-specific UI techniques;
- test commands tied to one language or repository;
- detailed multi-agent allocation policy;
- long memory indexes, decision records, failure registries, or historical evidence;
- formatting/style preferences that do not materially affect engineering work.

These belong in repository instructions, repository/global Skills, project knowledge, or historical evidence as appropriate.

## Size and wording constraints

Target roughly 25-40 non-blank lines. Prefer direct behavioral rules over rationale. Avoid duplicated examples, nested procedure trees, role taxonomies, and phrases that accidentally turn routine work into an approval gate.

Do not encode a generic requirement to "plan first", "ask when unsure", "run the full test suite", or "wait for approval before editing". Those patterns are too broad and conflict with the Astra initiative and proportional-verification goals.

## Canonical and deployment model

`global/AGENTS.md` is the canonical source. `~/.codex/AGENTS.md` is a deployed runtime copy and must not silently diverge from the canonical file.

Repository-local `AGENTS.md` files may add or specialize repository rules, but shared behavior should not be duplicated there merely for visibility.

## Validation

Before deployment, verify:

- no project-specific names or paths appear in the global file;
- no generic mandatory approval, planning, or full-suite test ceremony is introduced;
- bounded recall is routing-oriented and does not force broad history reads;
- side-effect authority distinguishes requested actions from unsolicited ones;
- the file is concise enough to remain cheap as always-on context;
- `git diff --check` passes.

After deployment, validate from at least one repository that Codex reports the global file before repository-local instructions and that representative action, recall, and verification prompts behave as intended.
