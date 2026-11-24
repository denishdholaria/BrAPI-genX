# RFC-058 — Expression QTL (Scientific Compute)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D7).

## 1. Problem

GenX proposes separately identified expression quantitative trait locus
(eQTL) analysis metadata alongside official BrAPI version 2.1 resources.
A reproducible association needs genetic and expression measurements,
gene and variant identities, tissue context, covariate handling, statistical
models, and multiple-testing policy. The current candidate does not require
those details or independently validate gene regulation.

## 2. Object

`ExpressionQtl` — one immutable expression QTL result record.

## 3. Endpoints

- `GET /genx/v1/expression-qtls` (`genxListExpressionQtls`)
- `POST /genx/v1/expression-qtls` (`genxRecordExpressionQtl`)
- `GET /genx/v1/expression-qtls/{expressionQtlDbId}` (`genxGetExpressionQtl`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- `analysisMethodDbId` is a required method identifier string, not an
  exact method-version binding or evidence of executed eQTL inference.
- A result is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `expressionQtlDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional results linked by `supersedes`.
- `analysisMethodDbId` is required; `qtls`, `jobDbId`, `studyDbId`,
  and provenance are optional.
- `qtls` is an unconstrained object. Marker/gene relationships, p-values,
  multiple-testing correction, expression units and effect uncertainty
  are not schema-enforced.
- A registered result does not establish transcriptomic association
  significance, regulatory causality, comparability or scientific approval.

## 6. Deferred questions

- D-172: Should `qtls` be required? (Current: optional.)
- D-173: Should expression QTLs link to GenX `GenomicDataset`? (Current:
  no `genomicDatasetDbId` field is modelled.)
- D-174: Should p-value threshold be required? (Current: no first-class
  p-value threshold is modelled; `qtls` may contain opaque method data.)

## 7. Classification

Primary domain: D7 — Scientific Analysis, Models and Derived Evidence.
Cross-cutting: C1, C2, C3 (POST), C6, C9.