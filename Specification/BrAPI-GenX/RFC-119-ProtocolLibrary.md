# RFC-119 — Protocol Library (Cross-cutting S)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (S).

## 1. Problem

BrAPI v2.1 has no place to record protocol libraries. Breeding and genotyping
protocols circulate as unversioned documents with no stated method, version, or
provenance, so they cannot be audited or reproduced.

## 2. Object

`ProtocolLibrary` — one immutable protocol library record, with its name, type,
version, methods, and provenance.

## 3. Endpoints

- `GET /genx/v1/protocol-libraries` (`genxListProtocolLibraries`)
- `POST /genx/v1/protocol-libraries` (`genxRegisterProtocolLibrary`)
- `GET /genx/v1/protocol-libraries/{protocolLibraryDbId}` (`genxGetProtocolLibrary`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `protocolLibraryDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-355: Should `methods` be required? (Current: optional.)
- D-356: Should `protocolType` be a controlled vocabulary? (Current: free-form string.)
- D-357: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting S).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
