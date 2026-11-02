# RFC-088 — Crop Trait Dictionary (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record crop-specific trait dictionaries. Crop trait
dictionaries are the routine reference for trait semantics. Without a record,
traits arrive as unversioned strings with no stated crop, definition, or
provenance, so they cannot be audited or reproduced.

## 2. Object

`CropTraitDictionary` — one immutable crop trait dictionary entry, with its
crop linkage, trait, definition, and provenance.

## 3. Endpoints

- `GET /genx/v1/crop-trait-dictionaries` (`genxListCropTraitDictionaries`)
- `POST /genx/v1/crop-trait-dictionaries` (`genxRegisterCropTraitDictionary`)
- `GET /genx/v1/crop-trait-dictionaries/{cropTraitDictionaryDbId}` (`genxGetCropTraitDictionary`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Crop trait dictionary entries reference BrAPI `Germplasm` by identifier; they
  do not duplicate those resources.
- An entry is not a BrAPI Observation and must not be treated as one.

## 5. Invariants

- A published `cropTraitDictionaryDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the trait is validated or endorsed.

## 6. Deferred questions

- D-262: Should `cropDbId` be required? (Current: optional.)
- D-263: Should `trait` be a controlled vocabulary? (Current: free-form
  string.)
- D-264: Should entries link to GenX `VariableTerm`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
