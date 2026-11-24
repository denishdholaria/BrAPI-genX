# RFC-062 — Variant Annotation (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-009 (Analysis Methods), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 provides a `Variant` resource with an open `additionalInfo` object,
but not the separately identified annotation lifecycle proposed here.
Functional variant interpretation requires controlled methods and reference
context to be comparable across pipelines. The present GenX candidate can
carry annotation metadata; it does not guarantee that an annotation is
scientifically interpretable, comparable, or independently reproducible.

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
- `variantDbId` is optional and does not establish a validated, authority-
  matched link to a BrAPI `Variant`; a candidate annotation does not duplicate
  or amend that official resource.
- `analysisMethodDbId` is optional, and no exact method-version binding is
  enforced by this record's schema. A supplied string does not establish that
  the named analysis was executed.
- An annotation is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `variantAnnotationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional annotations linked by `supersedes`.
- A record does not imply scientific validation or approval.
- `annotations` is an optional unconstrained object. No gene, transcript,
  consequence vocabulary, reference assembly, allele-normalization rule,
  provenance or method-version constraint is enforced. External scientific
  interpretation requires independent evidence.

## 6. Deferred questions

- D-184: Should `variantDbId` be required? (Current: optional.)
- D-185: Should `annotations` be required, and should its shape be
  constrained beyond a free-form object? (Current: optional, opaque object.)
- D-186: Should variant annotations link to GenX `VariantSet` or
  `GenomicDataset` rather than only BrAPI `Variant`? (Current: not modelled.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
