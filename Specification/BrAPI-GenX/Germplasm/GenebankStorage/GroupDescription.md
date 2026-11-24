# Group GenebankStorage

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 015; not a scientifically validated conservation outcome, official Breeding Application Programming Interface (BrAPI) version 2.1 resource, or independently implemented persistent service.

The proposed `StorageLocation` record carries a namespaced identity, required fields according to its source schema, and a lifecycle state with optional supersession and provenance. The register, list and retrieve operations are candidate contracts; idempotent replay and immutable record claims remain unverified against an independently deployed persistent implementation.

**Conservation, material identity and experimental evidence boundaries:** The storage facility and status are required, while capacity, currentCount, temperature, humidity and their units are optional. No monitored environmental time series, sensor calibration, seed-lot inventory placement, chain of custody, equipment alarms or stock conservation assurance is represented. A location-level condition is not evidence that a particular seed lot has been stored at that temperature. The source proposal still defers questions beginning at D-42. Optional or plain-string seed-lot identifiers should not be treated as independently checked custody, germplasm provenance, facility ownership, transactional inventory movement or authoritative biological test results.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/StorageLocation.yaml), [registration request](./Schemas/StorageLocationNewRequest.yaml), [draft operations](./GenebankStorage_GET_POST.yaml), [RFC](../../RFCs/RFC-015-Genebank-Storage.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
