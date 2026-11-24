# Mission 013 — Registry Semantic-Neighbor Root-Cause and Safe Drift Reduction

**Reviewed:** 2026-11-24  
**Starting `main`:** `8d3e6840ae4522734440b46f8b779c13a47033a3`  
**Disposition:** source-history investigation, source/registry boundary analysis and a bounded regression-gate repair. This document is advisory, not a scientific decision.

## Evidence trail and attribution boundary

The existing `Specification/ENDPOINT-REGISTRY.json` is the authority for **historical catalogue relationship metadata**, while individual GenX operation OpenAPI documents are the source for their `x-brapi-genx.semanticNeighbors` declarations. `Scripts/generateEndpointArtifacts.py` **reads the registry** and renders its values into `Specification/ENDPOINT-CATALOG.md` and other documentation. It does not infer a GenomicDataset neighbor from biology or derive registry relationships from the reviewed source schema.

The repository commit history shows that module-creation commits **inserted operation-neighbor references directly into the registry**:

| Historical commit | Module | Added registry-only repeated target | Source-contract distinction |
|---|---|---|---|
| [`5b6a2c`](https://github.com/denishdholaria/BrAPI-genX/commit/5b6a2caafc0a21146d15f982730c97a83f6996b2) | ArtifactCatalogue | `genxRegisterGenomicDataset` in three source-operation rows | Source operation lists `genxRegisterResearchAsset` and same-module operations; does not declare the added genomic registration neighbor |
| [`a16c90`](https://github.com/denishdholaria/BrAPI-genX/commit/a16c90bdc1b8c17f2635abbee5e03d435bd3d9fc) | IrrigationAdvice | `genxRegisterGenomicDataset` in three operation rows | Agronomic recommendation operations are separate from molecular dataset registration |
| [`34433b`](https://github.com/denishdholaria/BrAPI-genX/commit/34433bd982516ba568be5f1f97f8ea0a41271ee9) | ExperimentalProtocol | `genxRegisterGenomicDataset` in three operation rows | Experimental protocol source operations do not declare this genomic registration neighbor |
| [`3b0b49`](https://github.com/denishdholaria/BrAPI-genX/commit/3b0b49386abe1ea26aa9850c3980943b7ffa002a) | AssayExecution | `genxRecordAssayDesign` in three operation rows | An assay execution is not the same operation as recording its design |

These are demonstrable **registry additions during historical module-creation changes**. The repeated three-operation template strongly suggests template-driven seeding, but the available history does **not** prove which agent, script or drafting process selected the targets. **No causal generator script was identified**, and this report does not invent one.

The pre-existing source audit `Scripts/auditEndpointRegistrySourceConsistency.py` correctly reports source/registry differences without automatically deleting historical links; the frozen ledger tracks 153 inherited IDs. The other pre-existing drift gate already rejects **new** registry-only references against an older pinned baseline, so an additional indiscriminate global rejection guard would be redundant.

## Real regression-gate defect

`Scripts/check_registry_drift_regression.py` compared an entire
`registryOnlyNeighbors` report object (including its `neighbors` array)
as a single JSON value. Removing *one* unsupported neighbor from an operation
while leaving two others changed that entire object, incorrectly triggering
a `New or changed registryOnlyNeighbors` error. Thus the implementation
contradicted its stated invariant that **removing historical drift is allowed**.

### Engineering correction

- Compare individual records with the stable triple
  `(catalogId, module, neighbor)`, instead of treating the mutable neighbor
  array as the regression identity.
- Use a multiset (Counter) so a newly duplicated neighbor is not silently
  discarded; reject malformed report shapes and empty identity tokens.
- Allow subset/removal or reorderings of grandfathered neighbor lists;
  continue rejecting novel edges, changes of source identity, and mismatches.
- Retain the frozen baseline SHA `d9259dca0bab21a131fa1f6a20e7643eadd6f3d7`;
  no grandfathered edge is declared scientifically valid.
- Do **not** remove any of the 153 ledger identities or alter current
  source/registry semantic records in this mission.

## Verification performed

Local isolated execution against script content equivalent to the repository
files (the resulting Git object hash is verified after committing):

```sh
cd /mnt/data/brapigenx_mission013
python -m unittest -v test_registry_drift_regression.py
python -m py_compile check_registry_drift_regression.py test_registry_drift_regression.py
```

Result: **13/13 unit/mutation tests passing**, including
partial removal of one legacy neighbor, order-only change, new link,
replacement link, moved source, duplicate edge and malformed records.
This is **not** the full checked-out repository's baseline-drift check,
which requires the historical Git worktree, complete registry and sources.
The monthly hosted GitHub Actions minutes limit remains a separate blocker.

## Governance boundary and next slice

This repair establishes one prerequisite for a future **authorized** terminal
decision to remove a rejected link from the registry. A separate governance
validator currently distinguishes new links by whether they are present in
the *current* registry-only inventory. That can misclassify a historically
inherited link after authorized removal; its behavior must also be checked
before any terminal cleanup. No terminal decisions or scientific mappings
were made in this mission.

**Non-goals:** no official BrAPI version 2.1 change; no GenX public contract
or operation identifier change; no undocumented scientific equivalence claim;
no Request for Comments (RFC) maturity promotion; no historical link deletion.
