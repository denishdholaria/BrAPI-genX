# RFC-105 — Crosswalk (Germplasm)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record crosswalks. Crosswalks are the routine
reference for germplasm and genetic resources. Without a record, crosswalks
arrive as unversioned notes with no stated source, target, or provenance, so
they cannot be audited or reproduced.

## 2. Object

`Crosswalk` — one immutable crosswalk record, with its source, target, and
provenance.

## 3. Endpoints

- `GET /genx/v1/crosswalks` (`genxListCrosswalks`)
- `POST /genx/v1/crosswalks` (`genxRegisterCrosswalk`)
- `GET /genx/v1/crosswalks/{crosswalkDbId}` (`genxGetCrosswalk`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Crosswalk records reference BrAPI entities by identifier; they do not
  duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `crosswalkDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the crosswalk is validated or endorsed.

## 6. Deferred questions

- D-313: Should `source` and `target` be required? (Current: optional.)
- D-314: Should `source`/`target` be controlled vocabularies? (Current:
  free-form strings.)
- D-315: Should records link to GenX `McpdAdapter`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
