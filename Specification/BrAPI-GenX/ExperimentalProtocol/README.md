# BrAPI-GenX — ExperimentalProtocol

ExperimentalProtocol records describe ExperimentalProtocol entries.
BrAPI v2.1 has no ExperimentalProtocol record.

- `POST /genx/v1/experimental-protocols` (`genxRegisterExperimentalProtocol`) registers one
  `ExperimentalProtocol` (`Schemas/ExperimentalProtocolNewRequest.yaml`). Same
  `experimentalProtocolDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/experimental-protocols` (`genxListExperimentalProtocols`) lists records,
  optionally filtered by status.
- `GET /genx/v1/experimental-protocols/{experimentalProtocolDbId}`
  (`genxGetExperimentalProtocol`) retrieves one record.

Details and falsifiers: `../RFC-117-ExperimentalProtocol.md`.
