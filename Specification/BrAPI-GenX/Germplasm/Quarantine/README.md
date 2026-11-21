# BrAPI-GenX — Quarantine (Genebank Conservation)

Quarantine records capture the isolation and inspection of conserved material.
BrAPI v2.1 has seed lots but no quarantine record.

- `POST /genx/v1/quarantine-records` (`genxRecordQuarantine`) records one
  `QuarantineRecord` (`Schemas/QuarantineRecordNewRequest.yaml`). Same
  `quarantineRecordDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/quarantine-records` (`genxListQuarantineRecords`) lists records,
  optionally filtered by seed lot or status.
- `GET /genx/v1/quarantine-records/{quarantineRecordDbId}`
  (`genxGetQuarantineRecord`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-030-Quarantine.md`.