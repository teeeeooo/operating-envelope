# Host deployment and verification

`global/AGENTS.md` and `skills/` in this repository are canonical. Edit them first. Deploy only the changed managed files after validation; preserve unrelated installed Skills and host configuration.

## Choose the host paths

This desktop retains the previously selected deployment at `~/.codex/skills/` and global guidance at `~/.codex/AGENTS.md`. File equality can be verified independently; do not describe a retained path as a fresh host-discovery result.

The [official Skills documentation](https://developers.openai.com/codex/skills), checked 2026-09-22, documents `~/.agents/skills/` as a USER discovery location. Do not classify that path as universally retired. Inspect actual host discovery before choosing or migrating a deployment root; do not copy the same managed Skills into multiple discovered roots. Same-name Skills are not merged. The 2026-09-22 Codv app-server discovery probe was command-blocked, so fresh host discovery remains unverified.

`deployment/desktop.json` classifies every canonical Skill as selected or intentionally absent. It is a repository-owned validation manifest, not native Codex configuration. Soluna remains canonical and explicit-only, but is intentionally absent from this desktop. Catalog membership must not reinstall it. Another host can supply `--deployment-manifest /absolute/path/host.json`.

Check for a nonempty global `AGENTS.override.md` and duplicate managed Skill names across the host's discovered roots. A successful byte comparison alone does not prove that the host loaded those files.

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
