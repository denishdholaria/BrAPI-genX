# Mission 111 — Reject malformed version 2.1-only server-info fallback envelopes

**Date:** 2026-11-25. **Parent:** Mission 110 review head `c9fdfd1e6ea3f97e7a27b359abc1b8fdbea4f79c`. **Integration dependency:** complete Mission 110 before retargeting this stacked change to `main`.

## Confirmed verification weakness

Registered live probe **L-06** previously accepted an HTTP 200 response if its `result` merely contained a `calls` key. That condition also accepted `calls: null`, a scalar, an empty array, or entries without usable service/version/method descriptors. Static fallback-fixture probe **S-08** required the keys to be present but did not validate their types. Thus passing a fallback probe did not necessarily demonstrate machine-readable negotiation data.

## Bounded correction

- Share a minimal legacy response-shape validator between S-08 and L-06. Require `result.calls` to be a nonempty array of objects, each with nonblank `service` and nonempty arrays of nonblank strings for `versions` and `methods`.
- Reject malformed or missing envelopes and unexpected HTTP statuses on L-06, keeping the same registered probe IDs, endpoints, fixture and server responses.
- Add twelve regression cases covering a valid fallback, bad HTTP status, null/string/empty calls, missing service, invalid versions/methods, nonobject calls, missing result and the static fixture check.
- Execute the new test suite in hosted static conformance and guard its workflow command against silent removal.

## Falsifiers and integration gate

```sh
python Scripts/test_v21_fallback_envelope.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18083/genx/v1 --only L-06
```

The final command requires an independently started TypeScript reference server using `--profile v21`. All actual reference-server executions must pass; deliberately malformed mock responses must fail. Require hosted static, Python live, cross-runtime/legacy fallback and specification generation on the exact pull-request head before merging. Verify integrated `main` separately.

**Evidence boundary:** This validates a minimal useful fallback shape, not the complete official Breeding Application Programming Interface (BrAPI) version 2.1 schema, third-party server interoperability, authenticated authorization or deployment readiness. No official BrAPI 2.1 source, proposed GenX wire schema, endpoint registry, Request for Comments (RFC) maturity or unresolved scientific digest decision is altered.
