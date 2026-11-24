# BrAPI-GenX — Bulk Capture (Phenotyping)

`BulkCapture` proposes an immutable **capture-event envelope** associated with a Study. It does **not** replace official BrAPI (Breeding Application Programming Interface) version 2.1 Observations or provide proof of a transactional batch import: the official `POST /observations` already accepts an array of observation requests.

The GenX registration request requires `bulkCaptureDbId`, `studyDbId`, `capturedAt`, and `entries`. That array may be empty; each entry requires only `variableDbId`. ObservationUnit identity, nullable *numeric* value, unit, and quality flag are optional, unlike an approved or scientifically complete measurement. No `phenotypeCaptureDbId` or `fieldBookDbId` relationship exists in the current schema, and no automatic official Observation creation is established.

- `POST /genx/v1/bulk-captures` (`genxRecordBulkCapture`) registers one `BulkCapture` (`Schemas/BulkCaptureNewRequest.yaml`). Same `bulkCaptureDbId` + identical body is described as replayable; a different body is rejected with `409`.
- `GET /genx/v1/bulk-captures` (`genxListBulkCaptures`) lists records, optionally filtered by study or status.
- `GET /genx/v1/bulk-captures/{bulkCaptureDbId}` (`genxGetBulkCapture`) retrieves one record.

Source-contract limits and deferred questions: [group description](./GroupDescription.md), [RFC-040](../../RFCs/RFC-040-Bulk-Capture.md).
