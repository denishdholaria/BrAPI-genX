# BrAPI-GenX — Spray Application (Crop Health)

Spray application records describe pesticide or treatment applications to a
field. BrAPI v2.1 has no spray application record.

- `POST /genx/v1/spray-applications` (`genxRegisterSprayApplication`) registers one
  `SprayApplication` (`Schemas/SprayApplicationNewRequest.yaml`). Same
  `sprayApplicationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/spray-applications` (`genxListSprayApplications`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/spray-applications/{sprayApplicationDbId}`
  (`genxGetSprayApplication`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-081-Spray-Application.md`.
