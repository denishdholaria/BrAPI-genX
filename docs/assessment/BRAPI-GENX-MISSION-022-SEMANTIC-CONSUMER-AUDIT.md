# Mission 022 — Executable Semantic-Neighbor Consumer Audit

**Date:** 2026-11-24
**Baseline main:** `a9f225f5da4d8037b427b7675a023b56a5fad2ca`
**Status:** static/executable-source inventory and regression gate; **not** a runtime behavioral proof or a new scientific decision.

## Source inspection and verified categories

The inspected repository code currently contains distinct classes of
readers of the `semanticNeighborIds`, `semanticNeighborCatalogIds`,
`semanticNeighbors`, and `registryOnlyNeighbors` metadata fields:

| Script | Classified purpose | Safe inference / limitation |
|---|---|---|
| `Scripts/auditEndpointRegistrySourceConsistency.py` | Source–registry drift and reference checker | Verifies reference shape and differences; scientific identity not inferred |
| `Scripts/checkEndpointRegistry.py` | Catalogue/registry structural validator | Checks IDs and registry shape; **not** scientific evidence |
| `Scripts/checkGenXEndpointCatalog.py` | Source contract validator | Checks source-level metadata presence; not a runtime client |
| `Scripts/check_registry_drift_regression.py` | Per-edge historical drift guard | Prevents newly unreviewed links; not a correctness endorsement of grandfathered links |
| `Scripts/check_semantic_neighbor_governance.py` | Governance transition validator | Preserves status/identity and terminal publication consistency; not a scientific mapping |
| `Scripts/generateEndpointArtifacts.py` | Documentation renderer | **Publishes** registry labels in catalogues; avoid presenting them as equivalence or write permission |
| `Scripts/semantic_neighbor_lineage.py` | Historical/terminal governance helper | Detects invalid lineage and contradictory publication; not a service consumer |

The current inspected `Scripts/genx_test_server.py` and
`Scripts/checkGenXConformance.py` do **not** directly reference the four
neighbor metadata names. That is evidence about literal source usage,
**not proof** that dynamic or external consumers are absent.

The source-level guard scans code under `Scripts/`, `src/`, and
`generator/` for literal metadata names and assigns known paths to
documented roles. A previously unreviewed executable path referencing
these names causes a failure until assessed and added to the reviewed
inventory. Removing a reviewed consumer must also update the inventory
explicitly. Documentation, specification prose and test sources are
excluded to avoid mistaking citations and fixtures for production consumers.

## Implementation

- Added `Scripts/report_semantic_neighbor_consumers.py` with concise
  output or `--json`, deterministic path/line reporting and fail-closed
  inspection failures.
- Added `Scripts/test_semantic_neighbor_consumers.py` with **10 isolated
  mutation and positive tests**.
- Integrated report and tests in the static conformance workflow, including
  changed-file triggers and diagnostic report collection.
- Preserved all existing registry neighbor links and the 153 original
  governance identities.

## Limits and next decisions

The scanner is **lexical**, not a complete static data-flow analysis. It can
miss computed property names, compiled generated clients in other
repositories, and indirect code paths. It does not establish whether an
operation can be safely invoked or whether a typed scientific relationship
exists. Endpoint-catalogue rendering still uses its historical field labels;
changing published interpretations requires an explicit compatibility
decision (issue #17).

The test suite was run locally against exact source bytes:

```sh
cd /mnt/data/brapigenx_mission022
python -m unittest -v test_semantic_neighbor_consumers.py
python -m py_compile report_semantic_neighbor_consumers.py test_semantic_neighbor_consumers.py
```

**10/10 passed**. Exact local Git object hashes:

- scanner: `782c584b5bdd1c10e79eb97aeec633b5200db71e`
- tests: `b32a3f4c07cdf5f382c9cf5882b9fe526ccf722c`

Hosted Continuous Integration (CI) and full-checkout execution have not
run because the GitHub Actions budget is exhausted. No official Breeding
API (BrAPI) version 2.1 source, GenX wire schema, operation identifier,
scientific status, or Request for Comments (RFC) maturity was changed.
