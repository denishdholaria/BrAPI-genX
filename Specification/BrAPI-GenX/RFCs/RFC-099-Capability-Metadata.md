# RFC-099 — Capability Metadata (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

BrAPI v2.1 has no place to record server and profile capability metadata.
Capability metadata is the routine reference for capability negotiation. Without
a record, capabilities arrive as unversioned notes with no stated profile or
provenance, so they cannot be audited or reproduced.

## 2. Object

`CapabilityMetadata` — one immutable capability metadata record, with its
profile, capabilities, and provenance.

## 3. Endpoints

- `GET /genx/v1/capability-metadata` (`genxListCapabilityMetadata`)
- `POST /genx/v1/capability-metadata` (`genxRegisterCapabilityMetadata`)
- `GET /genx/v1/capability-metadata/{capabilityMetadataDbId}` (`genxGetCapabilityMetadata`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Capability metadata records reference BrAPI server info by identifier; they
  do not duplicate those resources.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `capabilityMetadataDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the capabilities are validated or endorsed.

## 6. Deferred questions

- D-295: Should `profile` be required? (Current: optional.)
- D-296: Should `capabilities` be a controlled structure? (Current: free-form
  object.)
- D-297: Should records link to GenX `ServerInfoV3`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
