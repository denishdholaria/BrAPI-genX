# BrAPI-GenX — Yield Map (Field Agronomy)

YieldMap is a **STRUCTURAL_DRAFT** descriptor that can optionally describe a
spatial yield surface. The draft does not establish a measured surface,
validated harvest provenance, coordinate system or published map asset.
Mission 090's G-090-3 payload-integrity decision remains open.

- `POST /genx/v1/yield-maps` (`genxRegisterYieldMap`) registers one `YieldMap`
  (`Schemas/YieldMapNewRequest.yaml`). Same `yieldMapDbId` + identical body
  replays; different body is rejected with `409`.
- `GET /genx/v1/yield-maps` (`genxListYieldMaps`) lists maps, optionally
  filtered by study, crop cycle, or status.
- `GET /genx/v1/yield-maps/{yieldMapDbId}` (`genxGetYieldMap`) retrieves one
  map record.

These draft operations do not transport map bytes. `storageUri` and
`fileDigest` are optional, so neither retrieval nor digest verification is
promised by a registered YieldMap record.

Details and falsifiers: `../../RFCs/RFC-070-Yield-Map.md`.
