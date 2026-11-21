# BrAPI-GenX — Variant Annotation (Genomics)

Variant annotation records describe variant functional annotations and provenance.
BrAPI v2.1 has no variant annotation record.

- `POST /genx/v1/variant-annotations` (`genxRecordVariantAnnotation`) registers one
  `VariantAnnotation` (`Schemas/VariantAnnotationNewRequest.yaml`). Same
  `variantAnnotationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/variant-annotations` (`genxListVariantAnnotations`) lists annotations,
  optionally filtered by method, study, or status.
- `GET /genx/v1/variant-annotations/{variantAnnotationDbId}`
  (`genxGetVariantAnnotation`) retrieves one annotation.

Details and falsifiers: `../../RFCs/RFC-062-Variant-Annotation.md`.