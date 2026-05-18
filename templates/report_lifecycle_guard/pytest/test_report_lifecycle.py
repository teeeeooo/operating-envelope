"""Optional pytest guard for the report lifecycle convention.

Drop this file into the target project's test suite (or import it from a
conftest) to verify that every file under ``result_reports/active/`` and
``result_reports/archive/`` satisfies the convention defined in
``REPORT_LIFECYCLE.md``.

Scope of this guard:

- Naming pattern: ``NNN_<kebab-case-slug>.md``.
- Ordinal uniqueness across active + archive.
- No stray files in either folder (only ``*.md`` allowed).

Out of scope (handled elsewhere or by humans):

- Whether a commit ships *with* a report (see the pre-commit hook).
- Whether a report's contents satisfy the §5 minimum sections (human
  review).

The guard is intentionally read-only and skips silently when the report
folders do not exist, so it is safe to drop into a project that is just
starting to adopt the convention.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List, Tuple

import pytest

REPORT_ROOT_ENV = "REPORT_LIFECYCLE_ROOT"
DEFAULT_ROOT = "result_reports"
ACTIVE_DIR = "active"
ARCHIVE_DIR = "archive"
NAME_PATTERN = re.compile(r"^(\d{3})_([a-z0-9]+(?:-[a-z0-9]+)*)\.md$")


def _root() -> Path:
    import os

    return Path(os.environ.get(REPORT_ROOT_ENV, DEFAULT_ROOT))


def _iter_reports() -> Iterable[Tuple[str, Path]]:
    root = _root()
    for state in (ACTIVE_DIR, ARCHIVE_DIR):
        folder = root / state
        if not folder.is_dir():
            continue
        for entry in folder.iterdir():
            yield state, entry


@pytest.fixture(scope="module")
def report_files() -> List[Tuple[str, Path]]:
    return list(_iter_reports())


def test_report_lifecycle_root_exists_or_skips(report_files):
    if not report_files:
        pytest.skip(
            f"No reports under {_root()!s}/(active|archive); "
            "guard is a no-op until the project adopts the convention."
        )


def test_report_names_match_convention(report_files):
    if not report_files:
        pytest.skip("No reports to check.")
    bad: List[str] = []
    for state, entry in report_files:
        if not entry.is_file():
            bad.append(f"{state}/{entry.name} is not a file")
            continue
        if entry.suffix != ".md":
            bad.append(f"{state}/{entry.name} is not a .md file")
            continue
        if not NAME_PATTERN.match(entry.name):
            bad.append(
                f"{state}/{entry.name} does not match NNN_<kebab-slug>.md"
            )
    assert not bad, "Report name violations:\n  - " + "\n  - ".join(bad)


def test_report_ordinals_are_unique(report_files):
    if not report_files:
        pytest.skip("No reports to check.")
    seen: dict[str, str] = {}
    dupes: List[str] = []
    for state, entry in report_files:
        match = NAME_PATTERN.match(entry.name)
        if not match:
            continue  # already reported by the naming test
        ordinal = match.group(1)
        if ordinal in seen:
            dupes.append(f"{ordinal}: {seen[ordinal]} vs {state}/{entry.name}")
        else:
            seen[ordinal] = f"{state}/{entry.name}"
    assert not dupes, "Duplicate report ordinals:\n  - " + "\n  - ".join(dupes)
