# BrAPI-GenX — Kinship (Scientific Compute)

Kinship matrices record relationship matrices used in genomic analysis.
BrAPI v2.1 has no kinship record.

- `POST /genx/v1/kinship-matrices` (`genxRegisterKinshipMatrix`) registers one
  `KinshipMatrix` (`Schemas/KinshipMatrixNewRequest.yaml`). Same
  `kinshipMatrixDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/kinship-matrices` (`genxListKinshipMatrices`) lists matrices,
  optionally filtered by method, study, or status.
- `GET /genx/v1/kinship-matrices/{kinshipMatrixDbId}`
  (`genxGetKinshipMatrix`) retrieves one matrix.

Details and falsifiers: `../../RFCs/RFC-052-Kinship.md`.