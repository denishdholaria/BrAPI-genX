# Mission 089 — BulkCapture source review and official Observation parity

**Parent:** Mission 088 draft development branch `33f92e9a4618285cb2d04e55727144c35a65606a`.  
**Scope:** documentation, source-backed group evidence and schema-derived regressions only; no official BrAPI (Breeding Application Programming Interface) 2.1 schema, GenX wire schema, route/operation identity, endpoint registry, maturity state or approved decision is modified.

## Verified defects and scientific limits

- **BrAPI overlap:** official `POST /observations` already accepts an array of `ObservationNewRequest` objects. It is false to imply official BrAPI cannot perform batch submissions. The GenX proposal represents a separate capture-event envelope and does not define atomic ingestion or a verified mapping to official Observation records.
- **Required fields:** GenX BulkCapture requires `bulkCaptureDbId`, `studyDbId`, timestamp `capturedAt` and an `entries` array in registration; the response additionally requires lifecycle `status`.
- **Empty batch allowed:** `entries` has no `minItems`. Each entry requires only `variableDbId`; optional `observationUnitDbId`, nullable numeric `value`, `unit`, and `qualityFlag` are not enforced as complete or scientifically valid observations.
- **Type narrowing:** official ObservationNewRequest `value` is nullable string data, which may represent categorical responses; GenX BulkCapture's optional numeric value does not cover the same range of scientific scales.
- **Unsupported relationship claims:** D-119 and D-120 in RFC-040 described proposed PhenotypeCapture/FieldBook links as optional, but neither `phenotypeCaptureDbId` nor `fieldBookDbId` exists in either BulkCapture schema. Both are now stated as **unmodelled**, without approving new links. D-118 (minimum entry cardinality) remains deferred.
- No source-backed authority join, per-entry Observation identity, transactional upload status, measurement-unit validation, instrument-calibration evidence, missing-reason condition or guaranteed quality flag is represented.

## Changes and test gate

- Replaced the title-only BulkCapture group description with evidence-backed `STRUCTURAL_DRAFT` documentation, preserving all deferred decisions.
- Qualified module README and RFC-040 to separate a capture-event record from official BrAPI array submission and correct unsupported relationship language.
- Added regression assertions on exact schema required fields, missingness/cardinality, entry numeric type and optionals, unmodelled relationships, official Observation array submission and string-valued scale.
- Proposed reviewed-description coverage increases from **139/156** to **140/156**, leaving **16 evidence-deferred** if tests pass. This is documentation-review evidence, not scientific acceptance or server conformance.

## Verification required

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkGenXConformance.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
```

The full hosted static, live and generated-artifact checks must pass on the final head before merging. **Status: draft; validation pending at authoring time.**
