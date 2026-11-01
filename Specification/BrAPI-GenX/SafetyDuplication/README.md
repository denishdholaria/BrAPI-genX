# BrAPI-GenX — Safety Duplication (Genebank Conservation)

Safety duplication records the backup of conserved material at a secondary
site. BrAPI v2.1 has no safety duplication record.

- `POST /genx/v1/safety-duplications` (`genxRegisterSafetyDuplication`) registers one
  `SafetyDuplication` (`Schemas/SafetyDuplicationNewRequest.yaml`). Same
  `safetyDuplicationDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/safety-duplications` (`genxListSafetyDuplications`) lists records,
  optionally filtered by seed lot or status.
- `GET /genx/v1/safety-duplications/{safetyDuplicationDbId}`
  (`genxGetSafetyDuplication`) retrieves one record.

Details and falsifiers: `../RFC-034-Safety-Duplication.md`.