# Group AssayDesign

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 061. This is not an official Breeding Application Programming Interface (BrAPI) version 2.1 resource, laboratory-validated design, or independently verified implementation.

The `AssayDesign` schema requires an assayDesignDbId and status in its response, but the registration request requires only assayDesignDbId. analysisMethodDbId, studyDbId, platform and markerCount are optional metadata; the proposal does not require probe sequences, a marker inventory, a genomic dataset, a versioned instrument method or a proven physical assay. The optional analysisMethodDbId string is not evidence of referential integrity to an AnalysisMethod.

**Design versus execution boundary:** Recording a candidate design does not establish that an assay was ordered, executed, quality-controlled or reproduced. Nor is there a typed link from this design to MarkerProbe, AssayExecution or GenomicDataset. D-181–D-183 remain open; the stated supersession and replay behavior is proposed rather than independently confirmed against a persistent authenticated service. BrAPI Sample, Variant and CallSet identity must remain separate.

**Sources:** [module overview](./README.md), [record schema](./Schemas/AssayDesign.yaml), [registration schema](./Schemas/AssayDesignNewRequest.yaml), [operation](./AssayDesign_GET_POST.yaml), [RFC](../../RFCs/RFC-061-Assay-Design.md), [official samples](../../../BrAPI-Genotyping/Samples/Samples_GET_POST_PUT.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
