# RFC-117 — ExperimentalProtocol

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 Study already carries experimental-design and cultural-practice metadata; Observation Units describe applied factors, and Events actual interventions. This candidate explores separately versioned protocol descriptions, but optional free-text properties cannot validate executable steps or scientific reproducibility.

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
- A record is not an official BrAPI Study, Observation Unit or Event. No typed Study, ExperimentalDesign, ProtocolLibrary or GenomicDataset reference appears in this schema.

## 5. Invariants

- A published `experimentalProtocolDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- Only `experimentalProtocolDbId` is mandatory in registration; `protocolName`, `provenance` and method details are optional. `treatments`, `replicates` and `blocks` are strings, not validated numeric or structural models.

## 6. Deferred questions

- D-349: Should `protocolName` be required? (Current: optional.)
- D-350: Should `protocolName` use controlled terminology? (Current: free-form string.)
- D-351: Should records link to GenX `GenomicDataset`? (Current: no link.)

## 7. Classification

Primary domain: D2.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
