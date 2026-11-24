# RFC-112 — Value Missingness (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI version 2.1 already defines the Observation `value` field and observation identity and context. This candidate separately records optional `value` and optional boolean `missing`, but it does not specify how their combinations behave, how an observation is referenced, or how missingness differs from invalid, corrected or imputed values.

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
- No typed link to an official BrAPI Observation or GenX PhenotypeCapture record is present in this candidate schema; D-336 remains unresolved. Matching labels or navigation links do not create scientific identity.
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
