# Mission 175 — L-25 visible first-page Job status integrity

**Status:** implemented; hosted verification required before merge.
**Dependency:** Mission 174, Pull Request #124.
**Scope:** the L-25 jobs-collection `collection_contains_created`
assertion, existing mandatory synthetic pagination/envelope tests,
and conformance documentation.

## Confirmed false-positive risk

The published Job schema requires lifecycle `status` in its
six-value string enumeration. After Missions 172–174, initial,
replay, concurrent and **complete-collection** evidence enforce
that field. L-25's distinct **first-page-only** readback still
accepted a malformed visible Job with missing, unsupported or
nonstring `status`, provided job identities and pagination were
otherwise well-formed.

## Bounded correction

- Reuse `valid_job_lifecycle_status` for each Job on L-25's
  returned first page.
- Keep existing first-page pagination arithmetic, created-job
  binding, unique IDs and optional idempotency-key checks.
- Preserve valid multi-page collections; do not claim to validate
  unreturned records on later pages.
- Extend both mandatory L-25 synthetic test suites with negative
  missing/invalid statuses and positive mixed valid statuses.
- Align previously abbreviated synthetic positive Job records
  to the published required shape. Preserve specificity of the
  missing-created-identity regression.

## Verification

```sh
python Scripts/test_collection_pagination_arithmetic.py
python Scripts/test_collection_envelope_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation
before merge. Post-merge main-branch checks are separate.

## Boundaries

No official BrAPI (Breeding Application Programming Interface)
version 2.1 source contract, proposed GenX wire schema, Job state
transition policy, scientific maturity or embargo policy changes.
