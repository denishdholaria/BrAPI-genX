# BrAPI-GenX — Developmental Stage (Terminology)

`DevelopmentalStage` proposes a **draft growth-stage vocabulary entry**. The checked official BrAPI (Breeding Application Programming Interface) version 2.1 specifications contain ObservationVariables and Observations capable of phenology representation, but no standalone `DevelopmentalStage` record; GenX does not replace those resources.

The registration request requires only `developmentalStageDbId`. Crop reference, `stageCode`, stage name, definition, and provenance are all **optional**. A `BBCH-31` example is not a controlled Biologische Bundesanstalt, Bundessortenamt und Chemische Industrie (BBCH) scale, and optional `cropDbId` does not establish an authoritative crop/Germplasm join.

- `POST /genx/v1/developmental-stages` (`genxRegisterDevelopmentalStage`) registers one `DevelopmentalStage` (`Schemas/DevelopmentalStageNewRequest.yaml`). Same `developmentalStageDbId` + identical body replays; different body is described as rejected with `409`.
- `GET /genx/v1/developmental-stages` (`genxListDevelopmentalStages`) lists entries, optionally filtered by crop or status.
- `GET /genx/v1/developmental-stages/{developmentalStageDbId}` (`genxGetDevelopmentalStage`) retrieves an entry.

Source-contract limits and open decisions: [group description](./GroupDescription.md), [RFC-079](../../RFCs/RFC-079-Developmental-Stage.md).
