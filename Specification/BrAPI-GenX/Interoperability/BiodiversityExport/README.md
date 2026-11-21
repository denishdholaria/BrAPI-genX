# BrAPI-GenX — BiodiversityExport

BiodiversityExport records describe BiodiversityExport entries.
BrAPI v2.1 has no BiodiversityExport record.

- `POST /genx/v1/biodiversity-exports` (`genxRegisterBiodiversityExport`) registers one
  `BiodiversityExport` (`Schemas/BiodiversityExportNewRequest.yaml`). Same
  `biodiversityExportDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/biodiversity-exports` (`genxListBiodiversityExports`) lists records,
  optionally filtered by status.
- `GET /genx/v1/biodiversity-exports/{biodiversityExportDbId}`
  (`genxGetBiodiversityExport`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-121-BiodiversityExport.md`.
