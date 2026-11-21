# RFC-074 — Field Scouting (Field Agronomy)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-029 (Crop Cycle), RFC-069 (Farm), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has no place to record field scouting observations or work orders.
Scouting is the routine interface between a field and crop-health decisions.
Without a record, scouting notes arrive as unversioned text with no stated
field, type, or provenance, so they cannot be audited or reproduced.

## 2. Object

`FieldScouting` — one immutable record of a scouting observation or work order
for a field, with its type, observations, and provenance.

## 3. Endpoints

- `GET /genx/v1/field-scouting` (`genxListFieldScouting`)
- `POST /genx/v1/field-scouting` (`genxRegisterFieldScouting`)
- `GET /genx/v1/field-scouting/{fieldScoutingDbId}` (`genxGetFieldScouting`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Scouting records reference BrAPI `Study`/`Location` and GenX `Farm` by
  identifier; they do not duplicate those resources.
- A scouting record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `fieldScoutingDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the work order was completed, validated, or
  scientifically endorsed.

## 6. Deferred questions

- D-220: Should `fieldDbId` be required? (Current: optional.)
- D-221: Should `observations` be a structured object rather than free text?
  (Current: free text.)
- D-222: Should scouting type be a controlled GenX terminology? (Current:
  free-form string.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
