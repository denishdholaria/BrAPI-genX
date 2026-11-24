# Group PipelineProvenance

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 116, not an independently verified execution trace or reproducible bioinformatics record.

The candidate requires namespaced `pipelineProvenanceDbId` and lifecycle `status`, but `pipelineName`, `pipelineVersion`, `parameters`, `inputs`, `outputs`, `supersedes` and provenance are optional. Same-identity replay and conflict are proposed contract semantics, not verified persistent service behavior.

**Boundaries:** This object describes possible computational pipeline metadata, **not a reference genome assembly**. Free-form input/output strings and optional parameters do not prove data lineage, tool checksums, environment identity, reproducibility, or actual execution. The schema has no typed GenX GenomicDataset link (D-348); whether parameters must be required (D-346) and version governed (D-347) remain unresolved. Official BrAPI genotyping resources retain their independent meanings.

**Sources:** [module overview](./README.md), [candidate schema](./Schemas/PipelineProvenance.yaml), [registration request](./Schemas/PipelineProvenanceNewRequest.yaml), [draft operations](./PipelineProvenance_GET_POST.yaml), [RFC-116](../../RFCs/RFC-116-Pipeline-Provenance.md), [official BrAPI ReferenceSets](../../../BrAPI-Genotyping/ReferenceSets/README.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
