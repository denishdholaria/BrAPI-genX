# BrAPI-GenX — Breeding Pipeline (Stage Gates)

Breeding pipelines record the stages, entry/exit criteria, and advancement
rules for a breeding program. BrAPI v2.1 has programs and crosses but no
pipeline or stage-gate record.

- `POST /genx/v1/breeding-pipelines` (`genxRegisterBreedingPipeline`) registers one
  `BreedingPipeline` (`Schemas/BreedingPipelineNewRequest.yaml`). Same
  `breedingPipelineDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/breeding-pipelines` (`genxListBreedingPipelines`) lists pipelines,
  optionally filtered by program or status.
- `GET /genx/v1/breeding-pipelines/{breedingPipelineDbId}`
  (`genxGetBreedingPipeline`) retrieves one pipeline.

Details and falsifiers: `../RFC-014-Breeding-Pipeline.md`.