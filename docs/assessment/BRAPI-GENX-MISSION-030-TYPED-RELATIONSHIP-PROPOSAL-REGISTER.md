# Mission 030 — Proposal-only typed scientific relationship register

**Date:** 2026-11-24. **Parent main:** `e8664cdabe4fdda3cce05ef360556db68cd63d60`.

Internal architectural D-026 accepts separation of advisory
operation navigation from independently governed scientific relationships.
This mission creates a **separate, initially empty** YAML proposal register
(`Specification/BrAPI-GenX/Conformance/typed-relationship-candidates.yaml`)
with a strict validator and a new static conformance workflow gate.

The proposal vocabulary distinguishes `typed-resource-reference`,
`provenance-derivation` and `operation-contract-equivalence`.
Every future record must remain `proposal-only` and cite an actual
repository-local schema for each side, a plain-language falsifiable claim,
evidence references and unresolved scientific questions. Unknown fields,
`accepted` status, fake approvals, unsafe paths and unsupported kinds
are rejected. No existing neighbor is migrated, mapped or deleted.

**Verification:** 14/14 isolated positive/mutation tests passed in
`/mnt/data/genx_typed`; Python compilation passed. Exact tested Git
object hashes: validator `2b872b80a2bc3d6264df9c53be29ba9837bc6108`;
tests `238a98f1bd86f07c4d6a020eddb6d37f8b581f35`.

**Limit:** the records are proposals and the validator does not prove
scientific correctness, authorial approval, record resolution, production
data ownership, or independent software interoperability. Full checkout
and hosted Continuous Integration (CI) have not run. No official Breeding
Application Programming Interface (BrAPI) version 2.1 source, existing
GenX route, endpoint registry link or Request for Comments (RFC)
maturity status was modified.
