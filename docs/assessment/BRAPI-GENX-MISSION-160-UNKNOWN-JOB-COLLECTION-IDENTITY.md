# Mission 160 — Complete job identity evidence for unknown job-type rejection

**Status:** implemented; hosted verification pending.
**Dependency:** Mission 159, pull request #109.
**Scope:** registered L-04, existing collection validator, mandatory
negative regression suite and conformance documentation.

## Confirmed false-positive risk

L-04 verifies that a rejected unknown job type did not create a stored
job. Its earlier collection-readback check enforced complete first-page
pagination arithmetic and absence of the rejected job type and key, but
did not require valid, unique identifiers for other jobs. A response
with duplicated unrelated jobDbIds, blank identifiers or absent job types
could still pass, despite being unreliable collection evidence.

## Bounded correction

- Reuse the proven `immutable_job_snapshot` validator from the L-02
  conflict test to check HTTP 200, a complete unpaged jobs collection,
  integer pagination metadata, valid job identifiers and job types,
  optional correctly typed idempotency keys, and unique jobDbIds.
- Check the rejected job type and idempotency key against every validated
  row in the resulting snapshot.
- Permit legitimate unrelated jobs and optional absent idempotency keys,
  avoiding an assumption that the entire collection is empty.
- Extend the already-mandatory
  `Scripts/test_unknown_jobtype_no_stored_job.py` regression suite
  with duplicate/missing/blank unrelated job identity mutations, invalid
  keys and positive multi-job and optional-key cases.
- Preserve the original POST HTTP 400, two-call L-04 manifest and
  existing workflow commands. No new assertion or wire schema.

## Required verification

```sh
python Scripts/test_unknown_jobtype_no_stored_job.py
python Scripts/test_job_conflict_collection_unchanged.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require successful hosted static, live-reference and independent-runtime
conformance, plus specification generation before merge.

## Boundaries

This improves trustworthiness of the existing negative collection
assertion, not global consistency or cross-process storage durability.
No official Breeding Application Programming Interface (BrAPI)
version 2.1 contracts, GenX wire schemas, scientific maturity or
unresolved embargo metadata-visibility policy change.
