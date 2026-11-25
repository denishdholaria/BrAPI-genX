# Mission 171 — Persisted deprecated-model evidence in L-27

**Status:** implementation proposed for hosted verification.
**Dependency:** Mission 170, Pull Request #120 (stacked on Mission 169).
**Scope:** registered L-27 deprecated-model inference; executor,
manifest safeguards, already-mandatory synthetic regressions and
conformance documentation.

## Confirmed false-positive risk

The L-27 test previously checked that an initial deprecated-model
registration acknowledgment retained the submitted fields, and that
a subsequent warned inference job completed with the original model
identity/version and recomputed input digest. It did not independently
read the model's stored published version. The job-result pathway
alone is not direct storage evidence for the registered model.

## Bounded correction

- Insert a version-specific model GET immediately after deprecated
  model registration and before inference submission.
- Require HTTP 200 and every original submitted model field, including
  identity, version, status `deprecated`, digests, nested metrics
  and provenance; allow additional server-managed fields.
- Reject absent, wrong-version, rewritten or malformed readbacks
  before submitting inference.
- Preserve initial model acknowledgment verification, inference job
  acknowledgment, WARNING, terminal completion and input digest.
- Extend the existing mandatory L-27 regression suites, and lock the
  additional GET/assertion into the fail-closed manifest validator.

## Verification

```sh
python Scripts/test_deprecated_inference_completion.py
python Scripts/test_deprecated_inference_result_binding.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_step_manifest.py
python Scripts/checkGenXConformance.py
```

Require GitHub-hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation before
merge. Main-branch post-merge verification is separate.

## Boundaries

No official BrAPI (Breeding Application Programming Interface) version
2.1 contract, GenX wire schema, model lifecycle policy, scientific
maturity or unresolved embargo policy is modified.
