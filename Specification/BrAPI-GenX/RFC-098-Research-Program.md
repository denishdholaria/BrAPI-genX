# RFC-098 — Research Program (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record research programs. Research programs are the
routine reference for research organization. Without a record, programs arrive
as unversioned notes with no stated title or provenance, so they cannot be
audited or reproduced.

## 2. Object

`ResearchProgram` — one immutable research program record, with its title and
provenance.

## 3. Endpoints

- `GET /genx/v1/research-programs` (`genxListResearchPrograms`)
- `POST /genx/v1/research-programs` (`genxRegisterResearchProgram`)
- `GET /genx/v1/research-programs/{researchProgramDbId}` (`genxGetResearchProgram`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Research program records reference BrAPI `Study` by identifier; they do not
  duplicate those resources.
- A record is not a BrAPI Study and must not be treated as one.

## 5. Invariants

- A published `researchProgramDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the program is validated or endorsed.

## 6. Deferred questions

- D-292: Should `title` be required? (Current: optional.)
- D-293: Should program records link to GenX `Project`? (Current: no link.)
- D-294: Should program records link to GenX `ResearchAsset`? (Current: no
  link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
