# RFC-062 — Variant Annotation (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 has no variant annotation record. Functional variant annotation
is essential for interpreting genotyping results. Without this record,
annotations produced by different pipelines cannot be audited, compared, or
reproduced.

## 2. Object

`VariantAnnotation` — one immutable variant annotation record.

## 3. Endpoints

- `GET /genx/v1/variant-annotations` (`genxListVariantAnnotations`)
- `POST /genx/v1/variant-annotations` (`genxRecordVariantAnnotation`)
- `GET /genx/v1/variant-annotations/{variantAnnotationDbId}` (`genxGetVariantAnnotation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Variant annotations reference BrAPI `Variant` by identifier; they do not
  duplicate that resource.
- Variant annotations reference GenX AnalysisMethod by identifier when
  applicable; they do not duplicate that resource.
- An annotation is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `variantAnnotationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional annotations linked by `supersedes`.
- A record does not imply scientific validation or approval.
- Annotation content is opaque to the transport; interpretation is governed
  by the referenced method and provenance.

## 6. Deferred questions

- D-184: Should `variantDbId` be required? (Current: optional.)
- D-185: Should `annotations` be required, and should its shape be
  constrained beyond a free-form object? (Current: optional, opaque object.)
- D-186: Should variant annotations link to GenX `VariantSet` or
  `GenomicDataset` rather than only BrAPI `Variant`? (Current: not modelled.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
