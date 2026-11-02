# BrAPI-GenX — Reference Data Version (Reference Data)

Reference data version records describe versions of reference data systems.
BrAPI v2.1 has no reference data version record.

- `POST /genx/v1/reference-data-versions` (`genxRegisterReferenceDataVersion`) registers one
  `ReferenceDataVersion` (`Schemas/ReferenceDataVersionNewRequest.yaml`). Same
  `referenceDataVersionDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/reference-data-versions` (`genxListReferenceDataVersions`) lists records,
  optionally filtered by status.
- `GET /genx/v1/reference-data-versions/{referenceDataVersionDbId}`
  (`genxGetReferenceDataVersion`) retrieves one record.

Details and falsifiers: `../RFC-093-Reference-Data-Version.md`.
