
# Mission 151 — Verify the original append before telemetry conflict

**Status:** implemented, hosted verification pending.
**Baseline:** `main` at `628eb45194068ed2eff934b8396c88ba5c463f7e`.
**Scope:** registered live L-22, manifest guard and existing synthetic tests.

## Proven false-positive risk

The conflict probe posted a three-record telemetry batch and then submitted a
single value different from the previously used device/sensor/timestamp.
It checked the second response's rejected natural key and the readback of the
original data, but did not validate the first POST's `appended`, `replayed`
or `conflicts` result. A server could report a partly or wholly rejected
initial batch while returning the expected conflict and readback and still
pass the live probe. The earlier L-21 clean-replay checks do not establish
the result of the separate fresh batch used by L-22.

## Narrow correction

- Preserve the original L-22 three-step procedure and its original fixture.
- Require the first POST's exact `telemetry_counts` of appended=3,
  replayed=0, and `telemetry_no_conflicts` true.
- Retain the second POST's no-append/no-replay and actual rejected natural
  key checks, plus the unchanged original-field readback.
- Make the L-22 manifest guard fail closed if original acceptance evidence
  is removed, altered or replaced with a different input fixture.
- Add synthetic negative cases for partial append, noninteger and missing
  counters, fabricated or malformed conflict arrays and rejected HTTP status.
- Reuse existing mandatory workflow suites; no new assertion vocabulary.

## Required verification

```sh
python Scripts/test_telemetry_conflict_identity.py
python Scripts/test_telemetry_conflict_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static conformance, live-reference conformance,
independent runtime verification and specification generation before merge.

## Boundaries

No official Breeding Application Programming Interface (BrAPI) version 2.1
contracts, GenX wire schemas, scientific maturity levels or embargo
metadata-visibility policy are changed. The assertion proves the recorded
first-append response of L-22, not durable cross-server storage guarantees.
