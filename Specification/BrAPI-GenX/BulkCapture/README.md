# BrAPI-GenX — Bulk Capture (Phenotyping)

Bulk capture records the batch capture of observations for a study, including
entries and quality flags. BrAPI v2.1 has observations but no bulk capture
record.

- `POST /genx/v1/bulk-captures` (`genxRecordBulkCapture`) registers one
  `BulkCapture` (`Schemas/BulkCaptureNewRequest.yaml`). Same
  `bulkCaptureDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/bulk-captures` (`genxListBulkCaptures`) lists captures,
  optionally filtered by study or status.
- `GET /genx/v1/bulk-captures/{bulkCaptureDbId}`
  (`genxGetBulkCapture`) retrieves one capture.

Details and falsifiers: `../RFC-040-Bulk-Capture.md`.