# BrAPI-GenX — IrrigationAdvice

IrrigationAdvice records describe IrrigationAdvice entries.
BrAPI v2.1 has no IrrigationAdvice record.

- `POST /genx/v1/irrigation-advices` (`genxRegisterIrrigationAdvice`) registers one
  `IrrigationAdvice` (`Schemas/IrrigationAdviceNewRequest.yaml`). Same
  `irrigationAdviceDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/irrigation-advices` (`genxListIrrigationAdvices`) lists records,
  optionally filtered by status.
- `GET /genx/v1/irrigation-advices/{irrigationAdviceDbId}`
  (`genxGetIrrigationAdvice`) retrieves one record.

Details and falsifiers: `../RFC-131-IrrigationAdvice.md`.
