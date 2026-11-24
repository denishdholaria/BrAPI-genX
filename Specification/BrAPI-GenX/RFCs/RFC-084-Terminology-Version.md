# RFC-084 — Terminology Version (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 Ontology metadata already supports a version label through `/brapi/v2/ontologies`. This candidate explores separate namespaced terminology release metadata, but a version string and provenance alone do not pin the content of an external vocabulary, guarantee reproducible resolution, or justify a distinct record.

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
- The candidate contains no typed GenX `VariableTerm` reference (D-252 remains open), and a shared label does not establish terminology release equivalence to an official BrAPI Ontology.
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
