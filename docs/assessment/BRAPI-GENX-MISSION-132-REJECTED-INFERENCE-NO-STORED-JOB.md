# Mission 132 — Rejected inference has no observable stored job

**Status:** implemented, mandatory hosted checks pending.  
**Scope:** registered L-15, runner, manifest and regression suite.  
**Dependency:** Mission 131. No wire-schema or scientific maturity changes.

## False-positive risk

L-15 already demands HTTP 400 for inference against an unknown model and
a revoked model. But returning a rejection does not prove the server did
not store or enqueue a corresponding job.

## Change

The runner captures fresh request idempotency keys and modelDbId values
from both attempted inference submissions, before seeing any server reply.
After both expected 400 responses it calls GET /jobs, requiring:

- HTTP 200 and complete single-page pagination with strict integer counts.
  An empty collection is valid; other unrelated jobs are allowed.
- No job with either rejected idempotency key, regardless of jobType.
- No inference job referencing either denied model identity, even if a
  server changes the key before persistence.

The manifest validator requires the exact 4-step L-15 sequence, and
`rejected_inference_not_stored: true` is restricted to GET /jobs.
`Scripts/test_rejected_inference_no_stored_job.py` exercises accepted and
rejected responses, hidden jobs, changed keys, unrelated records, malformed
collection evidence and incomplete pagination. The hosted static workflow
and scope regression require the new suite.

## Verification

```bash
python Scripts/test_rejected_inference_no_stored_job.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required hosted static, Python live-reference, independent runtime, and
generation workflows are merge gates.

## Important scope limit

This proves no **visible persisted job record** for the rejected request
identities in the project-owned in-memory reference implementation. It does
not prove that no unobservable worker side effect, audit record, or other
processing occurred. Distributed durability, authorization, external
integrations and scientific validity are not assessed. The existing
model/job contracts and scientific maturity statuses remain unchanged.
