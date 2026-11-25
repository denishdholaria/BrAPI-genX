# Mission 143 — Preserve original telemetry metadata and provenance

**Status:** implemented, required hosted checks pending.  
**Scope:** existing registered L-21, L-22 and L-23 assertions and their
already mandatory conformance regression suites.  
**Dependency:** Mission 142. No GenX schema or official BrAPI 2.1 change.

## Confirmed false-positive risk

The prior `telemetry_original_intact` assertion compared only the natural
key (deviceDbId, sensorDbId, timestamp) and the numeric value. A replay or
rejected conflicting update could silently alter the original unit,
quality indicator, provenance algorithm/actor or other submitted fields
while still passing. These fields matter scientifically even if the
reading's numeric value is unchanged.

## Correction

- Preserve the full originally submitted telemetry point dictionaries.
- Verify all expected natural keys are present once, with no extras or
  duplicates.
- Require every originally submitted field to remain present and
  equal in its stored readback, including nested provenance content.
- Continue allowing additional server-managed fields not present in the
  submission.
- Add negative mutation tests for units, quality, nested provenance and
  missing fields to the existing replay, conflict and mean-source suites.
  Also test that unrelated server-managed metadata remains allowed.

No registered probe steps or assertion vocabulary change. Existing
manifest guards and static workflow commands already require the affected
suites, so no redundant workflow edits are introduced.

## Verification

```bash
python Scripts/test_telemetry_replay_postcondition.py
python Scripts/test_telemetry_conflict_postcondition.py
python Scripts/test_telemetry_mean_source_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Full hosted static, Python live-reference, independent-runtime differential
and specification-generation workflows remain merge gates.

## Evidence boundaries

This is an observable original-field retention check against synthetic
reference-server records, not an independent verification of sensor
calibration, unit correctness, upstream provenance authenticity, database
durability or external interoperability.
