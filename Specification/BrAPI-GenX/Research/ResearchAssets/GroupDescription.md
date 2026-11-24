# Group ResearchAssets

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 016; not proof of independent research asset validity, reproducibility, scholarly acceptance or enforced access permissions.

The proposed `ResearchAsset` record defines an independent namespaced identifier, lifecycle `status` and optional descriptive metadata, `supersedes` and provenance. Draft operations register, list and retrieve metadata. Their replay and immutable-publication descriptions are candidate rules, not verified persistent service behavior.

**Scientific evidence, archival and access boundaries:** The record permits draft/published/superseded/withdrawn statuses and optional accessPolicy, license, embargoUntil, persistentIdentifier and fairPackageDbId. A recorded identifier is not a minted or independently resolved DOI. A documented license/embargo state is not enforcement of data access, a public repository release, scientific validity, or a FAIR package payload. No direct typed link to BrAPI data resources is defined. Decisions beginning at D-45, together with the other open questions in the governing RFC, remain unresolved. The presence of a record and advisory operation links does not create a typed scientific correspondence, immutable bytes, rights grant or editorial approval.

**Sources:** [module overview](./README.md), [record schema](./Schemas/ResearchAsset.yaml), [registration request](./Schemas/ResearchAssetNewRequest.yaml), [candidate operations](./ResearchAssets_GET_POST.yaml), [RFC](../../RFCs/RFC-016-Research-Assets.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
