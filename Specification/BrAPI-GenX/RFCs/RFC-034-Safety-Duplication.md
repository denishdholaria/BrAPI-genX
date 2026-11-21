# RFC-034 — Safety Duplication (Genebank Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 has seed lots but no safety duplication record. Backup of
conserved material at secondary sites is essential for conservation. Without
this record, safety duplication cannot be audited or linked to seed lots with
provenance.

## 2. Object

`SafetyDuplication` — one immutable safety duplication record.

## 3. Endpoints

- `GET /genx/v1/safety-duplications` (`genxListSafetyDuplications`)
- `POST /genx/v1/safety-duplications` (`genxRegisterSafetyDuplication`)
- `GET /genx/v1/safety-duplications/{safetyDuplicationDbId}` (`genxGetSafetyDuplication`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Safety duplications reference BrAPI SeedLot by identifier; they do not
  duplicate that resource.
- A safety duplication is not a BrAPI SeedLot transaction and must not be
  treated as one.

## 5. Invariants

- A published `safetyDuplicationDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `backupSite` and `duplicatedAt` are required.
- A record does not imply a complete conservation record.

## 6. Deferred questions

- D-99: Should `quantity` be required? (Current: optional.)
- D-100: Should safety duplications link to GenX `StorageLocation`?
  (Current: optional, not required.)
- D-101: Should backup site be a governed vocabulary? (Current: free
  string.)

## 7. Classification

Primary domain: D1 — Germplasm and Biological Resources.
Cross-cutting: C1, C2, C3 (POST), C6, C9.