# RFC-148 — Telemetry Normalization (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record telemetry normalization records. Telemetry
normalization circulates without a stated type, raw data reference, or
provenance, so normalized data cannot be traced or audited.

## 2. Object

`TelemetryNormalization` — one immutable telemetry normalization record, with
its normalization type, raw data reference, normalized data reference, method,
and provenance.

## 3. Endpoints

- `GET /genx/v1/telemetry-normalizations` (`genxListTelemetryNormalizations`)
- `POST /genx/v1/telemetry-normalizations` (`genxRegisterTelemetryNormalization`)
- `GET /genx/v1/telemetry-normalizations/{telemetryNormalizationDbId}` (`genxGetTelemetryNormalization`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.
- The candidate has no typed GenX `ResearchAsset` reference; D-444 remains open. An advisory operation-neighbor link cannot establish scientific identity.

## 5. Invariants

- A published `telemetryNormalizationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-442: Should `normalizedDataReference` be required? (Current: optional.)
- D-443: Should `normalizationType` be a controlled vocabulary? (Current: free-form string.)
- D-444: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
