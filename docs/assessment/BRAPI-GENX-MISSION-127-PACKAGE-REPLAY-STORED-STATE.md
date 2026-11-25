# Mission 127 — FAIR package replay stored-state integrity

**Status:** implemented; hosted checks required before integration.  
**Scope:** existing registered L-18, runner refactor and regression tests.  
**Dependency:** Mission 126.  
**Scientific and wire-schema impact:** none.

## False-positive risk

L-18 previously accepted two replies carrying the same packageDbId without
observing whether the stored package was duplicated, rewritten, or lost.
That could hide altered license/access rights, tampered external evidence
digests, or changed nested provenance.

## Implementation

- Preserve a deep copy of the original submitted package, independent of
  subsequent server responses.
- After replay, query GET /fair-packages; require HTTP 200 and one **complete**
  page with consistent totalCount, pageSize, currentPage and totalPages.
- Exactly one record with the fresh package identifier must exist; unrelated
  packages may coexist.
- Verify all submitted package fields, including nested payload references
  and digests, license, access rights, identifiers, and provenance. Extra
  server-managed fields are allowed.
- Extract the collection postcondition from L-16 into the runner-local
  `replay_collection_problem` helper reused by L-18, rather than duplicating
  the same logic. The helper preserves L-16's existing behavior.
- Protect L-18's registered three-step procedure in manifest validation,
  require the assertion to be true, and run
  `Scripts/test_package_replay_stored_state.py` in hosted static conformance.

## Verification

```bash
python Scripts/test_matrix_replay_stored_state.py
python Scripts/test_package_replay_stored_state.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

All hosted static, live-reference, independent runtime, and specification
generation checks must pass before merge.

## Boundaries

The assertion is for observable state in a synthetic, in-memory reference
server and fails closed when the unfiltered collection is multipage. It
does not independently establish trustworthiness of scientific evidence,
external reference validity, database durability, crash recovery,
authorization, or third-party conformance. No official BrAPI 2.1 or GenX
wire-schema changes or scientific maturity promotions were made.
