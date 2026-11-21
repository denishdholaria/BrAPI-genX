# RFC-086 — Ontology Mapping (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record ontology mappings and crosswalks. Ontology
mapping is the routine reference for semantic interoperability. Without a
record, mappings arrive as unversioned notes with no stated source, target,
mapping, or provenance, so they cannot be audited or reproduced.

## 2. Object

`OntologyMapping` — one immutable ontology mapping or crosswalk entry, with its
source, target, mapping, and provenance.

## 3. Endpoints

- `GET /genx/v1/ontology-mappings` (`genxListOntologyMappings`)
- `POST /genx/v1/ontology-mappings` (`genxRegisterOntologyMapping`)
- `GET /genx/v1/ontology-mappings/{ontologyMappingDbId}` (`genxGetOntologyMapping`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Ontology mapping entries reference GenX `OntologyTerm` by identifier; they
  do not duplicate those resources.
- An entry is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `ontologyMappingDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the mapping is validated or endorsed.

## 6. Deferred questions

- D-256: Should `source` and `target` be required? (Current: optional.)
- D-257: Should `mapping` be a controlled structure? (Current: free-form
  object.)
- D-258: Should entries link to GenX `OntologyTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
