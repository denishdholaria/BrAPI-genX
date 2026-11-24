# Mission 076 — Genomic prediction and selection evidence boundaries

**Parent:** Mission 075 branch, commit `4d902711b142fd27808097cadf77e4c3b9a1b4ec`, 2026-11-24.  
**Scope:** two previously title-only draft group descriptions, accompanying readme/RFC qualification and source-backed regression checks. This mission does not change official Breeding Application Programming Interface (BrAPI) v2.1 contracts, candidate schemas or endpoints, registry/semantic links, proposed maturity, or deferred policy.

## Source-verified findings

1. **GenomicPrediction** (RFC-054; D-160–D-162): the response requires `genomicPredictionDbId`, `analysisMethodDbId` and `status`, and registration requires the first two. `predictions`, `accuracy`, `traitDbId`, `studyDbId`, `jobDbId` and provenance are optional. The predicted-value object is unconstrained despite a germplasm-keyed description. Accuracy is a bare number without an enforced range or validation design, and no exact `methodVersion` or `genomicDatasetDbId` is modelled. A candidate record cannot establish genomic estimated breeding value (GEBV) validity, transferability or independent validation. D-161's earlier "optional" dataset-linkage description was corrected to "not modelled".
2. **GenomicSelection** (RFC-055; D-163–D-165): the response requires `genomicSelectionDbId`, `analysisMethodDbId` and `status`, and registration requires the first two. `selectedGermplasm` is an optional string array; `selectionThreshold` is an optional number. Neither requires an approved index, breeding population, trait weights, candidate-germplasm authority, or breeder signature. GenX `SelectionDecision` separately requires `decision`, `decisionDate` and `programReference`; no automatic equivalence is established. D-164's purported optional GenomicDataset linkage was corrected to an unmodelled field.

## Assurance

- Create source-linked draft `GroupDescription.md` evidence for both groups.
- Correct unsupported claims in both READMEs and RFC-054/RFC-055.
- Extend the existing guarded reviewed list from **117 to 119 of 156** module descriptions, leaving **37 deferred** on the stacked branch.
- Add test assertions for exact required sets, optional evidence, unconstrained accuracy and predictions, unmodelled version/dataset linkage, separate selection verdict semantics, and outstanding decision references.

## Scope and verification

No source OpenAPI, schema, operation identifier, route, endpoint registry, decision authority or maturity promotion is authorized. Source-link resolution and branch-level review are possible through the GitHub connector. The full Python and Bun test suites must be executed before merging:

```sh
python Scripts/test_genx_group_descriptions.py
python Scripts/check_genx_group_descriptions.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Passing a syntax or documentation-link check does not show statistical correctness, deployed security, or validated scientific interoperability.
