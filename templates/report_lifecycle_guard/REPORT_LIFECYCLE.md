# Report Lifecycle Convention

This document is the **single source** for the report lifecycle convention
used by this optional template. Adopt the convention in a target project
to make agent work auditable and resumable.

This template is independent of the `small` agent rule tree. It can be
copied alongside it, used by itself, or skipped entirely.

## 1. Why a report lifecycle

Agent-driven changes accumulate quickly. Without a convention:

- Reports for finished work clutter the same folder as in-progress notes.
- Naming drift makes it hard to find the most recent decision.
- Reviewers cannot tell which reports describe shipped code vs. proposals.

The convention below fixes those failures with a fixed directory layout,
a fixed file name pattern, and a fixed transition rule between states.

## 2. Directory layout

```
result_reports/
├── active/         # reports describing in-progress or recently shipped work
└── archive/        # reports superseded, rolled back, or older than the active window
```

- `result_reports/active/` is the working folder. Every new report starts
  here. Reviewers and agents read it first.
- `result_reports/archive/` is the historical record. Files are moved
  here, not edited. The Git history retains the move.

Both folders may be empty when a project first adopts the template.

## 3. File name pattern

```
NNN_<kebab-case-slug>.md
```

- `NNN`: a zero-padded three-digit ordinal that increases monotonically
  across all reports (active + archive combined). The next report uses
  `max(existing) + 1`.
- `<kebab-case-slug>`: short, lowercase, hyphen-separated description of
  the work. No spaces, no underscores, no uppercase.
- Extension: `.md`.

Examples:

- `001_initial-template-adoption.md`
- `042_login-flow-rate-limit.md`
- `103_drop-deprecated-config-key.md`

The ordinal is shared between `active/` and `archive/` so a file keeps
its name when it is moved.

## 4. State transitions

A report has exactly one state at a time:

- **active**: lives in `result_reports/active/`.
- **archived**: lives in `result_reports/archive/`.

Transitions:

- **create**: a new file is added to `active/`. The ordinal is one
  greater than the largest ordinal in either folder.
- **archive**: an existing file is moved from `active/` to `archive/`
  using a single `git mv`. The content may be edited in the same commit
  only to add an "Archived: <reason>" note.
- **resurrect** (rare): a file may be moved back from `archive/` to
  `active/` only with explicit user approval.

Files are **not** deleted. Even outdated reports stay in `archive/` so
the history is preserved.

## 5. Minimum content

Every report should contain at least:

- Goal
- Scope (files / areas touched)
- Non-goals
- Verification (commands run and their outcome)
- Result summary

Additional sections are allowed but optional. Project-specific report
shape lives in the target project's `PROJECT_RULES.md`, not here.

## 6. What this convention does **not** cover

- How long a report stays active. That is a project decision.
- Which branches / commits the report attaches to. That is a project
  decision.
- Format of internal sections beyond §5. That is a project decision.

Each enforcement layer (pytest / git hook / devcontainer) checks a
subset of the rules above. See `README.md` of this template for the
role separation.
