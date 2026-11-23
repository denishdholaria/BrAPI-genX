# Mission 006 — ExperimentalProtocol–GenomicDataset Semantic Review

**Date:** 2026-11-23  
**Baseline:** `6d1533da25ce257718e0d39ff4cbf157e56669ba`  
**Authority:** advisory source-contract assessment only, non-normative.

## Three inherited operation-level links

| Source operation | Target operation | New ledger status |
|---|---|---|
| `genxGetExperimentalProtocol` | `genxRegisterGenomicDataset` | `requires-decision` |
| `genxListExperimentalProtocols` | `genxRegisterGenomicDataset` | `requires-decision` |
| `genxRegisterExperimentalProtocol` | `genxRegisterGenomicDataset` | `requires-decision` |

The links are registry-only: they are absent from source OpenAPI
semantic-neighbor declarations. They are not public foreign-key or
resource-reference contracts.

## Verified source-contract boundary

- `Specification/BrAPI-GenX/Breeding/ExperimentalProtocol/Schemas/ExperimentalProtocol.yaml`
  models a design-time procedure: protocol design, treatments, blocks,
  randomization, versions and provenance. It has no typed GenomicDataset link.
- `Specification/BrAPI-GenX/Genotyping/GenomicDatasets/Schemas/GenomicDataset.yaml`
  models a prepared molecular dataset: assembly, pipeline metadata, counts,
  digests, access and release status. It has no typed ExperimentalProtocol link.
- RFC-117 and RFC-013 are structural proposals, not accepted inter-resource
  mappings. Their D2/D3 scientific-domain distinction is real; a cross-domain
  link could exist, but would require specific evidence.
- None of the three *operation identifiers* can be equated with a scientific
  data-derivation relation. Reading/listing a protocol does not create
  or validate a genomic dataset.

## Scientific ownership and safety

ExperimentalProtocol remains authoritative for a protocol definition;
GenomicDataset remains authoritative for genomic dataset metadata. Neither
should copy the other's identity or infer generation/equivalence.
Preserve original registry entries and IDs while awaiting a decision.
No automatic registration, duplication, conversion or authorization
is justified by the current references.

## Pending maintainer question: SEM-EP-GD-Q1

What relationship, if any, should these operation-neighbor entries represent?

| Option | Preconditions | Assessment |
|---|---|---|
| A — Reject generated operation links in a separate authorized migration | Preserve historical ledger records, document rejection, update registry and drift baseline correctly | Preferred without evidence for an actual protocol–dataset link |
| B — Define an optional explicit provenance mapping | Real workflow, authoritative source/target identities, exact version, directionality, consent/security, examples and independent tests | Reasonable only after the evidence exists |
| C — Retain as discovery-only neighbors | Precise, non-equivalent operation-level discovery semantics and a falsifiable use case | Not supported by present schemas |

**Current disposition:** all three `requires-decision`, not rejected or
accepted. No terminal decision is being taken on behalf of the maintainer.

## Falsifiers and acceptance criteria

An independently reproducible use case with a typed source/target relationship,
identity scope and provenance would justify reconsidering Option B.
A supposed equivalence between protocol GET/LIST and dataset POST is contradicted
by operation semantics. Before approval, require source-version stability,
access enforcement, non-disclosure and two independent interpretations.

## Inventory after this bounded review

- Original relationship identities: **153 retained**.
- `inherited-unreviewed`: **150**.
- `requires-decision`: **3**.
- Rejected/superseded/promoted by this review: **0**.

This document is scientific design evidence, not an implementation or conformance
result. No public routes, OpenAPI contracts, or official BrAPI v2.1 sources change.
