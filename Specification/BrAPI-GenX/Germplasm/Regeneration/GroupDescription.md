# Group Regeneration

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 036; not a scientifically validated conservation outcome, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently implemented persistent service.

The proposed `RegenerationRecord` record carries a namespaced identity, required fields according to its source schema, and a lifecycle state with optional supersession and provenance. The register, list and retrieve operations are candidate contracts; idempotent replay and immutable record claims remain unverified against an independently deployed persistent implementation.

**Conservation, material identity and experimental evidence boundaries:** The mandatory seedLotDbId, timestamp and method label do not prove successful multiplication, genetic identity or purity, seed-lot mass balance, accession continuity, pollen isolation, harvest outcomes, population bottleneck management or viability improvement. Quantity and units are optional. A regeneration event is not an automatic inventory increase or a verified source-to-progeny relationship. The source proposal still defers questions beginning at D-106. Optional or plain-string seed-lot identifiers should not be treated as independently checked custody, germplasm provenance, facility ownership, transactional inventory movement or authoritative biological test results.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/RegenerationRecord.yaml), [registration request](./Schemas/RegenerationRecordNewRequest.yaml), [draft operations](./Regeneration_GET_POST.yaml), [RFC](../../RFCs/RFC-036-Regeneration.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
