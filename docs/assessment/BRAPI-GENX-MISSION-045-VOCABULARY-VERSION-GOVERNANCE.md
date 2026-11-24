# Mission 045 — Candidate vocabulary/version governance audit

**Date:** 2026-11-24
**Prepared parent:** `6f4f5d2fc1f08c2d1c6aaa5e83cf3ae7a991b5ad`
**Scope:** ExternalVocabulary (RFC-083), TerminologyVersion (RFC-084), ReferenceDataVersion (RFC-093), CropTraitDictionary (RFC-088), plus evidence/provenance guard updates. No wire-schema or official BrAPI source modification.

## Official standards reuse

Official BrAPI v2.1 `/ontologies` already publishes metadata about locally or externally available ontologies, including a `version` field, and `/traits` plus observation variables already model traits. The four GenX draft objects are not substitutes for these official resources; they propose separate metadata scopes with unproven need for new independent identities.

## Source-backed distinctions

- ExternalVocabulary has optional source/target strings and an unrestricted mapping object. It does not execute synchronization or represent verified ontology equivalence.
- TerminologyVersion contains optional terminology/version strings and no release content digest, immutable membership set, or typed VariableTerm link.
- ReferenceDataVersion has optional source/version strings, no immutable external snapshot proof, and no typed link to BrAPI or VariableTerm.
- CropTraitDictionary has an optional free-text `cropDbId`, trait and definition, no enforced official Germplasm/trait identity, and no typed VariableTerm link. Official Trait/Ontology resources remain authoritative for official BrAPI exchange.

Four candidate RFCs and four README files were corrected to reflect these limits rather than asserting missing official capabilities or nonexistent typed links. Four source-backed group descriptions were pinned, bringing the guarded set to **30 of 156**, with **126 deferred**.

## Evidence and tests

The Mission 043 manifest now records nine (formerly five) missing/unratified typed-link observations. The audit enforces schema/decision provenance with source-linked test fixtures. Two group-description regression tests protect the new modules and official source overlap. All local Markdown evidence links were resolved against the inspected repository tree.

Outstanding decisions D-247–D-249, D-250–D-252, D-277–D-279 and D-262–D-264 remain open. No source becomes normative or independently conformant solely through documentation or tests.

## Verification

Hosted static/live conformance and specification generation must be confirmed on the integrated commit. Prior successful runs do not establish this commit's status.
