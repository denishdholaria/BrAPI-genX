# Group DuplicateReview

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 104, not an accepted material transfer, phytosanitary decision, official Breeding Application Programming Interface (BrAPI) version 2.1 inventory contract, or independently verified persistent implementation.

The `DuplicateReview` candidate includes a namespaced record identity and lifecycle state, with scientific/operational fields and provenance as defined by its source schema. Its proposed register, list and retrieve routes specify provisional immutable-revision and retry semantics; those are not evidence of an authenticated material operation.

**Biological material, authorization, custody and transaction boundaries:** The candidateDbId and decision are optional free strings, with no compared second accession, normalized identifier authority, reviewer identity, molecular or morphological match evidence, quality threshold or conflict resolution. A confirmed-duplicate example is not proof of material identity or authority to merge accessions. Existing deferred questions begin at D-310; any operation-neighbor link is advisory navigation, not a typed foreign key, laboratory finding or legal authority.

**Sources:** [module overview](./README.md), [record schema](./Schemas/DuplicateReview.yaml), [registration request](./Schemas/DuplicateReviewNewRequest.yaml), [draft operation](./DuplicateReview_GET_POST.yaml), [RFC](../../RFCs/RFC-104-Duplicate-Review.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
