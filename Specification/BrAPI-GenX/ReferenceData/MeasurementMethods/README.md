# BrAPI-GenX — Measurement Methods (Terminology)

Measurement methods record the procedures, equipment, and precision used to
measure traits. Official BrAPI v2.1 already includes `Method` records and
`/brapi/v2/methods` operations; GenX proposes a separate, namespaced,
immutable method-definition record with provenance. The current draft has
no typed BrAPI Method or Scale linkage, and does not establish equivalence.

- `POST /genx/v1/measurement-methods` (`genxRegisterMeasurementMethod`) registers one
  `MeasurementMethod` (`Schemas/MeasurementMethodNewRequest.yaml`). Same
  `measurementMethodDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/measurement-methods` (`genxListMeasurementMethods`) lists methods,
  optionally filtered by type or status.
- `GET /genx/v1/measurement-methods/{measurementMethodDbId}`
  (`genxGetMeasurementMethod`) retrieves one method.

Details and falsifiers: `../../RFCs/RFC-017-Measurement-Methods.md`.