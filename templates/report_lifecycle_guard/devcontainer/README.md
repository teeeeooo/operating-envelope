# Devcontainer Integration

This folder documents how to wire the report lifecycle guard into a
devcontainer or any equivalent reproducible environment (Codespaces,
Dev Containers, Nix shell, asdf, plain Makefile). It contains **no
runtime code** — only the integration recipe.

## Role of this layer

The pytest guard and the git hook each catch issues at a different
moment. The devcontainer layer is the one-time bootstrap that makes
those two layers available without each contributor (or each agent)
re-discovering the install steps.

| Layer | When it runs | What it catches |
| --- | --- | --- |
| Devcontainer setup | Environment build / first open | Missing tools, hook not installed |
| Git pre-commit hook | `git commit` (local) | Bad report file names, ordinal collisions |
| Pytest guard | Test run (CI or local) | Bad names across the whole repo, orphan files |

The three layers are independent. A project can adopt any subset.

## Minimal devcontainer recipe

Below is a tool-agnostic checklist. Concrete files (Dockerfile,
`devcontainer.json`, `post-create.sh`) are project-specific and stay in
the target project, not in this template.

1. **Install the python toolchain** required by the pytest guard
   (Python 3.10+ and `pytest`).
2. **Copy the pre-commit hook** into `.git/hooks/pre-commit` and mark
   it executable. Example one-liner in a post-create script:

   ```bash
   install -m 0755 \
       templates/report_lifecycle_guard/hooks/pre-commit-report-guard.sh \
       .git/hooks/pre-commit
   ```

3. **Expose an environment variable** `REPORT_LIFECYCLE_ROOT` if the
   project does not use the default `result_reports/` path.
4. **Document the bypass**: tell contributors how to run
   `git commit --no-verify` and when it is appropriate (rarely).
5. **Wire the pytest guard into CI** so that the same checks run again
   without trusting the local hook.

## Non-goals for this layer

- Auto-archiving stale reports. The archive step is intentionally a
  human decision.
- Generating reports. Reports are written by the agent or by humans.
- Editing or reformatting report contents.

## Failure modes the devcontainer cannot fix

The bootstrap layer does not catch:

- A contributor disabling hooks via `core.hooksPath`.
- A CI pipeline that skips the pytest guard.
- Reports written outside the configured root.

Those failures are detected only when the other two layers run, which
is why the layers stay independent.
