# BrAPI-GenX — Assay Design (Genomics)

Assay design records describe genotyping assay designs and provenance.
BrAPI v2.1 has no assay design record.

- `POST /genx/v1/assay-designs` (`genxRecordAssayDesign`) registers one
  `AssayDesign` (`Schemas/AssayDesignNewRequest.yaml`). Same
  `assayDesignDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/assay-designs` (`genxListAssayDesigns`) lists designs,
  optionally filtered by method, study, or status.
- `GET /genx/v1/assay-designs/{assayDesignDbId}`
  (`genxGetAssayDesign`) retrieves one design.

Details and falsifiers: `../../RFCs/RFC-061-Assay-Design.md`.