# BrAPI-GenX — Collecting Mission (Germplasm)

Collecting mission records describe collecting missions.
BrAPI v2.1 has no collecting mission record.

- `POST /genx/v1/collecting-missions` (`genxRegisterCollectingMission`) registers one
  `CollectingMission` (`Schemas/CollectingMissionNewRequest.yaml`). Same
  `collectingMissionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/collecting-missions` (`genxListCollectingMissions`) lists records,
  optionally filtered by status.
- `GET /genx/v1/collecting-missions/{collectingMissionDbId}`
  (`genxGetCollectingMission`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-101-Collecting-Mission.md`.
