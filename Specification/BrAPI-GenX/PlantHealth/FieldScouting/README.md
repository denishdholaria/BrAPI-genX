# BrAPI-GenX — Field Scouting (Field Agronomy)

Field scouting and work order records describe scouting observations and tasks
for a field or site. BrAPI v2.1 has no field scouting record.

- `POST /genx/v1/field-scouting` (`genxRegisterFieldScouting`) registers one
  `FieldScouting` (`Schemas/FieldScoutingNewRequest.yaml`). Same
  `fieldScoutingDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/field-scouting` (`genxListFieldScouting`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/field-scouting/{fieldScoutingDbId}`
  (`genxGetFieldScouting`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-074-Field-Scouting.md`.
