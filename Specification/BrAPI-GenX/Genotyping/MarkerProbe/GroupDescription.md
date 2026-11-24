# Group MarkerProbe

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 071. This proposal does not constitute an official BrAPI marker identity, verified biological probe, or independently verified assay result.

Official BrAPI v2.1 models variants and marker positions. In the official `/brapi/v2/markerpositions` operation, the identifying query field is `variantDbId`, not the GenX `markerDbId`. The proposed MarkerProbe response requires markerProbeDbId and status, and the registration request requires only markerProbeDbId. markerDbId, probeSequence and platform are optional free-text fields. There is no validated relationship or identity mapping from `markerDbId` to a BrAPI Variant or marker position; the sequence is neither format-constrained nor verified to bind a target or represent a deployable oligonucleotide.

**Scope boundary:** Publishing a probe's descriptive record is not proof of assay design, assay execution, marker specificity, vendor supply, or analytical validity. D-211–D-213 remain open, and operation-neighbor references are advisory rather than typed foreign keys. The immutable-record and idempotent-retry semantics remain candidate behavior.

**Sources:** [module overview](./README.md), [record schema](./Schemas/MarkerProbe.yaml), [registration schema](./Schemas/MarkerProbeNewRequest.yaml), [operation](./MarkerProbe_GET_POST.yaml), [RFC](../../RFCs/RFC-071-Marker-Probe.md), [official marker positions](../../../BrAPI-Genotyping/GenomeMaps/MarkerPositions_GET.yaml), [official variants](../../../BrAPI-Genotyping/Variants/Variants_GET.yaml), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
