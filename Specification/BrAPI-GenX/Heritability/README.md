# BrAPI-GenX — Heritability (Scientific Compute)

Heritability estimates record the estimated heritability for a trait within a
study. BrAPI v2.1 has no heritability record.

- `POST /genx/v1/heritability-estimates` (`genxRecordHeritability`) registers one
  `HeritabilityEstimate` (`Schemas/HeritabilityEstimateNewRequest.yaml`). Same
  `heritabilityEstimateDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/heritability-estimates` (`genxListHeritabilityEstimates`) lists estimates,
  optionally filtered by method, study, or status.
- `GET /genx/v1/heritability-estimates/{heritabilityEstimateDbId}`
  (`genxGetHeritabilityEstimate`) retrieves one estimate.

Details and falsifiers: `../RFC-050-Heritability.md`.