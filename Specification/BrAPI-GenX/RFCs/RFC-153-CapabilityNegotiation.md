# RFC-153 — Capability Negotiation (T/W/A)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (T/W/A).

## 1. Problem

BrAPI v2.1 has no place to record capability negotiation records. Capability
negotiation circulates without a stated type, counterparty, or provenance, so
it cannot be used for capability discovery.

## 2. Object

`CapabilityNegotiation` — one immutable capability negotiation record, with its
negotiation type, counterparty, last seen timestamp, and provenance.

## 3. Endpoints

- `GET /genx/v1/capability-negotiations` (`genxListCapabilityNegotiations`)
- `POST /genx/v1/capability-negotiations` (`genxRegisterCapabilityNegotiation`)
- `GET /genx/v1/capability-negotiations/{capabilityNegotiationDbId}` (`genxGetCapabilityNegotiation`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `capabilityNegotiationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- RFC-153-Q1: Should `lastSeen` be required? (Current: optional.)
- RFC-153-Q2: Should `negotiationType` be a controlled vocabulary? (Current: free-form string.)
- RFC-153-Q3: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting T/W/A).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
