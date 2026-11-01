# BrAPI-GenX — Genebank Storage (Conservation)

Genebank storage records the physical storage locations, capacity, and
environmental conditions for conserved germplasm. BrAPI v2.1 has germplasm
and seed lots but no storage location or conservation record.

- `POST /genx/v1/genebank-storage` (`genxRegisterStorageLocation`) registers one
  `StorageLocation` (`Schemas/StorageLocationNewRequest.yaml`). Same
  `storageLocationDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/genebank-storage` (`genxListStorageLocations`) lists locations,
  optionally filtered by facility, vault, or status.
- `GET /genx/v1/genebank-storage/{storageLocationDbId}`
  (`genxGetStorageLocation`) retrieves one location.

Details and falsifiers: `../RFC-015-Genebank-Storage.md`.