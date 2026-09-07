---
name: desktop-table-ui
description: Design or implement spreadsheet-like desktop table interactions such as selection, keyboard navigation, copy/paste, rectangular paste, batch editing, read-only cells, scrolling, and selection preservation. Use when a desktop application table or grid needs consistent interaction behavior.
---

# Desktop Table UI

Use this skill for reusable table-interaction behavior. Repository-specific domain rules and visual design remain with the repository owner.

## Interaction contract

Prefer familiar spreadsheet conventions unless the product explicitly defines different behavior.

Cover the relevant behaviors:

- row, column, and cell selection;
- Shift range extension and Ctrl/Cmd additive selection where supported;
- keyboard navigation and edit entry/commit/cancel;
- copy and paste through the system clipboard;
- rectangular multi-cell paste;
- batch input and multi-row editing;
- read-only versus editable cell behavior;
- scrolling and viewport containment;
- selection persistence across safe refreshes;
- header interaction and column sizing; and
- invalid-input feedback without silently mutating unrelated cells.

Do not invent a product-specific interaction when an existing table adapter or shared behavior already owns it.
## Data boundaries

Keep these representations distinct:

1. domain value/schema — authoritative business value and validation;
2. table presentation schema — ordering, labels, editability, formatting, visibility;
3. clipboard/export representation — tabular text or interchange form.

Do not couple domain truth to a view-only column index, rendered string, or clipboard layout when a canonical value owner exists.

For paste, define how source rows/columns map to the selected rectangle, how overflow is handled, and whether invalid cells reject the operation atomically or per cell according to the existing product contract.

## Lifecycle behavior

- Preserve selection and scroll position when a refresh does not invalidate them.
- Do not let a visual refresh silently commit an in-progress edit unless the existing interaction contract requires it.
- Keep read-only cells non-editable through keyboard, mouse, paste, and batch paths consistently.
- Distinguish empty, zero, invalid, read-only, and inactive states; the domain validator decides whether an empty value is allowed. Apply the same state permissions to inline edit, paste, clear, and batch paths.
- Where undo is supported, make one user edit, paste, or clear one undo action. Define undo-history lifetime when the underlying data context changes so undo cannot restore values into a different dataset.
- Avoid duplicate local event handlers when an existing table abstraction can own the behavior once.

## Implementation approach

1. Inspect the repository's current table owner, adapters, delegates, models, and tests.
2. Identify the smallest reusable owner that can express the interaction consistently.
3. Keep toolkit mechanics below the repository's domain boundary.
4. Verify observable interaction behavior with the narrowest meaningful checks available.

Framework-specific Qt, Tkinter, or other toolkit details are implementation references, not global product rules.
