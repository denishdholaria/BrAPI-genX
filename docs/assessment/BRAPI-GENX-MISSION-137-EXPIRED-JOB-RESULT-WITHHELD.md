# Mission 137 — Expired job result withholding

**Status:** implemented, mandatory hosted tests pending.  
**Scope:** existing registered L-05 and synthetic mutation tests.  
**Dependency:** Mission 136. No official BrAPI 2.1 or GenX wire-schema changes.

## False-positive risk

The previous L-05 checked only `result.status: EXPIRED`. An implementation
could report EXPIRED and simultaneously return the expired job's actual
result data, violating the test's stated expectation to refuse retrieval.

## Corrected postcondition

The registered L-05 check now requires:
- HTTP 200 and a structured job record.
- A `jobDbId` matching the requested known-expired job.
- The terminal status EXPIRED.
- No job `result` field, or an explicit null result. A non-null result
  value fails, including an empty array, empty object or scalar.

The runner executes the `expired_result_withheld` assertion after the
existing status check. Manifest validation protects the known-expired
GET and both assertions. The
`Scripts/test_expired_job_result_withheld.py` mutation suite tests result
leaks, wrong job/status, unavailable and malformed records. The static
workflow and workflow-scope guard require this suite.

## Verification

```bash
python Scripts/test_expired_job_result_withheld.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

### Critical live-coverage distinction

The live conformance runner requires a real expired-job identifier passed
through `--expired-job`. Without one, L-05 is marked SKIP. Success of a
live-reference workflow **without** that fixture does not prove L-05 ran.
The hosted static regression suite exercises the assertion with synthetic
responses; it does not establish real expiry behavior or durable deletion.

## Scope limits

This checks the reference response envelope for absence of an expired
job's result data. It does not certify data erasure in storage, caches,
backups, audit logs or external systems, nor third-party interoperability.
