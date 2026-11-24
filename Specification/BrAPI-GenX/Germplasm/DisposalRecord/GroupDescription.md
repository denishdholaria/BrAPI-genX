# Group DisposalRecord

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 065, not an accepted material transfer, phytosanitary decision, official Breeding Application Programming Interface (BrAPI) version 2.1 inventory contract, or independently verified persistent implementation.

The `DisposalRecord` candidate includes a namespaced record identity and lifecycle state, with scientific/operational fields and provenance as defined by its source schema. Its proposed register, list and retrieve routes specify provisional immutable-revision and retry semantics; those are not evidence of an authenticated material operation.

**Biological material, authorization, custody and transaction boundaries:** Sample and lot identifiers, disposal reason, method, timestamp and quantity are all optional; quantity has no direct unit field. The completed lifecycle label is a claimed disposal, not a cryptographic proof of destruction or authorized destruction order. Disposal cannot automatically decrement the authoritative seed-lot ledger or prove a regulated phytosanitary procedure occurred. Existing deferred questions begin at D-193; any operation-neighbor link is advisory navigation, not a typed foreign key, laboratory finding or legal authority.

**Sources:** [module overview](./README.md), [record schema](./Schemas/DisposalRecord.yaml), [registration request](./Schemas/DisposalRecordNewRequest.yaml), [draft operation](./DisposalRecord_GET_POST.yaml), [RFC](../../RFCs/RFC-065-Disposal-Record.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
