# Mission 121 — Concurrent job stored-effect assurance

**Status:** implementation submitted for hosted verification.  
**Scope:** existing registered live probe L-24 and its regression checks.  
**Dependency:** Mission 120 integrated into `main`.  
**Scientific and wire-schema impact:** none.

## Failure mode

The L-24 promise is that eight concurrent, identical job submissions result
in one effect. Previously its executable check compared only the jobDbId
returned by each POST. An implementation could report the same identifier
to all callers while storing an additional job under the same idempotency key.

## Verification design

L-24 retains eight concurrent identical POST calls and now follows them with
GET /jobs, requiring `concurrent_single_stored_job: true`. The runner saves
the originally submitted job type and idempotency key along with the unanimous
response identifier. Readback then requires:

- HTTP 200 and a well-formed jobs collection.
- An untruncated first/only page with complete pagination metadata.
- Exactly one job bearing the submitted idempotency key and exactly one row
  for the returned identifier, representing the **same** record.
- The stored jobType matches the original submission.

Unrelated records are allowed. The runner rejects missing/malformed records,
duplicate key/identifier, identity mismatch, and insufficient pagination
evidence. A manifest guard rejects weakening L-24's eight-way submission or
removing/moving its readback check. The dedicated
`Scripts/test_concurrent_job_stored_effect.py` mutation suite is required
by the existing static conformance workflow.

## Verification

```bash
python Scripts/test_concurrent_job_stored_effect.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Hosted static, live-reference, cross-runtime differential, and generated
specification checks are merge gates; their results must be reviewed before
integration.

## Explicit limits

This confirms a single **observable** in-memory job record for the test
idempotency key and current collection behavior. It does not prove
exactly-once execution of arbitrary side effects, database durability,
crash/restart recovery, distributed race safety, security/authorization,
complete paginated enumeration of large collections, or compatibility with
third-party implementations. The proposed GenX contracts and official
BrAPI 2.1 schemas are unchanged.
