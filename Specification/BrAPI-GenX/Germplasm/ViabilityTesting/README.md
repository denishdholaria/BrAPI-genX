# BrAPI-GenX — Viability Testing (Genebank Conservation)

Viability testing records germination and viability results for conserved
seed lots. BrAPI v2.1 has seed lots but no viability test record.

- `POST /genx/v1/viability-tests` (`genxRecordViabilityTest`) records one
  `ViabilityTest` (`Schemas/ViabilityTestNewRequest.yaml`). Same
  `viabilityTestDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/viability-tests` (`genxListViabilityTests`) lists tests,
  optionally filtered by seed lot or status.
- `GET /genx/v1/viability-tests/{viabilityTestDbId}`
  (`genxGetViabilityTest`) retrieves one test.

Details and falsifiers: `../../RFCs/RFC-021-Viability-Testing.md`.