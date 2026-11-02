# RFC-100 — Research Location (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record research locations. Research locations are
the routine reference for research organization. Without a record, locations
arrive as unversioned notes with no stated name or provenance, so they cannot
be audited or reproduced.

## 2. Object

`ResearchLocation` — one immutable research location record, with its name and
provenance.

## 3. Endpoints

- `GET /genx/v1/research-locations` (`genxListResearchLocations`)
- `POST /genx/v1/research-locations` (`genxRegisterResearchLocation`)
- `GET /genx/v1/research-locations/{researchLocationDbId}` (`genxGetResearchLocation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Research location records reference BrAPI `Location` by identifier; they do
  not duplicate those resources.
- A record is not a BrAPI Location and must not be treated as one.

## 5. Invariants

- A published `researchLocationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the location is validated or endorsed.

## 6. Deferred questions

- D-298: Should `name` be required? (Current: optional.)
- D-299: Should records link to BrAPI `Location`? (Current: no link.)
- D-300: Should records link to GenX `Farm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
