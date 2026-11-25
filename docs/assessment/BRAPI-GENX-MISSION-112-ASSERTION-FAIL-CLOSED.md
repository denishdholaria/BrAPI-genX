# Mission 112 — Fail closed on unknown or non-executable live assertions

**Date:** 2026-11-25. **Inspected `main`:** `480d592d56b2de8bef9dc3a15a31e9d02c07a27f`, post-merge Mission 111 checks verified successful.

## Confirmed defect

Live probes specify assertions as mappings in `Specification/BrAPI-GenX/Conformance/probes.yaml`, but the runner previously inspected only known keys. A misspelled key (for example `stauts: 409`) was silently ignored. If that was the only assertion on a negative test step, the probe could report success regardless of whether the expected conflict was observed. Mission 108 guarded the existence and basic shape of registered calls but did not validate assertion vocabulary.

## Bounded correction

- Validate every live `assert` mapping before running any probe, rejecting unknown assertion names, empty or nonmapping assertion objects, Boolean guards whose value is not exactly true, invalid status codes, negative/noninteger counts, invalid `body` and `telemetry_counts` mappings, and improperly paired mean/sample expectations.
- Require the existing replay-capture step to have `same_jobDbId: true` and the existing concurrent-submission step to have `single_effect: true`; mismatched directive/assertion pairs fail.
- Add 18 regression methods in a separate `Scripts/test_conformance_assertion_manifest.py` suite, including a subprocess test showing an unknown assertion fails before contacting any server.
- Add the test to the hosted static job and enforce its execution with a workflow-scope mutation test.
- Preserve the current 21 static and 28 live registered probe identifiers, their actual assertions, and their wire contracts.

## Verification

```sh
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

The first two suites and normal static conformance must pass. Deliberately changed assertion keys must fail, not silently reduce coverage. Require passing hosted static, Python live, TypeScript differential/legacy fallback, and specification-generation workflows at the exact pull-request head before merging; recheck integrated `main` separately.

**Evidence boundary:** An assertion grammar guard prevents test-suite false positives; it does not demonstrate production scientific integrity, durable storage, external-vendor interoperability or independent laboratory validation. No official Breeding Application Programming Interface (BrAPI) version 2.1 contracts, GenX schemas/registries, Request for Comments (RFC) maturity or unresolved geospatial decisions are changed.
