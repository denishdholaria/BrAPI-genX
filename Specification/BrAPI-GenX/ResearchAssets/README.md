# BrAPI-GenX — Research Assets (Publication & Knowledge)

Research assets record citable scientific outputs: datasets, models, protocols,
reports, and evidence packs, with license, access policy, embargo, and
persistent identifiers. They build on the FAIR package envelope. BrAPI v2.1
has no research asset registry.

- `POST /genx/v1/research-assets` (`genxRegisterResearchAsset`) registers one
  `ResearchAsset` (`Schemas/ResearchAssetNewRequest.yaml`). Same
  `researchAssetDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/research-assets` (`genxListResearchAssets`) lists assets,
  optionally filtered by type, license, or access policy.
- `GET /genx/v1/research-assets/{researchAssetDbId}`
  (`genxGetResearchAsset`) retrieves one asset.

Details and falsifiers: `../RFC-016-Research-Assets.md`.