# Group CropSuitability

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 135, not an approved crop management rule, official Breeding Application Programming Interface (BrAPI) version 2.1 extension, or independently verified conformance.

The candidate `CropSuitability` record defines a namespaced identifier and a lifecycle status; optional `supersedes` and provenance may accompany its basic descriptive fields. It proposes register, list and retrieve operations, but immutable-publication and retry claims are not a replacement for independent test evidence. The schema—not examples or operation names—determines requiredness.

**Temporal, scientific and authority boundaries:** The optional suitabilityScore is a string, not a calibrated standardized score, and has no prescribed scale, uncertainty, validation dataset or reference conditions. Region, season and crop labels are also free text. A proposed suitability assessment is not a verified land classification or permission to plant. The governing Request for Comments (RFC) leaves D-403 and related requirements unresolved. No advisory-navigation link establishes a typed experimental identity, scientific conclusion, regulatory obligation or actual field operation.

**Sources:** [module overview](./README.md), [record schema](./Schemas/CropSuitability.yaml), [registration schema](./Schemas/CropSuitabilityNewRequest.yaml), [operation draft](./CropSuitability_GET_POST.yaml), [RFC](../../RFCs/RFC-135-CropSuitability.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
