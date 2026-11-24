# Group StabilityAnalysis

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 049. The proposed `StabilityAnalysisResult` is metadata for genotype performance stability across contexts, not a validated model fit, adaptation classification, or official BrAPI v2.1 resource.

The response schema requires `stabilityAnalysisResultDbId`, `analysisMethodDbId`, and lifecycle `status`; registration requires the identifier and method reference only. `stabilityIndex`, `traitDbId`, `studyDbId`, `jobDbId`, and `provenance` are optional. The index is a bare number without a schema-enforced range, interpretation direction (higher or lower is preferable), environmental strata, genotype set, model assumptions, scale, uncertainty interval, or multi-environment trial scope.

**Statistical boundary:** A stored `stabilityIndex` cannot establish stable genotypic ranking, adaptation across sites or seasons, statistical significance, or comparability across heterogeneous models. The required `analysisMethodDbId` is only a string; no exact `methodVersion` or execution evidence is required. There is no modelled `genomicDatasetDbId`, despite D-146 asking about such linkage. D-145–D-147 remain open. Contract-level replay and immutable-version language is not proof of persistent-service verification.

**Sources:** [module overview](./README.md), [response schema](./Schemas/StabilityAnalysisResult.yaml), [registration schema](./Schemas/StabilityAnalysisResultNewRequest.yaml), [endpoint operations](./StabilityAnalysis_GET_POST.yaml), [RFC](../../RFCs/RFC-049-Stability-Analysis.md), [AnalysisMethod schema](../../Research/AnalysisMethods/Schemas/AnalysisMethod.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
