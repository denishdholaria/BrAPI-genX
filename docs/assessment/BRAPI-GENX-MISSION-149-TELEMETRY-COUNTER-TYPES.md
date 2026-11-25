
# Mission 149 — Strict telemetry append and replay counter types

**Status:** implemented; required hosted verification pending.
**Dependency:** Mission 148.
**Scope:** existing L-21 and L-22 telemetry counter assertions, mandatory
synthetic regressions and conformance documentation.
**Baseline:** Mission 148 head `cc1abd9c9a1f2fd14fae537e4a155876520850f5`.

## Confirmed false-positive risk

The existing TelemetryBatchResult schema specifies `appended` and
`replayed` as JSON integers. The conformance runner compared their
returned values to expected counts using Python equality, under which
`False == 0` is true and `0.0 == 0` is also true.
Thus a server returning JSON booleans or floats for a zero appended or
replayed count could pass even though the wire response contradicts the
schema. No new data semantics are necessary to correct this defect.

## Bounded correction

- Require the telemetry append status be HTTP 200 when asserting counters.
- Require `result` to be an object with `appended` and `replayed`
  values of exact Python `int` type (excluding boolean), each nonnegative.
- Preserve existing expected numeric counts and original source-readback
  verification for L-21 and L-22.
- Extend the existing required suites
  `Scripts/test_telemetry_replay_postcondition.py` and
  `Scripts/test_telemetry_conflict_identity.py` with boolean, floating,
  missing, null, string, negative and rejected-status cases.
- No assertion manifest or workflow wiring changes are needed.

## Verification

```sh
python Scripts/test_telemetry_replay_postcondition.py
python Scripts/test_telemetry_conflict_identity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static, live-reference, independent runtime
conformance and specification generation before merging.

## Boundaries

The fix enforces the already-existing telemetry integer response type;
it does not change published Breeding Application Programming Interface
(BrAPI) 2.1 contracts, GenX wire schema, scientific maturity, or embargo
metadata-visibility policy.
