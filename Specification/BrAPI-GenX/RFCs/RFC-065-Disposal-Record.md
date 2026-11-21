# RFC-065 — Disposal Record (Genebank Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-003 (Seed Lot Ledger), RFC-015 (Genebank Storage), RFC-063 (Custody Transfer), `../CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 records germplasm, samples, and seed-lot transactions but has no
record for material leaving the collection permanently. Genebank retention
policy, lost-viability culls, quarantine destruction orders, and de-accessioning
all require defensible evidence of what was disposed of, why, how, when, and by
whose authority. Without a disposal record the collection inventory silently
shrinks and the reason is unrecoverable.

## 2. Object

`DisposalRecord` — one immutable record of a sample or seed lot being destroyed,
returned, or otherwise retired.

## 3. Endpoints

- `GET /genx/v1/disposal-records` (`genxListDisposalRecords`)
- `POST /genx/v1/disposal-records` (`genxRecordDisposalRecord`)
- `GET /genx/v1/disposal-records/{disposalRecordDbId}` (`genxGetDisposalRecord`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Disposals reference BrAPI `Sample` and GenX seed lots by identifier; they do
  not duplicate those resources.
- A disposal is not a BrAPI data resource and must not be treated as one.
- A disposal does not adjust BrAPI inventory by itself; the authoritative
  ledger effect is recorded through the seed-lot ledger.

## 5. Invariants

- A published `disposalRecordDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- Only a `completed` record asserts that disposal occurred.
- `cancelled` records remain visible; they are never deleted.
- A record does not by itself prove destruction; the referenced provenance must
  carry the evidence.
- `quantity` is meaningless without a unit; the unit belongs in provenance until
  a units module exists (see D-194).

## 6. Deferred questions

- D-193: Should at least one of `sampleDbId` or `lotDbId` be required? (Current:
  both optional.)
- D-194: Should `quantity` carry an explicit unit field or reference a GenX
  measurement-method/unit term? (Current: no unit field.)
- D-195: Should `method` and `reason` be controlled vocabularies rather than free
  strings? (Current: free strings.)

## 7. Classification

Primary domain: D1 — Genebank Storage and Conservation.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
