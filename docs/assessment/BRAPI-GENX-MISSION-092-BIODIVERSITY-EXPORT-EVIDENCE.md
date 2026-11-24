# Mission 092 — Biodiversity export candidate versus publishable dataset

**Parent:** Mission 091 draft branch `8b264a5251f5fc55b1dd2b586e7bc13b022a5904`. **Scope:** evidence-only documentation and source-based regression assertions; no official BrAPI (Breeding Application Programming Interface) contracts, GenX wire schemas, endpoint registry, authority, scientific maturity or governance decisions are changed.

## Primary source findings

- Current GenX `BiodiversityExportNewRequest` requires only `biodiversityExportDbId`. The response additionally requires lifecycle `status`.
- Optional `specimenType`, `occurrenceId`, `collectionDate`, `location`, `taxon`, `supersedes` and `provenance` are unvalidated metadata. `collectionDate` has no `format: date`; `taxon` is free text; location provides no structured coordinates.
- No typed Darwin Core Archive, mapping of occurrence fields, data bytes or archive retrieval address, dataset identifier, publisher/license metadata, destination, delivery state, accepted publication identifier, or export receipt exists. `active` reflects registry lifecycle, **not successful publication**.
- The official BrAPI version 2.1 Germplasm Multi-Crop Passport Descriptors source already carries collection context, and GenX FAIRPackage separately describes package metadata; this draft does not establish a typed `germplasmDbId`, ResearchAsset link or approved conversion between standards.
- Decision questions D-361 (required occurrence ID), D-362 (controlled taxon) and D-363 (ResearchAsset link) are still open. No automatic ratification or scientific acceptance is implied.

## Independent biodiversity standard comparison

The **Biodiversity Information Standards (TDWG)** Darwin Core term reference describes structured occurrence/event/taxonomic/location fields including occurrence identity, event date and coordinates: https://dwc.tdwg.org/terms/

The **Global Biodiversity Information Facility (GBIF)** publishing documentation describes dataset publication using Darwin Core Archives and quality/metadata requirements:
- https://techdocs.gbif.org/en/data-publishing/
- https://www.gbif.org/data-quality-requirements-occurrences

This comparison is **informative, not a declaration that the GenX draft implements those external standards or that every field listed is universally mandatory**. The export descriptor neither produces nor validates a Darwin Core Archive, and cannot establish GBIF acceptance.

## Changes and safeguards

- Replaced a title-only `GroupDescription.md` with source-linked **STRUCTURAL_DRAFT** interpretation.
- Corrected module README and RFC-121 to distinguish metadata registration from data transfer or publication.
- Added schema-derived regression assertions pinning requiredness, optional fields, absence of archive/publisher/typed Germplasm metadata, and exact endpoint identities.
- Proposed evidence-reviewed count **144/156**, **12 evidence-deferred**, if Missions 091 and 092 pass and integrate. Coverage reflects documentation evidence, not normative conformance or scientific validity.

## Verification

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Hosted static and live reference conformance and specification generation must succeed on this head before integration, and Mission 091 must merge first. **Status: draft pending tests.**
