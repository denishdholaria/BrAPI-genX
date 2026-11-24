# Group VariantAnnotation

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 062. A proposed `VariantAnnotation` is neither an automatically interpreted official Breeding Application Programming Interface (BrAPI) version 2.1 `Variant` nor a validated consequence annotation.

The response schema requires only `variantAnnotationDbId` and lifecycle `status`; the registration request requires only `variantAnnotationDbId`. `variantDbId`, `studyDbId`, `analysisMethodDbId`, `annotations`, and `provenance` are optional. The annotation payload is an unconstrained object: no gene/transcript vocabulary, allele normalization, reference assembly, effect ontology, consequence severity, or method-version binding is required or checked by these schemas. Identifiers are strings, not verified cross-authority joins.

**Official-contract boundary:** BrAPI v2.1 `Variant` already represents a sequence change and exposes `additionalInfo` for flexible supplemental content. That existing metadata is not a dedicated, interchangeable GenX annotation lifecycle, but neither may we claim official BrAPI has no place to express variant-related annotations. The candidate does not modify `Variant`, its `variantDbId`, or reference-coordinate semantics.

**Evidence and interpretation boundary:** Registering a record does not validate gene consequences, prove reproducibility, guarantee that a named method ran, or establish approval. Proposed replay, immutability and supersession behavior require independent service evidence. D-184–D-186 remain open; record identifiers and advisory operation neighbors must not be treated as semantic equivalence.

**Sources:** [module overview](./README.md), [record schema](./Schemas/VariantAnnotation.yaml), [registration schema](./Schemas/VariantAnnotationNewRequest.yaml), [endpoint operations](./VariantAnnotation_GET_POST.yaml), [RFC](../../RFCs/RFC-062-Variant-Annotation.md), [official Variant schema](../../../BrAPI-Genotyping/Variants/Schemas/Variant.yaml), [AnalysisMethod schema](../../Research/AnalysisMethods/Schemas/AnalysisMethod.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
