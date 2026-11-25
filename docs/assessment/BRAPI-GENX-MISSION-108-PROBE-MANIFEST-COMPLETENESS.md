# Mission 108 — Prevent false-green conformance from an emptied or truncated registry

**Date:** 2026-11-25. **Starting source:** Mission 107 review head `2ae8f5585c17babced07cc72c4380b12787af7e1`. **Dependency:** Mission 107 must integrate first.

## Confirmed failure mode

The conformance runner reads `Specification/BrAPI-GenX/Conformance/probes.yaml` and executes every registered probe, but an unfiltered invocation with `probes: []` executes no checks, reports zero failures, and returns success. Similarly, dropping a registered probe can silently reduce coverage. Mission 103 and Mission 107 addressed explicitly requested probes, but not the unfiltered registry-level risk.

The current authority contains exactly **S-01 through S-21** and **L-01 through L-28**. These 49 identifiers form a protected minimum *testing* baseline, not an assertion that all GenX proposals or external servers conform.

## Bounded implementation

- Before test execution, validate the probe registry is an array with the full existing baseline, unique well-formed identifiers, identifier/tier agreement, recognized static checker names, and non-empty/executable live call descriptions.
- Allow future, correctly formed probe registrations without automatically claiming their scientific maturity or broadening the normative specifications.
- Extend the already protected hosted `Scripts/test_conformance_probe_selection.py` suite with 12 cases, including empty/partial registries, duplicates, unrecognized checks, invalid live calls, and an end-to-end command-line test showing an empty registry fails before execution.
- Do not change the actual 49 registered probes, any wire contract, or the standard static-only live-SKIP behavior.

## Verification and falsifiers

```sh
python Scripts/test_conformance_probe_selection.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Expected: the first two test suites and the existing static runner pass; a deliberately truncated or empty registry fails with non-zero exit and explains which baseline probes are missing. No new external-server conformance evidence follows from a manifest guard. Hosted static, Python live, TypeScript differential and specification generation must all pass on the exact review head before integration; check integrated `main` separately.

**Governance:** The guard does not promote Request for Comments (RFC) maturity, change official Breeding Application Programming Interface (BrAPI) version 2.1 source, alter GenX routes/schemas, resolve field-specific digest preimages, or ratify deferred geospatial decisions.
