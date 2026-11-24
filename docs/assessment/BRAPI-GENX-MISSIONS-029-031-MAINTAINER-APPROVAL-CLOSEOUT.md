# BrAPI-GenX — Maintainer Approval and Evidence-Bounded Documentation Closeout

**Date:** 2026-11-24  
**Inspected starting `main`:** `1008819bbbfe27b512a2223263b03366e3ed507a`  
**Verified integrated implementation head:** `b4857c4a7d98fe881e842abab0c673efe7faa039`  
**Scope:** internal architectural decisions D-026 and D-027, terminal-decision binding, typed-relationship candidate isolation, and careful GenX group documentation.

## 1. Maintainer decisions captured

The maintainer explicitly approved the recommended directions in the
2026-11-24 project conversation:

- **D-026 — ACCEPTED:** legacy operation neighbors are advisory
  navigation, not typed scientific relationships, contract equivalence,
  data ownership, authorization or approval for writes. Scientific
  relationships belong in a separate governed track.
- **D-027 — ACCEPTED:** a terminal `rejected` or `superseded`
  semantic-neighbor disposition requires an exact, unique, maintainer-
  approved decision record identifying the original source–target link,
  action, and successor when applicable.

The detailed records are in
`Specification/BrAPI-GenX/DECISIONS.md`, the decision-governance
register, and the project decision-authority document. These are
internal architectural choices, **not** individual link rejections or
acceptance of any new official specification.

## 2. Mission 029 — exact terminal authorization binding

- New
  `Specification/BrAPI-GenX/Conformance/semantic-neighbor-terminal-decisions.yaml`,
  initially `schemaVersion: 1; entries: []`.
- New `Scripts/semantic_neighbor_terminal_decisions.py` and unit
  tests; **21/21 local positive and adversarial tests passed**.
- The canonical `Scripts/check_semantic_neighbor_governance.py` now
  loads the register fail-closed and refuses any terminal ledger entry
  whose `authorizationReference` does not bind an exact,
  matching `SEM-DEC-` decision record. A generic `RFC-002` label is
  insufficient.
- Existing temporary-checkout retirement tests now supply test-only
  synthetic decisions; an additional mutation denies a followable
  but non-authorizing Request for Comments (RFC) label.
- A malformed `entries` array is rejected before register lookup.
- The static conformance workflow now invokes the new unit test suite.

**Provenance boundary:** a record's `approvedBy` claim and a GitHub
issue-comment-shaped URL are *not* cryptographic proof that the maintainer
actually approved it. The maintainer must control review and confirm
referenced evidence. The checker enforces exact structural binding, not
remote identity authentication.

[Mission 029 details](./BRAPI-GENX-MISSION-029-TERMINAL-APPROVAL-BINDING.md).
The newly integrated full-checkout canonical mutation tests were **not**
executed in this environment.

## 3. Mission 030 — separate typed scientific proposal register

Added a distinct, **empty** candidate store at
`Specification/BrAPI-GenX/Conformance/typed-relationship-candidates.yaml`.
The validator requires `proposal-only` status, two resolvable local
schemas, a distinct relation type, evidence references, authoring context
and unresolved questions. Approved relationship claims, unsafe paths and
unrecognized kinds fail. No existing `semanticNeighborIds` value was
rewritten or upgraded into a typed relationship.

**14/14 synthetic local tests passed**, and the static workflow now
checks the empty register and runs its mutation suite.

[Mission 030 details](./BRAPI-GENX-MISSION-030-TYPED-RELATIONSHIP-PROPOSAL-REGISTER.md).

## 4. GenX `GroupDescription.md` evidence audit and Mission 031

The GitHub tree originally contained **156 GenX group-description files**,
all title-only. Nine groups now have source-backed descriptions with
clear maturity qualifications, responsibilities, and exclusions:

1. Jobs
2. Provenance
3. VariableTerms
4. BreedingPipeline
5. LotLedger
6. Models
7. FAIR
8. Telemetry
9. Genomics

The nine descriptions contain **42** direct relative documentation links.
Each resolved to a tracked file in an independent GitHub tree inspection.
The remaining **147** title-only groups have **not** been filled with
inferred scientific language. Their backlog and editorial review rules
are recorded in [issue #22](https://github.com/denishdholaria/BrAPI-genX/issues/22).

Mission 031 added a targeted regression guard:
`Scripts/check_genx_group_descriptions.py` requires each reviewed
description to preserve its substantial source-cited scope and explicit
candidate/proposal maturity. It deliberately does **not** fail unreviewed
placeholders merely for being empty.

**10/10 local tests passed.**

[Group audit](./BRAPI-GENX-GROUP-DESCRIPTION-EVIDENCE-AUDIT.md) and
[Mission 031 regression-gate report](./BRAPI-GENX-MISSION-031-GROUP-DESCRIPTION-REGRESSION-GATE.md).

## 5. Local verification evidence

All three new isolated local unit suites were rerun on 2026-11-24:

| Test suite | Passed | Git blob identities (checker; test) |
|---|---:|---|
| Terminal approval exact-match guard | 21/21 | `80524bafcd1c198d1303f99e64b06b713c06e733`; `cba2ece4b6bb18613c8737c3d759c27d5fa93e50` |
| Typed relationship proposal-only guard | 14/14 | `2b872b80a2bc3d6264df9c53be29ba9837bc6108`; `238a98f1bd86f07c4d6a020eddb6d37f8b581f35` |
| Group-description provenance guard | 10/10 | `ef237a0b861700792e22c8ba59f96c30d71e7edf`; `49daf500252e13eeec55a997580df53a8e11d75a` |
| **Total** | **45/45** | Byte-matched to committed repository files |

Python compilation passed for all six files. The GitHub repository
tree and static conformance workflow were inspected independently.

**Not executed:** the large full-checkout registry suite, copied-repo
mutation tests, historical Git baseline drift comparison, complete
generated-artifact consistency checks, hosted Continuous Integration
(CI), a persistent reference implementation or an independent scientific
service. GitHub cloning was not available in the isolated container;
connector access does not provide a mountable complete 2.45-megabyte
endpoint registry. The maintainer reports hosted GitHub Actions minutes
unavailable until the anticipated 2026-12-01 reset.

## 6. Preserved invariants and remaining gates

- The **153** historical semantic-neighbor IDs are retained; **51**
  remain `requires-decision` and **102** `inherited-unreviewed`.
- The decision register contains **zero actual approved link retirements**.
  The scientific candidate register contains **zero mapping proposals**.
- No official Breeding Application Programming Interface (BrAPI)
  version 2.1 source, GenX public route or wire contract, scientific
  equivalence, Request for Comments (RFC) maturity, or released artifact
  has been altered by these missions.
- Architectural decisions D-026/D-027 are accepted; specific link
  disposition decisions remain subject to separate evidence.
- Remaining execution dependency: identify a disposable, independent,
  persistent BreedingPipeline test service with two authenticated
  clients and state/effect readback for real Compare-and-Set concurrency
  conformance, tracked in [issue #21](https://github.com/denishdholaria/BrAPI-genX/issues/21).
  The selected *approach* is approved; the target deployment has not
  been identified.
- Document additional GenX groups only after source contracts and
  external overlaps have been reviewed; nine reviewed groups remain
  protected and 147 placeholders deliberately deferred.

**Outcome:** approved architectural boundaries have been expressed in
separate fail-closed governance and proposal gates, while the module
documentation has improved selectively without pretending that
scientific or interoperability drafts are finalized.
