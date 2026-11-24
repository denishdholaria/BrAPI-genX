# BrAPI-GenX — Collecting Mission (Germplasm)

Collecting mission records describe collecting missions.
Official BrAPI version 2.1 Germplasm Multi-Crop Passport Descriptors (MCPD) data already includes `collectingMissionIdentifier`. This draft proposes a separate CollectingMission metadata record, but it does not establish a typed germplasm membership, mission participants, expedition provenance or a demonstrated need for a new identifier.

- `POST /genx/v1/collecting-missions` (`genxRegisterCollectingMission`) registers one
  `CollectingMission` (`Schemas/CollectingMissionNewRequest.yaml`). Same
  `collectingMissionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/collecting-missions` (`genxListCollectingMissions`) lists records,
  optionally filtered by status.
- `GET /genx/v1/collecting-missions/{collectingMissionDbId}`
  (`genxGetCollectingMission`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-101-Collecting-Mission.md`.
