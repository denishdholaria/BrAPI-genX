# RFC-100 — Research Location (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 already defines `Location` resources and related research
location metadata. The separate GenX candidate presently contains only
an optional name besides its identity, status and provenance. The
reason to introduce another location identity and a mapping to official
BrAPI locations has not been established.

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
- The current schema contains no BrAPI `Location` identifier and no GenX
  `Farm` link (D-299 and D-300 remain open). Geographic or institutional
  equivalence with a BrAPI Location cannot be inferred.
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
