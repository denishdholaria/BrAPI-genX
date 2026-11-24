# Mission 093 — Experimental design, protocol and assignment source audit

**Baseline:** `fa1837a32a7f5180b157c91ebaf0419efe77a5eb` (integrated Mission 092). **Boundary:** evidence-based documentation and regression tests; no official Breeding Application Programming Interface (BrAPI) version 2.1 contract, GenX wire schema, route, endpoint registry, policy or maturity decision is changed.

## Verified draft-contract findings

1. **ExperimentalDesign (RFC-018, D-51–D-53):** The request requires `experimentalDesignDbId`, `studyDbId`, `designType`. Randomization seed, replication count, block size, treatment allocations and provenance are optional. Allocation entries have no required plot/treatment/replication/block fields. Official BrAPI `StudyNewRequest.experimentalDesign` already describes statistical design and `observationLevels` models hierarchy; Observation Unit positions and treatment-factor metadata also exist. The earlier novelty claim was too broad. No valid randomization, official plot mapping or reproducibility is established.

2. **ExperimentalProtocol (RFC-117, D-349–D-351):** Registration requires only `experimentalProtocolDbId`; `protocolName` (previous RFC text incorrectly said `name`) and all method descriptors are optional. `treatments`, `replicates`, `blocks` are free-text strings, not validated structures or counts. Study design, actual Event intervention and protocol definition are different facts. There is no typed connection to GenX ProtocolLibrary, Study, ExperimentalDesign or GenomicDataset; the earlier Mission 006 operation-neighbor deferral is unchanged.

3. **TreatmentAssignment (RFC-106, D-316–D-318):** Registration requires only `treatmentAssignmentDbId`; both `fieldDbId` and `treatment` are optional. No typed `studyDbId`, `locationDbId`, `observationUnitDbId` or `experimentalDesignDbId` link exists, contrary to the old RFC relationship claim. Official BrAPI Observation Unit `treatments` uses factor/modality, while Event covers interventions, affected units and time. Planned allocation cannot be inferred from either an unverified candidate record or an executed Event.

## Applied safeguards

- Replaced three title-only GroupDescriptions with traceable source evidence; corrected three overviews and three RFCs without introducing fictional relationships.
- Added three reviewed modules to the group-description guard and schema-derived regression assertions for official overlaps, request/response requiredness, unmodelled links and operation identities.
- **Expected source-backed description coverage:** 147 of 156 modules; 9 deferred, subject to passing tests and integration. This is *documentation evidence*, not scientific certification, Request for Comments maturity promotion or implementation conformance.

## Verification commands

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

This record does not claim successful hosted or local execution. Hosted static conformance, live reference conformance and specification generation on the branch head must pass before any merge. D-51–D-53, D-316–D-318 and D-349–D-351 remain unratified.
