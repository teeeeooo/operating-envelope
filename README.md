# agent-rule-tree

Reusable generic agent rule tree templates.

This repository stores portable agent rule trees that can be copied into small
projects, scripts, experiments, and lightweight tools.

The initial `small` template is intentionally minimal. It provides shared agent
operating rules while keeping project-specific constraints in one overlay file:
`PROJECT_RULES.md`.

## Small Template

`templates/small/` contains:

- `AGENTS.md`: common operating rules for agents
- `AGENT_TASK_ROUTER.md`: lightweight procedures by task type
- `PROJECT_RULES.md`: project-specific overlay to edit in the target project

Project-specific rules should live in `PROJECT_RULES.md`, not in the common
agent rules. Keep `AGENTS.md` generic so it can be reused across projects.

## Usage

1. Copy the files from `templates/small/` into the target project root.
2. Edit `PROJECT_RULES.md` for the target project.
3. Keep `AGENTS.md` as the common operating rules.
4. Adjust only the task types in `AGENT_TASK_ROUTER.md` when needed.

Avoid expanding the template with assumptions from any one project. Add narrow
local rules in the target project's `PROJECT_RULES.md` instead.

## Optional Templates

Optional templates live next to `small/` and can be adopted independently.
They are **not part of the small rule tree**; each is opt-in and can be
copied alone.

- `templates/report_lifecycle_guard/`: convention for managing agent work
  reports (`result_reports/active/` and `result_reports/archive/`) plus
  three independent enforcement layers — a pytest guard, a git pre-commit
  hook, and a devcontainer integration recipe. See the template's own
  `README.md` for the role separation between the three layers and for a
  project-specific adoption procedure (including a worked example for
  `predictor_v3`).

### When to reach for an optional template

- The convention solves a problem your project already feels (orphaned
  reports, name drift, ad-hoc archiving).
- You can pick a subset of enforcement layers. Adopt only what you will
  actually maintain.
- The convention should not duplicate or contradict anything in the
  target project's `PROJECT_RULES.md`. If there is overlap, link the
  template's doc from `PROJECT_RULES.md` instead of copying the rules in
  twice.

Optional templates follow the same "no project-specific assumptions"
rule as `small/`. Project-specific tuning belongs in `PROJECT_RULES.md`
in the target project, not in the template.
