# RFC-150 — Calibration Quality (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record calibration quality records. Calibration
quality circulates without a stated type, date, factor, or provenance, so
normalized sensor data cannot be traced or audited.

## 2. Object

`CalibrationQuality` — one immutable calibration quality record, with its
calibration type, date, factor, and provenance.

## 3. Endpoints

- `GET /genx/v1/calibration-qualities` (`genxListCalibrationQualitys`)
- `POST /genx/v1/calibration-qualities` (`genxRegisterCalibrationQuality`)
- `GET /genx/v1/calibration-qualities/{calibrationQualityDbId}` (`genxGetCalibrationQuality`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.
- The candidate has no typed GenX `ResearchAsset` reference; D-450 remains open. An advisory operation-neighbor link cannot establish scientific identity.

## 5. Invariants

- A published `calibrationQualityDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-448: Should `calibrationFactor` be required? (Current: optional.)
- D-449: Should `calibrationType` be a controlled vocabulary? (Current: free-form string.)
- D-450: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
