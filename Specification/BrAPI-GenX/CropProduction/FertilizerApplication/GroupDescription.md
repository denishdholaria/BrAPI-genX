# Group FertilizerApplication

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 026, not an approved agronomic decision model, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently demonstrated persistent-service implementation.

The proposed `FertilizerApplication` record has a namespaced identifier and lifecycle `status`, optional `supersedes` and provenance metadata, and candidate register/list/retrieve operations. Data-field requiredness differs among these drafts, and the schema is the authority for actual required properties. Idempotent replay and immutable revision claims remain proposed behavior, not proof of a running service.

**Scientific boundaries:** The required numeric `quantity` and string `unit` do not establish a validated nutrient composition, nutrient-to-product conversion, dose per area, precision, fertilizer formulation or field delivery. Location and Study fields are optional strings without typed referential validation; no SoilProfile linkage exists. A claimed application record is not proof of plant nutrient uptake or legal/regulatory approval. Outstanding questions start at D-75 and remain unratified. Adjacent operation names do not confer typed links, biological equivalence, or actual field intervention evidence.

**Sources:** [module overview](./README.md), [candidate schema](./Schemas/FertilizerApplication.yaml), [registration schema](./Schemas/FertilizerApplicationNewRequest.yaml), [draft operations](./FertilizerApplication_GET_POST.yaml), [RFC](../../RFCs/RFC-026-Fertilizer-Application.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
