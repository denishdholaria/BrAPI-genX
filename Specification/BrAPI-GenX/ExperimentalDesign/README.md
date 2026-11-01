# BrAPI-GenX — Experimental Design (Trial Layout)

Experimental designs record the layout, replication, randomization, and
treatment assignment for a study. BrAPI v2.1 has studies and observation
units but no design or randomization record.

- `POST /genx/v1/experimental-designs` (`genxRegisterExperimentalDesign`) registers
  one `ExperimentalDesign` (`Schemas/ExperimentalDesignNewRequest.yaml`). Same
  `experimentalDesignDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/experimental-designs` (`genxListExperimentalDesigns`) lists
  designs, optionally filtered by study or design type.
- `GET /genx/v1/experimental-designs/{experimentalDesignDbId}`
  (`genxGetExperimentalDesign`) retrieves one design.

Details and falsifiers: `../RFC-018-Experimental-Design.md`.