# RFC-098 — Research Program (Reference Data)

- Status: deferred; retained as historical proposal.
- Supersedes: none.
- Decision: D-BP-12 — the duplicate ResearchProgram surface is deferred; BrAPI Program remains authoritative.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Historical problem statement (not an accepted gap)

> The opening claim below is contradicted by the official BrAPI v2.1 Program resource. D-BP-12 deferred this duplicate candidate. This section is retained only for historical traceability.

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
- This proposal is deferred under D-BP-12: the official BrAPI `Program`
  is authoritative. The historical candidate schema contains no typed
  BrAPI `Study` reference or separate approved program ownership.
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
