# BrAPI-GenX — Planting Operation (Field Agronomy)

Planting records document sowing or transplanting operations. BrAPI v2.1 has no
planting operation record.

- `POST /genx/v1/planting-operations` (`genxRecordPlantingOperation`) registers one
  `PlantingOperation` (`Schemas/PlantingOperationNewRequest.yaml`). Same
  `plantingOperationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/planting-operations` (`genxListPlantingOperations`) lists
  operations, optionally filtered by study, crop cycle, or status.
- `GET /genx/v1/planting-operations/{plantingOperationDbId}`
  (`genxGetPlantingOperation`) retrieves one operation.

Details and falsifiers: `../RFC-066-Planting-Operation.md`.
