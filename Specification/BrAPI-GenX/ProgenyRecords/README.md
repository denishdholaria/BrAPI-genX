# BrAPI-GenX — Progeny Records (Breeding)

Progeny records link parents to offspring within a breeding program, including
generation and family identity. BrAPI v2.1 has pedigree and crosses but no
progeny/family record.

- `POST /genx/v1/progeny-records` (`genxRecordProgeny`) records one
  `ProgenyRecord` (`Schemas/ProgenyRecordNewRequest.yaml`). Same
  `progenyRecordDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/progeny-records` (`genxListProgenyRecords`) lists records,
  optionally filtered by program, parent, or generation.
- `GET /genx/v1/progeny-records/{progenyRecordDbId}`
  (`genxGetProgenyRecord`) retrieves one record.

Details and falsifiers: `../RFC-019-Progeny-Records.md`.