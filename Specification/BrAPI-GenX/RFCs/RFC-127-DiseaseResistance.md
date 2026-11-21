# RFC-127 — Disease Resistance (N)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (N).

## 1. Problem

BrAPI v2.1 has no place to record disease resistance. Resistance screening
results circulate without a stated resistance type, target, level, or
provenance, so they cannot be used for breeding decisions.

## 2. Object

`DiseaseResistance` — one immutable disease resistance record, with its
resistance type, target pest/disease, resistance level, screening method,
and provenance.

## 3. Endpoints

- `GET /genx/v1/disease-resistances` (`genxListDiseaseResistances`)
- `POST /genx/v1/disease-resistances` (`genxRegisterDiseaseResistance`)
- `GET /genx/v1/disease-resistances/{diseaseResistanceDbId}` (`genxGetDiseaseResistance`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `diseaseResistanceDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-379: Should `resistanceLevel` be required? (Current: optional.)
- D-380: Should `resistanceType` be a controlled vocabulary? (Current: free-form string.)
- D-381: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting N).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
