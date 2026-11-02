# RFC-083 — External Vocabulary (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record external vocabulary synchronization.
External vocab sync is the routine reference for terminology governance.
Without a record, syncs arrive as unversioned notes with no stated source,
target, mapping, or provenance, so they cannot be audited or reproduced.

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
- External vocabulary entries reference GenX `VariableTerm` by identifier; they
  do not duplicate those resources.
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
