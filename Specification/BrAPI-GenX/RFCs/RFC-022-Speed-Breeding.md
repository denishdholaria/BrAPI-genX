# RFC-022 — Speed Breeding (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 has no record for speed breeding protocols: environmental
conditions and generation time used to accelerate plant development. Without
this record, accelerated breeding processes cannot be audited or reproduced.

## 2. Object

`SpeedBreedingProtocol` — one immutable speed breeding protocol record.

## 3. Endpoints

- `GET /genx/v1/speed-breeding-protocols` (`genxListSpeedBreedingProtocols`)
- `POST /genx/v1/speed-breeding-protocols` (`genxRegisterSpeedBreedingProtocol`)
- `GET /genx/v1/speed-breeding-protocols/{speedBreedingProtocolDbId}` (`genxGetSpeedBreedingProtocol`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Speed breeding protocols reference BrAPI Program by identifier; they do not
  duplicate that resource.
- A protocol record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `speedBreedingProtocolDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `lightRegime`, `temperatureRegime`, `photoperiod`, and `generationTime` are
  recorded, not inferred.
- A record does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-63: Should `photoperiod` and `generationTime` be required? (Current:
  optional.)
- D-64: Should speed breeding protocols link to GenX `BreedingPipeline`?
  (Current: optional, not required.)
- D-65: Should generation time be a structured quantity? (Current: integer
  days.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.