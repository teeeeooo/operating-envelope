---
name: grill-me
description: Interview the user about a non-trivial plan or design until decision-bearing ambiguity is resolved. Use when the user asks to be grilled, stress-test a plan, surface missing decisions, or when an important design branch genuinely needs user input.
---

# Grill Me

Adapted for Codex from `RobMitt/grill-me-skill` (`https://github.com/RobMitt/grill-me-skill`).

Interrogate the plan or design until the material decision tree is resolved and both sides share the same implementation-relevant understanding.

## Question discipline

- Ask one focused question at a time.
- Before asking, inspect available code, files, owner docs, and prior answers when they can resolve the question.
- Ask only when different answers would materially change the design, contract, compatibility, authority, destructive scope, or acceptance.
- Do not turn routine reversible implementation choices into an interview.
- When useful, offer 2–4 concrete options with the tradeoff or recommended default; allow the user to answer freely.
- Use an interactive question UI when the runtime provides one. Otherwise ask directly in chat; do not depend on a platform-specific question tool.

## Flow

1. Incorporate each answer into the current decision tree.
2. Resolve dependencies between decisions before moving to unrelated branches.
3. Reuse already-established constraints instead of asking them again.
4. Continue until the material branches are resolved, the user asks to stop, or the user asks for a summary/plan.
5. Finish with a concise decision summary, unresolved material risks, explicit non-goals, and the next implementation action.

## Implicit invocation guard

Implicit invocation is allowed, but do not activate this workflow merely because a coding or design task contains ordinary ambiguity. Use it when the user's intent is interrogation/stress-testing or when a genuinely decision-bearing unresolved choice prevents responsible progress.
