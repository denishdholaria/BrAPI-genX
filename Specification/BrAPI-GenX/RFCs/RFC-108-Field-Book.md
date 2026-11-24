# RFC-108 — Field Book (Experimental Design)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI version 2.1 already provides Studies, Observation Units and variables. A separate candidate FieldBook definition may record capture-configuration provenance, but it is not established as an interoperable capture schema merely by naming it.

## 2. Object

`FieldBook` — one immutable field book definition record, with its field
linkage, definition, and provenance.

## 3. Endpoints

- `GET /genx/v1/field-books` (`genxListFieldBooks`)
- `POST /genx/v1/field-books` (`genxRegisterFieldBook`)
- `GET /genx/v1/field-books/{fieldBookDbId}` (`genxGetFieldBook`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The proposed record has no typed link to an official BrAPI identity and no validated identity mapping. The candidate `fieldBookDbId` is not a BrAPI Study or Location identity. Optional free-text `definition` and `fieldDbId` do not bind observation variables or define validated field layout; no typed GenX ExperimentalDesign reference exists. D-324 remains open.
- A record is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `fieldBookDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the field book is validated or endorsed.

## 6. Deferred questions

- D-322: Should `fieldDbId` be required? (Current: optional.)
- D-323: Should `definition` be required? (Current: optional.)
- D-324: Should records link to GenX `ExperimentalDesign`? (Current: no
  link.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
