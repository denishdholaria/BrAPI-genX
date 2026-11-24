# Mission 056 — Environmental observation, forecast and water accounting integrity

**Date:** 2026-11-24
**Prepared parent:** `8d2ac0b4d4df2d410c7ec5fa39b0d33621760bf1`
**Scope:** source-backed RFC/README and GroupDescription review of five environmental candidates; no wire contracts changed.

## Critical schema facts

- WeatherObservation requires observedAt and a measurements array, which may be empty. Each measurement requires a numeric value. A missing-quality flag is not associated with a conditional missing-value representation, and source/station/location are not necessarily present.
- WeatherForecast requires issued/valid-from/valid-to timestamps but no cross-field chronological ordering or nonempty measurements requirement. Its numeric forecasts are not observed weather and no typed WeatherObservation reference exists (D-91).
- ClimateNormal has a free-string `period` and required numeric mean, with no documented statistical computation or source measurement lineage. A typed WeatherObservation reference is absent (D-97).
- SoilProfile has required sample time and Location string, but optional texture, nutrient values and moisture; no sampling depth interval is present (D-68), and no typed WeatherObservation reference (D-67).
- WaterBalance requires only identifier and status. Its period endpoints, location/study, six flux/storage values and provenance are all optional; the schema does not require water-budget closure, date-ordering, common component windows or source record linkage (D-202–D-204). RFC-068 incorrectly claimed official BrAPI v2.1 supplied weather observations and irrigation events: those separately named resources are GenX candidate proposals, not official BrAPI source operations. The old RFC also asserted existing typed CropCycle/WeatherObservation/IrrigationOperation links not present in the candidate schema. Corrected as editorial source-truth only.

Five source-backed group descriptions and regression tests raise reviewed count to **58 of 156** and leave **98 evidence-deferred**. Missing typed-link audit observations rise from 29 to **33**, covering unratified WeatherObservation links; the explicit observation variable and Location string fields are not misclassified as missing.

## Boundaries

All drafts remain STRUCTURAL_DRAFT. No scientific formula, time ordering rule, reference link, weather source endorsement, error model, official BrAPI schema, GenX OpenAPI field, endpoint registry, experimental identity or mature RFC status has been changed.

Hosted full static/live and specification build must pass on integrated HEAD before verification can be claimed.
