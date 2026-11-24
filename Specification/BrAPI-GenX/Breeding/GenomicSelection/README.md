# BrAPI-GenX — Genomic Selection (Scientific Compute)

GenomicSelection proposes a candidate selection-result record, not an
authorized breeder's decision. `selectedGermplasm` and `selectionThreshold`
are optional; neither defines a validated population, index, authority or
consistent measurement scale.

The separate GenX `SelectionDecision` resource describes an actual verdict,
whereas a candidate selection result cannot establish official advancement.
Official BrAPI version 2.1 contracts remain unchanged.

- `POST /genx/v1/genomic-selections` (`genxRecordGenomicSelection`) registers one
  `GenomicSelection` (`Schemas/GenomicSelectionNewRequest.yaml`). Same
  `genomicSelectionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-selections` (`genxListGenomicSelections`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/genomic-selections/{genomicSelectionDbId}`
  (`genxGetGenomicSelection`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-055-Genomic-Selection.md`.