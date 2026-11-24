# Group NutrientAdvice

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 132; no normative scientific acceptance, official Breeding Application Programming Interface (BrAPI) version 2.1 identity substitution or independent service-conformance claim.

The `NutrientAdvice` record has its own namespaced identifier and candidate `status` lifecycle, with optional descriptive fields, `supersedes` and provenance. It exposes draft register/list/retrieve operations. The schemas, rather than historical problem statements or endpoint names, determine what is required; immutable publication and replay semantics remain candidate behaviors until an independent persistent implementation is verified.

**Evidence, ownership and deployment boundaries:** The proposed recommendedRate is an optional unconstrained string, not a validated application dose with nutrient concentration, soil-test result, area, uncertainty or formulation identity. The advisory has no typed connection to fertilizer applications or research evidence. It is not proof that the advice is safe, economically optimal, agronomically suitable or implemented. Deferred decisions D-394 and the remaining questions in the governing RFC have not been settled. Advisory operation-neighbor references do not create enforceable scientific or legal relationships.

**Sources:** [module overview](./README.md), [record schema](./Schemas/NutrientAdvice.yaml), [registration schema](./Schemas/NutrientAdviceNewRequest.yaml), [draft operation](./NutrientAdvice_GET_POST.yaml), [governing RFC](../../RFCs/RFC-132-NutrientAdvice.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
