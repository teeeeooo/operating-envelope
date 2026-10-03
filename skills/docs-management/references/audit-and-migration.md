# Audit and Migration

Read this when auditing existing documents, moving/retiring files or substantially condensing current-state owners. New projects with no existing documents do not need a migration inventory.

## Preserve the starting point

Record the starting revision and local changes when Git is available. Preserve the actual starting content of affected files, including uncommitted edits; a HEAD blob alone cannot recover those edits. Use a file snapshot when no history exists. Keep scratch inventories outside maintained docs unless a durable record is needed.

## Inventory and classify

- Collect paths, document roles, status claims, size, date evidence and inbound/outbound references. Distinguish current contracts, retained/deferred obligations, completed evidence, investigations and superseded context using the repository's categories.
- If chronological navigation is requested, follow rename history to the first Git addition, convert dates in the agreed timezone and label them as Git dates. Keep authoring, event, modification and archival dates distinct. Without reliable history, identify the available source or leave the date unknown; identify uncommitted new files explicitly.
- Prefer stable filenames and the established navigation format. Do not manipulate filesystem timestamps or rename every owner merely to sort it. Keep any catalog derived from actual files and out of current-state authority.
- Search explicit paths, unique filenames, relative links, anchors and code/test consumers. Missing references are a discovery signal, not proof of disuse. A catalog or broad history list does not make every record a current dependency. State limits on dynamic or external consumers.
- Do not infer that an old, large, completed or failed document is obsolete. Product contracts can remain current after implementation; rejected experiments can remain important evidence in their existing location.

## Apply the authorized change

- Before retiring a contract, map its surviving obligations to successor sections or an explicit retirement decision. A newer revision title is insufficient. Keep unresolved candidates in place with a precise reason while completing other authorized changes.
- For moves, identify old/new paths, original content hashes and reference repairs. Use the repository's archive policy; if none exists, establish one in its document map before moving files. Preserve basenames unless a rename has a purpose. Repair outgoing relative links, inbound references and used anchors.
- Preserve historical measurements, verdicts and provenance. Separate relocation/link-only edits from intentional content edits. Understand the consumer contract of machine fixtures, truth, manifests and fingerprints before changing paths or bytes.
- Condense current-state documents by replacing completed chronology with existing evidence links. Preserve acceptance state, baselines, authorization, restrictions, unresolved questions and the next transition. Do not turn local checks into another platform's acceptance or reopen closed work from historical pending prose.
- Retain unique facts in the responsible evidence/decision owner before removing them from a summary. A recoverable snapshot preserves provenance but is no substitute for discoverable current obligations. Avoid another continuously growing history ledger when records already own the detail.
- Update navigation and local management rules where needed. A small correction need not generate an audit report; larger moves may justify one mapping/verification record supporting scoped recovery.

## Verify preservation

- Check file conservation, destination collisions, affected links and used anchors. Check catalog coverage/order if it exists. Inspect ambiguous textual link matches before treating them as defects.
- Compare protected files with starting content. For link-only moves, verify the remaining content is unchanged. For summaries, verify obligation coverage and current-state equivalence separately from byte checks.
- Verify actual path consumers when moved data is executable input. Run applicable documentation/governance and whitespace checks. Broaden to consumer tests only when their contract changes; docs work alone does not require unrelated product or field requalification.
- Report applied changes, retained candidates and reasons, verification scope and limits. Keep recovery scoped to the actual starting worktree and this change.
