# Group LotLedger — Seed-Lot Movement Records

**Status:** BrAPI-GenX candidate contract associated with RFC-003, which has contract-validation evidence but is not a ratified interoperability standard. Security, multi-writer behavior and mappings to official BrAPI remain subject to review.

This module proposes append-only `LotLedgerEntry` movement records associated with an identified seed lot. The candidate operations append a new movement and list a seed lot's entries in source-local position order. The design treats retries as idempotent for the same scoped key and equivalent request; a conflicting reuse must not overwrite an existing movement. Balances, where calculated, are **derived** from the ledger, not authoritatively stored as an arbitrary new balance.

**Scope boundary:** Corrections are new records, not in-place replacement or deletion. A source-local position is not a globally comparable event timestamp. The relationship, authority, and potential double counting between official BrAPI `SeedLotTransaction` and a GenX `LotLedgerEntry` remain **unresolved under D-20**; never merge or duplicate official transactions solely because these operations concern the same seed lot. Idempotency durability and authorization are constrained by accepted D-24 and D-25, not proven by the draft endpoint text.

**Sources:** [Local module contract](./README.md), [ledger schema](./Schemas/LotLedgerEntry.yaml), [operations](./Ledger_GET_POST.yaml), [RFC-003](../../RFCs/RFC-003-Seed-Lot-Ledger.md), and [project decisions](../../DECISIONS.md).
