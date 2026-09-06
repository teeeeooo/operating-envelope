---
name: python-test-portability
description: Design or repair Python tests and test helpers that must remain portable across operating systems, working directories, locales, subprocess environments, filesystem representations, and logically equivalent artifacts. Use when cross-platform or non-repo-cwd behavior matters.
---

# Python Test Portability

Use this skill for reusable Python test-portability concerns. Repository-specific GUI/toolkit lifecycle, packaging, product contracts, and serialized-format rules remain with the repository owner.

## Filesystem and working directory

- Resolve repository/package resources from an explicit owner such as module `__file__`, package resources, configuration, or a passed root; do not depend on the caller's current working directory unless cwd is the contract under test.
- Exercise important import/resource paths from a non-repository cwd when portability depends on cwd independence.
- Compare platform-native filesystem identity with `pathlib.Path` or an equivalent normalized path representation rather than raw slash spelling.
- Assert a literal separator only when a public or serialized format explicitly owns that representation.

## Text and subprocesses

- Use an explicit encoding, normally UTF-8, for repository-owned text reads and writes.
- Non-interactive subprocess tests should not accidentally inherit stdin. Use `stdin=subprocess.DEVNULL` or another deliberate input owner when no input is expected.
- Declare text mode/encoding deliberately when subprocess output is textual rather than relying on the host locale.
- Set subprocess `cwd`, environment, and import path only when the invoked program's contract requires them; avoid hidden dependence on the parent test runner state.

## Identity and assertions

- Test logical artifact identity from deterministic logical content when container metadata may vary across OS/runtime versions.
- Use raw byte hashes only when exact bytes are themselves the declared contract.
- Prefer semantic error assertions when ordering, path rendering, locale wording, or the complete rendered message is not part of the public contract.
- Do not normalize away a real public serialization, protocol, path-format, or exact-artifact requirement merely to make tests cross-platform.

## Scope boundary

Apply the narrowest portability rule that matches the test. Do not introduce platform abstraction where the product intentionally owns platform-specific behavior.
