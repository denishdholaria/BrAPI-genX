# RFC-109 — Trial Network (Experimental Design)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 has no place to record trial networks and MET designs. Trial
networks are the routine reference for experimental design. Without a record,
networks arrive as unversioned notes with no stated name or provenance, so
they cannot be audited or reproduced.

## 2. Object

`TrialNetwork` — one immutable trial network or MET design record, with its
name and provenance.

## 3. Endpoints

- `GET /genx/v1/trial-networks` (`genxListTrialNetworks`)
- `POST /genx/v1/trial-networks` (`genxRegisterTrialNetwork`)
- `GET /genx/v1/trial-networks/{trialNetworkDbId}` (`genxGetTrialNetwork`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Trial network records reference BrAPI `Study` by identifier; they do not
  duplicate those resources.
- A record is not a BrAPI Study and must not be treated as one.

## 5. Invariants

- A published `trialNetworkDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- A record does not imply that the network is validated or endorsed.

## 6. Deferred questions

- D-325: Should `name` be required? (Current: optional.)
- D-326: Should records link to BrAPI `Study`? (Current: no link.)
- D-327: Should records link to GenX `ExperimentalDesign`? (Current: no
  link.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
