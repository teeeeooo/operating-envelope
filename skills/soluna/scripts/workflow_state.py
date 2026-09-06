#!/usr/bin/env python3
"""Maintain compact state for Soluna's contract and worker-allocation gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PHASES = (
    "INTAKE", "DESIGN_MAIN", "ALLOCATION_WAIT", "EXPLORE_LUNA",
    "EVIDENCE_LUNA", "IMPLEMENT_LUNA", "AUDIT_LUNA", "REPAIR_LUNA",
    "SPECIALIST_ASTRA", "FINAL_MAIN", "AUTHORITY_WAIT", "CLOSE_LUNA",
    "CLOSED", "BLOCKED",
)
WORKER_PHASES = {
    "EXPLORE_LUNA", "EVIDENCE_LUNA", "IMPLEMENT_LUNA", "AUDIT_LUNA",
    "REPAIR_LUNA", "SPECIALIST_ASTRA", "CLOSE_LUNA",
}
LIST_FIELDS = ("invariants", "required_checks", "findings", "evidence")
ASTRA_MODEL = "gpt-6-astra"
ASTRA_EFFORTS = {"low", "medium"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def fingerprint(value: dict[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def valid_contract(contract: Any) -> bool:
    if not isinstance(contract, dict):
        return False
    for key in ("outcomes", "acceptance"):
        items = contract.get(key)
        if not isinstance(items, list) or not items:
            return False
        if not all(isinstance(item, str) and item.strip() for item in items):
            return False
    return True


def valid_actor(actor: Any) -> bool:
    if not isinstance(actor, dict):
        return False
    if not all(isinstance(actor.get(k), str) and actor[k].strip() for k in ("model", "effort")):
        return False
    if actor["model"] == ASTRA_MODEL and actor["effort"] not in ASTRA_EFFORTS:
        return False
    return True


def valid_main(main: Any) -> bool:
    if not isinstance(main, dict):
        return False
    if "model" in main or "effort" in main:
        return False
    responsibilities = main.get("responsibilities")
    return isinstance(responsibilities, (str, list)) and bool(responsibilities)

def valid_stage(stage: Any) -> bool:
    if not valid_actor(stage):
        return False
    required = ("id", "role", "scope")
    if not all(isinstance(stage.get(k), str) and stage[k].strip() for k in required):
        return False
    count = stage.get("count")
    return isinstance(count, int) and count >= 1


def valid_allocation(allocation: Any) -> bool:
    if not isinstance(allocation, dict) or not valid_main(allocation.get("main")):
        return False
    stages = allocation.get("stages")
    if not isinstance(stages, list) or not all(valid_stage(stage) for stage in stages):
        return False
    ids = [stage["id"] for stage in stages]
    if len(ids) != len(set(ids)):
        return False
    return isinstance(allocation.get("authority"), dict)


def is_allocation_approved(data: dict[str, Any]) -> bool:
    allocation = data.get("allocation")
    approval = data.get("allocation_approval")
    return bool(
        valid_allocation(allocation)
        and isinstance(approval, dict)
        and fingerprint(allocation) == data.get("allocation_fingerprint")
        and approval.get("fingerprint") == data.get("allocation_fingerprint")
    )

def migrate_legacy(data: dict[str, Any]) -> dict[str, Any]:
    old_plan = data.get("execution_plan")
    contract = old_plan.get("contract") if isinstance(old_plan, dict) else None
    data = dict(data)
    data["schema_version"] = 3
    data["legacy_execution_plan"] = old_plan
    data["contract"] = contract if valid_contract(contract) else None
    data["contract_fingerprint"] = fingerprint(contract) if valid_contract(contract) else None
    data["allocation"] = None
    data["allocation_fingerprint"] = None
    data["allocation_approval"] = None
    data["pending_authority"] = None
    data["steering_revision"] = 0
    for key in ("execution_plan", "plan_fingerprint", "approval", "mode"):
        data.pop(key, None)
    return data


def load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    version = data.get("schema_version")
    if version in (1, 2):
        data = migrate_legacy(data)
    elif version != 3:
        raise SystemExit(f"unsupported schema_version in {path}")
    data.setdefault("contract", None)
    data.setdefault("contract_fingerprint", None)
    data.setdefault("allocation", None)
    data.setdefault("allocation_fingerprint", None)
    data.setdefault("allocation_approval", None)
    data.setdefault("pending_authority", None)
    data.setdefault("steering_revision", 0)
    return data

def save(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = now()
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def command_init(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    if path.exists():
        raise SystemExit(f"state already exists: {path}")
    if args.max_repair_rounds < 1:
        raise SystemExit("max repair rounds must be positive")
    created = now()
    data: dict[str, Any] = {
        "schema_version": 3,
        "run_id": args.run_id,
        "repository": str(Path(args.repository).expanduser().resolve()),
        "contract": None, "contract_fingerprint": None,
        "allocation": None, "allocation_fingerprint": None,
        "allocation_approval": None, "pending_authority": None,
        "steering_revision": 0, "phase": "INTAKE",
        "base_sha": args.base_sha, "head_sha": args.base_sha,
        "next_gate": None, "repair_rounds": 0,
        "max_repair_rounds": args.max_repair_rounds,
        "artifacts": {}, "invariants": [], "required_checks": [],
        "findings": [], "evidence": [],
        "history": [{"at": created, "phase": "INTAKE", "note": "initialized"}],
        "created_at": created, "updated_at": created,
    }
    save(path, data)
    print(path)

def command_contract(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    data = load(path)
    with Path(args.file).expanduser().open(encoding="utf-8") as handle:
        contract = json.load(handle)
    if not valid_contract(contract):
        raise SystemExit("contract requires nonempty outcomes and acceptance string lists")
    digest = fingerprint(contract)
    if digest != data.get("contract_fingerprint"):
        previous = data.get("contract")
        data["contract"] = contract
        data["contract_fingerprint"] = digest
        data["allocation_approval"] = None
        data["phase"] = "DESIGN_MAIN"
        data["history"].append({"at": now(), "phase": "DESIGN_MAIN", "note": "outcome contract recorded", "previous_contract": previous})
        save(path, data)
    print(digest)


def command_allocation(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    data = load(path)
    with Path(args.file).expanduser().open(encoding="utf-8") as handle:
        allocation = json.load(handle)
    if not valid_allocation(allocation):
        raise SystemExit("invalid allocation or spawned Astra child effort above medium")
    digest = fingerprint(allocation)
    if digest != data.get("allocation_fingerprint") or not is_allocation_approved(data):
        data["allocation"] = allocation
        data["allocation_fingerprint"] = digest
        data["allocation_approval"] = None
        data["phase"] = "ALLOCATION_WAIT"
        data["history"].append({"at": now(), "phase": "ALLOCATION_WAIT", "note": "worker allocation proposed"})
        save(path, data)
    print(digest)

def command_approve_allocation(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    data = load(path)
    allocation = data.get("allocation")
    if data.get("phase") != "ALLOCATION_WAIT" or not valid_allocation(allocation):
        raise SystemExit("approval requires ALLOCATION_WAIT and a valid current allocation")
    digest = fingerprint(allocation)
    if args.fingerprint != digest or args.fingerprint != data.get("allocation_fingerprint"):
        raise SystemExit("approval fingerprint does not match current allocation")
    if not args.note.strip():
        raise SystemExit("explicit user approval reference is required")
    data["allocation_approval"] = {"fingerprint": digest, "at": now(), "note": args.note}
    data["history"].append({"at": now(), "phase": "ALLOCATION_WAIT", "note": "user approved worker allocation"})
    save(path, data)


def command_steer(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    data = load(path)
    if not args.note.strip():
        raise SystemExit("steering note is required")
    data["steering_revision"] = int(data.get("steering_revision", 0)) + 1
    data["history"].append({"at": now(), "phase": data["phase"], "note": f"steering: {args.note}"})
    save(path, data)
    print(data["steering_revision"])

def command_transition(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    data = load(path)
    if args.phase in WORKER_PHASES:
        if not valid_contract(data.get("contract")):
            raise SystemExit("worker dispatch requires a frozen outcome contract")
        if not is_allocation_approved(data):
            raise SystemExit("approved worker allocation required before child-agent dispatch")
    if args.phase == "ALLOCATION_WAIT":
        data["allocation_approval"] = None
    if args.phase == "REPAIR_LUNA":
        rounds = int(data["repair_rounds"]) + 1
        if rounds > int(data["max_repair_rounds"]):
            raise SystemExit("repair round limit reached; transition to BLOCKED")
        data["repair_rounds"] = rounds
    if args.phase == "AUTHORITY_WAIT":
        if not args.pending_authority or not args.pending_authority.strip():
            raise SystemExit("AUTHORITY_WAIT requires --pending-authority")
        data["pending_authority"] = args.pending_authority.strip()
    elif data.get("phase") == "AUTHORITY_WAIT":
        data["pending_authority"] = None
    data["phase"] = args.phase
    if args.head_sha is not None:
        data["head_sha"] = args.head_sha
    data["next_gate"] = args.next_gate
    data["history"].append({"at": now(), "phase": args.phase, "note": args.note or "transition"})
    save(path, data)

def command_append(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    data = load(path)
    values = data[args.field]
    if args.value not in values:
        values.append(args.value)
    save(path, data)


def command_artifact(args: argparse.Namespace) -> None:
    path = Path(args.state).expanduser()
    data = load(path)
    data["artifacts"][args.name] = args.path
    save(path, data)


def command_show(args: argparse.Namespace) -> None:
    data = load(Path(args.state).expanduser())
    if args.compact:
        keys = (
            "run_id", "repository", "contract", "contract_fingerprint",
            "allocation", "allocation_fingerprint", "allocation_approval",
            "steering_revision", "pending_authority", "phase", "base_sha",
            "head_sha", "next_gate", "repair_rounds", "max_repair_rounds",
            "artifacts", "invariants", "required_checks", "findings", "evidence",
        )
        print(json.dumps({key: data.get(key) for key in keys}, ensure_ascii=False, separators=(",", ":")))
        return
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))

def command_gate_card(args: argparse.Namespace) -> None:
    data = load(Path(args.state).expanduser())
    lines = [
        f"RUN: {data['run_id']}",
        f"PHASE: {data['phase']}",
        f"BASE: {data['base_sha'] or 'N/A'}",
        f"HEAD: {data['head_sha'] or 'N/A'}",
        f"ALLOCATION_APPROVED: {str(is_allocation_approved(data)).lower()}",
        f"STEERING_REVISION: {data.get('steering_revision', 0)}",
        f"REPAIR_ROUNDS: {data['repair_rounds']}/{data['max_repair_rounds']}",
        f"FINDINGS: {len(data['findings'])}",
        f"EVIDENCE: {len(data['evidence'])}",
        f"NEXT_GATE: {data['next_gate'] or 'N/A'}",
    ]
    print("\n".join(lines))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    initialize = commands.add_parser("init")
    initialize.add_argument("--state", required=True)
    initialize.add_argument("--run-id", required=True)
    initialize.add_argument("--repository", required=True)
    initialize.add_argument("--base-sha")
    initialize.add_argument("--max-repair-rounds", type=int, default=2)
    initialize.set_defaults(func=command_init)

    contract = commands.add_parser("contract")
    contract.add_argument("--state", required=True)
    contract.add_argument("--file", required=True)
    contract.set_defaults(func=command_contract)

    allocation = commands.add_parser("allocation")
    allocation.add_argument("--state", required=True)
    allocation.add_argument("--file", required=True)
    allocation.set_defaults(func=command_allocation)

    approve = commands.add_parser("approve-allocation")
    approve.add_argument("--state", required=True)
    approve.add_argument("--fingerprint", required=True)
    approve.add_argument("--note", required=True)
    approve.set_defaults(func=command_approve_allocation)

    steer = commands.add_parser("steer")
    steer.add_argument("--state", required=True)
    steer.add_argument("--note", required=True)
    steer.set_defaults(func=command_steer)

    transition = commands.add_parser("transition")
    transition.add_argument("--state", required=True)
    transition.add_argument("--phase", choices=PHASES, required=True)
    transition.add_argument("--head-sha")
    transition.add_argument("--next-gate", choices=PHASES)
    transition.add_argument("--pending-authority")
    transition.add_argument("--note")
    transition.set_defaults(func=command_transition)

    append = commands.add_parser("append")
    append.add_argument("--state", required=True)
    append.add_argument("--field", choices=LIST_FIELDS, required=True)
    append.add_argument("--value", required=True)
    append.set_defaults(func=command_append)

    artifact = commands.add_parser("artifact")
    artifact.add_argument("--state", required=True)
    artifact.add_argument("--name", required=True)
    artifact.add_argument("--path", required=True)
    artifact.set_defaults(func=command_artifact)

    show = commands.add_parser("show")
    show.add_argument("--state", required=True)
    show.add_argument("--compact", action="store_true")
    show.set_defaults(func=command_show)

    gate = commands.add_parser("gate-card")
    gate.add_argument("--state", required=True)
    gate.set_defaults(func=command_gate_card)
    return root


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
