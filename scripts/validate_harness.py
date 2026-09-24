#!/usr/bin/env python3
"""Validate repository-owned invariants for the canonical user harness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SKILLS = {
    "soluna": False,
    "agent-policy-maintenance": True,
    "grill-me": True,
    "desktop-table-ui": True,
    "desktop-window-lifecycle": True,
    "python-test-portability": True,
}


def fail(message: str) -> None:
    raise SystemExit(f"harness validation failed: {message}")


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def validate_skill(name: str, implicit: bool | None = None) -> None:
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
    match = re.search(r"(?m)^\s*allow_implicit_invocation:\s*(true|false)\s*$", metadata)
    if not match:
        fail(f"skills/{name}/agents/openai.yaml must declare implicit policy")
    if implicit is not None and match.group(1) != str(implicit).lower():
        fail(f"skills/{name}/agents/openai.yaml implicit policy must be {implicit}")


def source_files(root: Path) -> dict[Path, bytes]:
    return {
        path.relative_to(root): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.relative_to(root).parts
        and path.suffix not in {".pyc", ".pyo"}
    }


def load_deployment(path: Path, known: set[str]) -> tuple[set[str], set[str]]:
    """Read this repository's deployment selection, not a native Codex config."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"cannot read deployment manifest {path}: {exc}")
    if not isinstance(data, dict) or data.get("version") != 1:
        fail("deployment manifest must be a version 1 object")
    groups = []
    for key in ("skills", "absent_skills"):
        values = data.get(key)
        if not isinstance(values, list) or any(
            not isinstance(v, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", v)
            for v in values
        ):
            fail(f"deployment {key} must contain plain Skill names")
        if len(values) != len(set(values)):
            fail(f"deployment {key} contains duplicate names")
        groups.append(set(values))
    selected, absent = groups
    if selected & absent:
        fail("deployment selected and absent Skills overlap")
    if selected | absent != known:
        fail("deployment must classify every canonical Skill exactly once")
    return selected, absent


def validate_runtime(
    home: Path, skills: Path, names: set[str], absent: set[str] | None = None
) -> None:
    override = home / "AGENTS.override.md"
    if override.is_file() and override.read_text(encoding="utf-8").strip():
        fail(f"runtime global guidance is shadowed by {override}")
    deployed = home / "AGENTS.md"
    if not deployed.is_file() or deployed.read_bytes() != (ROOT / "global/AGENTS.md").read_bytes():
        fail(f"runtime global guidance differs or is missing: {deployed}")
    for name in sorted(absent or set()):
        path = skills / name
        if path.exists() or path.is_symlink():
            fail(f"intentionally absent runtime skill is installed: {path}")
    for name in sorted(names):
        expected = source_files(ROOT / "skills" / name)
        actual = source_files(skills / name)
        if expected != actual:
            changed = sorted(str(p) for p in expected.keys() | actual.keys() if expected.get(p) != actual.get(p))
            fail(f"runtime skill {name} differs: {', '.join(changed)}")
    if (skills / "design-interview").exists():
        fail(f"retired runtime skill still exists: {skills / 'design-interview'}")
    print(f"runtime file equality: PASS ({home}; {skills}); discovery requires a host probe")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-home", type=Path, help="Also check deployed global guidance in this Codex home")
    parser.add_argument("--runtime-skills", type=Path, help="Skill deployment root; defaults to <runtime-home>/skills")
    parser.add_argument(
        "--deployment-manifest", type=Path,
        help="Repository deployment selection; defaults to deployment/desktop.json",
    )
    args = parser.parse_args()
    if args.runtime_skills is not None and args.runtime_home is None:
        parser.error("--runtime-skills requires --runtime-home")
    global_agents = read(ROOT / "global" / "AGENTS.md")
    if "Global Working Agreements" not in global_agents:
        fail("global/AGENTS.md is not the canonical global contract")

    names = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir() and path.name != "__pycache__"}
    missing = REQUIRED_SKILLS.keys() - names
    if missing:
        fail(f"missing required skills: {', '.join(sorted(missing))}")
    for name in sorted(names):
        validate_skill(name, REQUIRED_SKILLS.get(name))

    manifest = args.deployment_manifest or ROOT / "deployment/desktop.json"
    selected, absent = load_deployment(manifest.expanduser(), names)

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

    if args.runtime_home is not None:
        home = args.runtime_home.expanduser().resolve()
        skills = args.runtime_skills.expanduser().resolve() if args.runtime_skills is not None else home / "skills"
        validate_runtime(home, skills, selected, absent)

    print("harness validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
