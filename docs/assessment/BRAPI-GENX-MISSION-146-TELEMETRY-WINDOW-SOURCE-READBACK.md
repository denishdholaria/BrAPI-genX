
# Mission 146 — Telemetry window source-readback assurance

**Status:** implemented; hosted checks required before merge.
**Scope:** registered L-26, manifest guard, existing negative regression test and documentation.
**Dependency:** Mission 145 (pagination traversal).

## Confirmed gap

The L-26 registered procedure posted three one-minute-apart readings and
verified three separate mean buckets against the originally submitted values.
It never independently retrieved the original unaggregated records. A server
could manufacture the correct aggregate result from the submitted request
without storing, or while mutating, the source records.

L-23 independently checks its source before an overall mean, but that does
not establish L-26's particular one-minute partition source postcondition.

## Bounded correction

- Preserve the existing registered three-point POST and its original captured
  body.
- Require an intermediate HTTP 200 unaggregated telemetry GET, constrained
  to the captured device and original sensor, with
  `telemetry_original_intact: true`.
- Verify all three exact natural keys and every submitted field including
  units, quality and nested provenance before checking the windowed means.
- Preserve the original per-minute sample count, bucket timestamp, numeric
  value and aggregation assertions.
- Guard the complete three-step sequence with exact routes, fixtures, and
  assertions in `validate_probe_manifest`.
- Extend already mandatory synthetic tests to reject missing, altered,
  duplicate or incomplete source records. No new workflow command needed.

## Verification

```sh
python Scripts/test_telemetry_window_partition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Require hosted static and live-reference conformance, independent-runtime
verification and specification generation to pass before merging. Hosted
workflow results are the authoritative evidence.

## Boundaries

No official Breeding Application Programming Interface (BrAPI) version 2.1
contract, GenX schema, scientific maturity level or embargo metadata
policy is changed. This probes the persistence evidence exposed through
the reference server; it does not prove database crash recovery, source-device
authenticity or distributed atomicity.
