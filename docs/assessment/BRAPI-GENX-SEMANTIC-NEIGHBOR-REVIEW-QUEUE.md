# BrAPI-GenX — Semantic Neighbor Work Queue (Mission 006)

**For live status and current unreviewed groups:** run
`python Scripts/report_semantic_neighbor_inventory.py` from the repository root,
or add `--json` for a structured report. All counts below are historical
snapshot values, not necessarily the latest ledger state.

**Pinned ledger snapshot:** `09f94568d445905b3db17aacebd85876e34b83b0` (2026-11-23)  
**Status:** generated-style analytical inventory, advisory and non-normative. The source of truth remains the semantic-neighbor governance ledger.

## Verified distribution

- **153** inherited operation-neighbor identities retained in the ledger.
- **51** source-module/target-operation groups; each currently has three source operations.
- **150** inherited-unreviewed links and **3** requiring a maintainer decision.
- **120** links (**78.4%**) converge on a single operation: `genxRegisterGenomicDataset`.
- The three priority cross-domain links were reviewed in the dedicated ExperimentalProtocol–GenomicDataset assessment.

### Target-operation concentration

| Target operation | Link count | Source groups |
|---|---:|---:|
| `genxRegisterGenomicDataset` | 120 | 40 |
| `genxRegisterFieldScouting` | 12 | 4 |
| `genxPublishVariableTermVersion` | 9 | 3 |
| `genxRecordAssayDesign` | 3 | 1 |
| `genxRecordHarvest` | 3 | 1 |
| `genxRecordVcfImport` | 3 | 1 |
| `genxRegisterCropCycle` | 3 | 1 |

## Interpretation

The repeated three-to-one pattern (get/list/register operations from a source module all pointing to one target registration operation) is a **review priority signal**, not proof of scientific equivalence, derivation, data ownership, or invalidity. Its concentration suggests that inherited associations may reflect a generation heuristic rather than individually justified cross-resource links. This hypothesis must be checked against source contracts and real scientific exchanges.

Particularly suspect as *direct* dataset-registration mappings are links originating in modules such as CapabilityNegotiation, ConformanceProbe, and IrrigationAdvice; these still require evidence-based review rather than automatic deletion. Other sources, such as ArtifactCatalogue or PipelineProvenance, may have legitimate complementary metadata relationships without being equivalent operations.

## Ordered review strategy

1. **Decision already identified:** resolve the three ExperimentalProtocol links only with maintainer authorization; they remain `requires-decision` until then.
2. **Concentration batch:** review the 39 remaining source groups targeting `genxRegisterGenomicDataset` first, using sample source contracts and falsifiable mapping hypotheses. Do not infer that all 117 links should be deleted.
3. **Other targets:** review the remaining 11 groups covering FieldScouting, VariableTerm, AssayDesign, CropCycle, VcfImport and HarvestRecords, distinguishing complementary metadata from execution/events.
4. For every group, distinguish *operation neighbor* from *resource relationship*, identify authoritative ownership and stable identifiers, record provenance and security requirements, then update ledger entries individually according to permitted transitions.

## Complete grouped inventory

| Review batch | Source module | Target operation | Links | Boundary | Status |
|---|---|---|---:|---|---|
| Decision | `ExperimentalProtocol` | `genxRegisterGenomicDataset` | 3 | cross-domain | requires-decision |
| Concentration | `ArtifactCatalogue` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `BiodiversityExport` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `CalibrationQuality` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `CapabilityNegotiation` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `CloudMask` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `ConformanceProbe` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `CropHealthImage` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `CropRecommendation` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `CropSuitability` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `CrsTransform` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `DiagnosticEvidence` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `DiseaseObservation` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `DiseaseResistance` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `EdgeGatewayHealth` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `EvidencePack` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `ExplanationEvidence` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `FieldGeometry` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `HumanReview` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `IpmStrategy` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `IrrigationAdvice` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `LocalConstraint` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `NutrientAdvice` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `OutcomeFeedback` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `PestDiseaseRisk` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `PipelineProvenance` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `ProtocolLibrary` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `PublicationReview` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `RasterCatalogue` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `ReferenceAssembly` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `RemoteSensingMetadata` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `SchemaMapping` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `SensorDevice` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `SowingWindow` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `SpatialIndex` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `SpatialQuery` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `TelemetryNormalization` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `ThresholdAlert` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `VegetationIndex` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Concentration | `YieldForecast` | `genxRegisterGenomicDataset` | 3 | cross-module | inherited-unreviewed |
| Other | `AssayExecution` | `genxRecordAssayDesign` | 3 | cross-module | inherited-unreviewed |
| Other | `CaptureWorkflow` | `genxPublishVariableTermVersion` | 3 | cross-module | inherited-unreviewed |
| Other | `Farm` | `genxRegisterCropCycle` | 3 | cross-module | inherited-unreviewed |
| Other | `FieldBook` | `genxRegisterFieldScouting` | 3 | cross-module | inherited-unreviewed |
| Other | `Plot` | `genxRegisterFieldScouting` | 3 | cross-module | inherited-unreviewed |
| Other | `QualityFlag` | `genxPublishVariableTermVersion` | 3 | cross-module | inherited-unreviewed |
| Other | `TreatmentAssignment` | `genxRegisterFieldScouting` | 3 | cross-module | inherited-unreviewed |
| Other | `TrialNetwork` | `genxRegisterFieldScouting` | 3 | cross-module | inherited-unreviewed |
| Other | `ValueMissingness` | `genxPublishVariableTermVersion` | 3 | cross-module | inherited-unreviewed |
| Other | `VcfExport` | `genxRecordVcfImport` | 3 | cross-module | inherited-unreviewed |
| Other | `YieldMap` | `genxRecordHarvest` | 3 | cross-module | inherited-unreviewed |

## Non-actions and evidence requirements

- No data model, official BrAPI v2.1 source, route, registry mapping, or public resource identity is changed by this queue.
- No link becomes approved merely because it appears in the same target group.
- Proposed rejection requires explicit maintainer authorization and retention of the historical ledger identity; proposed mapping requires a scientifically valid relationship with independently verifiable behavior.
- Counts and grouping reflect the pinned snapshot only. Recompute from `Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml` after further governance changes.

See `docs/governance/BRAPI-GENX-SEMANTIC-NEIGHBOR-GOVERNANCE.md` and `docs/assessment/BRAPI-GENX-EXPERIMENTAL-PROTOCOL-GENOMIC-DATASET-REVIEW.md`.
