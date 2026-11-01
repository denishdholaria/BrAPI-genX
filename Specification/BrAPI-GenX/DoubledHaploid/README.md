# BrAPI-GenX — Doubled Haploid Programs (Breeding)

Doubled haploid programs record the method, donor, and counts for haploid
induction and chromosome doubling. BrAPI v2.1 has no doubled haploid record.

- `POST /genx/v1/doubled-haploid-programs` (`genxRegisterDoubledHaploidProgram`) registers one
  `DoubledHaploidProgram` (`Schemas/DoubledHaploidProgramNewRequest.yaml`). Same
  `doubledHaploidProgramDbId` + identical body replays; different body is
  rejected with `409`.
- `GET /genx/v1/doubled-haploid-programs` (`genxListDoubledHaploidPrograms`) lists programs,
  optionally filtered by program or status.
- `GET /genx/v1/doubled-haploid-programs/{doubledHaploidProgramDbId}`
  (`genxGetDoubledHaploidProgram`) retrieves one program.

Details and falsifiers: `../RFC-020-Doubled-Haploid.md`.