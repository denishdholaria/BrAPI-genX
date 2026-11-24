# Group SafetyDuplication

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 034; not a scientifically validated conservation outcome, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently implemented persistent service.

The proposed `SafetyDuplication` record carries a namespaced identity, required fields according to its source schema, and a lifecycle state with optional supersession and provenance. The register, list and retrieve operations are candidate contracts; idempotent replay and immutable record claims remain unverified against an independently deployed persistent implementation.

**Conservation, material identity and experimental evidence boundaries:** Required seedLotDbId, backupSite and duplicatedAt capture a claim of backup storage but not third-party acknowledgment, shipping custody, stock availability, disaster-recovery accessibility, deposited quantity, legal rights or physical receipt. No typed StorageLocation or institution identity is present; an example backup-site name must not imply confirmed deposit at that facility. The source proposal still defers questions beginning at D-99. Optional or plain-string seed-lot identifiers should not be treated as independently checked custody, germplasm provenance, facility ownership, transactional inventory movement or authoritative biological test results.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/SafetyDuplication.yaml), [registration request](./Schemas/SafetyDuplicationNewRequest.yaml), [draft operations](./SafetyDuplication_GET_POST.yaml), [RFC](../../RFCs/RFC-034-Safety-Duplication.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
