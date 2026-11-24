# RFC-101 — Collecting Mission (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 Germplasm Multi-Crop Passport Descriptors (MCPD) data already includes `collectingMissionIdentifier`. This draft proposes a separate CollectingMission metadata record, but it does not establish a typed germplasm membership, mission participants, expedition provenance or a demonstrated need for a new identifier.

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
- No typed link to an official BrAPI Germplasm or other candidate entity is established by the current record. Any externally meaningful resource linkage requires evidence and an explicit decision. D-302 remains open.
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
