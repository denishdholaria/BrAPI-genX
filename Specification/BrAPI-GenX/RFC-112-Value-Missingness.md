# RFC-112 — Value Missingness (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 has no place to record value and missingness. Value and missingness
are the routine reference for phenotyping. Without a record, values arrive as
unversioned notes with no stated value, missingness, or provenance, so they
cannot be audited or reproduced.

## 2. Object

`ValueMissingness` — one immutable value and missingness record, with its
value, missingness flag, and provenance.

## 3. Endpoints

- `GET /genx/v1/value-missingness` (`genxListValueMissingness`)
- `POST /genx/v1/value-missingness` (`genxRegisterValueMissingness`)
- `GET /genx/v1/value-missingness/{valueMissingnessDbId}` (`genxGetValueMissingness`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Value and missingness records reference BrAPI `Observation` by identifier;
  they do not duplicate those resources.
- A record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `valueMissingnessDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the value is validated or endorsed.

## 6. Deferred questions

- D-334: Should `value` be required? (Current: optional.)
- D-335: Should `missing` be required? (Current: optional.)
- D-336: Should records link to GenX `PhenotypeCapture`? (Current: no link.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Measurements.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
