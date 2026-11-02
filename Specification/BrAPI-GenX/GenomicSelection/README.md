# BrAPI-GenX — Genomic Selection (Scientific Compute)

Genomic selection results record selected germplasm and selection indices.
BrAPI v2.1 has no genomic selection result record.

- `POST /genx/v1/genomic-selections` (`genxRecordGenomicSelection`) registers one
  `GenomicSelection` (`Schemas/GenomicSelectionNewRequest.yaml`). Same
  `genomicSelectionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-selections` (`genxListGenomicSelections`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/genomic-selections/{genomicSelectionDbId}`
  (`genxGetGenomicSelection`) retrieves one result.

Details and falsifiers: `../RFC-055-Genomic-Selection.md`.