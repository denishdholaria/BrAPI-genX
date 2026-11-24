# Group AssayExecution

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 113. Registration metadata is not evidence of completed genotyping, validated results or an independently verified service.

The `AssayExecution` response schema requires only assayExecutionDbId and lifecycle status. The registration request requires only assayExecutionDbId. `assayDbId` is optional and differs in name from AssayDesign's `assayDesignDbId`; the schema does not enforce equality, existence or resolution of these identifiers. It does not require an execution timestamp, sample identifier, instrument, run conditions, raw-data reference, assay outcome, quality metrics or GenomicDataset/VendorOrder link.

**Scientific and provenance boundary:** An execution record does not prove that wet-laboratory work took place or that a BrAPI Sample yielded a CallSet, Call or VariantSet. GenX operation neighbors are advisory navigation, not typed scientific relationships. Deferred decisions D-337–D-339 remain open; immutable-revision and replay language describes a candidate contract, not tested persistence or authorized laboratory evidence.

**Sources:** [module overview](./README.md), [record schema](./Schemas/AssayExecution.yaml), [registration schema](./Schemas/AssayExecutionNewRequest.yaml), [operation](./AssayExecution_GET_POST.yaml), [design schema](../AssayDesign/Schemas/AssayDesign.yaml), [RFC](../../RFCs/RFC-113-Assay-Execution.md), [official call sets](../../../BrAPI-Genotyping/CallSets/CallSets_GET.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
