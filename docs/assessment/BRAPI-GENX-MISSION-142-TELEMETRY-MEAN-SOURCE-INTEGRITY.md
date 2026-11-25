# Mission 142 — Telemetry mean source integrity

**Status:** implemented; hosted verification pending.  
**Scope:** registered L-23 and supporting conformance regressions.  
**Dependency:** Mission 141. No official BrAPI 2.1 or GenX wire-schema change.

## Confirmed false-positive

L-23 submitted three known samples and checked that the aggregate GET
returned one row with sampleCount 3 and value 21.7. The probe did not
independently read the stored points, and could therefore accept an
unchanged hardcoded mean after the original readings were rewritten.

The earlier mean assertion also did not require HTTP 200 or a consistent
aggregation response envelope.

## Correction

- POST the fresh telemetry batch and independently GET the original
  device/sensor/time-range records with aggregation=none.
- Reuse the existing `telemetry_original_intact` check to verify each
  stored (deviceDbId, sensorDbId, timestamp, value) identity.
- GET aggregation=mean for the same range, validate HTTP 200 and the
  complete one-bucket pagination shape, aggregation type, original
  anchor timestamp, numeric finite value and precise sample count.
- Recompute the arithmetic mean from the original submitted numeric
  readings (rather than trusting the manifest's literal expected value
  alone) and compare with tolerance 1e-9.
- Protect all three steps in the L-23 manifest and require
  `Scripts/test_telemetry_mean_source_integrity.py` in hosted static
  conformance. The mutation suite covers altered source records, bucket
  status, mean, sample count, type, timestamp and pagination.

## Verification commands

```bash
python Scripts/test_telemetry_mean_source_integrity.py
python Scripts/test_telemetry_replay_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required hosted static/live, independent cross-runtime differential,
and specification-generation workflows must pass before merging.

## Limits

This is a scoped arithmetic consistency test against synthetic reference
telemetry samples, not a production-grade treatment of missing data,
uncertainty propagation, sensor calibration, unit conversion, sparse
windows, persistent storage, or external interoperability.
