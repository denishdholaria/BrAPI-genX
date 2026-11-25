# Mission 133 — Job replay single stored-effect verification

**Status:** implemented; mandatory hosted checks pending.  
**Scope:** existing registered probe L-01 and engineering assurance.  
**Dependency:** Mission 132. No official BrAPI 2.1 or GenX schema changes.

## Gap

L-01 required two identical job submissions to return the same jobDbId.
A server could return that identity both times and nevertheless store an
additional job with the same idempotency key or a duplicate jobDbId.

## Postcondition

After the replay, L-01 performs GET /jobs and checks:

- HTTP 200 with a complete, single-page, integer-consistent collection.
- Exactly one stored record bearing the originally submitted idempotency
  key, and exactly one record bearing the returned jobDbId.
- Both matches refer to the same stored row and preserve the original
  jobType. Unrelated jobs may coexist.

The runner uses the original captured request rather than untrusted replay
responses as the comparison baseline. The existing same_jobDbId assertion
remains mandatory. The manifest validator requires the complete three-step
L-01 procedure and the new `job_replay_single_stored` GET assertion.
`Scripts/test_job_replay_single_stored.py` supplies positive and mutation
tests for duplicate, missing, changed, malformed and incomplete records.
The static workflow and scope guard require this suite.

## Verification

```bash
python Scripts/test_job_replay_single_stored.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Hosted static/live/cross-runtime conformance and specification generation
must pass before merge.

## Limits

This checks observable in-memory stored job identity for one fresh key,
not durable exactly-once execution, external side effects, crash recovery,
multi-node races, authorization, or third-party interoperability.
