# BrAPI-GenX — Genomic Prediction (Scientific Compute)

Genomic prediction results record predicted breeding values (e.g. GEBVs)
for germplasm. BrAPI v2.1 has no genomic prediction result record.

- `POST /genx/v1/genomic-predictions` (`genxRecordGenomicPrediction`) registers one
  `GenomicPrediction` (`Schemas/GenomicPredictionNewRequest.yaml`). Same
  `genomicPredictionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genomic-predictions` (`genxListGenomicPredictions`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/genomic-predictions/{genomicPredictionDbId}`
  (`genxGetGenomicPrediction`) retrieves one result.

Details and falsifiers: `../RFC-054-Genomic-Prediction.md`.