# RFC-139 — Local Constraint (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 does not define a dedicated local-constraint rule-exchange
operation. However, this candidate currently records only free-text
constraint type, value, region and source; it specifies no issuing
authority, effective interval, legal jurisdiction, binding rule or
evaluation engine. Such a metadata record cannot itself enforce
water restrictions, application limits or other legal requirements.

## 2. Object

`LocalConstraint` — one immutable local constraint record, with its constraint
type, value, region/zone, source, and provenance.

## 3. Endpoints

- `GET /genx/v1/local-constraints` (`genxListLocalConstraints`)
- `POST /genx/v1/local-constraints` (`genxRegisterLocalConstraint`)
- `GET /genx/v1/local-constraints/{localConstraintDbId}` (`genxGetLocalConstraint`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `localConstraintDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-415: Should `constraintValue` be required? (Current: optional.)
- D-416: Should `constraintType` be a controlled vocabulary? (Current: free-form string.)
- D-417: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
