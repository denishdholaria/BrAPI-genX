# Mission 084 — Workflow-scope regression repair and integration checkpoint

**Parent:** `c122e83b82842e68f8be4edca2cfc9b8184ff6a5` (draft Mission 083, pull request #33).  
**Scope:** verification correctness only. No changes to official Breeding Application Programming Interface (BrAPI) version 2.1 contracts, GenX routes, schemas, registry, scientific decisions, maturity register or semantic neighbors.

## Deterministic defect discovered

The new `test_readme_route_gate_cannot_hide_in_failure_only_diagnostics` in `Scripts/test_conformance_workflow_scope.py` searched for an exact workflow step string that ended in `--strict`. The real GitHub Actions `static-conformance` job executes `python Scripts/audit_genx_readme_routes.py --module Geospatial/VegetationIndex --strict --require-coverage`.

Consequently, the test's `next(...)` would raise `StopIteration` before exercising its mutation assertion. This is a test failure independent of GitHub Actions' billing status.

## Correction

- Match the **full** actual command in the mutation test, including `--require-coverage`.
- Add a negative regression test that removes only the coverage flag and verifies `scope_errors` reports the missing mandatory command.
- The existing failure-only-diagnostic exclusion remains unchanged.

Direct GitHub source checks after the correction show the workflow contains exactly one unconditional `run:` command matching the required full command, while its diagnostic command is separately reported. The corrected VegetationIndex README lists three actual GET/POST endpoint claims, all of which match the authoritative source method/path/operation identities. The source check above is not an executed workflow-scope test. A separate isolated execution of the **exact upstream GitHub blob contents** of `Scripts/audit_genx_readme_routes.py` and `Scripts/test_genx_readme_routes.py` was completed in the available container using `python test_genx_readme_routes.py -v`: **8 tests ran, 8 passed** (exit 0). The copied files' local Git blob hashes matched the connector's authoritative GitHub blob identities exactly: `fd73cf06c458f90de51e7dbf0b514f193b0ab565` (auditor) and `bcef551808afe27435f44c6ca4e63bb77bbb2cd4` (unit tests). This verifies the bounded synthetic mutation suite only, not the real full-repository fixture, the workflow-scope suite, or live conformance.

## Independent stacked-branch integrity inspection

Using the immutable Git tree for the current stacked branch and the source-backed group descriptions:

- **156** group-description files exist; the reviewed-module guard contains **135 distinct entries**, all of which resolve to actual module descriptions; **21 remain evidence-deferred**. `Breeding/CrossingSchedule` remains outside reviewed coverage as required by D-BP-11.
- All **160 documentation source links** across the **22 newly reviewed modules** from Missions 074–082 were resolved against the Git tree, with five unique official BrAPI/governance targets separately checked through GitHub. Zero dangling links or invalid draft/evidence markers were found.
- The comparison against `main` includes **114 commits and 84 changed files**, limited to 66 GenX Markdown sources, 12 assessment/roadmap files, five assurance scripts and one workflow. No official BrAPI source, GenX OpenAPI schema, JSON (JavaScript Object Notation) registry or other wire-contract source file is changed.
- The above checks were performed on GitHub-hosted source content and tree metadata; they are independent source-integrity checks, **not** a substitute for executing the complete Python suite.

## Integration/testing requirements

All pull requests from #24 through #33 remain stacked and unmerged. This mission is a small follow-up on #33 and must be integrated after its parent.

Run at least:

```sh
python Scripts/test_conformance_workflow_scope.py
python Scripts/test_genx_readme_routes.py
python Scripts/audit_genx_readme_routes.py --module Geospatial/VegetationIndex --strict --require-coverage
python Scripts/test_genx_group_descriptions.py
python Scripts/check_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Full repository checkout is blocked from this session's container because GitHub's hostname could not be resolved. The separately materialized route-audit unit files were tested as noted above. GitHub Actions is independently blocked by account billing. Neither issue should be misrepresented as a passing test or repaired by weakening tests. Do not mark the stacked pull requests ready or merge until actual validation is available.
