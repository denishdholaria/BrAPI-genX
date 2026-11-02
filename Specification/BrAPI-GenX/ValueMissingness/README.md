# BrAPI-GenX — Value Missingness (Phenotyping)

Value and missingness records describe value and missingness.
BrAPI v2.1 has no value and missingness record.

- `POST /genx/v1/value-missingness` (`genxRegisterValueMissingness`) registers one
  `ValueMissingness` (`Schemas/ValueMissingnessNewRequest.yaml`). Same
  `valueMissingnessDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/value-missingness` (`genxListValueMissingness`) lists records,
  optionally filtered by status.
- `GET /genx/v1/value-missingness/{valueMissingnessDbId}`
  (`genxGetValueMissingness`) retrieves one record.

Details and falsifiers: `../RFC-112-Value-Missingness.md`.
