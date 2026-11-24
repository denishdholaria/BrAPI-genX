# Mission 083 — Non-normative README endpoint identity assurance

**Parent:** `ac4a932217ad91a48300febfc45e2f7ee6d37228` (Mission 082), 2026-11-24.  
**Scope:** report-first integrity checking of human-readable GenX endpoint descriptions against the existing authoritative endpoint registry. No official Breeding Application Programming Interface (BrAPI) version 2.1 source, GenX wire schema, operation identifier, path, registry entry, semantic relationship, or scientific maturity status is changed.

## Reason for this mission

Mission 080 found a concrete drift in `Geospatial/VegetationIndex/README.md`: the prose said `/genx/v1/vegetation-index` and `genxListVegetationIndex`; authoritative source and registry use `/genx/v1/vegetation-indexes` and `genxListVegetationIndexes`. Existing source/catalogue checks could not detect non-normative README endpoint misstatements.

## Implementation

- New `Scripts/audit_genx_readme_routes.py` discovers registered GenX operations by source ownership (`Domain/Module`). It checks explicit README claims expressed as `METHOD /genx/v1/path` plus parenthesized `operationId`.
- It reports **mismatches** (explicit false claims) separately from **uncovered** operations (README lacks a claim); absence of a claim is advisory, not a silently invented endpoint.
- `--module Domain/Module` narrows scope; `--strict` fails on explicit mismatches for that selection. Default mode reports mismatches without making legacy prose differences blocking. Unsafe/unknown modules and malformed source registry entries are errors.
- GitHub Actions triggers now watch both the audit and its tests. A new unconditional static gate enforces exact documented identity for **`Geospatial/VegetationIndex` only**, because that scope was manually reconciled by Mission 080. The fail-only diagnostics also run the same commands.
- `Scripts/test_conformance_workflow_scope.py` requires both trigger paths and actual commands, so diagnostic-only mentions cannot mask a missing gate.
- New mutation tests cover valid claims, stale singular routes, wrong operation names, missing-claim advisory behavior, invalid modules, unsafe source paths, and command-line strict/report-only behavior.

## Evidence and limitations

The eight synthetic tests in `Scripts/test_genx_readme_routes.py` **ran locally** using only the standard Python library and passed. The authoritative registry was independently checked in GitHub: three VegetationIndex entries use `GET /vegetation-indexes`, `POST /vegetation-indexes` and `GET /vegetation-indexes/{vegetationIndexDbId}` with matching GenX operation IDs. The corrected README from Mission 080 claims the corresponding `/genx/v1` paths.

These tests run on isolated temporary directory fixtures, not a cloned full repo. The complete workflow, original suite, and live conformance have **not** executed on the stacked repository branch in this environment. This is not proof of end-to-end readiness.

## Verification needed before merge

```sh
python Scripts/test_genx_readme_routes.py
python Scripts/audit_genx_readme_routes.py --module Geospatial/VegetationIndex --strict --require-coverage
python Scripts/test_conformance_workflow_scope.py
python Scripts/test_genx_group_descriptions.py
python Scripts/check_genx_group_descriptions.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Do not broaden strict validation across every README until historical mismatches have been inventoried and judged against authoritative contracts. A README never becomes normative solely by passing this audit.
