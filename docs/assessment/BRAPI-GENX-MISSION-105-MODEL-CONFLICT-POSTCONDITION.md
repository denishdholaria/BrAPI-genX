# Mission 105 — Check retained model-artifact identity after rejected version conflict

**Date:** 2026-11-25. **Parent:** Mission 104 review head `b48a39a5daace31f4d039fef48b1385c39d0f5b0`. **Stacked dependency:** integrate Mission 103, then Mission 104, before retargeting this mission to verified `main`.

## Verified conformance gap

Registered live probe **L-13** already promises rejection of a changed artifact under the same `modelDbId` and `modelVersion`, with the original artifact remaining unchanged. Its actual calls previously stopped after the second `POST /models` returned `409`. A server could mutate the stored digest while returning `409`, and the probe would still report success. Mission 104 added the existing L-13 to the TypeScript hosted suite, making this missing postcondition particularly relevant.

## Bounded repair

- Capture the original submitted `modelDbId`, `modelVersion` and `artifactDigest` as an immutable expected baseline.
- Extend the registered L-13 probe with a version-specific `GET /models/{modelDbId}?version={modelVersion}` after the rejected conflict.
- Verify the GET returns HTTP 200 and that the three baseline fields are unchanged. Missing/changed model, wrong version, missing/changed digest, or unavailable record must fail.
- Add seven mock-server tests (including mutation of digest while returning the expected rejection), run them in hosted static conformance and protect their invocation via the workflow-scope checker.
- Keep the existing published route, data contract and reference-server implementations unchanged. The check uses the already supported GET endpoint.

## Falsifiers and limits

```sh
python Scripts/test_model_conflict_postcondition.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 --only L-13
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --only L-13
```

The last two commands require separately started project-owned reference servers. Hosted Python full live and TypeScript L-13 checks must pass with the added GET postcondition. Require static, live, differential and generation workflows on exact head before integration; inspect `main` post-merge.

**Evidence boundary:** This improves an observable in-memory conflict invariant. It does not prove durable storage, multi-process concurrency, external-vendor conformance, scientific model validity or authorization. No official Breeding Application Programming Interface (BrAPI) version 2.1 or proposed GenX schema, endpoint registry, Request for Comments (RFC) maturity or unratified spatial-governance decision is changed.
