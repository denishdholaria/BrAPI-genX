# Mission 120 — Telemetry replay retained-state assurance

**Scope:** existing live probe L-21; engineering conformance only.  
**Dependency:** Missions 118–119 previously merged.  
**Wire and scientific contracts:** unchanged.

## Failure mode

L-21 reports append/replay counts after two identical telemetry batch
submissions. A server could claim that all three points were replayed without
duplicates yet actually append duplicates, remove records, or alter stored
values. The prior probe did not retrieve persistent state after its replay.

## Implementation

L-21 now makes a third, uniquely device-filtered GET with
`telemetry_original_intact: true`. The existing check from L-22 compares
the three original device/sensor/timestamp natural keys and associated numeric
values, rejecting missing, duplicate, mutated, or malformed rows.

The manifest validator requires this assertion on an L-21 GET call.
The dedicated `Scripts/test_telemetry_replay_postcondition.py` suite
exercises valid replay, false replay counters, duplicate storage despite
expected counters, altered values, missing rows, timestamp reassignment,
wrong sensor, malformed records, and unavailable reads. The existing static
workflow and its workflow-scope test enforce the suite.

## Verification

```bash
python Scripts/test_telemetry_replay_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Hosted Python live conformance executes the registered L-21. Verify all
required hosted checks before integration.

## Boundaries

These are in-memory reference-server checks. They do not demonstrate durable
database transactions, crash recovery, cross-process idempotency, authorization,
complete replay conflict semantics, scientific authority, or external-vendor
certification. No official BrAPI 2.1 contract, GenX wire schema, or scientific
maturity level was changed.
