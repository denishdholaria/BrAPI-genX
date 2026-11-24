# Group Quarantine

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 030, not an accepted material transfer, phytosanitary decision, official Breeding Application Programming Interface (BrAPI) version 2.1 inventory contract, or independently verified persistent implementation.

The `QuarantineRecord` candidate includes a namespaced record identity and lifecycle state, with scientific/operational fields and provenance as defined by its source schema. Its proposed register, list and retrieve routes specify provisional immutable-revision and retry semantics; those are not evidence of an authenticated material operation.

**Biological material, authorization, custody and transaction boundaries:** SeedLot identity, quarantine timestamp and reason are required, but a released status does not require a releasedAt timestamp, laboratory clearance, inspector authorization, specimen testing, movement restriction policy or jurisdiction. A recorded release claim does not demonstrate phytosanitary compliance, and no typed ViabilityTest or diagnostic link exists. Existing deferred questions begin at D-87; any operation-neighbor link is advisory navigation, not a typed foreign key, laboratory finding or legal authority.

**Sources:** [module overview](./README.md), [record schema](./Schemas/QuarantineRecord.yaml), [registration request](./Schemas/QuarantineRecordNewRequest.yaml), [draft operation](./Quarantine_GET_POST.yaml), [RFC](../../RFCs/RFC-030-Quarantine.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
