# BrAPI-GenX — Yield Map (Field Agronomy)

Yield map records describe spatial yield surfaces derived from harvest data.
BrAPI v2.1 has no yield map record.

- `POST /genx/v1/yield-maps` (`genxRegisterYieldMap`) registers one `YieldMap`
  (`Schemas/YieldMapNewRequest.yaml`). Same `yieldMapDbId` + identical body
  replays; different body is rejected with `409`.
- `GET /genx/v1/yield-maps` (`genxListYieldMaps`) lists maps, optionally
  filtered by study, crop cycle, or status.
- `GET /genx/v1/yield-maps/{yieldMapDbId}` (`genxGetYieldMap`) retrieves one
  map record.

The map payload itself is not transported by BrAPI; `storageUri` and
`fileDigest` locate and verify it.

Details and falsifiers: `../../RFCs/RFC-070-Yield-Map.md`.
