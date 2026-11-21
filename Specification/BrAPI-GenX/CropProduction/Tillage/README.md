# BrAPI-GenX — Tillage (Crop Production)

Tillage records capture soil preparation events for a location or study.
BrAPI v2.1 has no tillage record.

- `POST /genx/v1/tillage-records` (`genxRecordTillage`) registers one
  `TillageRecord` (`Schemas/TillageRecordNewRequest.yaml`). Same
  `tillageRecordDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/tillage-records` (`genxListTillageRecords`) lists records,
  optionally filtered by location, study, or date range.
- `GET /genx/v1/tillage-records/{tillageRecordDbId}`
  (`genxGetTillage`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-038-Tillage.md`.