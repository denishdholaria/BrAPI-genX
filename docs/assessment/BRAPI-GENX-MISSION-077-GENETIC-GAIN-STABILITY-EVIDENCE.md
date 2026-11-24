# Mission 077 — Genetic gain and stability analysis evidence boundaries

**Parent:** Mission 076 branch, commit `7ef5b34f2fdd87ccee679efb935ae09cb8e7d079`, 2026-11-24.  
**Scope:** draft GroupDescription, readme and Request for Comments (RFC) scientific claims plus source-derived tests only. No official Breeding Application Programming Interface (BrAPI) version 2.1 changes, GenX schemas, routes, operation identities, endpoint registry, or maturity or decision approval changes.

## Evidence from candidate schemas

1. **GeneticGainRecord** (RFC-046, D-136–D-138) requires `geneticGainRecordDbId`, `programDbId`, `traitDbId`, `gainValue` in the registration request; the response additionally requires `status`. The value is a bare number. `unit`, `period`, `method`, and `provenance` are optional. These do not mandate an annualized rate, estimation baseline, genetic comparison group, trait harmonization, uncertainty or authority-checked Program/Trait identity. The RFC previously called GenX AnalysisMethod linkage optional; only a free-text `method` field is modelled, and no `analysisMethodDbId` exists.
2. **StabilityAnalysisResult** (RFC-049, D-145–D-147) requires `stabilityAnalysisResultDbId`, `analysisMethodDbId` in the registration request; the response additionally requires `status`. `stabilityIndex` is an optional, unconstrained number. Trait, study, job and provenance are optional; no required environment/genotype coverage, index orientation, uncertainty or method version is supplied. D-146 previously called GenomicDataset linkage optional; no `genomicDatasetDbId` field is modelled.

## Assurance changes

- Add two scientifically qualified, source-linked GroupDescription documents marked `STRUCTURAL_DRAFT`.
- Correct and bound corresponding README and RFC prose, while preserving draft replay and deferred decision semantics.
- Extend reviewed documentation inventory from **119 to 121 of 156**, leaving **35 unreviewed** on the stacked branch.
- Add schema-grounded regression checks for required/optional fields, unstructured units and period, lack of `analysisMethodDbId` in GeneticGain, and missing method-version/dataset linkage in StabilityAnalysis.

## Verification boundary

GitHub connector operations establish file identities, links, diffs and commit history, but not local Python test execution. Before merge, run the group-description and full registry, source-consistency, generator and conformance checks. These documentation updates do not establish validated breeding progress, genotypic stability, production persistence, or officially endorsed scientific standards.
