# Mission 182 — Empty jobs collection positive pageSize integrity

**Status:** implemented; hosted checks required before integration.
**Dependency:** Mission 181, Pull Request #131.
**Scope:** the shared complete-jobs-collection snapshot and its
mandatory negative-effect tests; no wire contract changes.

## Confirmed false-positive

`immutable_job_snapshot` requires integer pagination counts,
`totalCount == len(rows)`, one complete page, and
`pageSize >= len(rows)`. For an empty collection, a server could
return `pageSize: 0` with `totalCount: 0` and otherwise correct
metadata and pass the probe. L-25 and other pagination assertions
already reject zero page size; an empty page still needs a
positive page size.

## Bounded correction

- Add an explicit `pageSize >= 1` condition to the shared
  complete jobs collection validator.
- Keep empty collections valid with `totalCount: 0`,
  `totalPages: 1`, `currentPage: 0`, a positive page size,
  and zero returned rows.
- Retain every existing single-effect, rejection, original
  request, record identity and lifecycle assertion.
- Extend L-04 and L-15 mandatory regression suites with
  empty-collection zero-page-size rejection and positive-size
  acceptance controls.

## Verification

```sh
python Scripts/test_unknown_jobtype_no_stored_job.py
python Scripts/test_rejected_inference_no_stored_job.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation
must succeed before merge.

## Boundaries

No official BrAPI (Breeding Application Programming Interface)
version 2.1 or GenX wire schema changes; no scientific maturity,
job lifecycle, timestamp, embargo or pagination-policy novelty.
