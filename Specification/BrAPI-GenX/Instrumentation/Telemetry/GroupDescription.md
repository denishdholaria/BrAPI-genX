# Group Telemetry — Sensor Measurement Streams

**Status:** BrAPI-GenX candidate sensor-telemetry profile (RFC-007); contract validation does not establish calibration, device trust, statistical soundness or production ingest reliability.

The module proposes timestamped `TelemetryPoint` records and batch ingestion for device/sensor observations, together with queries of recorded points or time-window aggregates. The candidate ingestion contract identifies a point by device, sensor and timestamp; identical retries should not duplicate samples, and conflicting values must not silently overwrite accepted observations. Aggregate calculations are distinct from the underlying original samples and need an explicit window and aggregation type.

**Scope boundary:** A sensor timestamp does not by itself establish time synchronization, calibration validity, spatial representativeness, or quality control. The draft does not finalize device registration, sensor identity, alert policy, resampling, gap-filling, or timezone authority. Those concerns require separate evidence under decisions D-16 to D-18. Idempotency and multi-instance durability follow project-level D-24 and D-25 constraints but are not verified for this endpoint.

**Sources:** [Local module contract](./README.md), [point schema](./Schemas/TelemetryPoint.yaml), [candidate operations](./Telemetry_GET_POST.yaml), [RFC-007](../../RFCs/RFC-007-Telemetry-Streams.md), and [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
