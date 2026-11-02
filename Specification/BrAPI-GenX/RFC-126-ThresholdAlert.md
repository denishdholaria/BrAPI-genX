# RFC-126 — Threshold Alert (N)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (N).

## 1. Problem

BrAPI v2.1 has no place to record threshold alerts. Alerts for pests,
diseases, or abiotic stress occur without a stated threshold, current value,
or provenance, so they cannot be acted on or audited.

## 2. Object

`ThresholdAlert` — one immutable threshold alert record, with its alert type,
threshold value, current value, status, trigger date, and provenance.

## 3. Endpoints

- `GET /genx/v1/threshold-alerts` (`genxListThresholdAlerts`)
- `POST /genx/v1/threshold-alerts` (`genxRegisterThresholdAlert`)
- `GET /genx/v1/threshold-alerts/{thresholdAlertDbId}` (`genxGetThresholdAlert`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `thresholdAlertDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-376: Should `currentValue` be required? (Current: optional.)
- D-377: Should `alertType` be a controlled vocabulary? (Current: free-form string.)
- D-378: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting N).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
