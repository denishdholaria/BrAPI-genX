# Group ReferenceAssembly

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 115. The record is not an official Breeding Application Programming Interface (BrAPI) version 2.1 ReferenceSet or an independently validated genome assembly.

The candidate uses required namespaced `referenceAssemblyDbId` and lifecycle `status`; `assemblyName`, `assemblyAccession`, `version`, `organism`, `supersedes` and provenance remain optional. Register/list/get and idempotent replay are proposed behaviors, not evidence of a deployed persistent implementation.

**Boundaries:** Official BrAPI version 2.1 already represents reference genomes with `ReferenceSet` resources comprising `Reference` contigs. The candidate has no typed BrAPI ReferenceSet or GenX GenomicDataset link (D-345), and a matching accession does not prove coordinate-space identity or reference sequence equivalence. Required accession (D-343), controlled accession vocabulary (D-344), and explicit dataset relationship (D-345) remain unresolved. Candidate metadata is not genomic reference authority or a mapping algorithm.

**Sources:** [module overview](./README.md), [candidate schema](./Schemas/ReferenceAssembly.yaml), [registration request](./Schemas/ReferenceAssemblyNewRequest.yaml), [draft operations](./ReferenceAssembly_GET_POST.yaml), [RFC-115](../../RFCs/RFC-115-Reference-Assembly.md), [official BrAPI ReferenceSets](../../../BrAPI-Genotyping/ReferenceSets/README.md), [official ReferenceSet schema](../../../BrAPI-Genotyping/ReferenceSets/Schemas/ReferenceSet.yaml), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
