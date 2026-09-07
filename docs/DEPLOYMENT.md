# Host deployment and verification

`global/AGENTS.md` and `skills/` in this repository are canonical. Edit them first. Deploy only the changed managed files after validation; preserve unrelated installed Skills and host configuration.

## Choose the host paths

The current desktop host exposes user Skills from `~/.codex/skills/` and global guidance from `~/.codex/AGENTS.md`. This is the verified local deployment choice.

The [official Skills documentation](https://developers.openai.com/codex/skills), checked 2026-09-07, also documents `~/.agents/skills/` as a USER discovery location. Do not classify that path as universally retired. On another host, inspect its available Skill inventory and current discovery documentation before selecting a deployment root. Do not copy the same managed Skills into multiple discovered roots; same-name Skills are not merged.

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

The optional runtime check compares global guidance and all managed Skill source files, including missing/extra files within each managed Skill; Python bytecode caches are ignored. It rejects a nonempty global override and the retired `design-interview` in the selected root. It does not scan other roots, install files, or prove behavioral discovery.

After a meaningful trigger change or host migration, use a small representative task in an isolated workspace and inspect which Skill was actually read. Keep model, host, prompt, outcome, and any unverified behavior with the change evidence. Reuse existing passing cases unless the change invalidates them; this is not a new per-task approval or full-suite gate.

## New projects

Start with repository-specific invariants and necessary owner pointers in a small `AGENTS.md`. Select existing global Skills by task. Add local Skills, recall indexes, or decision/failure records only when a concrete repeated workflow or expensive lesson warrants them; the architecture's six logical layers do not require six initial sets of files.
