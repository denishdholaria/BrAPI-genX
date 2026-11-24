# BrAPI-GenX — Measurement Scale (Terminology)

Measurement scale and value domain entries describe scales and allowed values.
Official BrAPI v2.1 already defines `Scale` records and `/brapi/v2/scales` operations. This optional GenX proposal explores independently versioned, namespaced scale-convention metadata; it does not replace an official Scale or establish a mapping to one. The need for a distinct record remains under review.

- `POST /genx/v1/measurement-scales` (`genxRegisterMeasurementScale`) registers one
  `MeasurementScale` (`Schemas/MeasurementScaleNewRequest.yaml`). Same
  `measurementScaleDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/measurement-scales` (`genxListMeasurementScales`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/measurement-scales/{measurementScaleDbId}`
  (`genxGetMeasurementScale`) retrieves one entry.

Details and falsifiers: `../../RFCs/RFC-087-Measurement-Scale.md`.
