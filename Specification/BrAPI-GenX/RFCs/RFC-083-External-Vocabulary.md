# RFC-083 — External Vocabulary (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 already exposes ontology metadata through `GET /brapi/v2/ontologies`. This separate draft explores recording external vocabulary synchronization metadata, but its optional source, target, and unstructured mapping properties are not a synchronization engine. Neither a reproducible term transfer nor the need for an additional GenX identity has been demonstrated.

## 2. Object

`ExternalVocabulary` — one immutable external vocabulary sync entry, with its
source, target, mapping, and provenance.

## 3. Endpoints

- `GET /genx/v1/external-vocabularies` (`genxListExternalVocabularies`)
- `POST /genx/v1/external-vocabularies` (`genxRegisterExternalVocabulary`)
- `GET /genx/v1/external-vocabularies/{externalVocabularyDbId}` (`genxGetExternalVocabulary`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The draft contains no typed GenX `VariableTerm` reference (D-249 remains open). Its free-form `mapping` object and string system names cannot attest to valid ontology equivalence or execution.
- An entry is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `externalVocabularyDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the sync is validated or endorsed.

## 6. Deferred questions

- D-247: Should `source` and `target` be required? (Current: optional.)
- D-248: Should `mapping` be a controlled structure? (Current: free-form
  object.)
- D-249: Should entries link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
