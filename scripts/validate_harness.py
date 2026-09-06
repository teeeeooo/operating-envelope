#!/usr/bin/env python3
"""Validate repository-owned invariants for the canonical user harness."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SKILLS = {
    "soluna": False,
    "grill-me": True,
    "desktop-table-ui": True,
    "desktop-window-lifecycle": True,
}


def fail(message: str) -> None:
    raise SystemExit(f"harness validation failed: {message}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def validate_skill(name: str, implicit: bool) -> None:
    root = ROOT / "skills" / name
    skill = read(root / "SKILL.md")
    parts = skill.split("---", 2)
    if len(parts) < 3:
        fail(f"skills/{name}/SKILL.md has no YAML frontmatter")
    frontmatter = parts[1]
    match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", frontmatter)
    if not match or match.group(1) != name:
        fail(f"skills/{name}/SKILL.md name does not match directory")
    if not re.search(r"(?m)^description:\s*\S", frontmatter):
        fail(f"skills/{name}/SKILL.md has no description")

    metadata = read(root / "agents" / "openai.yaml")
    expected = str(implicit).lower()
    match = re.search(r"(?m)^\s*allow_implicit_invocation:\s*(true|false)\s*$", metadata)
    if not match or match.group(1) != expected:
        fail(f"skills/{name}/agents/openai.yaml implicit policy must be {expected}")


def main() -> int:
    global_agents = read(ROOT / "global" / "AGENTS.md")
    if "Global Working Agreements" not in global_agents:
        fail("global/AGENTS.md is not the canonical global contract")

    for name, implicit in REQUIRED_SKILLS.items():
        validate_skill(name, implicit)

    if (ROOT / "skills" / "design-interview").exists():
        fail("retired skills/design-interview still exists")

    upstream = read(ROOT / "skills" / "grill-me" / "UPSTREAM.md")
    if not re.search(r"Imported baseline: `[0-9a-f]{40}`", upstream):
        fail("grill-me upstream baseline is not pinned")

    tracked = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.splitlines()
    generated = [p for p in tracked if "__pycache__/" in p or p.endswith((".pyc", ".pyo"))]
    if generated:
        fail(f"generated Python artifacts are tracked: {', '.join(generated)}")

    active_docs = "\n".join(
        read(ROOT / path)
        for path in ("README.md", "docs/ASTRA_AGENT_HARNESS_V2.md")
    )
    if "~/.agents/skills" in active_docs:
        fail("active docs still reference retired ~/.agents/skills runtime")

    print("harness validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
