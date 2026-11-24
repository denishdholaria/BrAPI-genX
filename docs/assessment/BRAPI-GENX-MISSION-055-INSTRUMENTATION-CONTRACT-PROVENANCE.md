# Mission 055 — Instrumentation provenance, scientific caution and exact routes

**Date:** 2026-11-24
**Prepared parent:** `3ee5332736bf6df95cfba74d56d6fdc6016dca4e`
**Scope:** Source-based RFC/README/GroupDescription review of CalibrationQuality, SensorDevice, TelemetryNormalization and EdgeGatewayHealth, plus regression checks.

## Exact-source findings

- CalibrationQuality contains an optional `sensorDeviceReference` string, calibration type/date and a string calibration factor. None guarantees an accepted physical calibration method, traceable standard or measurement accuracy. D-448–D-450 remain open.
- SensorDevice contains optional device category, sensor category, manufacturer, model and serial. A free-text serial does not establish authenticated device ownership or a valid sensor certificate. D-445–D-447 remain open.
- TelemetryNormalization contains optional free-form raw/normalized data references and method. This is neither a data transformation nor tested unit/error propagation. D-442–D-444 remain open.
- EdgeGatewayHealth contains optional device, gateway type, last-seen and health-status text. No heartbeat interval, threshold or independently observed health service is specified. D-451–D-453 remain open.

## False README/RFC route discrepancies repaired without wire changes

- CalibrationQuality README listed `/genx/v1/calibration-qualitiess` in three places; the actual YAML and RFC source use `/genx/v1/calibration-qualities`. The README was corrected.
- TelemetryNormalization RFC-148 listed singular `/genx/v1/telemetry-normalization` and a singular listing operation ID, despite actual source and README using `/genx/v1/telemetry-normalizations` and `genxListTelemetryNormalizations`. RFC prose was corrected.
- Actual source operation identities such as `genxListCalibrationQualitys`, `genxListEdgeGatewayHealths`, and the `/edge-gateway-healths` route were **preserved unchanged** notwithstanding awkward grammar. Renaming requires separately approved compatibility governance.

Four protected source-backed descriptions and a test comparing every draft source route/list operation ID with both README and RFC are added. Protected group count is **53 of 156**, **103 deferred**. Explicit no-typed-link observations reach **29**, including these four unratified GenX ResearchAsset links.

**No normative decisions, official BrAPI sources, GenX OpenAPI wire schemas, routes, endpoint registry, generator outputs, or maturity status were changed.** Hosted static/live and specification build must be verified against the integrated commit.
