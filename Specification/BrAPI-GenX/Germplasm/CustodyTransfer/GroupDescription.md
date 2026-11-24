# Group CustodyTransfer

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 063, not an accepted material transfer, phytosanitary decision, official Breeding Application Programming Interface (BrAPI) version 2.1 inventory contract, or independently verified persistent implementation.

The `CustodyTransfer` candidate includes a namespaced record identity and lifecycle state, with scientific/operational fields and provenance as defined by its source schema. Its proposed register, list and retrieve routes specify provisional immutable-revision and retry semantics; those are not evidence of an authenticated material operation.

**Biological material, authorization, custody and transaction boundaries:** Both sampleDbId and lotDbId, sending/receiving party, transfer timestamp and received condition are optional; only transfer identity and lifecycle status are required. A status of accepted is not a verified receiving-party signature, legal ownership transfer, authenticated evidence of custody, audit-ready actor identity or physical movement. The proposed pending-to-accepted/rejected rule is not guaranteed by a schema. Existing deferred questions begin at D-187; any operation-neighbor link is advisory navigation, not a typed foreign key, laboratory finding or legal authority.

**Sources:** [module overview](./README.md), [record schema](./Schemas/CustodyTransfer.yaml), [registration request](./Schemas/CustodyTransferNewRequest.yaml), [draft operation](./CustodyTransfer_GET_POST.yaml), [RFC](../../RFCs/RFC-063-Custody-Transfer.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
