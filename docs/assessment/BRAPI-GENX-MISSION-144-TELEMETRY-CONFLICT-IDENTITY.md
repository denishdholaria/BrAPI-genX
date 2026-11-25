# Mission 144 — Telemetry conflict natural-key identity

**Status:** implemented; required hosted verification pending.  
**Scope:** registered L-22, runner, manifest guards and regression tests.  
**Dependency:** Mission 143. No official BrAPI 2.1 or GenX wire-schema change.

## Confirmed false-positive risk

L-22 required a `conflicts` array of length one but did not verify which
element was named. A server could return an arbitrary unrelated conflict
string while rejecting or mishandling the actual input point and still
pass. The relevant GenX telemetry OpenAPI describes conflicts as strings
that name rejected natural keys, with an example of the expected
device/sensor/timestamp format.

## Correction

- Preserve the originally submitted conflicting telemetry point before
  seeing the response.
- Confirm that the point's deviceDbId, sensorDbId, timestamp correspond to
  exactly one original stored reading, with a different submitted value.
- Require HTTP 200 and exactly the string
  `{deviceDbId}/{sensorDbId}/{timestamp}` in the conflict list.
- Preserve the existing zero appended/replayed counters and full original
  field/metadata readback from Mission 143.
- Protect the L-22 register → rejected conflicting element → GET source
  sequence in the fail-closed manifest validator.
- Repair the older synthetic regression's fabricated conflict string to
  the actual submitted key and add
  `Scripts/test_telemetry_conflict_identity.py` with cases for wrong
  device/sensor/timestamp, arbitrary strings, malformed arrays, wrong
  counters, altered source fields and wrong HTTP status.
- Require the new suite in hosted static conformance and its scope guard.

## Verification

```bash
python Scripts/test_telemetry_conflict_identity.py
python Scripts/test_telemetry_conflict_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

All hosted static, live-reference, independent cross-runtime and generation
workflows must pass before merge.

## Boundaries

This verifies an exact natural-key conflict declaration and retained source
fields in the synthetic reference server. It does not establish distributed
transaction isolation, database recovery, sensor provenance authenticity,
scientific calibration or third-party interoperability.
