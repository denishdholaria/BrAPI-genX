# BrAPI-GenX — Population Advancement (Breeding)

Population advancement records the movement of a population between breeding
stages. BrAPI v2.1 has no population advancement record.

- `POST /genx/v1/population-advancements` (`genxRecordPopulationAdvancement`) registers one
  `PopulationAdvancement` (`Schemas/PopulationAdvancementNewRequest.yaml`). Same
  `populationAdvancementDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/population-advancements` (`genxListPopulationAdvancements`) lists records,
  optionally filtered by program, population, or status.
- `GET /genx/v1/population-advancements/{populationAdvancementDbId}`
  (`genxGetPopulationAdvancement`) retrieves one record.

Details and falsifiers: `../RFC-035-Population-Advancement.md`.