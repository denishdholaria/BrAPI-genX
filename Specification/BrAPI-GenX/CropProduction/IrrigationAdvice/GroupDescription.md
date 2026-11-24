# Group IrrigationAdvice

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 131, not an approved agronomic decision model, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently demonstrated persistent-service implementation.

The proposed `IrrigationAdvice` record has a namespaced identifier and lifecycle `status`, optional `supersedes` and provenance metadata, and candidate register/list/retrieve operations. Data-field requiredness differs among these drafts, and the schema is the authority for actual required properties. Idempotent replay and immutable revision claims remain proposed behavior, not proof of a running service.

**Scientific boundaries:** The recommendedAmount is a free-text optional string; frequency, region and crop type have no governed time, area or crop identity semantics. This is not a validated irrigation schedule, water budget, legal allocation, or record of an application. It has no typed relationship to IrrigationEvent, weather observations, soil-water balance, or authoritative research evidence. Outstanding questions start at D-391 and remain unratified. Adjacent operation names do not confer typed links, biological equivalence, or actual field intervention evidence.

**Sources:** [module overview](./README.md), [candidate schema](./Schemas/IrrigationAdvice.yaml), [registration schema](./Schemas/IrrigationAdviceNewRequest.yaml), [draft operations](./IrrigationAdvice_GET_POST.yaml), [RFC](../../RFCs/RFC-131-IrrigationAdvice.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
