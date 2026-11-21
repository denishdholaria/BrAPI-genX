# RFC-133 — Pest/Disease Risk (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record pest/disease risk. Risk advisories
circulate without a stated risk type, target, level, or provenance, so they
cannot be used for IPM decisions.

## 2. Object

`PestDiseaseRisk` — one immutable pest/disease risk record, with its risk
type, target pest/disease, risk level, probability, and provenance.

## 3. Endpoints

- `GET /genx/v1/pest-disease-risks` (`genxListPestDiseaseRisks`)
- `POST /genx/v1/pest-disease-risks` (`genxRegisterPestDiseaseRisk`)
- `GET /genx/v1/pest-disease-risks/{pestDiseaseRiskDbId}` (`genxGetPestDiseaseRisk`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `pestDiseaseRiskDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-397: Should `probability` be required? (Current: optional.)
- D-398: Should `riskType` be a controlled vocabulary? (Current: free-form string.)
- D-399: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
