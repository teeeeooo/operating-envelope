---
name: design-interview
description: Explicit-only design interrogation for resolving decision-bearing uncertainty before implementation. Use only when the user explicitly invokes this skill or directly asks to be questioned through a design decision.
---

# Design Interview

Use only when explicitly invoked. The user's explicit task takes precedence over this skill.

## Purpose

Resolve uncertainty that would materially change architecture, public or persisted contracts, compatibility, externally visible behavior, authority, destructive scope, or acceptance.

Do not turn routine implementation choices into a question loop.

## Before asking

1. Inspect the current owner, source, or documentation when the answer may already exist.
2. Distinguish a real product/design choice from an implementation detail the agent can safely resolve.
3. If different answers would not materially change the outcome, choose a reasonable conservative default and continue.
4. Ask only when the remaining choice is genuinely decision-bearing and cannot be recovered from evidence.
5. Ask one focused question at a time.

Do not ask questions merely to satisfy a process, checklist, or preference survey.
## Interview behavior

- Keep each question narrow enough that the answer changes a concrete design branch.
- Prefer contrasting real alternatives and their tradeoffs over open-ended brainstorming.
- Reuse prior answers; do not ask the user to restate a boundary that is already explicit.
- When repository evidence rules out an option, explain that briefly instead of presenting it as a false choice.
- Incorporate steering immediately and continue from decisions that remain valid.

## Stop rule

Stop when the decision-bearing tree is resolved enough to act, the user asks to stop, or the user asks for a summary or plan.

Do not prolong the interview for low-value polish, speculative edge cases, or choices that can be changed reversibly during implementation.

When stopping, summarize only:

- decisions that materially constrain implementation;
- unresolved material risks or choices;
- owner or contract boundaries;
- required validation or migration implications;
- explicit non-goals; and
- the next implementation action.

Persist a design document only when the user asks for one or the active repository contract requires one.