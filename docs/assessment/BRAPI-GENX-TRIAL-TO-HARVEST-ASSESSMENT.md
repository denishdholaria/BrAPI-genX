# BrAPI-GenX — Trial to Harvest Assessment (Mission 003)

**Status:** documentation and evidence slice. No source schemas, routes, or generated artifacts changed.
**Tracking issue:** https://github.com/denishdholaria/BrAPI-genX/issues/7
**Inspected base SHA:** `c780f656689a46553d747a081a03073c893fd792`
**Branch:** local `main` (working tree; no commit created)
**Companion machine-readable file:** `docs/assessment/BRAPI-GENX-TRIAL-TO-HARVEST-MAPPING.json`

## 1. Purpose and scope

This assessment answers one scientific question for one synthetic wheat trial:

> Can an independent system recover, for each plot, the cultivar planted, the irrigation actually applied, the relevant soil and weather context, and the measured grain yield?

The slice is synthetic and illustrative: one study, one season, two cultivars, two irrigation treatment levels. It keeps three things distinct:

- **Planned treatment assignment** (design intent),
- **Applied irrigation event** (what actually happened),
- **Measured outcome** (yield observation or harvest record).

Only the two files named in the deliverables were created. Source schemas, routes, module classification, governance decisions, generated compatibility artifacts, and external issue comments were not modified.

## 2. Standards and sources used

| Source | Version / state | Authority / location |
|---|---|---|
| BrAPI | v2.1, released 2022-07-01 | https://brapi.org/specification ; local schemas under `Specification/BrAPI-Schema` |
| MIAPPE | v1.1, released January 2019 | https://github.com/MIAPPE/MIAPPE/tree/v1.1/MIAPPE_Checklist-Data-Model-v1.1 ; overview https://www.miappe.org/overview/ ; local mapping `docs/docs/best_practices/MIAPPE.rst` |
| BrAPI-GenX RFCs | `STRUCTURAL_DRAFT` per `docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md` | `Specification/BrAPI-GenX/RFCs` |
| Specification quality standard | Phase 0 mandatory gate | `docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md` |

BrAPI v2.1 schema descriptions cite MIAPPE V1.1. MIAPPE v1.2 (October 2024) exists but is not the version referenced by the inspected BrAPI v2.1 contracts, so v1.1 is the version recorded here.

## 3. Synthetic example

| Item | Value |
|---|---|
| Trial | `institute-a:trial:wheat-trial-network-2026` (BrAPI Trial) |
| Study | `institute-a:study:wheat-yield-trial-2026` (BrAPI Study) |
| Season | 2026 (one season) |
| Location | `institute-a:location:field-12` (BrAPI Location) |
| Cultivars | `institute-a:germplasm:cv-alpha`, `institute-a:germplasm:cv-beta` |
| Irrigation levels | `low-water`, `high-water` |
| Plots | 4 (two cultivars x two irrigation levels, illustrative) |

## 4. Path from germplasm and study to measured yield

