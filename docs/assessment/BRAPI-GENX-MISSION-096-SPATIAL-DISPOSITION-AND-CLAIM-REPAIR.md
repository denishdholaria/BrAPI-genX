# Mission 096 — Spatial candidate disposition without premature execution claims

**Parent:** Mission 095 branch head `a7245af10b4857ed5dfbad7a7b307eb1c7440d41`. This work follows [Mission 090](./BRAPI-GENX-MISSION-090-SPATIAL-GOVERNANCE-PREFLIGHT.md): the earlier G-090-1/2/3 options are **not ratified**. The spatial GroupDescriptions remain **evidence-deferred** and are deliberately not added to the reviewed-description guard.

## Source-derived corrections

1. **SpatialIndex (RFC-141, D-421–D-423):** A metadata descriptor is not a physical spatial index. Registering an optional `indexType`, `coverageArea` or `resolution` cannot construct or query an index. The previous statement that absent registry metadata prevents spatial queries was unsupported.
2. **SpatialQuery (RFC-143, D-427–D-429):** A record requiring only `spatialQueryDbId` cannot establish reproducible execution; `queryType`, `queryGeometry`, `queryParams` and `resultReference` are optional, and no dataset or execution status is specified. `queryParams` is a string, not a structured object.
3. **YieldMap (RFC-070, D-208–D-210):** The registration requires only `yieldMapDbId`. `storageUri`, `fileDigest`, `resolutionM`, Study/Location/harvest/crop-cycle identifiers and provenance are optional, and digest/URI fields are not schema-validated. No retrieval, immutable bytes, scientific accuracy or digest verification is demonstrable from this metadata record. The prior RFC/README claims were stronger than the wire contract.

## Governance disposition

**G-090-1:** Maintainer must choose between metadata-only SpatialIndex (safe present interpretation), an evidenced executable design, and continued deferral. **G-090-2:** choose stored-query description, executable query jobs with provenance and security, or deferral. **G-090-3:** choose optional YieldMap metadata, published payload lifecycle with enforced digest/storage/coordinate-reference-system requirements, or deferral.

Until those choices are explicitly ratified, no executable spatial endpoint, automatic map-payload publication, authoritative cross-resource relationship, scientific-comparability guarantee or normative maturity promotion may be inferred. Descriptions remain title-only in the guarded evidence inventory. Any approved future implementation should be a separate, versioned contract migration with negative geometry, authority and digest tests.

## Scope and verification

- Corrected prose in three RFCs and three module READMEs, plus a schema-derived regression guard for missing mandatory scientific properties and unratified disposition.
- **Reviewed-description count unchanged at 151/156** after predecessor Mission 095; **five evidence-deferred** remain. The two breeding deferrals (CrossingSchedule D-BP-11 and ProgenyRecords D-BP-08) are untouched.
- No official BrAPI (Breeding Application Programming Interface) version 2.1 source, GenX wire schema, route, identity, endpoint registry, maturity or decision-log value is changed.

```sh
python Scripts/test_genx_group_descriptions.py
python Scripts/check_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Require hosted static conformance, live-reference conformance and specification generation on the final branch head before merging. No hosted outcome is assumed from this assessment.
