# BrAPI-GenX — Trial to Harvest Assessment (Mission 003)

**Status:** documentation and evidence slice. No source schemas, routes, or generated artifacts changed.
**Tracking issue:** https://github.com/denishdholaria/BrAPI-genX/issues/7
**Inspected base SHA:** `23c9e09b76f338b8785d208e3872a6660b1425d0` (Mission 003A re-verification)
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
- **Applied irrigation** is an operation fact. BrAPI v2.1 `Event` supports `eventType='irrigation'`, affected `observationUnitDbIds`, `eventDateRange` (discrete dates), and `eventParameters` (e.g. applied water depth), so plot-level applied irrigation is recoverable on read via `GET /events` (TH-013, corrected). The GenX `IrrigationEvent` schema still has no plot or observation-unit reference and remains field/study-level; plot attribution through BrAPI `Event` requires a shared usage convention and a released write path.
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
| TH-013 | Reuse existing contract (BrAPI Event) + convention | BrAPI Event covers irrigation; parameter/write gaps remain |
| TH-014 | Document an interoperability gap | Planned vs applied irrigation distinction |
| TH-015 | Reuse existing contract | BrAPI Observation for measured yield |
| TH-016 | Clarify existing GenX proposal | HarvestRecord yield/moisture/area/plot link |
| TH-017 | Reuse existing contract | BrAPI SeedLot linkage for harvest provenance |
| TH-018 | Defer for lack of evidence | Geometry area vs harvested area reconciliation |

Every GenX finding cites the current maturity status `STRUCTURAL_DRAFT` from `docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md`.

### Corrections recorded in Mission 003A

- **TH-003** (Location): `location.coordinates` uses the shared GeoJSON schema (RFC 7946), which supports Point or Polygon geometry; Location is not point-only.
- **TH-004** (ObservationUnit): BrAPI ObservationUnit supports a persistent identifier (`observationUnitPUI`, MIAPPE DM-72) and `externalReferences`, in addition to `observationUnitDbId`.
- **TH-013** (irrigation): BrAPI v2.1 `Event` supports `eventType='irrigation'`, affected `observationUnitDbIds`, dates, and `eventParameters`; read via `GET /events`. The earlier claim that BrAPI v2.1 has no irrigation resource is corrected. BrAPI Event read support and write support (absent in released source) are recorded separately.
- **TH-014** (planned vs applied): both planned (`ObservationUnit.treatments`) and applied (BrAPI `Event`) irrigation can be represented in BrAPI v2.1; the remaining gap is an explicit planned-to-applied link, not plot attribution.
- **TH-015/TH-016** (harvest): BrAPI `Event` supports `eventType='harvest'` with affected units, dates, and parameters; harvest quantity, moisture basis, harvested area, and plot-level yield comparison still need evidence.
- **TH-007/TH-008/TH-009/TH-010** (soil/weather): gap claims are provisional pending assessment of companion standards.
- **TH-011** (treatments): the released schema describes `ObservationUnit.treatments` as "List of treatments applied to an observation unit" (MIAPPE DM-74); planned-vs-applied semantics are by convention, not by contract. Write support exists: `PUT /observationunits` and `PUT /observationunits/{observationUnitDbId}` use `ObservationUnitNewRequest`, which includes `treatments` and `observationUnitPosition`.
- **ICASA pinned dictionary:** commit `7b0d81745b2ab93c54263f0b4a80fd8d8f95ac76`, file `CSV/Management_info.csv`, lines 205-206: `irrig_amount_depth` / `IRVAL` = "Irrigation amount, depth of water", unit `mm`. The fixture therefore uses `name='irrig_amount_depth'`, `code='IRVAL'`, `units='mm'`, `value='20'`. The 2013 Table 1 (White et al.) listed `IRADP` as applied depth in mm, but the pinned dictionary distinguishes `IRVAL` (applied amount depth, mm) from `IRADP` (application depth, cm); `IRADP` is retained as a negative case for the applied-amount reader even when supplied with mm. The earlier fixture ontology identifier `ICASA:irrigation` (for `eventTypeDbId`) lacked a verified authority and has been removed from the payload. The convention recognizes finite numeric IRVAL values in mm (e.g., 20 and 17.5); cm is outside this pilot convention.

### Three highest-priority findings

