# Mission 049 — Genomic reference identity and pipeline provenance

**Date:** 2026-11-24
**Prepared parent:** `e10e310de0002969933b1a1ed5374c25fafd27a9`
**Scope:** RFC-115 and RFC-116 candidate source truth, documentation and regression guards. No new wire contract.

## Finding 1: official BrAPI ReferenceSets

Official BrAPI version 2.1 `Specification/BrAPI-Genotyping/ReferenceSets/Schemas/ReferenceSet.yaml` already describes reference genomes, their reference sets, and coordinate context. RFC-115 falsely described assembly coverage as absent. Candidate ReferenceAssembly stores optional accession and version metadata but cannot prove a mapping to an official ReferenceSet or a GenX GenomicDataset.

## Finding 2: pipeline-provenance copy/paste contamination

RFC-116 originally described reference genome assemblies in its problem, object, compatibility and validity statements despite the actual PipelineProvenance schema containing optional pipeline name, version, string parameters, inputs and outputs. The RFC is corrected to discuss execution metadata and its limitations. No evidence establishes actual computation, reproducibility, input/output lineage, or a typed GenomicDataset reference.

## Governance and verification

New source-backed, explicitly STRUCTURAL_DRAFT group descriptions are pinned; guarded groups increase to **41/156** (115 evidence-deferred). The missing/unratified link evidence manifest grows to **20** observations and tests verify the official ReferenceSet schema. Scientific decisions D-343–D-345 and D-346–D-348 remain open.

No official BrAPI v2.1 sources, GenX route, OpenAPI schema, registry identity, scientific relationship approval or maturity status changed. Full hosted static/live and specification generation are required on the integrated commit.
