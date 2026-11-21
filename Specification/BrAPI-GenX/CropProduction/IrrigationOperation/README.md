# BrAPI-GenX — Irrigation Operation (Crop Production)

Irrigation operations record water application events for a location or study.
BrAPI v2.1 has locations but no irrigation record.

- `POST /genx/v1/irrigation-operations` (`genxRecordIrrigation`) records one
  `IrrigationEvent` (`Schemas/IrrigationEventNewRequest.yaml`). Same
  `irrigationEventDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/irrigation-operations` (`genxListIrrigations`) lists events,
  optionally filtered by location, study, or date range.
- `GET /genx/v1/irrigation-operations/{irrigationEventDbId}`
  (`genxGetIrrigation`) retrieves one event.

Details and falsifiers: `../../RFCs/RFC-024-Irrigation-Operation.md`.