
# Mission 152 — Clean source ingestion for aggregation and pagination probes

**Status:** implemented; hosted verification required.
**Dependency:** Mission 151, pull request #101.
**Scope:** L-23, L-26 and L-28 registered initial POST steps, manifest
guards, existing synthetic test suites, and conformance documentation.
**Baseline:** Mission 151 head `8a7e979039d743bdbebbc2d71ae286459557de65`.

## Reproducible assurance gap

L-23, L-26 and L-28 constructed expected aggregate or pagination results
from the originally submitted three-point fixture, then verified the
corresponding stored-source readbacks. The initial POST was captured but
its response counts and conflict list were not asserted. A defective server
could report partial ingestion or contradictory rejected natural keys in
that POST, while a subsequent readback fabricated the expected records.
The later arithmetic and identity assertions would still pass without
checking the first operation's explicit result.

## Bounded correction

- Preserve each existing 3-call procedure and submitted sample fixture.
- On the initial POST, require the existing strict `telemetry_counts`
  assertion for appended=3 and replayed=0, together with the existing
  `telemetry_no_conflicts` assertion.
- Preserve L-23's source-field readback and mean recomputation, L-26's
  original-field readback and minute buckets, and L-28's two-page
  source-field and pagination-envelope verification.
- Require these assertions in the existing L-23/L-26/L-28 manifest guards
  and reject weakened or altered initial count/conflict assertions.
- Extend the existing mandatory synthetic test suites for every affected
  probe to reject malformed initial counts, booleans, fabricated or missing
  conflict lists and failed initial HTTP responses.
- No new assertion vocabulary or hosted workflow commands.

## Required verification

```sh
python Scripts/test_telemetry_mean_source_integrity.py
python Scripts/test_telemetry_window_partition.py
python Scripts/test_telemetry_pagination_slice.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Hosted static and live-reference conformance, independent runtime
verification and specification generation must pass before merge.

## Boundaries

This strengthens verification of the existing telemetry response, not the
schema itself. No official Breeding Application Programming Interface
(BrAPI) version 2.1 contracts, GenX wire schemas, scientific maturity
levels or unresolved embargo metadata policy are changed.
