---
name: desktop-window-lifecycle
description: Design or implement desktop window, dialog, viewport, and dynamic page lifecycle behavior including open/close, geometry, focus, modal commit/cancel, dirty state, page activation/deactivation/disposal, layout ownership, and state preservation.
---

# Desktop Window Lifecycle

Use this skill for reusable desktop surface lifecycle behavior. Product-specific navigation, visual design, and domain state remain repository-local.

## Window and dialog contract

Define the relevant behavior for:

- open, close, minimize, maximize, restore, and reopen;
- modal versus modeless interaction;
- focus ownership and return focus;
- geometry, resize, minimum size, and restore behavior;
- dirty state and unsaved-change handling;
- explicit dialog commit, cancel, and dismissal semantics; and
- content fit, scrolling, and viewport containment.

Closing and reopening a surface must not silently reset authoritative application data unless that reset is an explicit product behavior.

A dialog's visual dismissal must not be confused with committing domain state.
## Dynamic page lifecycle

For pages, screens, tabs, or dynamically mounted content, distinguish:

1. create — allocate the view and stable resources;
2. activate — bind current data and become interactive;
3. deactivate — pause or detach transient behavior without destroying authoritative state;
4. dispose — release owned resources intentionally.

Do not use page refresh as a hidden domain mutation. Refresh should re-project current authoritative state unless the product contract explicitly says otherwise.

Avoid timer-driven repeated refit, resize, or re-layout loops as a workaround for unclear layout ownership. Prefer deterministic layout constraints and a single owner for geometry decisions.

## State ownership

- Keep domain state outside disposable view objects when the state must survive close/reopen or page replacement.
- Separate persisted application state, session state, view state, and transient interaction state.
- Restore only state whose lifetime actually spans the reopen/recreate boundary.
- Ensure subscriptions, callbacks, timers, and background work are disconnected or transferred when their owning surface is disposed.
- When an operation needs progress UI, let it render before work begins and keep its lifecycle tied to the operation. Success, failure, and supported cancellation must settle the progress state and restore appropriate controls; closing a dialog does not itself cancel background work.

## Implementation approach

1. Inspect the current surface owner, navigation/window manager, state owner, and lifecycle hooks.
2. Identify which object owns creation, activation, disposal, geometry, and authoritative state.
3. Remove competing lifecycle ownership rather than layering another workaround.
4. Verify close/reopen, resize, focus, commit/cancel, and dynamic-page behavior proportional to the change.

Framework-specific APIs belong in repository implementation or optional references, not in this global contract.
