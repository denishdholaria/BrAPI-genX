# Mission 163 — Concurrent Job acknowledgments retain original request binding

**Status:** implemented; hosted checks pending.
**Dependency:** Mission 162, pull request #112.
**Scope:** L-24 concurrent submission executor, its existing mandatory
synthetic suite and conformance documentation.

## Confirmed false-positive risk

The L-24 test dispatches eight copies of a single request in parallel,
then checks that all responses have the same jobDbId and that exactly
one stored job exists for the submitted key. Each response could
however echo an unrelated or missing jobType/idempotencyKey without
changing jobDbId, and the postcondition readback could still be
correct. That contradictory acknowledgment was not detected.

## Bounded correction

- Validate each response's result is a dictionary with the original
  submitted jobType and idempotencyKey, in addition to an identical
  nonempty jobDbId across all eight replies.
- Preserve the registered permitted 2xx statuses, existing
  single-effect assertion and full stored jobs readback.
- Permit additional server-managed metadata on individual replies.
- Extend the existing mandatory
  `Scripts/test_concurrent_job_stored_effect.py` with cases in
  which exactly one reply changes/omits the original type or key
  or returns an array, and a positive case for extra metadata.
- Do not change the accepted concurrency or exact HTTP response
  policy. No assertion vocabulary or workflow command added.

## Required verification

```sh
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_job_replay_single_stored.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Hosted static, live-reference, independent runtime conformance and
specification generation must pass before merge.

## Boundaries

This protects the evidence supplied by each response in an existing
conformance probe. It does not prove cross-process durable job storage,
nor change official BrAPI (Breeding Application Programming Interface)
version 2.1 contracts, GenX wire schemas, scientific maturity or
unresolved embargo policy.
