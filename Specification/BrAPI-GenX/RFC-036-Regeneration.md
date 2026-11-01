# RFC-036 — Regeneration (Genebank Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 has seed lots but no regeneration record. Multiplication of
conserved material is essential for maintaining viability. Without this
record, regeneration events cannot be audited or linked to seed lots with
provenance.

## 2. Object

`RegenerationRecord` — one immutable regeneration record.

## 3. Endpoints

- `GET /genx/v1/regeneration-records` (`genxListRegenerations`)
- `POST /genx/v1/regeneration-records` (`genxRecordRegeneration`)
- `GET /genx/v1/regeneration-records/{regenerationRecordDbId}` (`genxGetRegeneration`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Regeneration records reference BrAPI SeedLot by identifier; they do not
  duplicate that resource.
- A regeneration record is not a BrAPI SeedLot transaction and must not be
  treated as one.

## 5. Invariants

- A published `regenerationRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `method` and `regeneratedAt` are required.
- A record does not imply a complete conservation record.

## 6. Deferred questions

- D-106: Should `quantity` be required? (Current: optional.)
- D-107: Should regeneration records link to GenX `ViabilityTest`?
  (Current: optional, not required.)
- D-108: Should method be a governed vocabulary? (Current: free string.)

## 7. Classification

Primary domain: D1 — Germplasm and Biological Resources.
Cross-cutting: C1, C2, C3 (POST), C6, C9.