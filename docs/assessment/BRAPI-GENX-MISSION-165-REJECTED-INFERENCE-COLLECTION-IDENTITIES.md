# Mission 165 — Complete job identity evidence for rejected inference

**Status:** implemented, hosted verification pending.
**Dependency:** Mission 164, pull request #114.
**Scope:** registered L-15 rejected unknown and revoked model inference,
its mandatory synthetic regression suite and conformance documentation.

## Confirmed false-positive risk

The L-15 test confirms both requests fail with HTTP 400 and checks the
complete jobs collection for their rejected keys and model identifiers.
It previously accepted unrelated job rows with missing, blank or
duplicated jobDbIds, missing job types, or nonstring idempotency keys.
A malformed collection is not reliable evidence of absence.

## Bounded correction

- Reuse the existing `immutable_job_snapshot` helper to validate
  status 200, complete first-page pagination and unique well-formed
  job identities for the entire returned collection.
- Retain checks for both rejected idempotency keys and submitted unknown
  or revoked modelDbIds against all validated rows.
- Continue permitting legitimate unrelated jobs and optional absent
  idempotency keys.
- Extend the already-mandatory
  `Scripts/test_rejected_inference_no_stored_job.py` with negative
  unrelated-row duplication, missing identity/type and nonstring
  key cases, and positive unrelated-row cases.
- Preserve original four-call procedure, HTTP 400 expectations and
  existing specification maturity.

## Required verification

```sh
python Scripts/test_rejected_inference_no_stored_job.py
python Scripts/test_unknown_jobtype_no_stored_job.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static, live-reference, independent-runtime
conformance and specification generation before merging.

## Boundaries

This strengthens existing negative evidence, not job durability
or governance maturity. No official BrAPI (Breeding Application
Programming Interface) v2.1 contracts, GenX wire schemas or
unresolved embargo metadata-visibility policy changes.
