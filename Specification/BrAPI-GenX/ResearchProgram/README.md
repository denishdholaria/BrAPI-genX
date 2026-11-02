# BrAPI-GenX — Research Program (Reference Data)

Research program records describe research programs.
BrAPI v2.1 has no research program record.

- `POST /genx/v1/research-programs` (`genxRegisterResearchProgram`) registers one
  `ResearchProgram` (`Schemas/ResearchProgramNewRequest.yaml`). Same
  `researchProgramDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/research-programs` (`genxListResearchPrograms`) lists records,
  optionally filtered by status.
- `GET /genx/v1/research-programs/{researchProgramDbId}`
  (`genxGetResearchProgram`) retrieves one record.

Details and falsifiers: `../RFC-098-Research-Program.md`.
