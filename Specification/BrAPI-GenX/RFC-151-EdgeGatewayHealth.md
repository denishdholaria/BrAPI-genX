# RFC-151 — Edge Gateway Health (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record edge gateway health records. Edge gateway
health circulates without a stated type, device ID, last seen timestamp, or
provenance, so edge gateway health cannot be monitored or audited.

## 2. Object

`EdgeGatewayHealth` — one immutable edge gateway health record, with its
gateway type, device ID, last seen timestamp, health status, region/zone, and
provenance.

## 3. Endpoints

- `GET /genx/v1/edge-gateway-healths` (`genxListEdgeGatewayHealths`)
- `POST /genx/v1/edge-gateway-healths` (`genxRegisterEdgeGatewayHealth`)
- `GET /genx/v1/edge-gateway-healths/{edgeGatewayHealthDbId}` (`genxGetEdgeGatewayHealth`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `edgeGatewayHealthDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-451: Should `healthStatus` be required? (Current: optional.)
- D-452: Should `gatewayType` be a controlled vocabulary? (Current: free-form string.)
- D-453: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
