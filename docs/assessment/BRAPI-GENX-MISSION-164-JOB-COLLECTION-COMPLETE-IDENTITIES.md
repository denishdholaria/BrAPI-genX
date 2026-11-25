# Mission 164 — Complete identity validation in replay and concurrency readbacks

**Status:** implemented; hosted checks pending.
**Dependency:** Mission 163, pull request #113.
**Scope:** existing L-01 and L-24 stored-job readback assertions, synthetic
regression suites, and conformance documentation.

## Confirmed false-positive risk

L-01 and L-24 checked the original idempotency key and expected job
identifier in the complete stored-jobs collection, but they did not
validate the identity structure or uniqueness of every unrelated
collection row. Duplicate unrelated jobDbIds, missing jobType and
non-string idempotency keys could therefore pass while the expected
job itself remained intact.

A shared complete-collection validator, `immutable_job_snapshot`,
already establishes those guarantees for other job probes. Reuse it
rather than maintaining slightly different, less strict copies.

## Bounded correction

- Replace duplicated pagination and collection parsing in
  `job_replay_single_stored` and `concurrent_single_stored_job`
  with the existing `immutable_job_snapshot` validator.
- Require a complete status-200 first-page collection, unique nonempty
  `jobDbId` values, valid job types and correctly typed optional keys
  for all rows.
- Preserve exactly one original job for the submitted type/key/id
  and continue allowing legitimate unrelated jobs with optional
  idempotency keys absent.
- Add negative regression cases for duplicate unrelated ids,
  missing unrelated job types, blank ids and boolean keys, plus
  a positive missing optional-key case, to the already-mandatory
  L-01 and L-24 suites.
- Preserve all registered call sequences, prior replay/concurrent
  response checks, and workflow commands.

## Required verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_unknown_jobtype_no_stored_job.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static, live-reference, independent-runtime and
specification generation checks before merge.

## Boundaries

This strengthens the validity of collection evidence. It does not
establish cross-process job durability or modify official BrAPI
(Breeding Application Programming Interface) version 2.1 contracts,
GenX wire schemas, scientific maturity or unresolved embargo policy.
