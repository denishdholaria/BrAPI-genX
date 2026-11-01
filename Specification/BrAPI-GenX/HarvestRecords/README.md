# BrAPI-GenX — Harvest Records (Crop Production)

Harvest records capture the outcome of a harvest event: what was harvested,
from which study/location, how much, and its quality and moisture. They support
yield tracking and linkage to seed lots. BrAPI v2.1 has seed lots and
transactions but no harvest-event record.

- `POST /genx/v1/harvest-records` (`genxRecordHarvest`) records one
  `HarvestRecord` (`Schemas/HarvestRecordNewRequest.yaml`). Same
  `harvestRecordDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/harvest-records` (`genxListHarvestRecords`) lists records,
  optionally filtered by study, location, germplasm, or date range.
- `GET /genx/v1/harvest-records/{harvestRecordDbId}`
  (`genxGetHarvestRecord`) retrieves one record.

Details and falsifiers: `../RFC-011-Harvest-Records.md`.