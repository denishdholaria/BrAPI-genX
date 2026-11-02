# BrAPI-GenX — Project (Reference Data)

Project and funding reference records describe research projects and funding.
BrAPI v2.1 has no project record.

- `POST /genx/v1/projects` (`genxRegisterProject`) registers one
  `Project` (`Schemas/ProjectNewRequest.yaml`). Same
  `projectDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/projects` (`genxListProjects`) lists records,
  optionally filtered by status.
- `GET /genx/v1/projects/{projectDbId}`
  (`genxGetProject`) retrieves one record.

Details and falsifiers: `../RFC-089-Project.md`.
