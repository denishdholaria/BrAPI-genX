# BrAPI-GenX — Field Book (Experimental Design)

Field book definition records describe field book definitions.
BrAPI version 2.1 already provides Studies, Observation Units and variables. A separate candidate FieldBook definition may record capture-configuration provenance, but it is not established as an interoperable capture schema merely by naming it.

- `POST /genx/v1/field-books` (`genxRegisterFieldBook`) registers one
  `FieldBook` (`Schemas/FieldBookNewRequest.yaml`). Same
  `fieldBookDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/field-books` (`genxListFieldBooks`) lists records,
  optionally filtered by field or status.
- `GET /genx/v1/field-books/{fieldBookDbId}`
  (`genxGetFieldBook`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-108-Field-Book.md`.
