# Geometry and dynamic refit

Use for desktop surfaces whose requested change involves placement, content fitting, monitor recovery, or dynamic layout. Apply the existing product's placement and state contracts; this workflow does not choose a new toolkit, fixed size, palette, or product navigation. For web content, use only the viewport/layout parts supported by the host; do not assume native-window control.

## Separate placement modes

- Give initial launch, content/profile changes, detail open/close, and saved-geometry restore distinct handling under one geometry owner. Reuse shared calculations rather than scattering placement literals across views.
- On first show, build the default content and let layout settle before measuring visible content and applying margins, automatic size caps, and placement. Prefer hidden construction followed by one settled show when supported, so users do not see build/measure/resize stages. Use the product's parent/active-display placement policy and keep the shell within usable bounds.
- During visible content/profile changes, preserve the current monitor and horizontal position. Preserve vertical position for small changes unless content would become inaccessible. Do not reuse initial-launch centering or jump to the primary monitor unless recovering an unusable placement.
- For large detail surfaces, apply the same automatic fit caps, prefer a top-safe position, and expose overflow inside the content viewport. Opening or switching detail should start at the product's predictable useful scroll position, commonly the new detail's top.

## Automatic size and usable work areas

- Automatic fit caps must stay within a safe portion of the available work area. These caps are not manual resize limits: do not impose a hard maximum just to constrain auto-fit. Minimum size protects usability without forcing an oversized launch; users retain the supported ability to enlarge or shrink the window.
- Determine the current monitor/work area from the window handle or position where supported. Preserve negative coordinates or coordinates beyond the primary display when they belong to a valid other monitor. Account for DPI/scaling, taskbars, title bars, and borders.
- Treat raw screen dimensions as an approximation. If they are the only available fallback, retain a safety margin and state the work-area limitation rather than claiming multi-monitor correctness from that fallback alone.
- Restore saved placement only against currently available work areas. If it is no longer usable, recover to the intended or nearest available display and a safe placement; do not blindly clamp every saved position to the primary monitor.
- Keep large table/detail overflow in its own viewport. Scrollbar appearance must not recursively trigger geometry changes. Whether root-level horizontal scrolling is permitted is a product adoption rule.

## Settled refit and measurement

- Use currently visible content, including the selected nested tab, to measure both width and height. Replace a container's stale requested size with its chrome plus the current visible contribution so a fit can shrink as well as grow.
- Content/profile switches, nested-tab changes, and detail toggles should share a coalescing refit scheduler. If a first post-render measurement is unstable, schedule a bounded later event-loop fit after content settles; do not start repeated timer-driven refit loops.
- If measurement temporarily selects hidden tabs, suppress refit callbacks caused by that measurement. Do not synchronously combine measurement and geometry mutation in a configure path that recursively triggers itself.
- Prefer stable containers and reusable pages while content identity remains valid. When rebuilding is necessary, group content and geometry mutations into one settled visible transition.
- Hidden-first construction is different from repeatedly hiding/showing an already-visible shell. Avoid repeated hide/show, arbitrary fixed-size fallbacks, and excessive synchronous layout updates as flicker workarounds. Repeated content-hugging on visible transitions needs coalesced mutation.
- Shell fitting does not own authoritative input lifetime. Use the existing state owner for close/reopen and do not change table, copy/export, graph/detail, or calculation behavior as a geometry side effect.

## Focused verification

For the changed modes, verify first-show visibility, content/detail fitting without monitor jumps, internal overflow, predictable detail scroll, manual resize, and recovery from unavailable saved geometry. Include secondary-monitor or mixed-DPI checks when those boundaries change and the environment supports them.

For dynamic content, use focused helper/fake-trigger tests where possible to check settled refit scheduling, visible-tab sizing, suppression of measurement callbacks, and the absence of recursive geometry loops. Also inspect hidden-first display or stable visible transitions when the change affects them. Static source checks are not native display acceptance; record unavailable platform checks explicitly.
