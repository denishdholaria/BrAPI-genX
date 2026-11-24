# BrAPI-GenX — Genomic Prediction (Scientific Compute)

GenomicPrediction proposes metadata for predicted breeding values, not
independently validated genomic estimated breeding values (GEBVs).
`predictions`, `accuracy`, trait, study and provenance are optional. The
prediction map is unconstrained and the accuracy number has no prescribed
estimation protocol, validation population or interpretation range.

Official BrAPI version 2.1 contracts remain unchanged. A prediction record
is not an authorized breeding selection decision or evidence of calibrated
out-of-sample accuracy.

- `POST /genx/v1/genomic-predictions` (`genxRecordGenomicPrediction`) registers one
  `GenomicPrediction` (`Schemas/GenomicPredictionNewRequest.yaml`). Same
  `genomicPredictionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-predictions` (`genxListGenomicPredictions`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/genomic-predictions/{genomicPredictionDbId}`
  (`genxGetGenomicPrediction`) retrieves one result.

Details and falsifiers: `../../RFCs/RFC-054-Genomic-Prediction.md`.