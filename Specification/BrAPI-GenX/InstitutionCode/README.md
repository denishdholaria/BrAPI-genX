# BrAPI-GenX — Institution Code (Reference Data)

Institution and collection code entries describe institution codes.
BrAPI v2.1 has no institution code record.

- `POST /genx/v1/institution-codes` (`genxRegisterInstitutionCode`) registers one
  `InstitutionCode` (`Schemas/InstitutionCodeNewRequest.yaml`). Same
  `institutionCodeDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/institution-codes` (`genxListInstitutionCodes`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/institution-codes/{institutionCodeDbId}`
  (`genxGetInstitutionCode`) retrieves one entry.

Details and falsifiers: `../RFC-096-Institution-Code.md`.
