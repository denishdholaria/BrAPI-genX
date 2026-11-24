# Mission 075 — Heritability and genotype-by-environment evidence boundaries

**Parent:** Mission 074 branch, commit `653ef1b4d2803d9733202685f5b7a1c4c2e3c3ef`, 2026-11-24.  
**Scope:** two previously title-only GroupDescription records, their READMEs and Request for Comments (RFC) descriptions, and source-derived regression tests. No official Breeding Application Programming Interface (BrAPI) version 2.1 source changes, GenX schema/route/registry changes, maturity promotion or governance ratification.

## Findings

1. **HeritabilityEstimate** (RFC-050, D-148–D-150): response requires `heritabilityEstimateDbId`, `analysisMethodDbId`, `status`; registration request requires the first two. `heritabilityValue` is optional with type `number`, no estimate-type or uncertainty representation, and no range constraint. Trait, study, job, and provenance are also optional. The method identifier does not include `methodVersion` or prove execution. D-149 formerly described GenomicDataset linkage as optional although `genomicDatasetDbId` does not exist in the schema; this is corrected to *not modelled*. No distinction between broad-sense and narrow-sense heritability is enforced.
2. **GxeAnalysisResult** (RFC-051, D-151–D-153): response requires `gxeAnalysisResultDbId`, `analysisMethodDbId`, `status`; registration requires the first two. The optional `gxeEffect` is an unconstrained `object`, with no required genotype/environment identities, model parameterization, inferential uncertainty, or significance policy. Trait, study, job, and provenance are optional; exact method version is absent. D-152 previously described GenomicDataset linkage as optional but the field is not modelled.

## Assurance

- Two `GroupDescription.md` records are added as **STRUCTURAL_DRAFT** with source-linked claims and unresolved scientific boundaries.
- Module READMEs and RFC-050/RFC-051 distinguish representation from validated inference and correct two inaccurate optional-link descriptions.
- The existing reviewed-module guard is expanded to include `Breeding/Heritability` and `Breeding/GxeAnalysis`. Expected reviewed documentation coverage after the stacked Mission 074 branch: **117 of 156**, leaving **39 deferred**.
- The group-description test suite gains schema-derived checks for response/request required sets, optional inputs and results, absent method-version and dataset linkage, and opaque numeric/object interpretation.

## Verification and limits

Review and execute:

```sh
python Scripts/test_genx_group_descriptions.py
python Scripts/check_genx_group_descriptions.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

The GitHub connector verifies source files and records commits but does not execute Python. Until these commands are actually run on the branch, the evidence is source inspection and repository review, not an executed conformance claim. Hostable reference-server tests do not demonstrate production method resolution, reproducible statistical estimation or persistent-service correctness.
