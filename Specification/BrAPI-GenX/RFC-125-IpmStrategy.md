# RFC-125 — IPM Strategy (N)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (N).

## 1. Problem

BrAPI v2.1 has no place to record IPM strategies. Integrated pest
management strategies circulate without a stated target, type, tactics, or
provenance, so they cannot be compared or audited.

## 2. Object

`IpmStrategy` — one immutable IPM strategy record, with its name, target
pest/disease, type, tactics, and provenance.

## 3. Endpoints

- `GET /genx/v1/ipm-strategies` (`genxListIpmStrategies`)
- `POST /genx/v1/ipm-strategies` (`genxRegisterIpmStrategy`)
- `GET /genx/v1/ipm-strategies/{ipmStrategyDbId}` (`genxGetIpmStrategy`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `ipmStrategyDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-373: Should `tactics` be required? (Current: optional.)
- D-374: Should `strategyType` be a controlled vocabulary? (Current: free-form string.)
- D-375: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting N).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
