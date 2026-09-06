# Worker-allocation record

Use `scripts/workflow_state.py` to record the frozen outcome contract and the worker allocation separately. The ledger records user approval; it is not a scheduler, identity provider, or substitute for Main checking actual runtime state.

## Contract

Create a compact JSON object with nonempty `outcomes` and `acceptance` lists. Keep only frozen original outcomes and protected observable acceptance here. Put editorial specification text, timestamps, test logs, and changing head SHAs elsewhere.

```sh
python3 scripts/workflow_state.py contract --state <state.json> --file <contract.json>
```

Changing this frozen contract is material and clears any current worker-allocation approval. Main should use contract changes for actual outcome/acceptance changes, not wording cleanup.

## Allocation

Create a JSON object with:

- `main`: object naming Main responsibilities. Do not encode or validate the current Main session's model/effort here; the user owns that root-session choice.
- `stages`: ordered child-worker objects with stable `id`, worker `count`, `role`, bounded `scope`, exact `model` and `effort`, dependencies/timing, and mutation authority. Include bounded repair or closeout reuse when intended.
- `authority`: overall delegated modification/commit/push/PR boundaries; absent authority is not granted.

For child stages only, any `gpt-6-astra` entry must use `low` or `medium`; the helper rejects higher Astra effort. Luna stages may use any reasoning effort supported by `gpt-5.6-luna`, selected by Main and recorded exactly in the allocation presented to the user.

```sh
python3 scripts/workflow_state.py allocation --state <state.json> --file <allocation.json>
python3 scripts/workflow_state.py show --state <state.json> --compact
# Only after presenting this allocation and receiving explicit user approval:
python3 scripts/workflow_state.py approve-allocation --state <state.json> --fingerprint <shown-hash> --note <user-approval-reference>
```

`allocation` enters `ALLOCATION_WAIT` and clears approval when the allocation fingerprint changes. Reapproval is required for worker count, role, model/effort, delegated scope, dependency structure, or mutation-authority changes.

Head movement, evidence changes, ordinary implementation choices, and steering that does not change the frozen contract or allocation do not alter the allocation fingerprint.

Use `steer` to record user steering that preserves the current contract/allocation:

```sh
python3 scripts/workflow_state.py steer --state <state.json> --note <steering-summary>
```

If steering materially changes the frozen contract or worker allocation, update those artifacts through `contract` or `allocation`; do not hide the change in a steering note.

Legacy schema v1/v2 ledgers remain readable, but their old global approval is not promoted into worker-allocation approval. Register the current contract/allocation and obtain allocation approval before new child-agent dispatch.