1. **TH-013 — applied irrigation is recoverable per plot through BrAPI Event, but convention and write gaps remain.**  
   Evidence: `Specification/BrAPI-Phenotyping/Events/Schemas/Event.yaml` (`eventType` includes `irrigation`; `observationUnitDbIds`; `eventDateRange.discreteDates`; `eventParameters`); `Specification/BrAPI-Phenotyping/Events/Events_GET.yaml` (filters by `studyDbId`, `observationUnitDbId`, `eventType`, date range); `Specification/BrAPI-GenX/CropProduction/IrrigationOperation/Schemas/IrrigationEvent.yaml` (no plot/observation-unit property).  
   Why it matters: BrAPI v2.1 does have an irrigation-capable Event resource with affected observation units, so plot-level applied irrigation can be read. The remaining risk is an unstated parameter convention (e.g. applied water depth) and the absence of a released write endpoint/schema.

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

1. **NC-001 — wrong-plot irrigation event.** A BrAPI Event is recorded with `eventType='irrigation'` and `observationUnitDbIds=['plot-b']`, although an independent field log shows water was applied to plot A. Expected: structural checks pass (plot-b is a valid plot in the study), but cross-checking the Event against the independent irrigation log exposes the discrepancy; detection is not provided by the Event schema alone (TH-013, TH-014).
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
| `python3 /tmp/scratchpad/validate_fixture.py` (inline snippet reproduced in section 12) | `brapi-genx` | 0 | Passed: BrAPI Event fixture validates against released Event schema; 4/4 relationship checks pass (explicit plot-a resolves; unknown/foreign plot flagged; omitted IDs -> all units; plot substitution passes structural checks but independent log exposes discrepancy). |
| Local file existence check for all cited paths | `brapi-genx` | 0 | All cited local files exist (verified by inspection). |

No other checks were run. Runtime implementation, conformance tests beyond the registry check, and generated-artifact rebuilds were deliberately not performed because this is a documentation and evidence slice.

## 11.1 Executable fixture (Mission 003A)

Fixture `FX-001` is embedded in `docs/assessment/BRAPI-GENX-TRIAL-TO-HARVEST-MAPPING.json` under the `fixture` key: one study (`institute-a:study:wheat-yield-trial-2026`), two plot-level ObservationUnits (`plot-a`, `plot-b`), and one BrAPI `Event` with `eventType='irrigation'`, `observationUnitDbIds=['plot-a']`, `eventDateRange.discreteDates=['2026-06-15T06:00:00Z']`, and `eventParameters` carrying an applied water depth of `20` (unit `mm`). The parameter name `applied_water_depth` is illustrative fixture terminology; a standard term, if recommended, should cite its authority (ICASA management-event variables / Crop Ontology). The independent field log (`field-log-irrigation-plot-a-001`) is kept separate from the official Event payload.

Reproducible local validation snippet:

