# Mission 134 — Job conflict immutable collection postcondition

**Status:** implemented, pending required hosted verification.  
**Scope:** existing L-02 registered live probe and supporting tests.  
**Dependency:** Mission 133. No official BrAPI 2.1, GenX schema or
scientific maturity changes.

## Defect

L-02 reported a passing result if the second job submission with the same
idempotency key and different body returned any rejection. A server could
have persisted an additional job with a new server-generated key or silently
rewritten the original job's immutable identity.

## Correction

L-02 now reads GET /jobs both before and after the conflicting POST,
requiring a complete collection with consistent pagination. The runner
compares a map of every jobDbId to its (jobType, idempotencyKey), ensuring:

- The initial job is present and matches the original submitted key/type.
- No job was added, removed, duplicated or had these immutable identity
  fields rewritten after the conflicting write.
- Mutable fields such as worker status and timestamps may progress without
  producing a false failure.

The runner-local `immutable_job_snapshot` helper rejects invalid collection
rows, duplicate identifiers, truncated pagination and malformed counts.
The fail-closed manifest validator now requires the four-step L-02 sequence
and both explicit collection assertions. The mandatory
`Scripts/test_job_conflict_collection_unchanged.py` regression suite
exercises before/after modifications, unrelated jobs, status progression,
incorrect rejections and incomplete evidence.

## Verification

```bash
python Scripts/test_job_conflict_collection_unchanged.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Hosted static, live-reference, independent-runtime and specification
generation checks must succeed before merging.

## Boundary

This verifies a single observable immutable collection snapshot across a
synthetic conflict test in the project's in-memory reference server.
It does not demonstrate transaction isolation from concurrent external
clients, durable storage, exactly-once side effects, audit log immutability,
or third-party conformance.
