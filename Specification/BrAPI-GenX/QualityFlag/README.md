# BrAPI-GenX — Quality Flag (Phenotyping)

Quality flag records describe quality flags.
BrAPI v2.1 has no quality flag record.

- `POST /genx/v1/quality-flags` (`genxRegisterQualityFlag`) registers one
  `QualityFlag` (`Schemas/QualityFlagNewRequest.yaml`). Same
  `qualityFlagDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/quality-flags` (`genxListQualityFlags`) lists records,
  optionally filtered by status.
- `GET /genx/v1/quality-flags/{qualityFlagDbId}`
  (`genxGetQualityFlag`) retrieves one record.

Details and falsifiers: `../RFC-111-Quality-Flag.md`.
