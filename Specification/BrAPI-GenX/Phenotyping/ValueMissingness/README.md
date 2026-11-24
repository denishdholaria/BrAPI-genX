# BrAPI-GenX — Value Missingness (Phenotyping)

Value and missingness records describe value and missingness.
BrAPI version 2.1 already defines the Observation `value` field and observation identity and context. This candidate separately records optional `value` and optional boolean `missing`, but it does not specify how their combinations behave, how an observation is referenced, or how missingness differs from invalid, corrected or imputed values.

- `POST /genx/v1/value-missingness` (`genxRegisterValueMissingness`) registers one
  `ValueMissingness` (`Schemas/ValueMissingnessNewRequest.yaml`). Same
  `valueMissingnessDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/value-missingness` (`genxListValueMissingness`) lists records,
  optionally filtered by status.
- `GET /genx/v1/value-missingness/{valueMissingnessDbId}`
  (`genxGetValueMissingness`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-112-Value-Missingness.md`.
