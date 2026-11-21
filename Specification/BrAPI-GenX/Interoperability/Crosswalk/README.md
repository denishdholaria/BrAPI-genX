# BrAPI-GenX — Crosswalk (Germplasm)

Crosswalk records describe crosswalks between systems.
BrAPI v2.1 has no crosswalk record.

- `POST /genx/v1/crosswalks` (`genxRegisterCrosswalk`) registers one
  `Crosswalk` (`Schemas/CrosswalkNewRequest.yaml`). Same
  `crosswalkDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/crosswalks` (`genxListCrosswalks`) lists records,
  optionally filtered by status.
- `GET /genx/v1/crosswalks/{crosswalkDbId}`
  (`genxGetCrosswalk`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-105-Crosswalk.md`.
