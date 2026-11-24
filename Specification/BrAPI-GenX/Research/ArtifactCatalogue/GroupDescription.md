# Group ArtifactCatalogue

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 118; not proof of independent research asset validity, reproducibility, scholarly acceptance or enforced access permissions.

The proposed `ArtifactCatalogue` record defines an independent namespaced identifier, lifecycle `status` and optional descriptive metadata, `supersedes` and provenance. Draft operations register, list and retrieve metadata. Their replay and immutable-publication descriptions are candidate rules, not verified persistent service behavior.

**Scientific evidence, archival and access boundaries:** The storageReference, version, digest and size are optional strings; the digest is not constrained to a complete SHA-256 checksum, and there is no integrity verification or dereference guarantee. A catalogue entry is not evidence that a dataset exists, is accessible, licensed, reproducible or identical to a claimed artifact; D-354 leaves the ResearchAsset link open. Decisions beginning at D-352, together with the other open questions in the governing RFC, remain unresolved. The presence of a record and advisory operation links does not create a typed scientific correspondence, immutable bytes, rights grant or editorial approval.

**Sources:** [module overview](./README.md), [record schema](./Schemas/ArtifactCatalogue.yaml), [registration request](./Schemas/ArtifactCatalogueNewRequest.yaml), [candidate operations](./ArtifactCatalogue_GET_POST.yaml), [RFC](../../RFCs/RFC-118-ArtifactCatalogue.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
