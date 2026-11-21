# RFC-149 — Sensor Device (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record sensor device records. Sensor devices
circulate without a stated type, manufacturer, model, or provenance, so they
cannot be tracked or audited.

## 2. Object

`SensorDevice` — one immutable sensor device record, with its device type,
sensor type, manufacturer, model, serial number, and provenance.

## 3. Endpoints

- `GET /genx/v1/sensor-devices` (`genxListSensorDevices`)
- `POST /genx/v1/sensor-devices` (`genxRegisterSensorDevice`)
- `GET /genx/v1/sensor-devices/{sensorDeviceDbId}` (`genxGetSensorDevice`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `sensorDeviceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-445: Should `serialNumber` be required? (Current: optional.)
- D-446: Should `sensorType` be a controlled vocabulary? (Current: free-form string.)
- D-447: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
