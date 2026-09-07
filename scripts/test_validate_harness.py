"""Exercise deployment drift and canonical discovery without touching user files."""

from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import validate_harness as validator


class HarnessValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "canonical"
        self.home = Path(self.temp.name) / "codex-home"
        self.skills = Path(self.temp.name) / "host-skill-root"
        self.home.mkdir()
        for folder in ("global", "skills"):
            shutil.copytree(validator.ROOT / folder, self.root / folder,
                            ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(self.root / "global/AGENTS.md", self.home / "AGENTS.md")
        shutil.copytree(self.root / "skills", self.skills)
        self.names = set(validator.REQUIRED_SKILLS)
        self.addCleanup(patch.stopall)
        patch.object(validator, "ROOT", self.root).start()

    def check_runtime(self):
        validator.validate_runtime(self.home, self.skills, self.names)

    def test_explicit_host_root_and_unmanaged_skill_are_allowed(self):
        (self.skills / "unrelated").mkdir()
        (self.skills / "desktop-table-ui/__pycache__").mkdir()
        (self.skills / "desktop-table-ui/__pycache__/cache.pyc").write_bytes(b"cache")
        self.check_runtime()

    def test_missing_changed_and_extra_managed_files_fail(self):
        target = self.skills / "desktop-table-ui/SKILL.md"
        original = target.read_bytes()
        for mutation in ("missing", "changed", "extra"):
            with self.subTest(mutation=mutation):
                extra = target.parent / "stale.md"
                if mutation == "missing":
                    target.unlink()
                elif mutation == "changed":
                    target.write_bytes(original + b"drift")
                else:
                    extra.write_text("obsolete instructions", encoding="utf-8")
                with self.assertRaises(SystemExit):
                    self.check_runtime()
                target.write_bytes(original)
                extra.unlink(missing_ok=True)

    def test_global_drift_and_nonempty_override_fail(self):
        override = self.home / "AGENTS.override.md"
        override.write_text("override", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.check_runtime()
        override.write_text("", encoding="utf-8")
        self.check_runtime()
        (self.home / "AGENTS.md").write_text("drift", encoding="utf-8")
        with self.assertRaises(SystemExit):
            self.check_runtime()

    def test_new_skill_is_validated_without_required_list_entry(self):
        new = self.root / "skills/new-workflow"
        shutil.copytree(self.root / "skills/desktop-table-ui", new)
        # A copied skill with the wrong name must fail even outside REQUIRED_SKILLS.
        with patch("sys.argv", ["validate_harness.py"]):
            with self.assertRaisesRegex(SystemExit, "name does not match"):
                validator.main()


if __name__ == "__main__":
    unittest.main()
