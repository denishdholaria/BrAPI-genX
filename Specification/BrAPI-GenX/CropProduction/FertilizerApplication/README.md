# BrAPI-GenX — Fertilizer Application (Crop Production)

Fertilizer applications record nutrient application events for a location or
study. BrAPI v2.1 has no fertilizer record.

- `POST /genx/v1/fertilizer-applications` (`genxRecordFertilizerApplication`) registers one
  `FertilizerApplication` (`Schemas/FertilizerApplicationNewRequest.yaml`). Same
  `fertilizerApplicationDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/fertilizer-applications` (`genxListFertilizerApplications`) lists applications,
  optionally filtered by location, study, or date range.
- `GET /genx/v1/fertilizer-applications/{fertilizerApplicationDbId}`
  (`genxGetFertilizerApplication`) retrieves one application.

Details and falsifiers: `../../RFCs/RFC-026-Fertilizer-Application.md`.