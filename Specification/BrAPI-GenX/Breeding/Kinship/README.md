# BrAPI-GenX — Kinship (Scientific Compute)

KinshipMatrix proposes a registration record for relationship-matrix metadata,
not a verified or necessarily accessible matrix. The matrix location and
digest are optional; the contract does not require sample identities, matrix
dimensions, estimator details, or an exact method version.

Official BrAPI version 2.1 resources remain unchanged. A kinship matrix
must not be assumed equivalent to a separately registered genomic
relationship matrix or a pedigree-derived coefficient.

- `POST /genx/v1/kinship-matrices` (`genxRegisterKinshipMatrix`) registers one
  `KinshipMatrix` (`Schemas/KinshipMatrixNewRequest.yaml`). Same
  `kinshipMatrixDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/kinship-matrices` (`genxListKinshipMatrices`) lists matrices,
  optionally filtered by method, study, or status.
- `GET /genx/v1/kinship-matrices/{kinshipMatrixDbId}`
  (`genxGetKinshipMatrix`) retrieves one matrix.

Details and falsifiers: `../../RFCs/RFC-052-Kinship.md`.