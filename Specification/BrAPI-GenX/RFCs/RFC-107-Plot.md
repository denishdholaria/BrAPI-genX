# RFC-107 — Plot (Experimental Design)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI version 2.1 Observation Units already represent a `plot` hierarchy level. A separate GenX plot identity must be justified and mapped explicitly; absence of a `/plots` route does not prove a missing plot concept.

## 2. Object

`Plot` — one immutable plot identity record, with its field linkage, name, and
provenance.

## 3. Endpoints

- `GET /genx/v1/plots` (`genxListPlots`)
- `POST /genx/v1/plots` (`genxRegisterPlot`)
- `GET /genx/v1/plots/{plotDbId}` (`genxGetPlot`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The proposed record has no typed link to an official BrAPI identity and no validated identity mapping. A candidate `plotDbId` is not an official observation-unit ID, level code or validated field position. `fieldDbId` and `plotName` are optional strings and no typed Study, Location or GenX ExperimentalDesign link is defined. D-321 remains open.
- A plot record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `plotDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the plot is validated or endorsed.

## 6. Deferred questions

- D-319: Should `fieldDbId` be required? (Current: optional.)
- D-320: Should `plotName` be required? (Current: optional.)
- D-321: Should records link to GenX `ExperimentalDesign`? (Current: no
  link.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
