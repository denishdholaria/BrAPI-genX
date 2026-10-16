# BrAPI GenX — Sensor Telemetry Streams

Timestamped sensor samples with idempotent batch ingest and server-computed
aggregates. Retried uploads never duplicate; disagreements never overwrite.

- `POST /brapi/v3/telemetry` (`genxAppendTelemetryBatch`) takes an array of `TelemetryPoint`
  (`Schemas/TelemetryPoint.yaml`) and reports `{appended, replayed,
  conflicts[]}`. The natural key `(deviceDbId, sensorDbId, timestamp)` +
  identical value replays; same key + different value rejects the element
  with `409` semantics without failing the batch.
- `GET /brapi/v3/telemetry` (`genxQueryTelemetrySamplesOrAggregates`) reads ranges (`from`/`to`) as points or as
  `TelemetryBucket` aggregates (`mean|min|max|count` over `windowSeconds`
  buckets).

Device registries, alerting, and resampling policies are out of scope.
Details and falsifiers: `../RFC-007-Telemetry-Streams.md`.
