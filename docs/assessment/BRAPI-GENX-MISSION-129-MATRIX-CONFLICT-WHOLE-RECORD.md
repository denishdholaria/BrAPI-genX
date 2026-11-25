# Mission 129 — Matrix conflict whole-record postcondition

**Status:** implemented, pending hosted verification.  
**Scope:** existing L-17 probe and engineering assurance only.  
**Dependency:** Mission 128. No official BrAPI 2.1 or proposed GenX wire-schema change.

## Gap

L-17 already rejected a conflicting publication with HTTP 409 and read back
the published matrix. Its assertion compared only matrixDbId and fileDigest.
A server could alter the fileURL, index digest, indexURL, variant statistics,
access service or nested provenance without invalidating the existing probe.

## Correction

The original matrix submission is saved independently of the response.
On GET /variantmatrices/{matrixDbId} after the 409, the existing
`unchanged_matrix_digest: true` assertion now verifies **every originally
submitted field**, not just the file digest. Additional server-managed fields
may be present.

The new localized `published_record_problem` helper rejects invalid HTTP
status, missing or malformed record, identity mismatch and any changed or
missing original field. Manifest validation requires L-17 to retain the
capture → conflict rejection → GET sequence. The
`Scripts/test_matrix_conflict_whole_record.py` mutation suite tests the
formerly unobserved fields, nested provenance, absent records, and incorrect
conflict responses, while existing publication-conflict regressions stay
registered.

## Verification

```bash
python Scripts/test_matrix_conflict_whole_record.py
python Scripts/test_publication_conflict_postconditions.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

All required hosted conformance and specification-generation checks must
pass before merging.

## Boundary

This verifies observable readback from the project-owned in-memory
reference server. It is not a guarantee of database durability,
distributed transaction isolation, external provenance authority,
scientific validity, or third-party interoperability. No scientific
maturity promotions are made.
