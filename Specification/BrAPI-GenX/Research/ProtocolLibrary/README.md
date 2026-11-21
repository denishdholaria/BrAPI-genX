# BrAPI-GenX — ProtocolLibrary

ProtocolLibrary records describe ProtocolLibrary entries.
BrAPI v2.1 has no ProtocolLibrary record.

- `POST /genx/v1/protocol-libraries` (`genxRegisterProtocolLibrary`) registers one
  `ProtocolLibrary` (`Schemas/ProtocolLibraryNewRequest.yaml`). Same
  `protocolLibraryDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/protocol-libraries` (`genxListProtocolLibraries`) lists records,
  optionally filtered by status.
- `GET /genx/v1/protocol-libraries/{protocolLibraryDbId}`
  (`genxGetProtocolLibrary`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-119-ProtocolLibrary.md`.
