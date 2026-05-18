# report_lifecycle_guard (optional template)

A portable, **opt-in** convention for managing agent work reports plus
three independent enforcement layers. Adopt any subset.

This template is independent of `templates/small/`. It can sit next to
the small template, replace its report rules in `PROJECT_RULES.md`, or
be used in a project that has no agent rule tree at all.

## Contents

| Path | Purpose |
| --- | --- |
| `REPORT_LIFECYCLE.md` | The convention itself: directory layout, naming, state transitions. Drop into the target project as-is. |
| `pytest/test_report_lifecycle.py` | Optional pytest guard. Verifies naming + ordinal uniqueness across active + archive. Skips when no reports exist. |
| `hooks/pre-commit-report-guard.sh` | Optional git pre-commit hook. Validates staged report names + ordinal collisions before each commit. |
| `devcontainer/README.md` | Integration recipe for devcontainers / reproducible shells. Documents how the three layers compose. |

## Role separation (pytest vs hook vs devcontainer)

The three enforcement layers are deliberately split so each one stays
small and each catches a different failure mode. None of them depend on
the others.

| Layer | When it runs | What it checks | What it does NOT do |
| --- | --- | --- | --- |
| **pytest** (`pytest/test_report_lifecycle.py`) | Test suite (CI or local `pytest`) | Naming pattern, ordinal uniqueness, no stray files, applied across **all** reports in the repo | Does not block commits; does not install itself |
| **git hook** (`hooks/pre-commit-report-guard.sh`) | `git commit` on a developer machine | Same naming + ordinal rules but **only on staged report files** | Does not see un-staged files; can be bypassed with `--no-verify`; not run in CI |
| **devcontainer** (`devcontainer/README.md`) | Environment build / first open | Bootstrap: hook installed, python + pytest available, env vars set | Does not validate report content; does not run continuously |

Pick one if you only want one:

- **CI-first project**: adopt the pytest guard. Skip the hook.
- **Solo / scrappy project**: adopt the hook for fast local feedback.
  Skip the pytest guard.
- **Team project**: adopt all three. The devcontainer wires the hook;
  the hook catches local mistakes; the pytest guard catches what slipped
  past the hook.

A project can also adopt only `REPORT_LIFECYCLE.md` as a convention
document and rely on human review for enforcement. The doc is useful on
its own.

## Generic copy procedure (any project)

1. Decide which layers you want (any subset of pytest / hook /
   devcontainer / docs-only).
2. Copy `REPORT_LIFECYCLE.md` into the target project root or a docs
   folder. Do **not** edit the rules — write project-specific notes in
   your `PROJECT_RULES.md` overlay (or a project-local README) instead.
3. For the pytest layer: copy `pytest/test_report_lifecycle.py` into
   the project's existing test folder. No conftest changes are required.
4. For the hook layer: copy `hooks/pre-commit-report-guard.sh` into
   `.git/hooks/pre-commit` and `chmod +x` it. (Or use your hook
   manager.)
5. For the devcontainer layer: follow `devcontainer/README.md` and add
   a small post-create script in the target project.
6. Create `result_reports/active/` and `result_reports/archive/` even
   if they start empty.

## predictor_v3-specific adoption procedure

`predictor_v3` already has `result_reports/active/` with reports such as
`094_iso16358-table-contract-alignment-audit.md` and a global
`AGENTS.md` / `AGENT_TASK_ROUTER.md`. The copy procedure below assumes
that layout.

1. **Pre-flight check (no edits).**
   - Confirm `result_reports/active/` exists.
   - Confirm naming convention already matches `NNN_<kebab-slug>.md`
     (predictor_v3 currently does).
   - List ordinals: `ls result_reports/active | head` — the next report
     uses `max(existing) + 1`.

2. **Copy the convention doc.**
   ```bash
   mkdir -p docs/agent
   cp <agent-rule-tree>/templates/report_lifecycle_guard/REPORT_LIFECYCLE.md \
      docs/agent/REPORT_LIFECYCLE.md
   ```
   - Do not edit. Predictor-v3-specific report sections (Goal, Scope,
     Non-goals, Verification, task-by-task summary) already exceed the
     §5 minimum.

3. **Wire AGENTS.md / AGENT_TASK_ROUTER.md to the convention.**
   - Add one bullet under "Output" in `AGENTS.md`:
     `report lifecycle 규칙은 docs/agent/REPORT_LIFECYCLE.md를 따른다.`
   - In `AGENT_TASK_ROUTER.md` under "Result Report Workflow", add a
     line that points to the same doc.
   - Do not duplicate the lifecycle rules in either file.

4. **Add the pytest guard.**
   ```bash
   cp <agent-rule-tree>/templates/report_lifecycle_guard/pytest/test_report_lifecycle.py \
      tests/test_report_lifecycle.py
   ```
   - Run `python3 -B -m pytest tests/test_report_lifecycle.py -q`.
     Expected: 3 passed (or 1 skip + 2 passed if `archive/` is empty;
     the active folder is non-empty so the skip path is unlikely).
   - If failures appear, the existing report folder violates the
     convention. Fix names before continuing (do not weaken the test).

5. **Add the git hook (optional, local-only).**
   ```bash
   install -m 0755 \
       <agent-rule-tree>/templates/report_lifecycle_guard/hooks/pre-commit-report-guard.sh \
       .git/hooks/pre-commit
   ```
   - Predictor_v3 does not run hooks in CI; this is a developer
     convenience only.
   - If a project hook already exists, chain them — do not overwrite.

6. **Devcontainer step (skip unless predictor_v3 starts using one).**
   - Predictor_v3 currently runs locally without a devcontainer. Leave
     `devcontainer/README.md` as reference. Revisit if a devcontainer
     or CI image is added.

7. **First commit.**
   - Stage: `docs/agent/REPORT_LIFECYCLE.md`,
     `tests/test_report_lifecycle.py`, and the AGENTS / Router hook
     edits.
   - Commit message suggestion:
     `chore: adopt report_lifecycle_guard template (docs + pytest)`.
   - Do **not** mass-rename existing reports in the same commit. If any
     name fixes are needed, do them in a follow-up commit so the
     adoption diff stays reviewable.

8. **Verification.**
   - `python3 -B -m pytest tests/test_report_lifecycle.py -q` → passes.
   - `python3 -B -m pytest -q` → existing suite still passes
     (predictor_v3 baseline is `464 passed, 34 xfailed`; the new test
     adds 3 passes).
   - `git status` shows only the intended adoption files.

9. **Out of scope for the adoption.**
   - Auto-archiving existing reports. Manual decision per report.
   - Changing the predictor_v3 report content shape (sections beyond
     §5). Already richer than the minimum.
   - Editing `core/`, `ui/`, calculator, or unit adapter code. The
     adoption is docs + test only.

## Non-goals for this template

- Defining what makes a report "good" beyond §5 of the convention doc.
- Auto-generating reports from commit messages or PR bodies.
- Replacing the project's own change-management or PR review.
