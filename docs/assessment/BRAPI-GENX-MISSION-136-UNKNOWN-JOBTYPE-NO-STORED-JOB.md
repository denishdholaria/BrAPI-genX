# Mission 136 — Unknown jobType rejected with no stored job

**Status:** implemented, required hosted checks pending.  
**Scope:** existing registered L-04, manifest and regression tests.  
**Dependency:** Mission 135; no official BrAPI 2.1 or GenX schema changes.

## False-positive risk

Registered L-04 verified that an unadvertised jobType was rejected with
HTTP 400, but the conformance runner did not verify that no job was
stored despite the rejection.

## Postcondition

After attempting a fresh submission with
`jobType: this-door-does-not-exist`, L-04 performs GET /jobs.
The runner uses the **original submitted** key and job type as baseline and
requires:

- HTTP 200 with a complete, consistently paginated jobs collection,
  including valid empty-collection behavior.
- No record bearing the rejected idempotency key, even under a different
  jobType.
- No record bearing the unknown jobType, even under a server-generated key.

The manifest validator requires the two-step L-04 sequence, and restricts
`unknown_job_type_not_stored: true` to GET /jobs. The
`Scripts/test_unknown_jobtype_no_stored_job.py` suite tests allowed
unrelated jobs, empty results, falsifying stored records, malformed and
incomplete pagination, and incorrect rejection responses. Hosted static
conformance and its workflow-scope guard require the regression command.

## Verification

```bash
python Scripts/test_unknown_jobtype_no_stored_job.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Static, live-reference, independent-runtime and specification-generation
hosted workflows are required merge gates.

## Boundaries

This proves observable absence of stored jobs in the project-owned
in-memory reference server. It does not prove no invisible side effects,
distributed persistence, transaction safety, or external conformance.
