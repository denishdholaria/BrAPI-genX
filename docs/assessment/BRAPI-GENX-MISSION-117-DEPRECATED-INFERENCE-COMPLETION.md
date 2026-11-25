# Mission 117 — Verify deprecated inference completion after warning

**Date:** 2026-11-25. **Parent:** Mission 116 review head `cc3f54ed29203e0d1f529db852023685b35584a7`. **Dependency:** integrate Mission 116 before retargeting.

## Confirmed verification gap

Registered live probe **L-27** states that inference using a deprecated model must be accepted with a warning, *and the job completes*. Its existing executable steps registered a deprecated model and submitted inference, checking only HTTP 202 and a `WARNING` metadata message. A server could accept the request and immediately fail the job while still passing the probe.

## Bounded correction

- Preserve the existing deprecated-model registration and inference POST calls, together with the original HTTP status and warning assertions.
- Introduce a `deprecated_inference_completed: true` assertion on the inference acceptance step. After validating the original response, poll the accepted `jobDbId` using the established `wait_terminal` helper and require the **same job** to reach `COMPLETED`.
- Add ten mock-server regressions covering a successful completed job, running/failed/expired terminal results, missing/wrong job identity, missing warning and inappropriate acceptance status.
- Execute the new tests in hosted static conformance, protected by workflow-scope regression testing. No new wire operation, registered probe ID or reference-server behavior is required.

## Falsifiers and boundaries

```sh
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py --server http://127.0.0.1:18080/genx/v1 --only L-27
```

The live command requires the project-owned Python reference server running separately. Require full hosted static, live-reference, TypeScript differential/legacy fallback and specification generation on exact pull-request head before merge. Recheck integrated `main`.

**Evidence boundary:** Completing an in-memory echo inference is not independent scientific model accuracy, durable job persistence, authorization, external-vendor conformance or production readiness. No official Breeding Application Programming Interface (BrAPI) version 2.1 source, GenX wire schema, endpoint registry, Request for Comments (RFC) maturity or geospatial decision changes.
