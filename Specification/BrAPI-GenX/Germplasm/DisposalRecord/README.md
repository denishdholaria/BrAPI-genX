# BrAPI-GenX — Disposal Record (Genebank Conservation)

Disposal records document the destruction, return, or retirement of a sample or
seed lot. BrAPI v2.1 has no disposal record.

- `POST /genx/v1/disposal-records` (`genxRecordDisposalRecord`) registers one
  `DisposalRecord` (`Schemas/DisposalRecordNewRequest.yaml`). Same
  `disposalRecordDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/disposal-records` (`genxListDisposalRecords`) lists records,
  optionally filtered by sample, lot, or status.
- `GET /genx/v1/disposal-records/{disposalRecordDbId}`
  (`genxGetDisposalRecord`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-065-Disposal-Record.md`.
