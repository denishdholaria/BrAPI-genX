
# Mission 150 — Clean telemetry append/replay conflict integrity

**Status:** implemented; required hosted verification pending.
**Dependency:** Mission 149.
**Scope:** L-21 and the existing live-conformance assertion vocabulary,
manifest guard, synthetic regressions and documentation.

## Confirmed false-positive risk

L-21 verified the first successful append counters (appended=3, replayed=0)
and identical retry counters (appended=0, replayed=3), and re-read the exact
three originally stored telemetry records. It did not check the `conflicts`
arrays in those two responses. A server could report an arbitrary rejected
natural key while reporting all three elements appended/replayed, and still
pass. The existing TelemetryBatchResult contract states that conflicts
identify rejected elements, which is inconsistent with that success case.

## Bounded correction

- Add `telemetry_no_conflicts` as a validated, executable boolean live
  assertion; require HTTP 200 and an exact empty `conflicts` list.
- Register the assertion on both L-21 POST operations and guard the original
  batch fixture, captured source, expected counters and clean conflict
  assertion from silent manifest weakening.
- Extend the already mandatory `Scripts/test_telemetry_replay_postcondition.py`
  and `Scripts/test_conformance_assertion_manifest.py` suites to detect
  fabricated rejected keys, malformed conflict fields, false assertions,
  swapped fixtures and incorrect original counters.
- Leave L-22's true conflicting-natural-key test unchanged.
- No hosted workflow command, wire schema or official standard change.

## Verification

```sh
python Scripts/test_telemetry_replay_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Merge only with successful hosted static, Python live-reference and
independent runtime conformance plus specification generation.

## Boundaries

The new assertion applies to the reference clean append and identical replay,
not to batches containing genuinely conflicting elements. No official
Breeding Application Programming Interface (BrAPI) version 2.1 contract,
GenX wire schema, scientific maturity or embargo metadata visibility
policy is changed.
