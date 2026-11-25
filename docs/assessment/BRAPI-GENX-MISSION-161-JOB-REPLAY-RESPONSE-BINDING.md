# Mission 161 — Bind asynchronous job replay reply to original request

**Status:** implemented; hosted checks pending.
**Dependency:** Mission 160, pull request #110.
**Scope:** registered L-01, existing job-replay step, mandatory synthetic
regression suite and conformance documentation.

## Demonstrated false-positive risk

The L-01 replay executor accepted any successful HTTP 2xx status with
the originally accepted `jobDbId`. Consequently, 201, 204 or 206 passed
although the registered probe explicitly permits only 200 or 202.
The replay response's `jobType` or `idempotencyKey` could also be
missing or changed while subsequent readback showed the original
stored job, producing another false positive.

The existing proposed `Job` schema marks `jobType` required and says
a supplied idempotency key is echoed in the Job response. This mission
enforces those already-defined response fields without changing the
allowed replay status policy.

## Bounded correction

- Require replay status 200 or 202, not arbitrary 2xx.
- Require object-shaped result with the accepted `jobDbId`, the
  original submitted `jobType` and the original nonempty
  `idempotencyKey` echoed unchanged.
- Preserve existing exact-body replay submission and final stored-jobs
  uniqueness/readback checks, including unrelated pre-existing jobs.
- Extend the mandatory `Scripts/test_job_replay_single_stored.py`
  with positive 200 and 202, negative other-success statuses, missing
  or changed type/key, malformed body, and extra server metadata.
- No new assertion vocabulary or workflow command.

## Verification

```sh
python Scripts/test_job_replay_single_stored.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static, Python live-reference and independent runtime
conformance plus specification generation before merge.

## Boundaries

No new conflict status is selected. No official Breeding Application
Programming Interface (BrAPI) version 2.1 contracts, GenX wire
schema, scientific maturity or unresolved embargo metadata policy
is changed.
