# BrAPI-GenX — Research Location (Reference Data)

Research location records describe research locations.
Official BrAPI v2.1 already provides `/brapi/v2/locations` and Location resources; the proposed GenX ResearchLocation identity is currently a draft duplicate without a typed mapping.

- `POST /genx/v1/research-locations` (`genxRegisterResearchLocation`) registers one
  `ResearchLocation` (`Schemas/ResearchLocationNewRequest.yaml`). Same
  `researchLocationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/research-locations` (`genxListResearchLocations`) lists records,
  optionally filtered by status.
- `GET /genx/v1/research-locations/{researchLocationDbId}`
  (`genxGetResearchLocation`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-100-Research-Location.md`.
