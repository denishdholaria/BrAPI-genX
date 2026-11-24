# Mission 049b — VCF import record and actual identifier semantics

**Date:** 2026-11-24
**Prepared parent:** `1507f5076a2aabdb528c2605ddda854b281f281b`
**Scope:** candidate RFC-043/README correction, one source-backed group description, regression tests.

Official BrAPI v2.1 already represents VariantSets and reference genomes. The proposed GenX VcfImport record has a **required** string `genomicDatasetDbId`, `importedAt` and `sourceFormat`. This explicit dataset identifier is not evidence of real persistent referential integrity or successful VCF parsing/ingestion. The candidate has **no typed VariantMatrix field**, despite RFC-043's previous statement that this was optional; D-128 remains unresolved.

The guarded group inventory reaches **42 of 156** (114 deferred). The absent-link evidence manifest grows to **21**, with **VcfImport -> VariantMatrix** counted as absent, while **VcfImport -> GenomicDataset** is explicitly present as a draft string field and thus not misclassified.

No official BrAPI source, GenX wire schema or route, scientific relationship decision, endpoint registry or maturity was changed. Hosted static/live and generation verification remain required on integrated commit.
