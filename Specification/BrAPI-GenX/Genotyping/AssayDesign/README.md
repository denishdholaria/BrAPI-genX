# BrAPI-GenX — Assay Design (Genomics)

AssayDesign proposes metadata for a genotyping assay design, distinct
from BrAPI version 2.1 Samples, Variants and genotype results. The
optional analysisMethodDbId is not a verified join; the design schema has
no GenomicDataset or MarkerProbe reference.

- `POST /genx/v1/assay-designs` (`genxRecordAssayDesign`) registers one
  `AssayDesign` (`Schemas/AssayDesignNewRequest.yaml`). Same
  `assayDesignDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/assay-designs` (`genxListAssayDesigns`) lists designs,
  optionally filtered by method, study, or status.
- `GET /genx/v1/assay-designs/{assayDesignDbId}`
  (`genxGetAssayDesign`) retrieves one design.

Details and falsifiers: `../../RFCs/RFC-061-Assay-Design.md`.