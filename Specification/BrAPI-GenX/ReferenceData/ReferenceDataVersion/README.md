# BrAPI-GenX — Reference Data Version (Reference Data)

Reference data version records describe versions of reference data systems.
This candidate proposes reference-data release metadata. Official BrAPI version 2.1 Ontology already includes a version label, but it does not imply that this GenX record captures or verifies any dataset snapshot; the proposed `source` and `version` strings and links remain unratified.

- `POST /genx/v1/reference-data-versions` (`genxRegisterReferenceDataVersion`) registers one
  `ReferenceDataVersion` (`Schemas/ReferenceDataVersionNewRequest.yaml`). Same
  `referenceDataVersionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/reference-data-versions` (`genxListReferenceDataVersions`) lists records,
  optionally filtered by status.
- `GET /genx/v1/reference-data-versions/{referenceDataVersionDbId}`
  (`genxGetReferenceDataVersion`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-093-Reference-Data-Version.md`.
