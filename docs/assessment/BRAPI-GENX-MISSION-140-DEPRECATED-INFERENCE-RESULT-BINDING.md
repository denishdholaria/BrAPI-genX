# Mission 140 — Deprecated inference result binding

**Status:** implemented; mandatory hosted verification pending.  
**Scope:** registered live probe L-27 and conformance regressions.  
**Dependency:** Mission 139. No official BrAPI 2.1 or GenX wire-schema changes.

## Confirmed false-positive

L-27 previously accepted a 202 with a WARNING message and then a completed
job with the same identifier. It did not verify that the completed inference
record had the originally registered deprecated model/version or bound the
original input parameters. An unrelated inference completion could pass.

## Implementation

- Preserve the original deprecated model submission and the original
  inference request.
- Verify that the captured registered model identity and version match the
  original deprecated model, which must retain status `deprecated`.
- Verify that the accepted inference explicitly references the captured
  deprecated model and version.
- After completion, assert the accepted jobDbId, jobType, and original
  idempotencyKey; require exactly one result record.
- Check that the result model identifier/version matches the original
  deprecated model and that `inputsDigest` equals the SHA-256 digest of the
  conformance runner's canonicalized original input object.
- Retain the existing 202 and WARNING requirements and protect the complete
  two-step procedure in the manifest validator.
- Add 17 positive and mutation regressions in
  `Scripts/test_deprecated_inference_result_binding.py` and require the
  suite in hosted static conformance.

## Verification

```bash
python Scripts/test_deprecated_inference_result_binding.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required hosted static, live-reference, independent runtime differential,
and specification-generation checks must pass before merging.

## Evidence limits

The reference inference server returns synthetic echo-style outputs.
This verifies the identity and digest binding of those outputs to the
submitted request, not the scientific quality of a trained model, actual
inference reproducibility, external model provenance, or third-party
interoperability.
