# BrAPI-GenX — Variant Annotation (Genomics)

VariantAnnotation proposes a separately identified functional-annotation record,
not an independently validated biological consequence. Its `variantDbId`,
`annotations`, method reference, and provenance are optional. The annotation
object has no standardized gene, transcript, allele, or effect vocabulary.

Official BrAPI version 2.1 `Variant` already offers flexible `additionalInfo`;
the GenX proposal is not a replacement for that metadata or a verified join.
Its scientific and lifecycle claims remain draft and require evidence.

- `POST /genx/v1/variant-annotations` (`genxRecordVariantAnnotation`) registers one
  `VariantAnnotation` (`Schemas/VariantAnnotationNewRequest.yaml`). Same
  `variantAnnotationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/variant-annotations` (`genxListVariantAnnotations`) lists annotations,
  optionally filtered by method, study, or status.
- `GET /genx/v1/variant-annotations/{variantAnnotationDbId}`
  (`genxGetVariantAnnotation`) retrieves one annotation.

Details and falsifiers: `../../RFCs/RFC-062-Variant-Annotation.md`.