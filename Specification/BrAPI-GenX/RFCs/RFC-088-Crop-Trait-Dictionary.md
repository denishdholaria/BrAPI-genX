# RFC-088 — Crop Trait Dictionary (Terminology)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 already provides `Trait`, `Ontology` and `ObservationVariable` resources. The candidate GenX crop-trait dictionary is a proposed different governance surface with optional crop and trait strings; no evidence presently establishes that the existing controlled ontology/trait model is insufficient or that a separate dictionary identity is needed.

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
- The candidate `cropDbId` is a plain string rather than a typed BrAPI Germplasm or crop-reference contract. It contains no typed GenX `VariableTerm` reference (D-264 remains open); matching names do not certify trait equivalence.
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
