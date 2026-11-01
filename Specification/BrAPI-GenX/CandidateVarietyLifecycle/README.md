# BrAPI-GenX — Candidate Variety Lifecycle (Breeding)

Candidate variety lifecycle records the status and progression of a candidate
variety through registration. BrAPI v2.1 has no candidate variety record.

- `POST /genx/v1/candidate-varieties` (`genxRegisterCandidateVariety`) registers one
  `CandidateVariety` (`Schemas/CandidateVarietyNewRequest.yaml`). Same
  `candidateVarietyDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/candidate-varieties` (`genxListCandidateVarieties`) lists records,
  optionally filtered by program or status.
- `GET /genx/v1/candidate-varieties/{candidateVarietyDbId}`
  (`genxGetCandidateVariety`) retrieves one record.

Details and falsifiers: `../RFC-039-Candidate-Variety-Lifecycle.md`.