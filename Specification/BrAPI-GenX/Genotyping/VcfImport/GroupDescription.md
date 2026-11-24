# Group VcfImport

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 043; neither an implemented Variant Call Format (VCF) importer nor an official Breeding Application Programming Interface (BrAPI) version 2.1 VariantSet operation.

The proposed registration and listing of immutable import metadata uses required `vcfImportDbId`, `genomicDatasetDbId`, `importedAt`, `sourceFormat`, and `status`. Optional `sourceFile`, `variantCount`, `sampleCount`, `supersedes` and provenance describe the candidate record. Identical-body replay and conflict-on-change are proposed behavior without persistent service verification.

**Boundaries:** The candidate **does explicitly include** a string `genomicDatasetDbId` field naming a GenX dataset; it must not be misreported as an absent link, nor confused with checked referential integrity. Official BrAPI already models VariantSets and reference genomes. Registering an import description does not prove a VCF file existed, was parsed correctly, matched the target assembly, or was transactionally ingested. A typed GenX VariantMatrix reference is absent (D-128); sourceFile requiredness (D-127) and sourceFormat governance (D-129) remain unresolved.

**Sources:** [candidate overview](./README.md), [candidate schema](./Schemas/VcfImport.yaml), [registration request](./Schemas/VcfImportNewRequest.yaml), [draft operations](./VcfImport_GET_POST.yaml), [RFC-043](../../RFCs/RFC-043-Vcf-Import.md), [official BrAPI VariantSets](../../../BrAPI-Genotyping/VariantSets/README.md), [official BrAPI ReferenceSets](../../../BrAPI-Genotyping/ReferenceSets/README.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
