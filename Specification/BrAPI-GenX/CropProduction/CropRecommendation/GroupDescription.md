# Group CropRecommendation

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 129; no normative scientific acceptance, official Breeding Application Programming Interface (BrAPI) version 2.1 identity substitution or independent service-conformance claim.

The `CropRecommendation` record has its own namespaced identifier and candidate `status` lifecycle, with optional descriptive fields, `supersedes` and provenance. It exposes draft register/list/retrieve operations. The schemas, rather than historical problem statements or endpoint names, determine what is required; immutable publication and replay semantics remain candidate behaviors until an independent persistent implementation is verified.

**Evidence, ownership and deployment boundaries:** Recommended variety and practice fields are optional free text, not a resolved Germplasm identifier, validated crop/season ontology, authorized variety-release label, field-specific trial result, or verified farm suitability assessment. The proposed recommendation does not establish adoption, scientific effectiveness or regulatory authorization. Deferred decisions D-385 and the remaining questions in the governing RFC have not been settled. Advisory operation-neighbor references do not create enforceable scientific or legal relationships.

**Sources:** [module overview](./README.md), [record schema](./Schemas/CropRecommendation.yaml), [registration schema](./Schemas/CropRecommendationNewRequest.yaml), [draft operation](./CropRecommendation_GET_POST.yaml), [governing RFC](../../RFCs/RFC-129-CropRecommendation.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
