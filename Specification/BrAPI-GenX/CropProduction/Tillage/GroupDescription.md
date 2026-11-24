# Group Tillage

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 038, not an approved agronomic decision model, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently demonstrated persistent-service implementation.

The proposed `TillageRecord` record has a namespaced identifier and lifecycle `status`, optional `supersedes` and provenance metadata, and candidate register/list/retrieve operations. Data-field requiredness differs among these drafts, and the schema is the authority for actual required properties. Idempotent replay and immutable revision claims remain proposed behavior, not proof of a running service.

**Scientific boundaries:** The required tillage timestamp and method describe a claimed soil-management operation; optional numeric depth and free-text unit do not prove a calibrated working depth or soil response. Optional Study/Location identifiers do not enforce experiment or field ownership. No SoilProfile relationship or verification of equipment/area is present; a tillage event is not a soil-measurement result. Outstanding questions start at D-112 and remain unratified. Adjacent operation names do not confer typed links, biological equivalence, or actual field intervention evidence.

**Sources:** [module overview](./README.md), [candidate schema](./Schemas/TillageRecord.yaml), [registration schema](./Schemas/TillageRecordNewRequest.yaml), [draft operations](./Tillage_GET_POST.yaml), [RFC](../../RFCs/RFC-038-Tillage.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
