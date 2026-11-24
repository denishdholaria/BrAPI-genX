# BrAPI-GenX — VegetationIndex

VegetationIndex proposes catalogue metadata, not an index calculation or
measured vegetation response. Its type, acquisition date, spatial reference,
resolution and provenance are optional; no numerical index value, raster
reference, sensor bands or formula is modelled. Official BrAPI version 2.1
data remain separate and unaffected.

- `POST /genx/v1/vegetation-indexes` (`genxRegisterVegetationIndex`) registers one
  `VegetationIndex` (`Schemas/VegetationIndexNewRequest.yaml`). Same
  `vegetationIndexDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/vegetation-indexes` (`genxListVegetationIndexes`) lists records,
  optionally filtered by status.
- `GET /genx/v1/vegetation-indexes/{vegetationIndexDbId}`
  (`genxGetVegetationIndex`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-146-VegetationIndex.md`.
