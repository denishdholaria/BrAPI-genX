# Group Farm

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 069; no normative scientific acceptance, official Breeding Application Programming Interface (BrAPI) version 2.1 identity substitution or independent service-conformance claim.

The `Farm` record has its own namespaced identifier and candidate `status` lifecycle, with optional descriptive fields, `supersedes` and provenance. It exposes draft register/list/retrieve operations. The schemas, rather than historical problem statements or endpoint names, determine what is required; immutable publication and replay semantics remain candidate behaviors until an independent persistent implementation is verified.

**Evidence, ownership and deployment boundaries:** The optional `locationDbIds` is a list of plain strings; membership and geometric overlap are not validated. A farm's declared `totalAreaHa` is not a surveyed cadastral area or provable sum of component fields. This metadata record does not confer ownership, water rights or legal title, nor does the schema encode an explicit overlapping-farm agreement. Deferred decisions D-205 and the remaining questions in the governing RFC have not been settled. Advisory operation-neighbor references do not create enforceable scientific or legal relationships.

**Sources:** [module overview](./README.md), [record schema](./Schemas/Farm.yaml), [registration schema](./Schemas/FarmNewRequest.yaml), [draft operation](./Farm_GET_POST.yaml), [governing RFC](../../RFCs/RFC-069-Farm.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
