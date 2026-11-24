# Mission 079 — Haplotype, expression-QTL and methylation evidence boundaries

**Parent:** Mission 078 branch, commit `ed4e2e4f1244a1255420bb76bc5bd8b7e8d8b822`, 2026-11-24.  
**Scope:** scientific interpretation of three draft GenX data records with source-derived assertions only. Official Breeding Application Programming Interface (BrAPI) version 2.1 contracts, GenX wire schemas and operations, registry identities, scientific decision statuses, and maturity remain unchanged.

## Source-grounded findings

1. **HaplotypeAnalysis** (Request for Comments (RFC) 059, D-175–D-177): response requires `haplotypeAnalysisDbId`, `analysisMethodDbId` and status; registration requires the first two. `haplotypes` is an optional, unconstrained object. No mandatory phase-set/sample identity, ploidy, reference genome, haplotype length, allele encoding or confidence. D-176 inaccurately described the absent `genomicDatasetDbId` as merely optional; D-177 described a haplotype-length field as optional, although none is defined.
2. **ExpressionQtl** (RFC-058, D-172–D-174): response requires `expressionQtlDbId`, `analysisMethodDbId` and status; registration requires the first two. `qtls` is optional/opaque. Example nested p-values do not define required test results, gene and variant identities, expression normalization, covariate controls, false-discovery threshold or significance. There is no modelled `genomicDatasetDbId`, and D-174 refers to a p-value threshold that does not exist as a first-class field.
3. **MethylationAnalysis** (RFC-057, D-169–D-171): response requires `methylationAnalysisDbId`, `analysisMethodDbId` and status; registration requires the first two. `regions` is optional/opaque. Example methylation `level` is not a required calibrated value; no obligatory assay tissue, cytosine context, genomic assembly, coverage, or scale. D-170 refers to an unmodelled dataset field, and D-171 to an unmodelled first-class methylation level.

For all three, a required `analysisMethodDbId` is a string, not an exact method-version or execution-evidence guarantee. A stored record is not proof of scientifically validated genomic/transcriptomic/epigenomic inference.

## Implementation

- Add source-linked, clearly draft `GroupDescription.md` documents for three previously title-only modules.
- Qualify READMEs and RFCs to avoid unsupported evidence claims and correct **optional vs unmodelled** distinctions while retaining all deferred decisions.
- Extend reviewed-description guards to **127/156** on the stacked branch (29 deferred).
- Add schema-derived regression checks for required and optional property sets, opaque nested structures, absence of version/dataset linkage, and preservation of RFC deferred boundaries.

## Verification

Source links and authoritative schema fields should be inspected before integration. Execute the group-description test suite, group-description guard, strict registry/source audit, generated-artifact check, endpoint registry and static/live conformance where applicable. GitHub connector writes and remote source inspection do not equal executed Python tests.

No scientific equivalence, normative promotion, pipeline correctness, or production persistence is claimed.
