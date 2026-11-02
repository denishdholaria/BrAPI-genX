# RFC-123 — Disease Observation (N)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (N).

## 1. Problem

BrAPI v2.1 has no place to record disease/pest observations. Observations
occur without a stated pest/disease, severity, date, or provenance, so they
cannot be tracked or used for IPM decisions.

## 2. Object

`DiseaseObservation` — one immutable disease observation record, with its
type, pest/disease, severity, date, field/plot, and provenance.

## 3. Endpoints

- `GET /genx/v1/disease-observations` (`genxListDiseaseObservations`)
- `POST /genx/v1/disease-observations` (`genxRegisterDiseaseObservation`)
- `GET /genx/v1/disease-observations/{diseaseObservationDbId}` (`genxGetDiseaseObservation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `diseaseObservationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-367: Should `severity` be required? (Current: optional.)
- D-368: Should `pestOrDisease` be a controlled vocabulary? (Current: free-form string.)
- D-369: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting N).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
