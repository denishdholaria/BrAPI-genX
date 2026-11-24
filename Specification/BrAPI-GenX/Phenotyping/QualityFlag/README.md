# BrAPI-GenX — Quality Flag (Phenotyping)

Quality flag records describe quality flags.
BrAPI version 2.1 already represents individual Observations with values, variables, timestamps, units of observation and collectors. A separate quality-flag history may be useful, but the candidate is only an optional string flag and lifecycle metadata. It does not define an observation linkage, controlled quality taxonomy or validated quality assessment.

- `POST /genx/v1/quality-flags` (`genxRegisterQualityFlag`) registers one
  `QualityFlag` (`Schemas/QualityFlagNewRequest.yaml`). Same
  `qualityFlagDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/quality-flags` (`genxListQualityFlags`) lists records,
  optionally filtered by status.
- `GET /genx/v1/quality-flags/{qualityFlagDbId}`
  (`genxGetQualityFlag`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-111-Quality-Flag.md`.
