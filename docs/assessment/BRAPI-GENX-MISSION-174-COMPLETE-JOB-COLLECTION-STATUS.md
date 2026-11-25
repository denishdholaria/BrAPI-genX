# Mission 174 — Complete stored-Job collection lifecycle status integrity

**Status:** implementation proposed for hosted verification.
**Dependency:** Mission 173, Pull Request #123.
**Scope:** the shared `immutable_job_snapshot` validator used by
registered L-01, L-02, L-04, L-15 and L-24; their mandatory synthetic
regressions and conformance documentation.

## Confirmed false-positive risk

The published `Job` schema requires a string `status` from six
lifecycle values. Complete jobs-collection validation previously
checked pagination, unique nonempty `jobDbId`, nonempty `jobType`,
and correctly typed optional `idempotencyKey`. Missing or invalid
`status` on an unrelated stored Job could pass if pagination,
identity and negative-effect checks were otherwise consistent.

## Bounded correction

- Require every Job row in a **complete** collection to satisfy
  `valid_job_lifecycle_status`, reusing the shared schema-aligned
  validator introduced in Mission 172.
- Keep all identity and negative-effect checks and the rule that
  idempotencyKey can be missing on unrelated records.
- Permit different valid lifecycle phases across stored Jobs.
- Add direct regressions for missing, nonstring and unsupported
  statuses on accepted and unrelated stored records.
- Align positive synthetic fixtures and negative-test otherwise-valid
  rows with the published required Job shape, retaining specificity
  of duplicate, forbidden-key and malformed-identity assertions.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_rejected_inference_no_stored_job.py
python Scripts/test_unknown_jobtype_no_stored_job.py
python Scripts/test_job_conflict_collection_unchanged.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static, live-reference, independent-runtime differential
and specification-generation workflows before merge. Post-merge
main-branch verification is separately tracked.

## Boundaries

L-25 intentionally validates a first page rather than a complete
jobs collection and is not modified here. No official BrAPI (Breeding
Application Programming Interface) v2.1 contract, GenX Job wire
schema, lifecycle transition rule, maturity decision, or embargo
policy changes.
