# Host deployment and verification

`global/AGENTS.md` and `skills/` in this repository are canonical. Edit them first. Deploy only the changed managed files after validation; preserve unrelated installed Skills and host configuration.

## Choose the host paths

This desktop retains the previously selected deployment at `~/.codex/skills/` and global guidance at `~/.codex/AGENTS.md`. File equality can be verified independently; do not describe a retained path as a fresh host-discovery result.

The [official Skills documentation](https://developers.openai.com/codex/skills), checked 2026-09-22, documents `~/.agents/skills/` as a USER discovery location. Do not classify that path as universally retired. Inspect actual host discovery before choosing or migrating a deployment root; do not copy the same managed Skills into multiple discovered roots. Same-name Skills are not merged. The 2026-09-22 Codv probe was command-blocked. A fresh CLI app-server probe on 2026-09-25 succeeded as described below; it does not establish desktop-app parity or model behavior.

`deployment/desktop.json` classifies every canonical Skill as selected or intentionally absent. It is a repository-owned validation manifest, not native Codex configuration. Soluna remains canonical and explicit-only, but is intentionally absent from this desktop. Catalog membership must not reinstall it. Another host can supply `--deployment-manifest /absolute/path/host.json`.

Check for a nonempty global `AGENTS.override.md` and duplicate managed Skill names across the host's discovered roots. A successful byte comparison alone does not prove that the host loaded those files.

## Observed CLI discovery (2026-09-25)

Codex CLI `0.153.4`, with shell `CODEX_HOME` unset, successfully queried the
[official app-server discovery API](https://learn.chatgpt.com/docs/app-server)
using `skills/list` with `forceReload: true`. No extra roots, config overrides,
model turns, or user-session restarts were used. The five selected managed Skills
were enabled at `~/.codex/skills/`; Soluna was absent. This supports retaining
that root. Raw inventories and instruction-path checks remain in the separate
2026-09-22 audit folder's `evidence/2026-09-25-discovery.json` and
`evidence/2026-09-25-instruction-chain.json`.

Six independent read-only CLI probes on the same date observed the intended
Skill selection/non-selection and required May Web reference reads. The current
configured model was `gpt-6-astra` with medium reasoning. Prompts, traces, findings,
and limits remain in the separate audit's
`evidence/2026-09-25-behavior/REPORT.md`. These single-run planning/review probes
do not establish desktop-app parity, statistical activation reliability, or
reference timing and product outcomes during real implementation.

## Checks

Canonical CI check, with no dependency on a user's installed files:

```sh
python3 scripts/validate_harness.py
```

Current desktop deployment check (read-only):

```sh
python3 scripts/validate_harness.py --runtime-home ~/.codex
```

Explicit Skill root for another verified host:

```sh
python3 scripts/validate_harness.py --runtime-home ~/.codex --runtime-skills ~/.agents/skills
```

The optional runtime check compares global guidance and every selected Skill source file, including missing/extra files within each selected Skill; Python bytecode caches are ignored. It also rejects intentionally absent Skills, a nonempty global override, and retired `design-interview` in the selected root. Canonical validation still covers the entire catalog, including Skills intentionally not installed. It does not scan other roots, install files, change permissions, or prove behavioral discovery.

Reconcile intentional runtime refinements into canonical source before copying; do not overwrite them with stale source. Install only changed files selected by the manifest, not the full catalog. Preserve `.system`, unrelated installed Skills, `config.toml`, and execution rules. Check validator changes with `python3 -B -m unittest discover -s scripts -p 'test_validate_harness.py'`.

After a meaningful trigger change or host migration, use a small representative task in an isolated workspace and inspect which Skill was actually read. Keep model, host, prompt, outcome, and any unverified behavior with the change evidence. Reuse existing passing cases unless the change invalidates them; this is not a new per-task approval or full-suite gate.

## New projects

Start with repository-specific invariants and necessary owner pointers in a small `AGENTS.md`. Select existing global Skills by task. Add local Skills, recall indexes, or decision/failure records only when a concrete repeated workflow or expensive lesson warrants them; the architecture's six logical layers do not require six initial sets of files.
