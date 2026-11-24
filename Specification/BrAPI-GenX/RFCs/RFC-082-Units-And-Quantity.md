# RFC-082 — Units and Quantity (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record units and quantity semantics. Unit and
quantity conventions are the routine reference for measurement interpretation.
Without a record, units arrive as unversioned strings with no stated quantity
kind, definition, or provenance, so they cannot be audited or reproduced.

## 2. Object

`UnitsAndQuantity` — one immutable units and quantity semantics entry, with its
unit, quantity kind, definition, and provenance.

## 3. Endpoints

- `GET /genx/v1/units-and-quantities` (`genxListUnitsAndQuantities`)
- `POST /genx/v1/units-and-quantities` (`genxRegisterUnitsAndQuantity`)
- `GET /genx/v1/units-and-quantities/{unitsAndQuantityDbId}` (`genxGetUnitsAndQuantity`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The current units-and-quantity candidate contains no typed reference to
  GenX `VariableTerm` (D-246 remains unresolved). Matching descriptions,
  unit symbols or advisory operation links do not establish identity.
- A units entry is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `unitsAndQuantityDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the unit is validated or endorsed.

## 6. Deferred questions

- D-244: Should `unit` be required? (Current: optional.)
- D-245: Should `quantity` be a controlled vocabulary? (Current: free-form
  string.)
- D-246: Should entries link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
