# BrAPI-GenX — Hybrid Architecture Assurance

- **Status:** Implemented on `work/hybrid-architecture-assurance-20261122`; full current-branch runtime verification is pending trustworthy GitHub Actions diagnostics.
- **Review:** Draft pull request [#10](https://github.com/denishdholaria/BrAPI-genX/pull/10).
- **Date:** 2026-11-22.
- **Immutable pre-assurance baseline:** `d9259dca0bab21a131fa1f6a20e7643eadd6f3d7` (2026-11-21).
- **Authority:** Existing GenX source OpenAPI operations remain the wire-contract authority. The master endpoint registry remains authoritative for catalogue identity and crosswalk metadata. Classification is a non-normative proposal, not an official BrAPI taxonomy.

## Decision

**Keep the hybrid architecture already established by pull request #9.**
No new `Domains/` or `Platform/` hierarchy is introduced; no schema or endpoint identity is renamed; official BrAPI v2.1 files remain semantically unchanged. D-04 remains deferred: the legacy v2.1 generator is not silently expanded to include GenX.

The repository's master registry records 201 BrAPI v2.1 operations and 462 GenX candidate operations (663 catalogue identities). The established classification registry currently lists 156 independently governed GenX modules plus `Conformance/` support material.

## Slice 1 — Dependency-aware validation

**Implemented.** The GenX static/live workflow now watches `Specification/**` on push and pull requests, covering shared `Components/`, `OpenAPI-Components/`, `BrAPI-Schema/`, baseline v2.1 modules, `Generated/`, and GenX modules. Previously only GenX and a handful of catalogues triggered the workflow despite static references reaching across those directories.

`Scripts/test_conformance_workflow_scope.py` checks the event filters and required verification commands, with negative tests for a removed specification dependency and skipped validator. New scripts are also included in workflow filters.

## Slice 2 — Conformance and governance reconciliation

**Implemented.** The registered probe manifest is authoritative: S-01–S-21 and L-01–L-28. Historical references to experimental S-22 and L-29 have been labelled as branch-specific evidence rather than active probes. Separately executed capability-negotiation mutation coverage is preserved. `Conformance/RESULTS.md` and `DECISIONS.md` now explicitly distinguish dated historical results from present-branch verification.

No historical evidence or open standards decisions were deleted or silently ratified.

## Slice 3 — Registry/source descriptive drift control

**Implemented a pinned-baseline fail-closed non-regression gate; full zero-drift reconciliation is a distinct pending requirement if historical mismatches remain.**

`Scripts/auditEndpointRegistrySourceConsistency.py` now supports `--root` and `--report-json`, preserving its original `--plan-json` and `--strict` modes. New `Scripts/check_registry_drift_regression.py` audits both the current checkout and the fixed pre-assurance commit using the **same current audit code**. It refuses source-loading errors and any new or changed descriptive discrepancy, including registry-only semantic-neighbor references; disappearing discrepancies are permitted.

The fixed baseline is **not** a claim that prior metadata differences are valid. Source OpenAPI summaries and the `x-brapi-genx` metadata remain authoritative for the compared descriptive fields. `Scripts/test_registry_drift_regression.py` contains mutation tests covering introduced, changed, removed, and malformed discrepancies. The workflow fetches history to make the pinned comparison reproducible.

The existing `--strict` mode should replace the temporary non-regression allowance once the historical discrepancy set is actually zero. Do **not** mark full descriptive reconciliation complete simply because the baseline gate passes.

## Slice 4 — Documentation and repository hygiene

**Implemented.** The baseline generated-output README distinguishes `brapi_generated.json` from `brapi_openapi.json`. Each official BrAPI module README explicitly identifies this checkout as v2.1 while retaining older v2.0 navigation links as historical references. The intentional legacy `OpenAPI-Components/` mirror is documented as generator-dependent and is not merged into `Components/` prematurely. The namespace error message in `checkGenXEndpointCatalog.py` now says `brapi-genx.genx`, not the retired `brapi-den.genx`.

The two accidentally committed `src/brapi_genx/__pycache__/*.pyc` files were deleted, and `.gitignore` now excludes Python bytecode/cache files globally.

The master registry's `generatedAt` field and generated catalogue headers remain source-provenance dates; they have not been reset to an arbitrary review date.

## Slice 5 — Structural regression protection

**Implemented.** `Scripts/specification_structure.py` checks registered GenX module presence, local README and GroupDescription files, canonical `Schemas/` casing, nonempty schema definitions, source operation presence (except schema-only Provenance), valid registered source paths, and declared baseline generated artefact links. It deliberately does **not** rename or lint inherited v2.1 contract paths.

`Scripts/test_specification_structure.py` contains negative tests for missing operation/schema files, lowercase `schemas/`, bad source paths, and missing generated files. A separate workflow-scope suite protects transitive dependency coverage. The legacy upstream exceptions are recorded explicitly within the validator source.

## Verification

The existing `Specification/FILE-TREE.md` and classification registry were independently compared during the review: all **156 registered GenX modules** have the expected README, GroupDescription, `Schemas/` directory, and an operation YAML file where applicable. That is a **file-tree inspection**, not execution of the new Python validator.

The prior mainline restructuring (PR #9) reported successful local tests and byte-identical relocation of 616 contract files. Its checks do **not** certify this later branch.

GitHub Actions reported failed static and live jobs for PR #10, but the connector returned no job steps and its log-download action produced `BlobNotFound`. The same missing-log failure signature and unsuccessful workflow conclusion were observed for earlier PRs #9, #8, and #6. **No passing runtime test claim is made for this branch.** Do not merge until the workflows execute successfully or a documented alternative verification procedure runs.

To verify in a full checkout with Python 3.12 and the repository's pinned dependencies:

```sh
python -m pip install PyYAML==6.0.2 rfc8785==0.1.4
python Scripts/test_domain_classification.py
python Scripts/test_specification_structure.py
python Scripts/specification_structure.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/test_registry_drift_regression.py
python Scripts/check_registry_drift_regression.py
python Scripts/checkGenXConformance.py
python Scripts/checkGenXEndpointCatalog.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --report-json
python Scripts/generateEndpointArtifacts.py --check
```

Full validation also requires the existing cross-language test jobs, live reference-server probes, breeding-pipeline fixture tests, and the legacy schema-generator pipeline where applicable.

## Deferred matters preserved

- D-04 GenX-to-legacy generator wiring: intentionally not changed.
- Official BrAPI v2.1 naming and casing anomalies: documented, not rewritten.
- Full registry/source descriptive reconciliation: only required if the report shows remaining historical mismatches; the non-regression gate must not be confused with strict zero-drift conformance.
- Historical S-22/L-29 experiments: retained as historical evidence, not silently activated or represented as current manifest probes.
