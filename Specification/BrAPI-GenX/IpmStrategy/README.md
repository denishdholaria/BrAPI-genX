# BrAPI-GenX — IpmStrategy

IpmStrategy records describe IpmStrategy entries.
BrAPI v2.1 has no IpmStrategy record.

- `POST /genx/v1/ipm-strategies` (`genxRegisterIpmStrategy`) registers one
  `IpmStrategy` (`Schemas/IpmStrategyNewRequest.yaml`). Same
  `ipmStrategyDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/ipm-strategies` (`genxListIpmStrategies`) lists records,
  optionally filtered by status.
- `GET /genx/v1/ipm-strategies/{ipmStrategyDbId}`
  (`genxGetIpmStrategy`) retrieves one record.

Details and falsifiers: `../RFC-125-IpmStrategy.md`.
