# RFC-101 — Collecting Mission (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record collecting missions. Collecting missions are
the routine reference for germplasm and genetic resources. Without a record,
missions arrive as unversioned notes with no stated title or provenance, so
they cannot be audited or reproduced.

## 2. Object

`CollectingMission` — one immutable collecting mission record, with its title
and provenance.

## 3. Endpoints

- `GET /genx/v1/collecting-missions` (`genxListCollectingMissions`)
- `POST /genx/v1/collecting-missions` (`genxRegisterCollectingMission`)
- `GET /genx/v1/collecting-missions/{collectingMissionDbId}` (`genxGetCollectingMission`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Collecting mission records reference BrAPI `Germplasm` by identifier; they
  do not duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `collectingMissionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the mission is validated or endorsed.

## 6. Deferred questions

- D-301: Should `title` be required? (Current: optional.)
- D-302: Should records link to BrAPI `Germplasm`? (Current: no link.)
- D-303: Should records link to GenX `ResearchProgram`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
