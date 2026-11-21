# RFC-084 — Terminology Version (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record terminology versioning and provenance.
Terminology versioning is the routine reference for reproducible analytics.
Without a record, terminology versions arrive as unversioned strings with no
stated version, provenance, or status, so they cannot be audited or reproduced.

## 2. Object

`TerminologyVersion` — one immutable terminology version entry, with its
terminology name, version label, and provenance.

## 3. Endpoints

- `GET /genx/v1/terminology-versions` (`genxListTerminologyVersions`)
- `POST /genx/v1/terminology-versions` (`genxRegisterTerminologyVersion`)
- `GET /genx/v1/terminology-versions/{terminologyVersionDbId}` (`genxGetTerminologyVersion`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Terminology version entries reference GenX `VariableTerm` by identifier; they
  do not duplicate those resources.
- An entry is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `terminologyVersionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the terminology is validated or endorsed.

## 6. Deferred questions

- D-250: Should `terminology` be required? (Current: optional.)
- D-251: Should `version` be required? (Current: optional.)
- D-252: Should entries link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
