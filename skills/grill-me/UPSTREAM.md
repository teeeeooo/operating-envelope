# Upstream provenance

- Repository: `https://github.com/RobMitt/grill-me-skill`
- Upstream branch: `main`
- Imported baseline: `31d61d68fc406f8cc2a944b4b10e6f23877720f1`
- Upstream file: `SKILL.md`

## Local adaptation

The canonical global Skill intentionally preserves the upstream interview flow while adapting platform-specific behavior for Codex:

- remove the hard dependency on Claude/Cowork `AskUserQuestion`;
- use an interactive question UI only when the runtime actually exposes one, otherwise ask in chat;
- keep one focused question at a time;
- inspect repository evidence before asking the user;
- avoid turning routine reversible ambiguity into an interview;
- allow guarded implicit invocation through `agents/openai.yaml`.

## Update procedure

1. Read the latest upstream `SKILL.md` and resolve the current upstream `main` SHA.
2. Compare upstream behavior against this file's imported baseline and the canonical `skills/grill-me/SKILL.md`.
3. Preserve upstream improvements that remain platform-neutral.
4. Reapply only the Codex compatibility and guarded-implicit adaptations listed above.
5. Update `Imported baseline` to the reviewed upstream SHA.
6. Run repository harness validation, runtime sync, and explicit/implicit behavioral probes before deployment.

Do not blindly replace the canonical Skill with upstream text because upstream currently targets Claude Code/Cowork tool semantics.
