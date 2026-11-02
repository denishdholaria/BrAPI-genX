# BrAPI-GenX — Terminology Version (Terminology)

Terminology version entries describe versioned terminology/vocabulary records.
BrAPI v2.1 has no terminology version record.

- `POST /genx/v1/terminology-versions` (`genxRegisterTerminologyVersion`) registers one
  `TerminologyVersion` (`Schemas/TerminologyVersionNewRequest.yaml`). Same
  `terminologyVersionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/terminology-versions` (`genxListTerminologyVersions`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/terminology-versions/{terminologyVersionDbId}`
  (`genxGetTerminologyVersion`) retrieves one entry.

Details and falsifiers: `../RFC-084-Terminology-Version.md`.
