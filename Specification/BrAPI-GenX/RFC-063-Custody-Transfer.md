# RFC-063 — Custody Transfer (Genebank Conservation)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-003 (Seed Lot Ledger), RFC-030 (Quarantine), RFC-034 (Safety Duplication), `CLASSIFICATION.md` (D1).

## 1. Problem

BrAPI v2.1 covers germplasm, samples, and seed-lot ledgers but has no record of
who was responsible for a physical sample at a given time. Genebank
conservation, quarantine movement, and safety duplication all require a
defensible chain of custody. Without a custody record, transfers between
institutes, storage sites, and regeneration cycles cannot be audited, and
"who held this sample on this date" is unanswerable from the API.

## 2. Object

`CustodyTransfer` — one immutable record of custody moving from one party to
another for a sample or seed lot.

## 3. Endpoints

- `GET /genx/v1/custody-transfers` (`genxListCustodyTransfers`)
- `POST /genx/v1/custody-transfers` (`genxRecordCustodyTransfer`)
- `GET /genx/v1/custody-transfers/{custodyTransferDbId}` (`genxGetCustodyTransfer`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Custody transfers reference BrAPI `Sample` and GenX seed lots by identifier;
  they do not duplicate those resources.
- A custody transfer is not a BrAPI data resource and must not be treated as one.
- A custody transfer does not itself move bytes or physical material. It records
  that a movement was claimed and accepted.

## 5. Invariants

- A published `custodyTransferDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional transfers linked by `supersedes`.
- `fromParty` and `toParty` are distinct for an accepted transfer.
- A `rejected` transfer never establishes custody.
- `status` follows an append-only lifecycle: `pending` → `accepted` | `rejected`;
  corrections use `superseded` on the replaced record, never in-place edits.
- A record does not imply legal ownership, phytosanitary clearance, or material
  viability. Those remain separate claims.

## 6. Deferred questions

- D-187: Should `sampleDbId` or `lotDbId` be required, and should at least one be
  mandatory? (Current: both optional, so a record can exist with only parties.)
- D-188: Should `receivedCondition` be an enum drawn from a controlled
  vocabulary rather than free text? (Current: free string.)
- D-189: Should custody transfers link to GenX `Quarantine` and
  `SafetyDuplication` records explicitly, rather than only by `supersedes` and
  provenance? (Current: not modelled.)

## 7. Classification

Primary domain: D1 — Genebank Storage and Conservation.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
