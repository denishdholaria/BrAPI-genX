# RFC-017 — Measurement Methods (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting C4).

## 1. Problem

BrAPI v2.1 already defines a Method resource and dedicated
`/brapi/v2/methods` operations alongside observation variables. This GenX
proposal explores an additional immutable, namespaced method-definition
record with optional procedure, equipment, precision, and provenance fields.
It has not established that the official Method model cannot support the
intended governance workflow, nor that a separate identity is always needed.

## 2. Object

`MeasurementMethod` — one immutable measurement method definition.

## 3. Endpoints

- `GET /genx/v1/measurement-methods` (`genxListMeasurementMethods`)
- `POST /genx/v1/measurement-methods` (`genxRegisterMeasurementMethod`)
- `GET /genx/v1/measurement-methods/{measurementMethodDbId}` (`genxGetMeasurementMethod`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A typed link to an official BrAPI Method or Scale is not present in the
  current candidate `MeasurementMethod` schema. Equivalence or identity
  between these resources must not be inferred; D-49 remains open.
- A GenX measurement method is not a BrAPI Method and must not be treated as
  one.

## 5. Invariants

- A published `measurementMethodDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional methods linked by `supersedes`.
- `procedure`, `equipment`, and `precision` are recorded, not inferred.
- A method does not imply scientific validation or approval.

## 6. Deferred questions

- D-48: Should `methodType` be a governed enumeration? (Current: free string.)
- D-49: Should measurement methods require a BrAPI Method reference?
  (Current: optional.)
- D-50: Should precision be a structured quantity rather than a string?
  (Current: string.)

## 7. Classification

Primary domain: none (cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.