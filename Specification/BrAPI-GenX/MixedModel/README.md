# BrAPI-GenX — Mixed Model (Scientific Compute)

Mixed model results record variance components and BLUPs from mixed model
analysis. BrAPI v2.1 has no mixed model result record.

- `POST /genx/v1/mixed-model-results` (`genxRecordMixedModelResult`) registers one
  `MixedModelResult` (`Schemas/MixedModelResultNewRequest.yaml`). Same
  `mixedModelResultDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/mixed-model-results` (`genxListMixedModelResults`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/mixed-model-results/{mixedModelResultDbId}`
  (`genxGetMixedModelResult`) retrieves one result.

Details and falsifiers: `../RFC-048-Mixed-Model.md`.