| Step | From | To | Owner | Connecting identifier | Evidence |
|---:|---|---|---|---|---|
| 1 | BrAPI Trial | BrAPI Study | BrAPI v2.1 core server | `trialDbId` / `study.trial` | `Specification/BrAPI-Schema/BrAPI-Core/Trial.json`; `Specification/BrAPI-Schema/BrAPI-Core/Study.json` |
| 2 | BrAPI Study | BrAPI Location | BrAPI v2.1 core server | `study.locationName` / `locationDbId` | `Specification/BrAPI-Schema/BrAPI-Core/Study.json`; `Specification/BrAPI-Schema/BrAPI-Core/Location.json` |
| 3 | BrAPI Study | BrAPI Germplasm (cultivar) | BrAPI v2.1 germplasm server | `germplasmDbId` | `Specification/BrAPI-Schema/BrAPI-Germplasm/Germplasm.json` |
| 4 | BrAPI Study | BrAPI ObservationUnit (plot-level unit) | BrAPI v2.1 phenotyping server | `observationUnitDbId`, `germplasm`, `observationLevel` | `Specification/BrAPI-Schema/BrAPI-Phenotyping/ObservationUnit.json` |
| 5 | BrAPI ObservationUnit | GenX Plot identity | GenX proposal (Breeding/Plot) | `plotDbId` (no defined link to `observationUnitDbId`) | `Specification/BrAPI-GenX/Breeding/Plot/Schemas/Plot.yaml` |
| 6 | BrAPI ObservationUnit | measured grain yield | BrAPI v2.1 phenotyping server | `observationDbId`, `observationUnit`, `observationVariable`, `value`, `observationTimeStamp` | `Specification/BrAPI-Schema/BrAPI-Phenotyping/Observation.json`; `Specification/BrAPI-Schema/BrAPI-Phenotyping/ObservationVariable.json` |
| 7 | BrAPI ObservationUnit / GenX Plot | GenX HarvestRecord | GenX proposal (CropProduction/HarvestRecords) | `harvestRecordDbId`, `studyDbId`, `locationDbId`, `germplasmDbId` (no plot/observation-unit link) | `Specification/BrAPI-GenX/CropProduction/HarvestRecords/Schemas/HarvestRecord.yaml` |
| 8 | BrAPI Location / Study | GenX IrrigationEvent (applied) | GenX proposal (CropProduction/IrrigationOperation) | `irrigationEventDbId`, `locationDbId`, `studyDbId` (no plot/observation-unit link) | `Specification/BrAPI-GenX/CropProduction/IrrigationOperation/Schemas/IrrigationEvent.yaml` |
| 9 | BrAPI Location | GenX SoilProfile | GenX proposal (Environment/SoilProfile) | `soilProfileDbId`, `locationDbId`, `sampledAt` (no sampling depth) | `Specification/BrAPI-GenX/Environment/SoilProfile/Schemas/SoilProfile.yaml` |
| 10 | BrAPI Location / station | GenX WeatherObservation | GenX proposal (Environment/WeatherObservations) | `weatherObservationDbId`, `stationDbId`, `locationDbId`, `observedAt` | `Specification/BrAPI-GenX/Environment/WeatherObservations/Schemas/WeatherObservation.yaml` |
| 11 | GenX Plot / Location | GenX FieldGeometry | GenX proposal (Geospatial/FieldGeometry) | `fieldGeometryDbId` (no `locationDbId` or `plotDbId`) | `Specification/BrAPI-GenX/Geospatial/FieldGeometry/Schemas/FieldGeometry.yaml` |

## 5. How irrigation, soil, and weather attach

- **Planned irrigation level** is a design fact. It is carried by BrAPI `ObservationTreatment` (`factor`, `modality`) on each plot's `ObservationUnit` (reuse, TH-011). It is not an applied event.
- **Applied irrigation** is an operation fact. It is carried by GenX `IrrigationEvent` at `locationDbId` + `studyDbId` + `irrigatedAt` + `volume`/`volumeUnit` + `duration` (TH-013). The current schema has no plot or observation-unit reference, so plot attribution is a gap.
- **Soil context** is carried by GenX `SoilProfile` at `locationDbId` + `sampledAt` with texture, pH, organic matter, moisture, and nutrients (TH-007, TH-008). It is site-level in the current schema, has no sampling depth, and has no plot link.
- **Weather context** is carried by GenX `WeatherObservation` at `stationDbId`/`locationDbId` + `observedAt` with measurements, quality flag, and source (TH-009, TH-010). It is site/station-level and instantaneous; aggregation window and representativeness are undefined.
- **Measured yield** is carried either by BrAPI `Observation` (value + timestamp + yield variable) or by GenX `HarvestRecord` (quantity + unit + moisture + area) (TH-015, TH-016). The HarvestRecord has no plot/observation-unit link and no moisture-basis rule.
- **Field geometry** is a spatial boundary record, not an experimental unit (TH-006). It has no site or plot link in the current schema and cannot by itself identify a plot.

## 6. Findings

Eighteen findings are recorded in the companion JSON with stable IDs `TH-001` through `TH-018`. Summary:

