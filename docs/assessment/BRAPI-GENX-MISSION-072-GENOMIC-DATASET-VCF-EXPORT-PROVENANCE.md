# Mission 072 — GenomicDataset reference identity and VCF export claims

**Prepared against parent:** `0362c8216a87f5b03323eb10f27c047851f24034` (Mission 071), 2026-11-24.
**Scope:** source-backed group documentation and source-claim regression tests. No wire-schema, endpoint, registry, official BrAPI or governance-maturity modification.

## Evidence and discrepancies

1. GenX `GenomicDataset` does **not** contain `variantSetDbId`, `callSetDbId`, or `variantMatrixDbId`, despite RFC-013 asserting those references. Its free-text `referenceAssembly` is not an official BrAPI ReferenceSet identity. Proposed data-release, access, digest and pipeline metadata do not establish storage, authorization, provenance validity or a checkable data lineage.
2. GenX `VcfExport` does **not** contain the `vcfImportDbId` referenced in RFC-114. Its schema has no required format, input dataset, output locator, content digest or file encoding. A registration is not a successful VCF export.
3. Official BrAPI 2.1 `POST /brapi/v2/variantsets/extract` creates a new VariantSet from selected Calls. This is an existing interoperable operation but cannot be presented as proof of an independently generated or delivered VCF file.

## Change scope and regression

Review `Genotyping/GenomicDatasets` and `Genotyping/VcfExport` module descriptions; correct RFC-013 and RFC-114, and qualify two module overviews. Add regression tests that pin actual schema required fields, absent reference fields and the official VariantSet extraction operation. Increase reviewed GroupDescription count from 109 to **111/156**; 45 remain evidence-deferred.

## Governance

D-36–38 and D-340–342 remain open. Source text and tests do not grant a new identifier mapping, data-access entitlement, scientific equivalence or independent implementation conformance. Hosted verification must be observed separately before marking execution gates passed.