```python
import json, yaml, datetime, sys, math
from jsonschema import validate, ValidationError

d = json.load(open('docs/assessment/BRAPI-GENX-TRIAL-TO-HARVEST-MAPPING.json'))
fx = d['fixture']; event = fx['brapiEvent']
study_units = {u['observationUnitDbId'] for u in fx['observationUnits']}
foreign_units = {u['observationUnitDbId'] for u in fx.get('foreignStudyObservationUnits', [])}

spec = yaml.safe_load(open('Specification/BrAPI-Phenotyping/Events/Schemas/Event.yaml'))
schema = spec['components']['schemas']['Event']

def is_dt(s):
    try:
        datetime.datetime.fromisoformat(s.replace('Z', '+00:00')); return True
    except Exception:
        return False

def schema_errors(payload):
    try:
        validate(instance=payload, schema=schema)
    except ValidationError as e:
        return [str(e.message)]
    errs = []
    for dd in (payload.get('eventDateRange', {}).get('discreteDates') or []):
        if not is_dt(dd): errs.append(f'bad datetime {dd}')
    return errs

def resolve(refs):
    if refs is None:
        return sorted(study_units), []
    resolved = [r for r in refs if r in study_units]
    unknown = [r for r in refs if r not in study_units]
    return resolved, unknown

base_errors = schema_errors(event)
case1_resolved, case1_unknown = resolve(event['observationUnitDbIds'])
case1 = (case1_resolved == ['plot-a']) and (case1_unknown == [])

case2_resolved, case2_unknown = resolve(['plot-z'])
case2 = (case2_resolved == []) and (case2_unknown == ['plot-z'])

case3_resolved, case3_unknown = resolve(['plot-c'])
case3 = (case3_resolved == []) and (case3_unknown == ['plot-c']) and ('plot-c' in foreign_units)

case4_resolved, case4_unknown = resolve(None)
case4 = (case4_resolved == sorted(study_units)) and (case4_unknown == [])

alt = json.loads(json.dumps(event)); alt['observationUnitDbIds'] = ['plot-b']
case5_resolved, case5_unknown = resolve(alt['observationUnitDbIds'])
case5 = (case5_resolved == ['plot-b']) and (case5_unknown == []) and (schema_errors(alt) == [])

wrong = json.loads(json.dumps(event))
wrong['observationUnitDbIds'] = [123]
case6 = (schema_errors(wrong) != [])

def is_finite_number(v):
    try:
        f = float(v); return math.isfinite(f)
    except (TypeError, ValueError):
        return False

def recognizes_applied_depth(ep):
    return (ep.get('code') == 'IRVAL' and ep.get('units') == 'mm'
            and is_finite_number(ep.get('value')))

param = event['eventParameters'][0]
case7 = recognizes_applied_depth(param)
case8 = recognizes_applied_depth({'code': 'IRVAL', 'units': 'mm', 'value': '17.5'})
case9 = not recognizes_applied_depth({'code': 'IRVAL', 'units': 'cm', 'value': '20'})
case10 = not recognizes_applied_depth({'code': 'IRADP', 'units': 'mm', 'value': '20'})
case11 = not recognizes_applied_depth({'code': 'XXXX', 'units': 'mm', 'value': '20'})

field_log_plot = fx['independentFieldLog']['plotDbId']
case12 = (event['observationUnitDbIds'] == ['plot-a'] and field_log_plot == 'plot-a')
case13 = (alt['observationUnitDbIds'] == ['plot-b'] and field_log_plot == 'plot-a')

print('schema errors:', base_errors or 'NONE')
print('case1 explicit plot-a resolves:', case1)
print('case2 unknown plot flagged:', case2)
print('case3 foreign-study plot flagged:', case3)
print('case4 omitted -> all units:', case4, case4_resolved)
print('case5 substituted plot passes structural checks:', case5)
print('case6 wrong-type mutation fails:', case6)
print('case7 IRVAL 20 mm recognized:', case7)
print('case8 IRVAL 17.5 mm recognized:', case8)
print('case9 cm outside convention:', case9)
print('case10 IRADP with mm rejected:', case10)
print('case11 unrecognized code rejected:', case11)
print('case12 base field-log agrees:', case12)
print('case13 substituted field-log disagrees:', case13)

if not (base_errors == [] and case1 and case2 and case3 and case4 and case5 and case6 and case7 and case8 and case9 and case10 and case11 and case12 and case13):
    sys.exit(1)
```

## 11.2 Planned-to-applied test (Mission 003B)

Fixture `FX-002` (in the companion JSON) uses two plausible planned applications for the same plot (`plot-a`: `low-water` and `high-water` via `ObservationUnit.treatments`) and one actual BrAPI `Event` (`irrigation`, 20 mm IRVAL, 2026-06-15).

What a reader can establish: the plot's planned modalities and the applied event's occurrence, affected plot, timestamp, and applied depth. What it cannot establish: which planned modality the event fulfilled, because no shared identifier or state links `ObservationTreatment` to `Event`.

Recommendation: document an explicit planned-treatment reference convention (e.g., `Event.additionalInfo` or a documented `plannedApplicationId`) before considering a schema change. Only propose a new field if the pilot must distinguish planned from applied irrigation and the convention cannot carry it.

## 12. Recommended next interoperability behavior to test

**Recommendation for this use case (Mission 003A): reuse BrAPI `Event` as written and document a shared usage convention; do not add a GenX irrigation field yet.** The fixture shows that BrAPI `Event` can represent an applied water depth of 20 mm for `plot-a` with plot-level attribution, and all structural checks pass. The precise meaning an independent reader would still lose before any new GenX field, schema, or operation is proposed is (a) the planned-to-applied irrigation link (which planned modality an applied event realizes) and (b) the standardized meaning of the `eventParameters` entry (name/code/units). Demonstrate that remaining gap with a reproducible case (NC-001 with an independent irrigation log) before proposing any GenX extension.