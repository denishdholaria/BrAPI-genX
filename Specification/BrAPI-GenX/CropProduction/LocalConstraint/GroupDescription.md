# Group LocalConstraint

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 139, not an approved crop management rule, official Breeding Application Programming Interface (BrAPI) version 2.1 extension, or independently verified conformance.

The candidate `LocalConstraint` record defines a namespaced identifier and a lifecycle status; optional `supersedes` and provenance may accompany its basic descriptive fields. It proposes register, list and retrieve operations, but immutable-publication and retry claims are not a replacement for independent test evidence. The schema—not examples or operation names—determines requiredness.

**Temporal, scientific and authority boundaries:** An optional constraintValue string and free-text constraintSource do not prove a legally binding restriction, competent authority, effective date, geographic jurisdiction, unit, precedence rule or enforceable policy decision. The current schema cannot support automatic enforcement and must not be represented as authoritative legal advice. The governing Request for Comments (RFC) leaves D-415 and related requirements unresolved. No advisory-navigation link establishes a typed experimental identity, scientific conclusion, regulatory obligation or actual field operation.

**Sources:** [module overview](./README.md), [record schema](./Schemas/LocalConstraint.yaml), [registration schema](./Schemas/LocalConstraintNewRequest.yaml), [operation draft](./LocalConstraint_GET_POST.yaml), [RFC](../../RFCs/RFC-139-LocalConstraint.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
