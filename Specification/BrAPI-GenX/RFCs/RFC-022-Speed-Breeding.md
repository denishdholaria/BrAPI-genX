# RFC-022 — Speed Breeding (Breeding)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D2).

## 1. Problem

BrAPI v2.1 Study already carries environmental parameters, growth-facility and cultural-practice metadata; Events capture actual interventions. This draft explores a separately registered protocol, but its optional regime descriptions and generation-time estimate do not establish an implemented treatment or experimentally validated acceleration.

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
- Speed breeding protocols require a `programDbId` string, without an authority-qualified server or independently verified Program relationship. This does not replace official Study records.
- A protocol record is not a BrAPI Program and must not be treated as one.

## 5. Invariants

- A published `speedBreedingProtocolDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `protocolName` and `programDbId` are required; `lightRegime`, `temperatureRegime`, `photoperiod` and `generationTime` are optional. No time-resolved environmental schedule or measured generational response is enforced.
- A record does not imply an approved breeding plan or release.

## 6. Deferred questions

- D-63: Should `photoperiod` and `generationTime` be required? (Current:
  optional.)
- D-64: Should speed breeding protocols link to GenX `BreedingPipeline`?
  (Current: no `breedingPipelineDbId` or typed relationship exists; the link is not implemented.)
- D-65: Should generation time be a structured quantity? (Current: integer
  days.)

## 7. Classification

Primary domain: D2 — Breeding Programs and Experimental Design.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