| Finding | Disposition | Subject |
|---|---|---|
| TH-001 | Reuse existing contract | BrAPI Germplasm for cultivar identity |
| TH-002 | Reuse existing contract | BrAPI Trial/Study/Season for study context |
| TH-003 | Reuse existing contract | BrAPI Location for site spatial context |
| TH-004 | Reuse existing contract | BrAPI ObservationUnit as experimental unit |
| TH-005 | Clarify existing GenX proposal | GenX Plot lacks cross-system links |
| TH-006 | Clarify existing GenX proposal | FieldGeometry is boundary, not experimental unit |
| TH-007 | Clarify existing GenX proposal | SoilProfile lacks sampling depth |
| TH-008 | Document an interoperability gap | Soil profile to plot attribution |
| TH-009 | Clarify existing GenX proposal | Weather time window / representativeness |
| TH-010 | Document an interoperability gap | Weather context to plot attribution |
| TH-011 | Reuse existing contract | BrAPI ObservationTreatment for planned treatment |
| TH-012 | Clarify existing GenX proposal | GenX TreatmentAssignment underspecified |
| TH-013 | Document an interoperability gap | IrrigationEvent lacks plot attribution |
| TH-014 | Document an interoperability gap | Planned vs applied irrigation distinction |
| TH-015 | Reuse existing contract | BrAPI Observation for measured yield |
| TH-016 | Clarify existing GenX proposal | HarvestRecord yield/moisture/area/plot link |
| TH-017 | Reuse existing contract | BrAPI SeedLot linkage for harvest provenance |
| TH-018 | Defer for lack of evidence | Geometry area vs harvested area reconciliation |

Every GenX finding cites the current maturity status `STRUCTURAL_DRAFT` from `docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md`.

### Three highest-priority findings

1. **TH-013 — applied irrigation cannot be attributed to a plot.**  
   Evidence: `Specification/BrAPI-GenX/CropProduction/IrrigationOperation/Schemas/IrrigationEvent.yaml` (properties `locationDbId`, `studyDbId`, `irrigatedAt`, `method`, `volume`, `volumeUnit`, `duration`; no plot or observation-unit property); RFC-024 D-69/D-70/D-71; `Specification/BrAPI-Schema/BrAPI-Phenotyping/ObservationUnit.json`.  
   Why it matters: BrAPI v2.1 has no irrigation resource and the GenX event stops at Location/Study, so a wrong-plot irrigation event cannot be detected and the scientific question's "irrigation actually applied" cannot be answered per plot.

2. **TH-005 — GenX Plot identity does not resolve to a BrAPI experimental unit.**  
   Evidence: `Specification/BrAPI-GenX/Breeding/Plot/Schemas/Plot.yaml` (`plotDbId`, `fieldDbId`, `plotName`, `status`, `supersedes`, `provenance`; no study/location/observation-unit link); RFC-107 D-319/D-320/D-321; `Specification/BrAPI-Schema/BrAPI-Phenotyping/ObservationUnit.json`.  
   Why it matters: without a defined mapping, two systems can mint different plot identities and the trace from germplasm/study to yield breaks at the plot.

3. **TH-016 — grain yield has no unambiguous measurement basis.**  
   Evidence: `Specification/BrAPI-GenX/CropProduction/HarvestRecords/Schemas/HarvestRecord.yaml` (`quantity`, `unit` required; `moisture`, `moistureUnit`, `areaHarvested`, `areaUnit` optional; no plot/observation-unit link); RFC-011 D-30/D-31/D-32; `Specification/BrAPI-Schema/BrAPI-Phenotyping/Observation.json`.  
   Why it matters: quantity without moisture basis and harvested area cannot be compared across plots, which is the core of the scientific question.

## 7. Worked record trace (prose)

Trial `wheat-trial-network-2026` (BrAPI Trial) contains Study `wheat-yield-trial-2026` (BrAPI Study) at Location `field-12` (BrAPI Location, WGS84 coordinates). The study has two cultivars, `cv-alpha` and `cv-beta` (BrAPI Germplasm), and two planned irrigation levels, `low-water` and `high-water`. Each of the four plots is a BrAPI ObservationUnit carrying `germplasmDbId`, `observationLevel = plot`, position, and an `ObservationTreatment` with `factor = irrigation` and the assigned modality; this is the planned treatment. GenX Plot records exist for the same four plots, but because the current schema has no `observationUnitDbId` or `studyDbId`, an external mapping table is required to join `plotDbId` to `observationUnitDbId`.

Soil context comes from a GenX SoilProfile at Location `field-12` with `sampledAt` and soil properties; however, the current schema has no sampling depth and no plot link, so the profile is site-level and its depth interval is unstated. Weather context comes from GenX WeatherObservation records for station `ws-07` at Location `field-12` with `observedAt` timestamps and measurements; they are site/station-level and their aggregation window and representativeness are unstated. Applied irrigation is recorded as GenX IrrigationEvent records with `locationDbId = field-12`, `studyDbId = wheat-yield-trial-2026`, `irrigatedAt`, `method`, `volume`, and `volumeUnit`; because there is no `plotDbId` or `observationUnitDbId`, these events are field/study-level and cannot be attributed to an individual plot without an external rule. Measured grain yield is recorded either as a BrAPI Observation for each plot's ObservationUnit (value, timestamp, grain-yield variable) or as a GenX HarvestRecord with quantity, unit, moisture, moistureUnit, and areaHarvested; the HarvestRecord has no plot/observation-unit link and no moisture-basis rule, so yield comparison across plots requires an external convention. FieldGeometry may describe the field boundary and area, but it has no location or plot link in the current schema, so it cannot by itself identify the harvested experimental unit.

