# Group SowingWindow

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 130, not an approved crop management rule, official Breeding Application Programming Interface (BrAPI) version 2.1 extension, or independently verified conformance.

The candidate `SowingWindow` record defines a namespaced identifier and a lifecycle status; optional `supersedes` and provenance may accompany its basic descriptive fields. It proposes register, list and retrieve operations, but immutable-publication and retry claims are not a replacement for independent test evidence. The schema—not examples or operation names—determines requiredness.

**Temporal, scientific and authority boundaries:** The recommended sowing date and end date are optional plain strings without enforced date syntax or validated ordering. Region, crop and season have no defined authoritative identifiers or evidence of crop-climate suitability. A candidate sowing window is an advisory record, not proof of planting or a universally safe sowing date. The governing Request for Comments (RFC) leaves D-388 and related requirements unresolved. No advisory-navigation link establishes a typed experimental identity, scientific conclusion, regulatory obligation or actual field operation.

**Sources:** [module overview](./README.md), [record schema](./Schemas/SowingWindow.yaml), [registration schema](./Schemas/SowingWindowNewRequest.yaml), [operation draft](./SowingWindow_GET_POST.yaml), [RFC](../../RFCs/RFC-130-SowingWindow.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
