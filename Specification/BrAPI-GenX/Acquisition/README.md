# BrAPI-GenX — Acquisition (Genebank Conservation)

Acquisition records capture the intake of conserved material into a genebank.
BrAPI v2.1 has germplasm and seed lots but no acquisition record.

- `POST /genx/v1/acquisitions` (`genxRecordAcquisition`) registers one
  `AcquisitionRecord` (`Schemas/AcquisitionRecordNewRequest.yaml`). Same
  `acquisitionRecordDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/acquisitions` (`genxListAcquisitions`) lists records,
  optionally filtered by seed lot or status.
- `GET /genx/v1/acquisitions/{acquisitionRecordDbId}`
  (`genxGetAcquisition`) retrieves one record.

Details and falsifiers: `../RFC-041-Acquisition.md`.