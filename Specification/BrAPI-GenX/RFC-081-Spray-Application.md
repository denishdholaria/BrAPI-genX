# RFC-081 — Spray Application (Crop Health)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-066 (Planting Operation), `CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has no place to record spray applications. Spraying is the routine
interface between crop health decisions and field operations. Without a
record, spray applications arrive as unversioned notes with no stated field,
product, rate, or provenance, so they cannot be audited or reproduced.

## 2. Object

`SprayApplication` — one immutable record of a spray application to a field,
with its product, rate, timestamp, and provenance.

## 3. Endpoints

- `GET /genx/v1/spray-applications` (`genxListSprayApplications`)
- `POST /genx/v1/spray-applications` (`genxRegisterSprayApplication`)
- `GET /genx/v1/spray-applications/{sprayApplicationDbId}` (`genxGetSprayApplication`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Spray records reference BrAPI `Location` and GenX `FieldScouting` by
  identifier; they do not duplicate those resources.
- A spray record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `sprayApplicationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the spray was validated or effective.

## 6. Deferred questions

- D-241: Should `fieldDbId` be required? (Current: optional.)
- D-242: Should `product` be a controlled GenX terminology? (Current:
  free-form string.)
- D-243: Should spray applications link to an IPM strategy? (Current: no
  link.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
