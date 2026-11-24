# RFC-085 — Ontology Term (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record ontology terms and synonyms. Ontology terms
are the routine reference for semantic interoperability. Without a record,
terms arrive as unversioned strings with no stated ontology, synonyms, or
provenance, so they cannot be audited or reproduced.

## 2. Object

`OntologyTermRecord` — one immutable ontology term or synonym entry, with its term,
synonyms, source ontology, and provenance.

## 3. Endpoints

- `GET /genx/v1/ontology-terms` (`genxListOntologyTerms`)
- `POST /genx/v1/ontology-terms` (`genxRegisterOntologyTerm`)
- `GET /genx/v1/ontology-terms/{ontologyTermDbId}` (`genxGetOntologyTerm`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The current ontology-term candidate contains no typed reference to GenX
  `VariableTerm` (D-255 remains unresolved). Labels and synonyms alone do
  not establish an external ontology identifier or term equivalence.
- An entry is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `ontologyTermDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the term is validated or endorsed.

## 6. Deferred questions

- D-253: Should `term` be required? (Current: optional.)
- D-254: Should `ontology` be a controlled vocabulary? (Current: free-form
  string.)
- D-255: Should entries link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
