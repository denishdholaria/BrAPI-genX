# BrAPI-GenX — Units and Quantity (Terminology)

Units and quantity semantics entries describe unit and quantity conventions.
BrAPI v2.1 has no units and quantity record.

- `POST /genx/v1/units-and-quantities` (`genxRegisterUnitsAndQuantity`) registers one
  `UnitsAndQuantity` (`Schemas/UnitsAndQuantityNewRequest.yaml`). Same
  `unitsAndQuantityDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/units-and-quantities` (`genxListUnitsAndQuantities`) lists entries,
  optionally filtered by status.
- `GET /genx/v1/units-and-quantities/{unitsAndQuantityDbId}`
  (`genxGetUnitsAndQuantity`) retrieves one entry.

Details and falsifiers: `../RFC-082-Units-And-Quantity.md`.
