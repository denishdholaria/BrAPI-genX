# RFC-044 — Phenotype Annotation (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 standardizes observations but not phenotype annotations: scored
or annotated observations for an observation unit and variable. Without this
record, annotation and scoring workflows cannot be audited or reproduced.

## 2. Object

`PhenotypeAnnotation` — one immutable phenotype annotation record.

## 3. Endpoints

- `GET /genx/v1/phenotype-annotations` (`genxListPhenotypeAnnotations`)
- `POST /genx/v1/phenotype-annotations` (`genxRecordPhenotypeAnnotation`)
- `GET /genx/v1/phenotype-annotations/{phenotypeAnnotationDbId}` (`genxGetPhenotypeAnnotation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Phenotype annotations reference BrAPI Study, ObservationUnit, and
  Observation Variable by identifier; they do not duplicate those resources.
- A phenotype annotation is not a BrAPI Observation and must not be treated
  as one.

## 5. Invariants

- A published `phenotypeAnnotationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `annotation` and `variableDbId` are required.
- A record does not imply a complete phenotype dataset.

## 6. Deferred questions

- D-130: Should `annotation` be a governed vocabulary? (Current: free
  string.)
- D-131: Should phenotype annotations link to GenX `PhenotypeCapture`?
  (Current: optional, not required.)
- D-132: Should `annotatedAt` be required? (Current: optional.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.