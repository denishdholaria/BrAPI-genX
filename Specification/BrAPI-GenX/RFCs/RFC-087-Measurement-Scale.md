# RFC-087 — Measurement Scale (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 already defines a Scale resource and dedicated `/brapi/v2/scales`
operations, including units and permitted values. This GenX proposal explores
a distinct, immutable, namespaced metadata entry for governing scale
descriptions across authorities. The necessity of a separate record and its
mapping to official BrAPI Scale identifiers remain to be demonstrated.
It must not be presented as filling an absent BrAPI Scale capability.

## 2. Object

`MeasurementScale` — one immutable measurement scale and value domain entry,
with its scale name, value domain, and provenance.

## 3. Endpoints

- `GET /genx/v1/measurement-scales` (`genxListMeasurementScales`)
- `POST /genx/v1/measurement-scales` (`genxRegisterMeasurementScale`)
- `GET /genx/v1/measurement-scales/{measurementScaleDbId}` (`genxGetMeasurementScale`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The candidate `MeasurementScale` schema defines no typed link to GenX
  `VariableTerm` or to the official BrAPI `Scale` resource. Such links are
  not implied by shared labels or operation-neighbor navigation.
- Official BrAPI Scale records and operations retain their published meaning.
- An entry is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `measurementScaleDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the scale is validated or endorsed.

## 6. Deferred questions

- D-259: Should `scaleName` be required? (Current: optional.)
- D-260: Should `valueDomain` be a controlled structure? (Current: free-form
  string.)
- D-261: Should entries link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
