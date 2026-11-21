# BrAPI-GenX — Regeneration (Genebank Conservation)

Regeneration records capture the multiplication of conserved material to
maintain viability. BrAPI v2.1 has seed lots but no regeneration record.

- `POST /genx/v1/regeneration-records` (`genxRecordRegeneration`) registers one
  `RegenerationRecord` (`Schemas/RegenerationRecordNewRequest.yaml`). Same
  `regenerationRecordDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/regeneration-records` (`genxListRegenerations`) lists records,
  optionally filtered by seed lot or status.
- `GET /genx/v1/regeneration-records/{regenerationRecordDbId}`
  (`genxGetRegeneration`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-036-Regeneration.md`.