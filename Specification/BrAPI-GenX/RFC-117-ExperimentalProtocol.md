# RFC-117 — ExperimentalProtocol

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 has no place to record ExperimentalProtocol. Without a record, ExperimentalProtocol arrive as
unversioned entries with no stated provenance, so they cannot be audited or
reproduced.

## 2. Object

`ExperimentalProtocol` — one immutable ExperimentalProtocol record, with its name and provenance.

## 3. Endpoints

- `GET /genx/v1/experimental-protocols` (`genxListExperimentalProtocols`)
- `POST /genx/v1/experimental-protocols` (`genxRegisterExperimentalProtocol`)
- `GET /genx/v1/experimental-protocols/{experimentalProtocolDbId}` (`genxGetExperimentalProtocol`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `experimentalProtocolDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-349: Should `name` be required? (Current: optional.)
- D-350: Should `name` be a controlled vocabulary? (Current: free-form string.)
- D-351: Should records link to GenX `GenomicDataset`? (Current: no link.)

## 7. Classification

Primary domain: D2.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
