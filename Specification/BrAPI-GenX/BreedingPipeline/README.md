# BrAPI-GenX — BreedingPipeline

BreedingPipeline records describe BreedingPipeline entries.
BrAPI v2.1 has no BreedingPipeline record.

- `POST /genx/v1/breeding-pipelines` (`genxRegisterBreedingPipeline`) registers one
  `BreedingPipeline` (`Schemas/BreedingPipelineNewRequest.yaml`). Same
  `breedingPipelineDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/breeding-pipelines` (`genxListBreedingPipelines`) lists records,
  optionally filtered by status.
- `GET /genx/v1/breeding-pipelines/{breedingPipelineDbId}`
  (`genxGetBreedingPipeline`) retrieves one record.

Details and falsifiers: `../RFC-154-BreedingPipeline.md`.
