# Group CommonCropName

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 094; not a replacement for the official Breeding Application Programming Interface (BrAPI) version 2.1 `GET /brapi/v2/commoncropnames` operation.

This group proposes a namespaced, immutable `CommonCropName` metadata entry with required `commonCropNameDbId` and `status` (`active`, `superseded`, `withdrawn`). `scientificName`, `commonName`, `supersedes`, and provenance are optional in the current schema. Proposed GenX operations register, list by optional status, and retrieve entries; identical record replay and changed-content conflict remain draft promises.

**Boundaries:** The official `/brapi/v2/commoncropnames` call already describes supported crops in a BrAPI server. It must not be confused with the separate proposed namespaced metadata record or with a controlled taxonomic authority. The draft lacks typed links to official BrAPI Germplasm or GenX `TaxonName` (D-282); requiredness of scientific and common names is unresolved (D-280–D-281). A matching crop name does not, by itself, identify a scientific taxon or prove two sources use identical naming conventions. The official resource source is at `Specification/BrAPI-Core/Common Crop Names/CommonCropNames_GET.yaml`.

**Sources:** [GenX module overview](./README.md), [candidate record schema](./Schemas/CommonCropName.yaml), [registration schema](./Schemas/CommonCropNameNewRequest.yaml), [draft operations](./CommonCropName_GET_POST.yaml), [RFC-094](../../RFCs/RFC-094-Common-Crop-Name.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
