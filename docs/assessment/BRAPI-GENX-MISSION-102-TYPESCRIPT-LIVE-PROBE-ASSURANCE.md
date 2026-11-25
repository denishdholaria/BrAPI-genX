# Mission 102 — Exercise independent TypeScript inference and concurrency live probes

**Date:** 2026-11-25. **Starting `main`:** `7ba05f984c9fc9337c768271fa887e79a6fdf5b6` (Mission 101). **Nature:** hosted conformance expansion using existing probes; no new contract semantics.

## Evidence gap

Missions 100–101 integrated an automated nine-request comparison of immediate responses from separately written Python and TypeScript in-memory reference servers, with fail-closed status expectations. The differential sequence submits an inference job but does **not** follow its eventual result or independently verify the output digest. Historic TypeScript probe evidence is not a successful current-run guarantee.

Existing registered live probe L-14 explicitly registers a model, submits inference, waits until the result is terminal, and verifies the computed `inputsDigest` against independently recomputed canonical input bytes. L-24 exercises eight concurrent submits for the same idempotency key and expects one created job. Both have been recorded previously as applicable to the TypeScript server, but are not currently run against it in hosted continuous integration.

## Bounded change

- Run `checkGenXConformance.py --only L-14` and `--only L-24` against the already launched TypeScript/Bun reference server in the cross-runtime job, after its existing differential comparison.
- Preserve the existing probe manifest and one-probe-at-a-time runner semantics. These jobs must fail if an existing probe fails, skips inappropriately, or the server is unavailable.
- Extend the workflow-scope guard and negative tests so that either command cannot be removed or moved into failure-only diagnostics unnoticed.
- Document precisely what these probes verify. Do not count them as two new probe definitions or evidence of external-vendor interoperability.

## Verification and boundaries

```sh
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED --only L-14
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED --only L-24
```

The two latter commands require a running TypeScript reference server and the pinned Python conformance dependencies. Require all hosted static, Python live, TypeScript differential/live-probe and schema-generation checks at the exact pull-request head before merging, followed by integrated `main` verification.

**Limitations:** L-14 validates the project-owned echo-stub inference result, not model scientific validity. L-24 validates in-process idempotency concurrency, not distributed persistence or durable recovery. No released Breeding Application Programming Interface (BrAPI) 2.1 source contract, GenX wire schema, endpoint identity, registry, Request for Comments (RFC) maturity or pending spatial governance decision changes.
