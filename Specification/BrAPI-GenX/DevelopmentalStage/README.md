# BrAPI-GenX — Developmental Stage (Terminology)

Developmental stage vocabulary entries describe growth-stage terms for crops.
BrAPI v2.1 has no developmental stage vocabulary record.

- `POST /genx/v1/developmental-stages` (`genxRegisterDevelopmentalStage`) registers one
  `DevelopmentalStage` (`Schemas/DevelopmentalStageNewRequest.yaml`). Same
  `developmentalStageDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/developmental-stages` (`genxListDevelopmentalStages`) lists entries,
  optionally filtered by crop or status.
- `GET /genx/v1/developmental-stages/{developmentalStageDbId}`
  (`genxGetDevelopmentalStage`) retrieves one entry.

Details and falsifiers: `../RFC-079-Developmental-Stage.md`.
