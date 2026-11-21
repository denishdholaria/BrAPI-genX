# RFC-021 — Viability Testing (Genebank Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 has seed lots but no viability/germination test record. Without
this record, conservation viability cannot be audited or reproduced.

## 2. Object

`ViabilityTest` — one immutable viability/germination test record.

## 3. Endpoints

- `GET /genx/v1/viability-tests` (`genxListViabilityTests`)
- `POST /genx/v1/viability-tests` (`genxRecordViabilityTest`)
- `GET /genx/v1/viability-tests/{viabilityTestDbId}` (`genxGetViabilityTest`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Viability tests reference BrAPI SeedLot by identifier; they do not duplicate
  that resource.
- A viability test is not a BrAPI SeedLot transaction and must not be treated
  as one.

## 5. Invariants

- A published `viabilityTestDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional tests linked by `supersedes`.
- `germinationPercent`, `viabilityPercent`, and `sampleSize` are recorded, not
  inferred.
- A test does not imply a complete conservation record.

## 6. Deferred questions

- D-60: Should `germinationPercent` and `viabilityPercent` be required for
  completed tests? (Current: optional.)
- D-61: Should test method be a governed enumeration? (Current: free string.)
- D-62: Should viability tests link to GenX `StorageLocation`? (Current:
  optional, not required.)

## 7. Classification

Primary domain: D1 — Germplasm and Biological Resources.
Cross-cutting: C1, C2, C3 (POST), C6, C9.