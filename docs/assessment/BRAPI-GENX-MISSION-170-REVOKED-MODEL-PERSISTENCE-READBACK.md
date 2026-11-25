# Mission 170 — Persisted revoked model evidence in L-15

**Status:** implementation proposed for hosted verification.
**Dependency:** Mission 169, Pull Request #119.
**Scope:** registered L-15 revoked-model negative inference;
executor, manifest safeguards, existing synthetic regressions and
conformance documentation.

## Confirmed false-positive risk

The runner previously accepted a revoked-model registration
acknowledgment and immediately submitted inference against the
claimed model identity. A backend that acknowledged registration
without persisting the revoked version would then deny inference
because the model was unknown. Both cases yielded HTTP 400 and
a jobs collection without rejected requests, allowing L-15 to
report success without evidence that *revocation* was enforced.

## Bounded correction

- Insert a version-specific model GET directly after registration and
  before the revoked-model inference submit.
- Capture the original revoked-model submission; compare every source
  field and nested value against the actual stored response, requiring
  HTTP 200 and the same `modelDbId`, `modelVersion`, and `revoked`
  status.
- Reject a missing or corrupted stored model before the downstream
  inference request, rather than allowing unknown-model rejection to
  stand in for revocation.
- Preserve unknown-model rejection, registered revoked-model rejection,
  and complete stored-jobs negative checks.
- Make the extra step mandatory in the probe manifest validator,
  plus mutation tests for omitted and disabled assertions.
- Extend the existing required L-15 synthetic regression suite for
  missing, changed and malformed stored model readbacks and valid
  extra server metadata.

## Verification

```sh
python Scripts/test_rejected_inference_no_stored_job.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_step_manifest.py
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance,
independent-runtime differential and specification generation before
merging. After merge, independently verify the main-branch workflows.

## Boundaries

No official BrAPI (Breeding Application Programming Interface) v2.1
source contracts, proposed GenX wire schemas, maturity levels or
embargo policies change.
