# RFC-123 — Disease Observation (N)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (N).

## 1. Problem

BrAPI v2.1 already exchanges phenotypic Observations associated with
ObservationVariables, including disease symptoms and severity traits.
This candidate proposes a distinct disease-event record, but it lacks
the required typed observation-unit identity, controlled pathogen vocabulary,
assessment scale and contextual linkage needed to demonstrate an independent
interoperability gap. The case for a separate identity is not yet established.

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
