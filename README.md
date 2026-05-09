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
