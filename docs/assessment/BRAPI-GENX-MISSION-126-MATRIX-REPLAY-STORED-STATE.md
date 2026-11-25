# Mission 126 — Variant-matrix replay stored-state integrity

**Status:** implemented; hosted verification required.  
**Scope:** registered live probe L-16 and engineering-assurance tests.  
**Scientific and wire-contract impact:** none.

## Confirmed false-positive

L-16 submitted the same variant-matrix reference twice and compared the
returned matrixDbId values. That does not prove that a second stored record
was not appended, nor that the original file, index or provenance attributes
remain unchanged.

## Postcondition

After the duplicate submission, L-16 performs GET `/variantmatrices`.
The runner preserves a deep copy of the original request independent of
server-returned values. It verifies:

- HTTP 200, a structured data array, and complete single-page pagination:
  totalCount equals the number of rows, totalPages is one, currentPage is
  zero and pageSize is sufficient. Truncated evidence fails closed.
- Exactly one record with the fresh matrixDbId exists, while unrelated
  previously published matrices are allowed.
- Every originally submitted field is present and unchanged, including
  variantSetDbId, fileURL, fileDigest, indexDigest, sample/variant counts,
  accessService and nested provenance. Additional server-managed fields
  are permitted.

The manifest validator requires the two submission steps and the subsequent
`matrix_replay_single_record` assertion on GET /variantmatrices. The
`Scripts/test_matrix_replay_stored_state.py` mutation suite checks correct
and incorrect replay and stored-state responses. Static conformance and the
workflow-scope test require the regression command.

## Verification

```bash
python Scripts/test_matrix_replay_stored_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required hosted static, live-reference, independent runtime, and generation
checks must pass before integration.

## Limitations

This is an observable assertion for a synthetic matrix on the project's
in-memory reference server. The unfiltered collection approach fails closed
for multi-page collections and does not certify pagination across a large
registry, persistent uniqueness, distributed races, crash recovery,
scientific correctness, access-control policy, or independent third-party
interoperability. Official BrAPI 2.1 and proposed GenX wire schemas are
unchanged; no maturity promotion is claimed.
