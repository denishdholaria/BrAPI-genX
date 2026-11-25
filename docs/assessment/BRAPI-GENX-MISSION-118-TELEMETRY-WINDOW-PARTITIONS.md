# Mission 118 — Telemetry window partition postconditions

**Status:** implemented; hosted verification required before integration.  
**Scope:** registered live probe L-26 and its supporting regression/manifest checks.  
**Scientific and wire-contract impact:** none.

## Gap and failure mode

The registered L-26 procedure says three one-minute-spaced telemetry readings
must form three separate 60-second mean buckets, each with one sample.
Previously, its only executable assertion checked `result.data` length = 3.
A server returning three bucket objects with incorrectly distributed samples,
altered means, or shifted/duplicated window starts could report PASS.

## Change

- L-26 now includes `telemetry_window_partitions: true` alongside its
  existing `data_length: 3` assertion.
- The runner checks HTTP 200, a structured three-row response, unique
  `windowStart` values matching the submitted test batch's timestamps,
  `aggregation: mean`, integer `sampleCount: 1`, and finite numeric
  `value` equal to each corresponding submitted reading within 1e-9.
  Bucket response order is deliberately irrelevant.
- The manifest validator rejects an absent, disabled, or misspelled
  L-26 partition assertion, preventing future accidental weakening.
- `Scripts/test_telemetry_window_partition.py` exercises the positive and
  negative response mutations, including count redistribution with three rows,
  wrong values, shifted/duplicate starts, malformed buckets, missing count,
  invalid aggregation and unsuccessful reads.
- Hosted static conformance executes the mutation suite, and the workflow-scope
  test requires the regression command to remain in that workflow.

## Verification

Locally runnable commands:

```bash
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_telemetry_window_partition.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

The hosted `GenX conformance (static and live)` workflow additionally
executes L-26 against the Python in-memory reference server. Report concrete
workflow conclusions on the pull request before merging.

## Boundaries

This is a fixture-specific, reference-server conformance check. It does not
establish full time-zone and daylight-saving boundary semantics, arbitrary
window alignment, variable-frequency sampling, missing-data policy,
distributed ordering guarantees, long-term persistence, external-vendor
interoperability, or scientific validation. Official BrAPI 2.1 definitions,
proposed GenX schemas, and maturity decisions are unchanged.
