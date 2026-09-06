"""Behavioral checks for Soluna schema v3."""

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import workflow_state as state


class WorkflowStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "state.json"
        self.contract = {
            "outcomes": ["Deliver the requested repository behavior"],
            "acceptance": ["Preserve protected baseline behavior"],
        }
        self.allocation = {
            "main": {
                "responsibilities": ["design", "final judgment"],
            },
            "stages": [{
                "id": "impl-1", "count": 1, "role": "Luna implementer",
                "scope": "bounded implementation", "model": "gpt-5.6-luna",
                "effort": "xhigh", "dependencies": [],
            }],
            "authority": {"modify": True, "commit": False, "push": False},
        }
        self.run_command("init", "--run-id", "test", "--repository", self.temp.name)

    def run_command(self, command, *args):
        parsed = state.parser().parse_args([command, "--state", str(self.path), *args])
        with contextlib.redirect_stdout(io.StringIO()):
            parsed.func(parsed)

    def write_json(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def record_contract(self, value=None):
        path = self.write_json("contract.json", value or self.contract)
        self.run_command("contract", "--file", str(path))

    def propose_allocation(self, value=None):
        allocation = value or self.allocation
        path = self.write_json("allocation.json", allocation)
        self.run_command("allocation", "--file", str(path))
        return state.fingerprint(allocation)

    def approve_allocation(self, allocation=None):
        allocation = allocation or self.allocation
        self.run_command(
            "approve-allocation",
            "--fingerprint", state.fingerprint(allocation),
            "--note", "user approved worker allocation",
        )

    def ready(self):
        self.record_contract()
        self.propose_allocation()
        self.approve_allocation()

    def test_main_design_does_not_require_allocation_approval(self):
        self.run_command("transition", "--phase", "DESIGN_MAIN")
        self.assertEqual(state.load(self.path)["phase"], "DESIGN_MAIN")

    def test_worker_dispatch_requires_contract_and_allocation_approval(self):
        with self.assertRaises(SystemExit):
            self.run_command("transition", "--phase", "IMPLEMENT_LUNA")
        self.record_contract()
        self.propose_allocation()
        with self.assertRaises(SystemExit):
            self.run_command("transition", "--phase", "IMPLEMENT_LUNA")
        self.approve_allocation()
        self.run_command("transition", "--phase", "IMPLEMENT_LUNA")

    def test_head_change_does_not_invalidate_allocation_approval(self):
        self.ready()
        self.run_command("transition", "--phase", "IMPLEMENT_LUNA", "--head-sha", "abc123")
        data = state.load(self.path)
        self.assertTrue(state.is_allocation_approved(data))
        self.assertEqual(data["head_sha"], "abc123")

    def test_allocation_change_invalidates_approval(self):
        self.ready()
        changed = json.loads(json.dumps(self.allocation))
        changed["stages"][0]["count"] = 2
        self.propose_allocation(changed)
        data = state.load(self.path)
        self.assertEqual(data["phase"], "ALLOCATION_WAIT")
        self.assertFalse(state.is_allocation_approved(data))

    def test_contract_change_invalidates_allocation_approval(self):
        self.ready()
        changed = {"outcomes": ["Changed outcome"], "acceptance": self.contract["acceptance"]}
        self.record_contract(changed)
        data = state.load(self.path)
        self.assertFalse(state.is_allocation_approved(data))
        self.assertEqual(data["phase"], "DESIGN_MAIN")

    def test_steering_preserves_unchanged_allocation_approval(self):
        self.ready()
        before = state.load(self.path)["allocation_approval"]
        self.run_command("steer", "--note", "clarified wording without changing scope")
        data = state.load(self.path)
        self.assertEqual(data["steering_revision"], 1)
        self.assertEqual(data["allocation_approval"], before)
        self.assertTrue(state.is_allocation_approved(data))

    def test_main_runtime_identity_is_not_part_of_allocation(self):
        changed = json.loads(json.dumps(self.allocation))
        changed["main"]["model"] = "user-selected-root"
        changed["main"]["effort"] = "user-selected-root"
        self.assertFalse(state.valid_allocation(changed))

    def test_astra_effort_above_medium_is_rejected_for_stage(self):
        changed = json.loads(json.dumps(self.allocation))
        changed["stages"].append({
            "id": "specialist", "count": 1, "role": "Astra specialist",
            "scope": "one design question", "model": "gpt-6-astra",
            "effort": "xhigh", "dependencies": ["impl-1"],
        })
        path = self.write_json("bad-stage.json", changed)
        with self.assertRaises(SystemExit):
            self.run_command("allocation", "--file", str(path))

    def test_astra_specialist_medium_is_valid(self):
        changed = json.loads(json.dumps(self.allocation))
        changed["stages"].append({
            "id": "specialist", "count": 1, "role": "Astra specialist",
            "scope": "one design question", "model": "gpt-6-astra",
            "effort": "medium", "dependencies": ["impl-1"],
        })
        self.assertTrue(state.valid_allocation(changed))

    def test_authority_wait_requires_specific_pending_authority(self):
        with self.assertRaises(SystemExit):
            self.run_command("transition", "--phase", "AUTHORITY_WAIT")
        self.run_command(
            "transition", "--phase", "AUTHORITY_WAIT",
            "--pending-authority", "push to origin/main",
        )
        self.assertEqual(state.load(self.path)["pending_authority"], "push to origin/main")
        self.run_command("transition", "--phase", "FINAL_MAIN")
        self.assertIsNone(state.load(self.path)["pending_authority"])

    def test_repair_round_limit_is_enforced(self):
        self.ready()
        self.run_command("transition", "--phase", "REPAIR_LUNA")
        self.run_command("transition", "--phase", "REPAIR_LUNA")
        with self.assertRaises(SystemExit):
            self.run_command("transition", "--phase", "REPAIR_LUNA")

    def test_legacy_state_is_readable_without_inferred_allocation_approval(self):
        legacy = state.load(self.path)
        legacy["schema_version"] = 2
        legacy["execution_plan"] = {
            "main": "orchestrate", "stages": [], "authority": {"modify": False},
            "contract": self.contract,
        }
        legacy["plan_fingerprint"] = "legacy"
        legacy["approval"] = {"fingerprint": "legacy"}
        for key in (
            "contract", "contract_fingerprint", "allocation", "allocation_fingerprint",
            "allocation_approval", "pending_authority", "steering_revision",
        ):
            legacy.pop(key, None)
        self.path.write_text(json.dumps(legacy), encoding="utf-8")
        loaded = state.load(self.path)
        self.assertEqual(loaded["schema_version"], 3)
        self.assertEqual(loaded["contract"], self.contract)
        self.assertIsNone(loaded["allocation_approval"])
        self.assertFalse(state.is_allocation_approved(loaded))

    def test_invalid_contract_is_rejected(self):
        bad = {"outcomes": [], "acceptance": ["x"]}
        path = self.write_json("bad-contract.json", bad)
        with self.assertRaises(SystemExit):
            self.run_command("contract", "--file", str(path))

    def test_luna_reasoning_is_not_capped_by_soluna(self):
        changed = json.loads(json.dumps(self.allocation))
        changed["stages"][0]["effort"] = "max"
        self.assertTrue(state.valid_allocation(changed))


if __name__ == "__main__":
    unittest.main()
