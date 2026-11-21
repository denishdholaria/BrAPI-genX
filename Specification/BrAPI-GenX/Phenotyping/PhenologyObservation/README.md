# BrAPI-GenX — Phenology Observation (Phenotyping)

Phenology observations record developmental stage observations for an
observation unit, including BBCH codes. BrAPI v2.1 has observations but no
phenology-specific record.

- `POST /genx/v1/phenology-observations` (`genxRecordPhenologyObservation`) records one
  `PhenologyObservation` (`Schemas/PhenologyObservationNewRequest.yaml`). Same
  `phenologyObservationDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/phenology-observations` (`genxListPhenologyObservations`) lists observations,
  optionally filtered by study, observation unit, or stage.
- `GET /genx/v1/phenology-observations/{phenologyObservationDbId}`
  (`genxGetPhenologyObservation`) retrieves one observation.

Details and falsifiers: `../../RFCs/RFC-027-Phenology-Observation.md`.