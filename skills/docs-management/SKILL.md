---
name: docs-management
description: Design and manage documentation structure, ownership and lifecycle for new or existing projects. Use to set up a docs folder, establish document rules, reorganize existing docs, or condense and archive them; not for isolated prose edits or agent-policy maintenance.
---

# Documentation Management

Give new and existing projects a documentation structure that stays useful as they grow. Organize by the questions documents answer, establish where current facts belong, and make updating or retiring a document part of completing the work. Repository instructions own project-specific categories, authorities and acceptance checks; this Skill supplies a reusable method.

## Choose the task path

- **New project or missing docs structure:** read [Structure and lifecycle](references/structure-and-lifecycle.md). Inspect the project brief, entry README, existing files and intended readers; create the smallest useful docs map, content and maintenance rules. Do not make every example category into an empty directory.
- **Existing project needs a structural plan or reorganization:** read [Structure and lifecycle](references/structure-and-lifecycle.md) and [Audit and migration](references/audit-and-migration.md). Map existing documents to their responsibilities, keep useful conventions, resolve duplicated authority and apply only the authorized migration.
- **Ongoing document management or closeout:** use the local documentation map and the lifecycle guidance in [Structure and lifecycle](references/structure-and-lifecycle.md). Update the affected owners and navigation. Read [Audit and migration](references/audit-and-migration.md) when moving, retiring or substantially condensing existing documents; a routine update needs no full-tree audit.
- **Isolated typo, prose edit or feature write-up:** follow the known local owner directly. Do not expand the task into structure design or a policy audit merely because the file is documentation.

Distinguish a proposal-only request from implementation. Preserve existing work and follow the user's current scope. A full-tree audit covers every file in the requested tree; a bounded task starts with the affected owners and references.

## Establish the local document contract

- Find the existing documentation router, current-state owners, repository Skill and helpers before adding alternatives. Use `docs/README.md` as the entry map when no local convention exists; connect it from the project README where useful. Do not move documentation out of a working site or package layout just to match this default.
- Decide the initial structure from project scope and readers. Separate current plans, durable contracts, instructions, decisions and evidence by responsibility when that separation is useful; a small project can express those roles as sections in a few files.
- Keep the local map responsible for category meanings, canonical paths, when to create versus update a file, naming/date rules and closeout/archive criteria. Keep product facts in their own documents and agent execution rules in their existing instruction owners.
- Establish one current owner for each fact or contract. Link summaries to it instead of copying current status into several documents. Identify unknowns from the brief or source; do not invent milestones, decisions, maintainers or validation results to fill a scaffold.
- Give stable owners stable names. Use dated names for bounded records when chronology matters. A date catalog is an optional navigation aid, never another source of current state.

## Keep growth deliberate

- Search by name and responsibility before creating a document. Extend the responsible file unless a distinct audience, contract, decision or execution record needs its own independently useful home.
- Close work by updating the current owner, preserving unique decisions/results in the appropriate record, shortening the current plan and repairing affected navigation in the same change. Do not create a new report for every conversation or duplicate completed chronology in the roadmap and work plan.
- Archive a superseded document only after mapping surviving obligations to successor sections or an explicit retirement. Age, size, missing references, completion or failure alone do not prove obsolescence. Preserve evidence and machine-consumed artifacts under their own contracts.
- Revisit structure when responsibilities diverge, navigation becomes difficult or ownership changes. Prefer targeted consolidation over growing parallel indexes, history ledgers and rule documents. Use existing checks before introducing automation.

## Verify the result

- For a new structure, check that created files have a real purpose and grounded content, the entry map links to existing paths, responsibilities do not overlap, and no empty scaffold or fabricated completion state was introduced.
- For existing documents, check affected links/anchors, preserved obligations and local checks; apply the migration reference's content and consumer checks when relevant. Check catalog coverage/order only if a catalog is part of the task.
- Verify that readers can locate the current plan, relevant contract or instructions, and historical evidence without treating them as interchangeable authorities.
- Report the chosen structure, created/updated/moved files, preservation decisions and verification limits. Keep scratch inventories outside project docs unless a durable migration record is warranted. Do not publish as a side effect of document management.
