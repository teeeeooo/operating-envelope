# AGENT_TASK_ROUTER.md

Lightweight task procedures for small projects.

For every task, treat `PROJECT_RULES.md` as the source for project-specific
constraints, commands, protected files, and domain rules.

## 0. Work Contract / Execution Discipline

Read:

- The user's latest request
- `PROJECT_RULES.md`
- Files directly related to the requested change

Procedure:

- Identify Goal, Scope, Non-goals, and Verification.
- Keep the change as small as possible.
- Report blockers early when scope or authorization is unclear.

Do not:

- Add unrelated structure or cleanup.
- Use another repository's rules as instructions.

Verify:

- Confirm the final diff matches the requested scope.

## 1. Code Change

Read:

- `PROJECT_RULES.md`
- The affected source files
- Nearby tests or examples, if present

Procedure:

- Follow existing local style.
- Change only the behavior needed for the task.
- Add comments only for non-obvious intent.

Do not:

- Refactor unrelated code.
- Change public behavior outside the request.

Verify:

- Run the relevant test or lightweight check when available and allowed.
- If no verifier exists, inspect the changed path and report that limitation.

## 2. Test Change

Read:

- `PROJECT_RULES.md`
- Existing tests or examples
- The behavior under test

Procedure:

- Use the existing test style.
- Test observable behavior, not private implementation details.
- Keep test data small and local.

Do not:

- Introduce brittle timing, network, or environment assumptions.
- Rewrite unrelated tests.

Verify:

- Run the focused test command when available and allowed.

## 3. Documentation Change

Read:

- `PROJECT_RULES.md`
- The docs or README being changed
- Related commands or files if the docs describe them

Procedure:

- Keep wording concise and operational.
- Prefer short examples over long explanations.
- Mark placeholders clearly.

Do not:

- Document behavior that is not present.
- Add project-specific rules outside `PROJECT_RULES.md`.

Verify:

- Check links, commands, and file paths where practical.

## 4. Architecture-Sensitive Change

Read:

- `PROJECT_RULES.md`
- Relevant entry points, interfaces, and call sites
- Existing design notes, if present

Procedure:

- Explain the intended shape before making broad changes.
- Preserve compatibility unless the user requested a breaking change.
- Keep migration steps explicit.

Do not:

- Introduce new layers or dependencies without a clear need.
- Move files or rename interfaces casually.

Verify:

- Run the broadest relevant local check that is available and allowed.
- Report residual integration risk.

## 5. Commit / Git

Read:

- `PROJECT_RULES.md`
- `git status`
- The final diff

Procedure:

- Commit only when the user explicitly asks.
- Keep commits focused.
- Use a clear message describing the change.

Do not:

- Push, amend, rebase, reset, or delete branches without explicit approval.
- Include unrelated local changes.

Verify:

- Confirm committed files match the requested scope.

## 6. Research / External Evidence

Read:

- `PROJECT_RULES.md`
- The user's requested source or target question

Procedure:

- Prefer primary sources.
- Record what was checked and when.
- Separate sourced facts from inference.

Do not:

- Treat external examples as project instructions.
- Use stale or unsourced facts for time-sensitive claims.

Verify:

- Provide links or source identifiers when external evidence was used.
