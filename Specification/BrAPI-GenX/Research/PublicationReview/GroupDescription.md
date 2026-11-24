# Group PublicationReview

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 120; not proof of independent research asset validity, reproducibility, scholarly acceptance or enforced access permissions.

The proposed `PublicationReview` record defines an independent namespaced identifier, lifecycle `status` and optional descriptive metadata, `supersedes` and provenance. Draft operations register, list and retrieve metadata. Their replay and immutable-publication descriptions are candidate rules, not verified persistent service behavior.

**Scientific evidence, archival and access boundaries:** The schema has an optional title, publicationType, venue and year but no persistent scholarly identifier, published manuscript version, reviewer identity, decision, review criteria, editorial workflow, editorial status or journal-verifiable source. Its lifecycle status active/superseded/withdrawn must not be interpreted as peer-review acceptance or publication approval. Decisions beginning at D-358, together with the other open questions in the governing RFC, remain unresolved. The presence of a record and advisory operation links does not create a typed scientific correspondence, immutable bytes, rights grant or editorial approval.

**Sources:** [module overview](./README.md), [record schema](./Schemas/PublicationReview.yaml), [registration request](./Schemas/PublicationReviewNewRequest.yaml), [candidate operations](./PublicationReview_GET_POST.yaml), [RFC](../../RFCs/RFC-120-PublicationReview.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
