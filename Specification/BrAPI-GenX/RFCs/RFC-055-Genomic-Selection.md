# RFC-055 — Genomic Selection (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes separately identified genomic selection results alongside
official BrAPI v2.1 records. Such a result does not independently establish
the breeder's authorized verdict, exact selection index, population
eligibility, or prediction-model validity. The proposal's optional result
fields cannot by themselves establish a reproducible breeding decision.

## 2. Object

`GenomicSelection` — one immutable genomic selection result record.

## 3. Endpoints

- `GET /genx/v1/genomic-selections` (`genxListGenomicSelections`)
- `POST /genx/v1/genomic-selections` (`genxRecordGenomicSelection`)
- `GET /genx/v1/genomic-selections/{genomicSelectionDbId}` (`genxGetGenomicSelection`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `analysisMethodDbId` is a required string reference, not a verified
  exact method-version join or evidence of authorized execution.
- This proposal does not replace a separately authorized
  `SelectionDecision` record or its required decision context.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `genomicSelectionDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required; `selectedGermplasm`,
  `selectionThreshold`, `studyDbId`, `jobDbId`, and provenance are optional.
- An array of germplasm identifier strings and a numeric threshold do not
  require a validated ranking, index scale, trait weights, eligibility
  population, breeder authorization, or a linked decision.
- A result does not imply genetic merit, scientific validation, release,
  advancement, or independent reproducibility.

## 6. Deferred questions

- D-163: Should `selectedGermplasm` be required? (Current: optional.)
- D-164: Should genomic selections link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` property is modelled.)
- D-165: Should selection threshold be required? (Current: optional.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.