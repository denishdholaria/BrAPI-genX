# Mission 141 — Inference result identity and digest binding

**Status:** implemented; mandatory hosted tests pending.  
**Scope:** registered L-14, manifest and regression tests.  
**Dependency:** Mission 140. No official BrAPI 2.1 or GenX wire-schema changes.

## Confirmed false-positive risk

The existing L-14 checked only the first returned inference record's
modelDbId and inputsDigest. A job for another modelVersion, a wrong
jobDbId, a non-completed job or multiple result records could still pass.

## Correction

L-14 now verifies the original registered model identity/version, the
model/version referenced in the original inference request, the completed
jobDbId, jobType, idempotency key and terminal COMPLETED state, and
exactly one inference record matching that version. The inputsDigest must
equal SHA-256 over the canonical original inputs. The submitted request
is the independent baseline rather than the GET response.

Manifest validation protects the complete three-step model registration,
captured inference submission with terminal wait, and stored job GET. The
new `Scripts/test_inference_result_identity_digest.py` mutation suite
covers identity/version drift, wrong statuses, missing or duplicated
results, wrong input digest, missing records and mismatched responses.
It is required in hosted static conformance.

## Verification

```bash
python Scripts/test_inference_result_identity_digest.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

All hosted static/live, independent cross-runtime differential and
specification-generation checks must pass before merge.

## Evidence limits

The reference implementation returns synthetic inference echoes. This
assertion verifies conformance bookkeeping, not scientific validity,
trained-model reproducibility, external model provenance, persistent
immutability or third-party interoperability.
