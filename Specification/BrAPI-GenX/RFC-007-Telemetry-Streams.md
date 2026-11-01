# RFC-007: Sensor Telemetry Streams

- Status: **proposal** (not accepted, not normative, grants no implementation authority)
- Builds on: RFC-001 (compatibility law, `409` evidence, standard envelope)
- Scope: timestamped sensor readings with idempotent ingest and server
  aggregates
- Non-scope: device/sensor registries, alert rules and alert events,
  continuous-weather modeling, actuation — each needs its own RFC or stays out

## 1. Problem

V2.1 `Observation` is one point value for one observation unit. Field reality
is streams: weather stations, soil probes, and phenotyping rigs emit
timestamped numeric samples at fixed cadences, and consumers need range reads
plus windowed aggregates (mean/min/max/count) — not one `Observation` per
sample and not client-side reassembly of millions of points. A prototype IoT
extension (devices, sensors, time-series telemetry with a
device/sensor/timestamp index, aggregates with period/min/max/sampleCount,
alert events) proved the vocabulary; RFC-007 standardizes the wire half:
points, idempotent batch ingest, range reads, and aggregates.

Reference experience (BijMantra prototype, pre-production research, cited as
evidence only): `iot_telemetry` time-series table indexed by
`(device, sensor, timestamp)`, `iot_aggregates` with period windows, and
`iot_alert_events`. Device registries and alerting stay server-side.

## 2. Object — TelemetryPoint

Files: `Telemetry/Schemas/TelemetryPoint.yaml`,
`Telemetry/Schemas/TelemetryBatchResponse.yaml` (inline in endpoint),
`Telemetry/Telemetry_GET_POST.yaml`.

Purpose: make one sensor sample an identifiable, replay-safe fact, and make
aggregates server-computed, named, and reproducible.

Fields: `deviceDbId` (required, opaque — registries are out of scope),
`sensorDbId` (required, opaque), `timestamp` (required, RFC 3339 — sample
time), `value` (required JSON number — sensor floats are honest measurements;
unlike inventory quantities they are never summed as money), `unit?`,
`quality` (`good`|`suspect`|`bad`, default `good`), `provenance?`
(`ProvenanceEnvelope` — calibration, firmware).

Aggregates are read shapes, not stored objects: `TelemetryBucket`
(`{windowStart, value, sampleCount, aggregation}`), computed over
`windowSeconds` buckets (default: one bucket over the whole range).

Responsibilities: sample identity, idempotent ingest, range + aggregate
reads. Non-responsibilities: device/sensor lifecycle; alert evaluation and
delivery; gap-filling or resampling semantics (servers document their own;
`quality: bad` marks distrust, it does not delete).

Invariants:

1. Natural key is `(deviceDbId, sensorDbId, timestamp)`. Same key + same
   value replays with zero new effects. Same key + different value is
   rejected with `409` — two observers disagreeing about one sample instant
   is a conflict, not an overwrite.
2. `POST /genx/v1/telemetry` (`genxAppendTelemetryBatch`) takes an array (V2.1 batch style) and reports
   `{appended, replayed}` counts. Batch mates conflicting with stored points
   fail the batch element-wise: conflicting elements are rejected and named,
   non-conflicting ones commit. (Element-wise semantics documented in the
   endpoint file.)
3. Aggregates are deterministic functions of stored points in
   `[from, to)`: `mean` is the arithmetic mean, `min`/`max` over values,
   `count` the sample count. Empty ranges yield empty `data`, never an error.

## 3. Endpoints

- `POST /genx/v1/telemetry` (`genxAppendTelemetryBatch`) with an array of `TelemetryPoint` → `200` +
  `{appended, replayed, conflicts[]}`. Conflicts reject the element, not the
  batch.
- `GET /genx/v1/telemetry` (`genxQueryTelemetrySamplesOrAggregates`) with `deviceDbId` (required), `sensorDbId?`, `from?`,
  `to?` (RFC 3339), `aggregation?` (`none`|`mean`|`min`|`max`|`count`,
  default `none`), `windowSeconds?` + standard pagination → points
  (`aggregation: none`) or `TelemetryBucket` rows.

## 4. Hypothesis, falsifier, verification

- Hypothesis: two systems can exchange sensor streams such that retried
  uploads never duplicate, disagreements never overwrite, and any consumer
  recomputes identical aggregates from the same range.
- Falsifier: a replay that appends; a conflict that overwrites; an aggregate
  that disagrees with the stored points; two reads that reorder a range.
- Verification: static probes S-19/S-20 plus live probes L-21–L-23 in
  `Conformance/probes.yaml` against the reference test server.

## 5. Explicit unknowns and requires-decision

1. `requires decision`: device/sensor registration and identity governance.
2. `requires decision`: alert rules, evaluation cadence, and delivery.
3. `requires decision`: gap-filling, resampling, and timezone-of-record
   policies for aggregates.
4. `assumption`: `value` floats are measurements, not accounting figures;
   the decimal-string rule (RFC-003) deliberately does not apply here.
5. `unknown`: continuous-weather modeling that merges station streams with
   forecast grids.

## 6. File map

```text
Specification/BrAPI-GenX/
  RFC-007-Telemetry-Streams.md   this document
  Telemetry/README.md + GroupDescription.md
    + Schemas/TelemetryPoint.yaml + Telemetry_GET_POST.yaml
```
