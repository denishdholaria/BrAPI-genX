# RFC-003: Seed-Lot Ledger

- Status: **proposal** (not accepted, not normative, grants no implementation authority)
- Builds on: RFC-001 (compatibility law, idempotency/`409` evidence, source-local ordering)
- Scope: append-only, idempotent ledger entries for seed-lot movements
- Non-scope: legal title, pricing, stored balances, multi-lot atomic transfers,
  germplasm identity — each needs its own RFC or stays out

## 1. Problem

V2.1 `SeedLotTransaction` records that material moved (`fromSeedLotDbId`,
`toSeedLotDbId`, `amount: number`, free-text description) but guarantees
nothing a traceability consumer needs: `amount` is a float (precision loss on
inventory arithmetic), there is no idempotency (a retried scan duplicates the
movement), no actor or custodian, no location pair, no provenance, no ordering
statement, and no conflict rule. Two systems exchanging transactions cannot
tell a replay from a new movement.

Reference experience (BijMantra seedlot slice, pre-production research, cited
as evidence only): every inventory adjustment lands one append-only
fixed-scale decimal ledger entry keyed by `(tenant, idempotencyKey)` with a
conflicting-payload rejection, plus an audit row and an outbox item in one
atomic commit. RFC-003 standardizes the wire half of that shape: the entry and
its replay/conflict contract. Storage, audit, and outbox stay server-side.

## 2. Object — LotLedgerEntry

Files: `LotLedger/Schemas/LotLedgerEntry.yaml`,
`LotLedger/Schemas/LotLedgerEntryNewRequest.yaml`,
`LotLedger/Ledger_GET_POST.yaml`.

Purpose: make every lot movement an identifiable, replay-safe, ordered fact.

Fields: `entryDbId` (server-assigned, required on read),
`seedLotDbId` (path-owned, echoed), `entryType` (`adjust`|`move`|`handoff`|
`production`|`planting`|`trade`), `quantity` (fixed-scale decimal **string**,
required, `^-?\d+(\.\d+)?$` — never float), `units` (required), `actor`
(required — who performed the movement), `custodian?`,
`previousCustodian?` (custody chain on `handoff`), `locationFrom?`,
`locationTo?`, `occurredAt` (required — when it happened; distinct from
record time), `idempotencyKey?`, `description?`, `provenance?`
(`ProvenanceEnvelope` — calibration, scale ticket, scan evidence).

Responsibilities: one lot's ordered movement facts with replay safety.
Non-responsibilities: balances (derived by summing entries, never stored on
the wire); legal title and pricing; atomic multi-lot transfers (explicit
`requires decision`, §5 — single-writer-per-shard lesson applies).

Invariants:

1. Append-only. No `PUT`/`DELETE` is defined for entries. Corrections are new
   reversing entries referencing the original via `provenance.sources`.
2. Same `idempotencyKey` + identical body replays the existing entry (`200`,
   zero new effects). Same key + different body is rejected with `409`.
3. Entries carry a server-assigned `position`: monotonically increasing per
   lot, opaque cursor for pagination. Positions are source-local; clients must
   assume no global ordering across lots or servers.
4. Unknown lots: servers document auto-provision vs `404`. The reference
   server auto-provisions and returns an empty list for untouched lots.

## 3. Endpoints

- `POST /genx/v1/seedlots/{seedLotDbId}/ledger` (`genxAppendSeedLotLedgerEntry`) with `LotLedgerEntryNewRequest` →
  `200` + single entry (create, replay, or `409` conflict with plain-text body).
- `GET /genx/v1/seedlots/{seedLotDbId}/ledger` (`genxListSeedLotLedgerEntries`) with `entryType?` + standard pagination
  over `position` order → list of entries.

Both live under the existing `Seed Lots` tag so tag-filtered clients keep
working.

### Relationship to the V2.1 SeedLotTransaction contract — D-20

This endpoint is an additive GenX ledger contract, **not currently a declared
wire-compatible replacement** for V2.1 `SeedLotTransaction`. Both can describe
a real-world movement of seed-lot material, but GenX uses one-lot, ordered
entries with fixed-scale decimal strings, actor/provenance and replay/conflict
rules, whereas V2.1 transactions express `fromSeedLotDbId` and
`toSeedLotDbId` with numeric `amount` and have no equivalent idempotency or
event-correlation guarantee.

Until D-20 is resolved, implementations must not silently mirror a single
movement into both streams, claim the streams are equivalent, or sum both as
independent movements. A compatibility adapter needs an explicit mapping and
a stable cross-surface event identity; the current proposal does not provide
that contract. Multi-lot atomicity remains separately unresolved under D-07.


## 4. Hypothesis, falsifier, verification

- Hypothesis: two systems can exchange lot movements such that retries never
  duplicate, conflicts never merge, and any consumer derives identical
  balances from the same entry stream.
- Falsifier: a replay that appends; a conflict that mutates; a quantity that
  loses precision through the round-trip; two reads that reorder entries.
- Verification: static probes S-11/S-12 plus live probes L-10/L-11 in
  `Conformance/probes.yaml` against the reference test server.

## 5. Explicit unknowns and requires-decision

1. `requires decision`: atomic multi-lot transfers (one movement, two lots,
   one writer) — out of scope; single-entry atomicity only.
2. `requires decision`: unknown-lot behavior (auto-provision vs `404`) —
   reference auto-provisions; the standard does not yet mandate either.
3. `assumption`: decimal scale agreement (units + scale) is out-of-band per
   `units` vocabulary; the wire guarantees precision, not unit semantics.
4. `unknown`: real custody-handoff acceptance workflows (two-party sign-off)
   — `custodian`/`previousCustodian` record claims, not approvals.

## 6. File map

```text
Specification/BrAPI-GenX/
  RFC-003-Seed-Lot-Ledger.md   this document
  LotLedger/README.md + GroupDescription.md
    + Schemas/LotLedgerEntry.yaml + Schemas/LotLedgerEntryNewRequest.yaml
    + Ledger_GET_POST.yaml
```
