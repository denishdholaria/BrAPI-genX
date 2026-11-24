# Group PersonReference

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 097; not an authenticated identity directory, authorization contract, or replacement for official Breeding Application Programming Interface (BrAPI) version 2.1 `People` resources.

The proposal defines an immutable `PersonReference` metadata entry with namespaced `personReferenceDbId`, required lifecycle `status` (`active`, `superseded`, `withdrawn`), and optional `name`, `role`, `supersedes`, and provenance. Proposed GenX operations register, list by optional status, and retrieve records, with replay/conflict behavior remaining an unverified candidate.

**Boundaries:** Official BrAPI already has `/brapi/v2/people` for person records. The GenX draft defines no typed association with official `personDbId` or with GenX `Project` (D-291). Its `role` string is neither an access-control grant nor evidence of employment, consent, or permission to disclose personal details. `name` and `role` requiredness remain open (D-289–D-290). Scientific attribution, subject identity, privacy policy and authentication must not be inferred from a matching display name.

**Sources:** [GenX module overview](./README.md), [candidate record schema](./Schemas/PersonReference.yaml), [registration schema](./Schemas/PersonReferenceNewRequest.yaml), [draft operations](./PersonReference_GET_POST.yaml), [RFC-097](../../RFCs/RFC-097-Person-Reference.md), [official BrAPI People](../../../BrAPI-Core/People/README.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
