# Group Acquisition

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 041, not an accepted material transfer, phytosanitary decision, official Breeding Application Programming Interface (BrAPI) version 2.1 inventory contract, or independently verified persistent implementation.

The `AcquisitionRecord` candidate includes a namespaced record identity and lifecycle state, with scientific/operational fields and provenance as defined by its source schema. Its proposed register, list and retrieve routes specify provisional immutable-revision and retry semantics; those are not evidence of an authenticated material operation.

**Biological material, authorization, custody and transaction boundaries:** The required SeedLot string, date and source only record an asserted intake. The schema does not contain a controlled accession source, documented material identity, collecting permit, phytosanitary inspection, declared quantity, receipt verification or typed link to CollectingMission/QuarantineRecord. A registration is not a seed-lot transaction or proof that material was received. Existing deferred questions begin at D-121; any operation-neighbor link is advisory navigation, not a typed foreign key, laboratory finding or legal authority.

**Sources:** [module overview](./README.md), [record schema](./Schemas/AcquisitionRecord.yaml), [registration request](./Schemas/AcquisitionRecordNewRequest.yaml), [draft operation](./Acquisition_GET_POST.yaml), [RFC](../../RFCs/RFC-041-Acquisition.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
