# BrAPI-GenX — Experimental Design (Trial Layout)

This **STRUCTURAL_DRAFT** describes a candidate separately registered, versioned experimental design; it does not establish statistical validity or executed treatment assignment. Official BrAPI version 2.1 Study already holds `experimentalDesign` metadata and Observation Units carry hierarchy, positions and factors.

- `POST /genx/v1/experimental-designs` (`genxRegisterExperimentalDesign`) registers `ExperimentalDesign` (`Schemas/ExperimentalDesignNewRequest.yaml`), requiring `experimentalDesignDbId`, `studyDbId`, `designType`. Other scientific fields are optional. Identical-body replay and `409` conflict are proposed behaviors, not independently confirmed persistence.
- `GET /genx/v1/experimental-designs` (`genxListExperimentalDesigns`) lists records optionally filtered by study/design type.
- `GET /genx/v1/experimental-designs/{experimentalDesignDbId}` (`genxGetExperimentalDesign`) retrieves a draft record.

No randomization-algorithm validation or typed official plot-unit relationship is defined. Details: [evidence review](./GroupDescription.md), [RFC-018](../../RFCs/RFC-018-Experimental-Design.md); D-51–D-53 remain open.
