# Mission 131 — Model conflict whole-record verification

**Status:** implemented, pending mandatory hosted checks.  
**Scope:** existing registered L-13 and conformance tests.  
**Dependency:** Mission 130 integrated on `main`.  
**Wire-schema and scientific maturity changes:** none.

## Confirmed false-positive risk

L-13 already rejects a conflicting model artifact publication with HTTP 409
and reads back the original version. The assertion previously checked only
modelDbId, modelVersion and artifactDigest. A server could silently alter the
training-data digest, model URL, framework, metrics, status or provenance
while satisfying the earlier conformance probe.

## Change

The original request is captured as a deep copy independent of the server's
response. The existing `unchanged_model_digest: true` assertion now uses
the runner-local `published_record_problem` helper and also requires the
captured model version to match the request. Every originally submitted
field must be present and identical in the GET response (including nested
metrics and provenance). Additional server-managed fields are permitted.

Manifest validation requires exactly one three-step L-13 sequence:
a captured model publication; a 409 on the conflicting model artifact; and
a GET on the original modelDbId/modelVersion with the retained-record check.
The new `Scripts/test_model_conflict_whole_record.py` suite tests
correct preservation and falsifying changes to formerly unchecked fields,
missing/malformed data and incorrect statuses. Previously registered
`Scripts/test_model_conflict_postcondition.py` remains mandatory.

## Verification

```bash
python Scripts/test_model_conflict_whole_record.py
python Scripts/test_model_conflict_postcondition.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Host-run static/live, independent cross-runtime and specification generation
workflows must all succeed before merging.

## Evidence limits

This proves observable post-conflict integrity for an in-memory reference
server, not database crash durability, transaction isolation, cryptographic
verification of remote artifact bytes, validated scientific model metrics,
external interoperability, or authorization. Official BrAPI 2.1 and GenX
wire contracts are unchanged.
