
# Mission 148 — Provenanced observation identity in reference echo jobs

**Status:** implemented; required hosted checks pending.
**Dependency:** Mission 147.
**Scope:** registered L-07, existing live executor, manifest guard,
negative synthetic regressions and conformance documentation.
**Baseline:** Mission 147 head `36e4deed0c3f51439ca730563c1720e60dc2445a`.

## Confirmed false-positive risk

The L-07 provenance assertion compared the completed response's nested
`provenance` object against the submitted one. A response with the correct
provenance but a changed observation value, observationDbId,
observationUnitDbId or observationVariableDbId could still pass.
The reference server's `analysis` job is explicitly implemented as an
observation **echo**, so retaining the complete original observation is
an appropriate conformance expectation for this particular test workflow.

## Correction

- Preserve the original request observation from the captured job.
- Require the completed GET to match the accepted jobDbId, original jobType
  and original idempotencyKey, with status COMPLETED and one observation.
- Verify that every originally submitted observation field and nested value
  survives unchanged (scientific identifiers, measurement value,
  provenance digests, uncertainty, sources, evidence links and others).
- Permit additional server-managed fields not present in the submission.
- Extend `Scripts/test_provenance_roundtrip_integrity.py` with negative
  cases where provenance remains intact but the scientific observation
  changes, and cases for mismatched completed job metadata.
- Require the exact two-step POST/capture/wait and completed GET/assertion
  sequence through the manifest validator; add negative manifest tests.
- Keep current hosted test commands; no new test runner step required.

## Verification

```sh
python Scripts/test_provenance_roundtrip_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Required hosted static, Python live-reference and independent runtime
conformance checks, plus specification generation, must pass before merge.

## Boundaries

This is specifically a reference-server echo roundtrip assertion. It is
not a new general-purpose scientific requirement that derived analytical
outputs must equal original inputs. No official Breeding Application
Programming Interface (BrAPI) 2.1 contract, GenX wire schema, maturity,
or embargo metadata visibility policy is changed.
