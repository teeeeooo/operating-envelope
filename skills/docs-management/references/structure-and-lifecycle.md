# Structure and Lifecycle

Use this guidance when starting project documentation, adopting a structure in an existing project, or managing documents through ordinary work. The paths below are adaptable examples, not a required folder template.

## Start from actual readers and content

Inspect the project brief, root README, repository instructions, current docs and relevant source entry points. Determine who needs the documents, which questions must be answered now, and which facts already have a reliable owner. Ask only when a missing choice materially changes the outcome; otherwise choose a modest structure from the available evidence.

For a small new project, a useful starting shape is:

```text
docs/
  README.md      # document map, ownership and upkeep rules
  plan.md        # current scope, open work and next steps, when needed
  design.md      # established design or explicitly identified proposals, when needed
```

Create `plan.md` or `design.md` only when there is content to own. An initial docs map can be sufficient. Link existing material instead of copying it, and omit empty directories, placeholder files and invented decisions. Keep setup/quickstart in the root README when that is already its role.

## Expand by responsibility

Split files into folders when there are several independently useful documents or a clear reader/ownership boundary. Use existing names and ordering conventions. A possible larger layout is:

| Responsibility | Possible location | When it earns a separate home |
| --- | --- | --- |
| Scope and current work | `project/` | Plans need more than a section; distinguish near-term work from milestone direction. |
| Product or interface contracts | `specs/` | Requirements, schemas or API behavior need a stable reference. |
| System design | `architecture/` | Component boundaries and design constraints have distinct owners. |
| How to use, develop or operate | `guides/` | Readers need task instructions beyond the quickstart. |
| Significant decisions | `decisions/` | A decision and its alternatives explain a lasting constraint. |
| Validation and execution evidence | `validation/`, optionally `evidence/` | Acceptance procedures and actual run results need distinct authority or retention. |
| Superseded context | `archive/` | A real retirement occurs; preserve original categories if useful. |

Do not create all of these upfront. A monorepo may keep package docs beside their code with a central routing map; a documentation site may already have its own navigation and taxonomy. Prefer those working structures to a forced migration. Numeric prefixes, dedicated diagnostics folders and platform qualification rules belong to repositories that need them.

## Make the entry map answer the management questions

Keep one local documentation map, normally `docs/README.md`, with enough information to answer:

- **Where do I start?** Link the useful reading paths for actual readers, not every historical record.
- **Which document owns this fact?** Map current scope/state, contracts, instructions, decisions and evidence to their canonical paths. Name an accountable role only when known; a file owner does not require inventing a person.
- **Where does new information belong?** Define category meanings and when to update an existing owner versus create a separate record.
- **How are names and dates used?** Keep stable owner names, identify event/authoring/Git dates accurately, and choose dated record names only where useful.
- **How does work close?** State which current owner, evidence and navigation must be updated; define supersession and archive criteria and any repository checks.

Link to existing policies rather than copying them into this map. Keep it navigational and concise. Do not add a second index, lifecycle handbook or policy file unless the existing map has a concrete responsibility it cannot reasonably serve.

## Use a lifecycle that prevents accumulation

**Create:** Search for an owner first. A new file should answer an independent question or record a distinct decision/run. For substantial documents, make purpose, authority/status and relevant context discoverable through the title, opening text or local metadata convention. Do not impose a metadata schema on every file.

**Update:** Change the canonical contract or instruction in place and fix dependent summaries/links. Distinguish a proposal from an accepted design and a validation plan from a result. Preserve significant decision rationale in its decision record when replacing current design text.

**Close:** Record results, corrections and unresolved conditions in the responsible evidence or decision record. Keep the work plan focused on present state and next actions; retain roadmap milestone direction only when it answers a different question. Do not make both files mandatory. Consolidate follow-up results from the same bounded effort instead of making a new report each turn.

**Retire:** Identify the successor and its relevant sections or the explicit retirement decision. Archive replaced contracts and procedures after references/consumers are handled. Completed evidence, failed experiments and deferred obligations may remain in their original category; their outcome is separate from their authority. Preserve historical measurements and verdicts.

**Review:** Revisit affected documents when work closes, an owner changes or navigation becomes hard. Split by responsibility or consolidate duplicates when useful; do not add arbitrary line-count limits or time-based expiry as universal rules. Use available link/navigation checks during changes. A scheduled cleanup is optional and requires a user request to create it.

## Adopt this in an existing project

Inventory the requested scope, identify the actual current owners and map existing material onto these responsibilities. Fix ambiguity and duplicated state before changing folder names. Retain working conventions and active paths unless a concrete benefit justifies migration.

Apply moves, substantial compaction and archival with [Audit and migration](audit-and-migration.md). Never initialize a new template over existing content. An existing project can adopt lifecycle rules and a better entry map without moving its documents.
