# RFC-030 — Quarantine (Genebank Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 has seed lots but no quarantine record. Isolation and inspection
of conserved material are essential for conservation. Without this record,
quarantine events cannot be audited or linked to seed lots with provenance.

## 2. Object

`QuarantineRecord` — one immutable quarantine record.

## 3. Endpoints

- `GET /genx/v1/quarantine-records` (`genxListQuarantineRecords`)
- `POST /genx/v1/quarantine-records` (`genxRecordQuarantine`)
- `GET /genx/v1/quarantine-records/{quarantineRecordDbId}` (`genxGetQuarantineRecord`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Quarantine records reference BrAPI SeedLot by identifier; they do not
  duplicate that resource.
- A quarantine record is not a BrAPI SeedLot transaction and must not be
  treated as one.

## 5. Invariants

- A published `quarantineRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `reason` and `quarantinedAt` are required.
- A record does not imply a complete conservation record.

## 6. Deferred questions

- D-87: Should `releasedAt` be required for released records? (Current:
  optional.)
- D-88: Should quarantine records link to GenX `ViabilityTest`? (Current:
  optional, not required.)
- D-89: Should quarantine reason be a governed vocabulary? (Current: free
  string.)

## 7. Classification

Primary domain: D1 — Germplasm and Biological Resources.
Cross-cutting: C1, C2, C3 (POST), C6, C9.