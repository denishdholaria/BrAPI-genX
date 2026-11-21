# BrAPI-GenX — Research Location (Reference Data)

Research location records describe research locations.
BrAPI v2.1 has no research location record.

- `POST /genx/v1/research-locations` (`genxRegisterResearchLocation`) registers one
  `ResearchLocation` (`Schemas/ResearchLocationNewRequest.yaml`). Same
  `researchLocationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/research-locations` (`genxListResearchLocations`) lists records,
  optionally filtered by status.
- `GET /genx/v1/research-locations/{researchLocationDbId}`
  (`genxGetResearchLocation`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-100-Research-Location.md`.
