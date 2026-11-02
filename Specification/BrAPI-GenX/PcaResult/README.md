# BrAPI-GenX — PCA Result (Scientific Compute)

PCA results record principal component analysis outputs for a study or
dataset. BrAPI v2.1 has no PCA result record.

- `POST /genx/v1/pca-results` (`genxRecordPcaResult`) registers one
  `PcaResult` (`Schemas/PcaResultNewRequest.yaml`). Same
  `pcaResultDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/pca-results` (`genxListPcaResults`) lists results,
  optionally filtered by method, study, or status.
- `GET /genx/v1/pca-results/{pcaResultDbId}`
  (`genxGetPcaResult`) retrieves one result.

Details and falsifiers: `../RFC-053-Pca-Result.md`.