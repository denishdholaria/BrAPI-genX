# RFC-072 — Genotype Call Semantics (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-013 (Genomic Datasets), RFC-043 (VCF Import), RFC-064 (Genotype QC), `../CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 standardizes variants, call sets, and calls but has no place to
record the semantics of how genotype calls and missing calls are interpreted:
missing-call policy, zygosity encoding, confidence thresholds, and allele
encoding. These conventions are exactly the evidence a reviewer needs to decide
whether two call sets are comparable. Without a semantics record, the same
dataset can be re-released with different interpretation claims and no audit
trail.

## 2. Object

`GenotypeCallSemantics` — one immutable record of call-interpretation
conventions applied to a BrAPI CallSet.

## 3. Endpoints

- `GET /genx/v1/genotype-call-semantics` (`genxListGenotypeCallSemantics`)
- `POST /genx/v1/genotype-call-semantics` (`genxRegisterGenotypeCallSemantics`)
- `GET /genx/v1/genotype-call-semantics/{genotypeCallSemanticsDbId}` (`genxGetGenotypeCallSemantics`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Semantics records reference BrAPI `CallSet` by identifier; they do not
  duplicate the CallSet or modify its calls.
- A semantics record is not a BrAPI data resource and must not be treated as
  one.

## 5. Invariants

- A published `genotypeCallSemanticsDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A semantics record does not alter BrAPI VariantCall values; it only documents
  conventions.
- A record does not imply that a call set passed QC, was released, or is
  scientifically valid.

## 6. Deferred questions

- D-214: Should `callSetDbId` be required? (Current: optional, so a record can
  describe a global convention.)
- D-215: Should `confidenceThreshold` and `missingCallPolicy` be required?
  (Current: both optional.)
- D-216: Should the encoding vocabularies be controlled GenX terminology
  instead of free-form strings? (Current: free-form strings.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
