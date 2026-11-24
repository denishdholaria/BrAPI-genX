# BrAPI-GenX — Candidate Variety Lifecycle (Breeding)

CandidateVariety proposes internal status metadata for a breeding-program
candidate. The request requires only candidate identity, Program identifier,
and variety name; its `status` defaults to `candidate`. Values such as
`registered` and `released` are candidate record labels, **not evidence of
official variety registration, statutory notification, seed certification,
or approval for commercial release**.

Neither the owning registration authority nor a legal decision document is
modelled. `registeredAt` is optional, and no validated Germplasm or
BreedingPipeline link is required. Official BrAPI version 2.1 Germplasm and
Program resources remain separately authoritative.

- `POST /genx/v1/candidate-varieties` (`genxRegisterCandidateVariety`) registers one
  `CandidateVariety` (`Schemas/CandidateVarietyNewRequest.yaml`). Same
  `candidateVarietyDbId` + identical body replays; different body is rejected
  with `409`.
- `GET /genx/v1/candidate-varieties` (`genxListCandidateVarieties`) lists records,
  optionally filtered by program or status.
- `GET /genx/v1/candidate-varieties/{candidateVarietyDbId}`
  (`genxGetCandidateVariety`) retrieves one record.

Details and falsifiers: `../../RFCs/RFC-039-Candidate-Variety-Lifecycle.md`.