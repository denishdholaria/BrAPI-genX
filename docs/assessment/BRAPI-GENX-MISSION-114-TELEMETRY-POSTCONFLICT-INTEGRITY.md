# Mission 114 — Enforce unchanged telemetry values after rejected conflict

**Date:** 2026-11-25. **Source parent:** Mission 113 review head `150e1b1633d27bcc2c4350f89e24c085a0e1c18d`. **Dependencies:** integrate Missions 112–113 in order before retargeting to `main`.

## Confirmed discrepancy between registered expectation and test execution

Registered live probe **L-22** states that submitting a different value for the same device/sensor/timestamp must produce an element-level conflict and leave the stored reading unchanged on re-GET. The actual call sequence previously had only two POSTs and asserted `appended: 0`, `replayed: 0`, and one conflict on the second response. A buggy implementation could overwrite the stored value while returning the expected conflict envelope and pass.

## Bounded correction

- Append a GET for the already supported telemetry collection, scoped to the fresh test device and `air-temp-01` sensor, without aggregation.
- Compare the original submitted three identity tuples (device, sensor, timestamp) and numeric values with the returned rows; reject different values, missing, extra, duplicated, or changed identities, non-200 status and missing data.
- Add nine mock-server unit tests to falsify accidental mutation even when the preceding conflict response looks valid, plus a static workflow guard.
- Preserve the existing L-22 identifier, proposed response contract, source specification and other probes.

## Falsifiers and evidence limitations

```sh
python Scripts/test_telemetry_conflict_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_step_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 --only L-22
```

The last command needs an independently started project-owned Python reference server. Host the full static, Python live, TypeScript differential/legacy and specification-generation checks at the exact review head before merging; verify integrated `main` separately.

**Limits:** This tests retention in the Python in-memory reference server using a random test device, not persisted production telemetry, real sensor identity, instrument calibration, durable storage, authorization, external-vendor compatibility or scientific validity. The TypeScript reference does not support telemetry. No official Breeding Application Programming Interface (BrAPI) version 2.1 or GenX wire schema, registry, Request for Comments (RFC) maturity or pending geospatial decision changes.
