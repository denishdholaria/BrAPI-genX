# Group HumanReview

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 136; not approved research governance, independently validated model evidence, or official Breeding Application Programming Interface (BrAPI) version 2.1 conformance.

The candidate `HumanReview` record defines a namespaced identifier, a required lifecycle `status` and optional descriptive content, `supersedes` and provenance. It offers draft register/list/retrieve operations. Immutable-publication and replay guarantees are proposed, not proven against a real persistent and independently implemented service.

**Evidence, reproducibility and human authority boundaries:** The optional reviewer and reviewDecision are free strings without authenticated actor identity, identity-provider binding, decision target, role/authorization policy, nonrepudiation proof, or target revision reference. An `accepted` example is not evidence of an authorized or independently evaluated scientific approval. An operation or historical navigation neighbor does not establish scientific identity, validated causality, evidence sufficiency or permission to act. The questions beginning at D-406 remain unratified.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/HumanReview.yaml), [registration schema](./Schemas/HumanReviewNewRequest.yaml), [draft operation](./HumanReview_GET_POST.yaml), [governing RFC](../../RFCs/RFC-136-HumanReview.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
