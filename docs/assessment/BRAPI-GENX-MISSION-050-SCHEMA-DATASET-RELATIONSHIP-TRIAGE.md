# Mission 050 — Schema mapping versus genomic dataset relationship triage

**Date:** 2026-11-24
**Prepared parent:** `51609a4ac31c27a228b9c595c681aa01370c85d3`
**Status:** Non-normative, decision-gated review of exactly three inherited operation-neighbor records.

## Source findings

- `Specification/BrAPI-GenX/Interoperability/SchemaMapping/Schemas/SchemaMapping.yaml` defines an independently named mapping metadata record. `mappingRules`, `sourceSchema`, and `targetSchema` are optional strings, not a verified executable transformation or a typed GenomicDataset reference. RFC-152 is DEFERRED, with D-457–D-459 unresolved.
- `Specification/BrAPI-GenX/Genotyping/GenomicDatasets/Schemas/GenomicDataset.yaml` defines a prepared genomic dataset with required dataset identity, name, type and reference-assembly string, but no typed reference to SchemaMapping. Registering a mapping cannot be inferred to register or validate a dataset.
- Existing inherited links are three operation neighbors: SchemaMapping get/list/record to `genxRegisterGenomicDataset`. A navigation edge cannot encode field-level transformations, scientific ownership, cardinality, execution results or authorization.

## Transition and open question (M050-Q1)

The three links change from `inherited-unreviewed` to `requires-decision`, which is expressly permitted by the governance ledger. The scientific question is whether a **future**, separately approved dataset release should reference an authority-scoped, versioned and verified transformation; if not, the operation neighbors may remain advisory. Neither outcome is decided here.

All **153** identities are retained: previously **51 requires-decision / 102 unreviewed**, now **54 requires-decision / 99 unreviewed**. No target/source operation was edited or deleted. The independent typed-relationship proposal register remains unchanged, no accepted status was introduced, and no semantics were promoted. An inventory regression test verifies these three records and the held identities.

Hosted governance and regression checks must run on the integrated commit before claiming success.
