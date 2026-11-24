# Mission 074 — Variant annotation and GWAS result evidence boundaries

**Parent:** `32de809d52147a1c204da781abae5eea427cc43b` (Mission 073), 2026-11-24.  
**Scope:** two previously title-only GroupDescription files and related draft wording/test guards. No official BrAPI v2.1 contract, GenX schema, endpoint path, operation identifier, registry, semantic-neighbor entry, maturity designation, or deferred decision is changed.

## Source-grounded findings

1. **VariantAnnotation** (RFC-062, D-184–D-186): response requires only `variantAnnotationDbId` and `status`; registration request requires only the identifier. The `variantDbId` and `analysisMethodDbId` are optional strings, `annotations` is an optional unconstrained object, and `provenance` is optional. A record cannot establish allele normalization, functional consequence truth, reference assembly or transcript context, valid cross-authority reference, scientific comparability or independent reproduction. The official BrAPI v2.1 `Variant` schema already provides a flexible `additionalInfo` object; do not assert official BrAPI cannot carry variant-related metadata.
2. **GwasResult** (RFC-047, D-139–D-141): registration requires `gwasResultDbId` and `analysisMethodDbId`; response adds required `status`. `significantMarkers`, `topPValue`, `studyDbId`, `jobDbId`, `resultData`, and `provenance` are optional. There is no required analysis-method version, association threshold, multiple-testing correction, probability range, dataset join or standardized association-result table. A scalar `topPValue` does not establish genome-wide significance or reproducibility. D-140 had described a GenomicDataset relationship as optional, although the GwasResult schema contains **no** `genomicDatasetDbId` property; the question is therefore recorded as *not modelled*.

## Assurance changes

- Add two source-linked GroupDescription documents explicitly marked `STRUCTURAL_DRAFT`.
- Qualify corresponding README and Request for Comments (RFC) claims to match actual schema requirements.
- Add two reviewed modules to the group-description guard (expected evidence-reviewed documentation coverage: **115 of 156**, with **41 remaining deferred**).
- Add schema-derived regression checks for required/optional fields, unconstrained payloads, missing method-version linkage, official `Variant.additionalInfo`, and open decisions.
- Preserve all draft routes, source schemas and scientific governance statuses.

## Verification and limitations

The newly modified regression suite is `python Scripts/test_genx_group_descriptions.py`; the documentation guard is `python Scripts/check_genx_group_descriptions.py`. Run these and the existing source/registry/contract checks before merging. GitHub connector edits do **not** constitute local test execution; a successful syntax or source inspection is not equivalent to passing the complete repository suite.

This work qualifies evidence, but does not standardize any variant consequence ontology, statistical inference policy, method/version resolution, workflow, or cross-generation equivalence.
