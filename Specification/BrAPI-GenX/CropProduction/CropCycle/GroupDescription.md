# Group CropCycle

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 029, not an approved crop management rule, official Breeding Application Programming Interface (BrAPI) version 2.1 extension, or independently verified conformance.

The candidate `CropCycle` record defines a namespaced identifier and a lifecycle status; optional `supersedes` and provenance may accompany its basic descriptive fields. It proposes register, list and retrieve operations, but immutable-publication and retry claims are not a replacement for independent test evidence. The schema—not examples or operation names—determines requiredness.

**Temporal, scientific and authority boundaries:** The `plantingDate`, `harvestDate`, `cropName`, Location and Study identifiers are all optional. Status `completed` does not establish that planting and harvest events occurred or satisfy an independently verified cropping interval. There is no typed HarvestRecord link (D-85) or validated crop taxonomy (D-86). The governing Request for Comments (RFC) leaves D-84 and related requirements unresolved. No advisory-navigation link establishes a typed experimental identity, scientific conclusion, regulatory obligation or actual field operation.

**Sources:** [module overview](./README.md), [record schema](./Schemas/CropCycle.yaml), [registration schema](./Schemas/CropCycleNewRequest.yaml), [operation draft](./CropCycle_GET_POST.yaml), [RFC](../../RFCs/RFC-029-Crop-Cycle.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
