# Mission 106 — Verify retained matrix digest and package license after conflicts

**Date:** 2026-11-25. **Source parent:** Mission 105 review head `fece66583c0cf51c66d8928cab15f6b930a3346c`. This is a stacked assurance mission, integrated only after Mission 105 passes and merges.

## Confirmed verification defects

Registered L-17 and L-19 live probes claimed the originally published matrix digest and package license remained unchanged after a rejected conflicting submission. Each actual call list stopped at the `409` response. Either reference implementation could silently overwrite the record, return `409` and still pass. These are the same structural failure mode that Mission 105 corrected for model artifacts.

## Bounded correction

1. For **L-17**, save the original submitted `matrixDbId` and `fileDigest`, then GET `/variantmatrices/{matrixDbId}` after rejecting the conflict; compare HTTP status, identifier and digest to the original submission.
2. For **L-19**, save the original submitted `packageDbId` and `license`, then GET `/fair-packages/{packageDbId}` after rejecting the conflict; compare status, identifier and license.
3. Add nine mock-response regression tests including false-green `409` followed by corrupted persisted state, wrong identifiers and missing GET records.
4. Run the suite in hosted static conformance and guard the test command from silent removal.

These changes strengthen existing registered **test procedures**, not wire contracts, published APIs or the semantics of any resource.

## Falsifiers and evidence limits

```sh
python Scripts/test_publication_conflict_postconditions.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 --only L-17
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 --only L-19
```

The last two commands require a running Python reference server. The test suite must fail if server output is `409` but the stored digest/license is altered. Require hosted static, live, differential and schema-generation verification on exact pull-request head, then recheck integrated `main`.

**Non-claims:** Correct metadata postconditions are not proof of actual file-byte integrity, enforceable package license authority, durable storage, multi-tenant authorization, third-party conformance or scientific validity. No official Breeding Application Programming Interface (BrAPI) version 2.1 or proposed GenX wire schema, endpoint registry, Request for Comments (RFC) maturity or unresolved spatial decision changes.