## 8. Negative cases for a later executable fixture

1. **NC-001 — wrong-plot irrigation event.** An IrrigationEvent is recorded with `locationDbId` matching the trial field but is attributed to plot B, although the water was applied to plot A. Expected: reject or flag the attribution because the current IrrigationEvent schema has no `plotDbId`/`observationUnitDbId` or documented distribution rule (TH-013, TH-014).
2. **NC-002 — soil data with no sampling depth.** A SoilProfile is recorded with `locationDbId` and `sampledAt` but no sampling depth, and its nutrient values are used to interpret plot performance. Expected: reject or mark incomplete because the depth interval to which the values apply is unstated (TH-007, TH-008).
3. **NC-003 — yield with an ambiguous measurement basis.** A HarvestRecord states quantity and unit but omits moisture, moistureUnit, areaHarvested, and moisture basis, or an Observation variable scale does not state moisture basis. Expected: reject or flag because grain yield cannot be compared across plots without a stated moisture basis and harvested area (TH-015, TH-016).

## 9. Unknowns recorded explicitly

- Whether GenX Plot is intended to replace, mirror, or supplement the BrAPI ObservationUnit plot level.
- Whether soil sampling depth should be a property of SoilProfile or a separate sample record with horizon semantics.
- Whether weather station representativeness radius, sensor height, and aggregation window belong in WeatherObservation or in station metadata.
- Whether IrrigationEvent volume is per field, per plot, or per application zone, and how application efficiency/runoff should be recorded.
- Whether HarvestRecord quantity is as-harvested or dry mass, and what standard moisture basis applies (for example 14% for wheat).
- Whether cultivar identity should be BrAPI Germplasm or a GenX crop-species/taxon reference for this trial.
- Whether planned treatment assignment should be BrAPI ObservationTreatment, GenX TreatmentAssignment, or both with an explicit link.

## 10. Scientific decisions the maintainer needs to make

1. Should GenX Plot become a cross-reference to BrAPI ObservationUnit (via `observationUnitDbId` or `externalReferences`), or should BrAPI ObservationUnit remain the sole plot identity and GenX Plot be deprecated as redundant?
2. Should sampling depth be added to SoilProfile as value+unit (and optionally horizon), or modelled as a separate soil-sample record?
3. Should IrrigationEvent gain `plotDbId`/`observationUnitDbId`, or should irrigation remain a field-level event with a documented distribution rule to plots?
4. Should HarvestRecord require moisture basis and area harvested for yield-per-area, or should those remain optional with an explicit "unknown" representation?
5. Should planned irrigation level live only in BrAPI ObservationTreatment, only in GenX TreatmentAssignment, or in both with a defined link?

## 11. Checks run

| Command | Working directory | Exit code | Result |
|---|---|---:|---|
| `python3 Scripts/checkEndpointRegistry.py` | `brapi-genx` | 0 | Passed: 201 BrAPI v2.1 entries, 462 proposed GenX entries, unique identities/routes, complete source links, and resolved semantic-neighbor IDs. |
| `python3 -m json.tool docs/assessment/BRAPI-GENX-TRIAL-TO-HARVEST-MAPPING.json` | `brapi-genx` | 0 | Passed: JSON parses. |
| Local file existence check for all cited paths | `brapi-genx` | 0 | All cited local files exist (verified by inspection). |

No other checks were run. Runtime implementation, conformance tests beyond the registry check, and generated-artifact rebuilds were deliberately not performed because this is a documentation and evidence slice.

## 12. Recommended next interoperability behavior to test

Test **NC-001: a wrong-plot irrigation event** first. The finding that justifies it is **TH-013**: the GenX `IrrigationEvent` schema carries `locationDbId` and `studyDbId` but no `plotDbId` or `observationUnitDbId`, and BrAPI v2.1 has no irrigation resource at all, so an independent system cannot detect when an irrigation event is attributed to the wrong plot. Testing this case will force the missing plot-attribution contract (or an explicit field-level distribution rule) to be defined before any yield conclusion depends on applied irrigation.