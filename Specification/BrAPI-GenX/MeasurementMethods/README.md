# BrAPI-GenX — Measurement Methods (Terminology)

Measurement methods record the procedures, equipment, and precision used to
measure traits. BrAPI v2.1 has methods but GenX adds versioned, namespaced
method definitions with provenance. They are complementary to VariableTerm.

- `POST /genx/v1/measurement-methods` (`genxRegisterMeasurementMethod`) registers one
  `MeasurementMethod` (`Schemas/MeasurementMethodNewRequest.yaml`). Same
  `measurementMethodDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/measurement-methods` (`genxListMeasurementMethods`) lists methods,
  optionally filtered by type or status.
- `GET /genx/v1/measurement-methods/{measurementMethodDbId}`
  (`genxGetMeasurementMethod`) retrieves one method.

Details and falsifiers: `../RFC-017-Measurement-Methods.md`.