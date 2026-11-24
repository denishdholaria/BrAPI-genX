# BrAPI-GenX — Institution Code (Reference Data)

Institution and collection code entries describe institution codes.
Official BrAPI version 2.1 Germplasm already carries institute codes and Multi-Crop Passport Descriptors (MCPD) fields. The candidate GenX record is not a registered Food and Agriculture Organization (FAO) World Information and Early Warning System (WIEWS) code authority.

- `POST /genx/v1/institution-codes` (`genxRegisterInstitutionCode`) registers one
  `InstitutionCode` (`Schemas/InstitutionCodeNewRequest.yaml`). Same
  `institutionCodeDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/institution-codes` (`genxListInstitutionCodes`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/institution-codes/{institutionCodeDbId}`
  (`genxGetInstitutionCode`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-096-Institution-Code.md`.
