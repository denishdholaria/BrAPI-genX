# BrAPI-GenX — Heritability (Scientific Compute)

HeritabilityEstimate proposes a separately identified statistical estimate, not
a validated or universally comparable heritability parameter. Its `traitDbId`,
`studyDbId`, `heritabilityValue`, job reference and provenance are optional.
The value is a bare number without a standardized heritability estimand,
variance-component definition or uncertainty model.

Official BrAPI version 2.1 resources are unchanged. Method identity does not
prove a version-bound analysis was run or its scientific assumptions verified.

- `POST /genx/v1/heritability-estimates` (`genxRecordHeritability`) registers one
  `HeritabilityEstimate` (`Schemas/HeritabilityEstimateNewRequest.yaml`). Same
  `heritabilityEstimateDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/heritability-estimates` (`genxListHeritabilityEstimates`) lists estimates,
  optionally filtered by method, study, or status.
- `GET /genx/v1/heritability-estimates/{heritabilityEstimateDbId}`
  (`genxGetHeritabilityEstimate`) retrieves one estimate.

Details and falsifiers: `../../RFCs/RFC-050-Heritability.md`.