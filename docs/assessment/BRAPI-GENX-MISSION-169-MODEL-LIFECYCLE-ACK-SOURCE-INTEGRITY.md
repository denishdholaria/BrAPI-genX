# Mission 169 — Initial lifecycle-model registration response fidelity

**Status:** implemented; hosted verification required before merge.
**Baseline:** `9a470cd4a5525bc16d57ca4cfabe021ff2eb6be4`.
**Scope:** registered L-15 revoked-model and L-27 deprecated-model
initial model-registration responses; their existing mandatory synthetic
regression suites; conformance documentation.

## False-positive risk

The standard `capture_model` path validates every submitted source
field in the initial POST acknowledgment. The specialized
`capture_model_revoked` and `capture_model_deprecated` paths
previously checked only HTTP 200/202 and captured a model identity.
The downstream inference response could be correct even though the
initial registration response changed status, artifactDigest, metrics,
modelVersion or nested provenance, or dropped a submitted field.

## Minimal correction

- Reuse `submitted_record_problem` for both specialized model
  registration captures, before reading their model identifiers.
- Preserve the original submitted source object, including nested
  metrics/provenance, and allow extra server-managed fields.
- Fail before submitting inference on malformed or mutated registration
  acknowledgment. Preserve existing accepted status codes and
  all L-15/L-27 negative-inference/terminal-result assertions.
- Extend the existing mandatory regressions with wrong status, digest,
  nested evidence, missing fields and malformed result, plus positive
  extra-metadata controls.

## Verification

```sh
python Scripts/test_rejected_inference_no_stored_job.py
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_deprecated_inference_result_binding.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification-generation
checks before merge. Post-merge checks are separately recorded.

## Boundaries

This strengthens source fidelity of existing responses without
changing official BrAPI (Breeding Application Programming Interface)
version 2.1 contracts, proposed GenX wire schemas, model lifecycle
semantics or scientific maturity. No unresolved embargo policy is
selected.
