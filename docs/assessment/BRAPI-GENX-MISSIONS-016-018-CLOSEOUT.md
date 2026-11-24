# BrAPI-GenX — Missions 016–018 Engineering Closeout

**Date:** 2026-11-24  
**Starting `main`:** `9fde41015d18e12d915faace493a3cb3dc024261`  
**Final inspected implementation:** `c9f6b5a42d5884a5406cfbfda2fe469f444decc4`  
**Scope:** non-normative semantic-neighbor governance safety, regression tests and an architectural decision package.

## Mission 016 — Terminal publication consistency

[First implementation commit](https://github.com/denishdholaria/BrAPI-genX/commit/036c7934c4788d60c23ed95df39f81cbadd56cf1)
and [test-byte alignment commit](https://github.com/denishdholaria/BrAPI-genX/commit/bc2104416e120653d9d997da34eaea3f42e856ba).

The original governance system allowed inconsistent metadata: a link could be
declared `rejected` or `superseded` but still advertised in the active
endpoint registry's `semanticNeighborIds`. The canonical validator now
checks the current (source catalogue identity, target operation identity)
pairs and rejects that contradiction.

The pure guard lives in `Scripts/semantic_neighbor_lineage.py`. The
existing `Scripts/test_semantic_neighbor_lineage.py` has 17 tests
(11 previous plus 6 positive/mutation tests for this invariant).
**17/17 passed locally**. The exact tested Git object identities are:

- module `3bc9f3d575ee9cc97f63bffd3511cc12c89ed3f3`;
- tests `4ff20db1c98e5f74f4a50e2efe021f2edb06e769`.

This guard is a consistency rule, not an actual rejection, supersession,
authorization or scientific identity mapping.

## Mission 017 — Canonical cross-file retirement test fixtures

[Commit](https://github.com/denishdholaria/BrAPI-genX/commit/ecbfbcb1bd9f06738e7da3a100d9ba7f43b8507b).

Three mutations were added to the existing full-checkout governance suite:

1. Terminal `rejected` but still advertised by the same source: expected
   failure with an explicit publication-consistency error.
2. Terminal disposition plus active-registry removal and retained ledger
   record: expected structural success.
3. Registry removal without terminal disposition: expected failure.

Each mutation runs against a copied checkout and an explicit before-change
ledger to exercise the actual source audit, registry and canonical validator.

**These three tests have not been executed in this session.** The test suite
requires the full repository including the large endpoint registry and
historical source files. The isolated helper-unit tests above do not replace
this integration verification.

A synthetic `authorizationReference` in the success fixture is
intentionally only a structurally followable string; it is **not** proof
of real maintainer approval. The remaining authorization-proof weakness
is now separately tracked in [issue #20](https://github.com/denishdholaria/BrAPI-genX/issues/20).

## Mission 018 — Typed relationship architecture proposal

[Commit](https://github.com/denishdholaria/BrAPI-genX/commit/c9f6b5a42d5884a5406cfbfda2fe469f444decc4).

[Decision package](./BRAPI-GENX-MISSION-018-SEMANTIC-RELATIONSHIP-ARCHITECTURE-PROPOSAL.md)
documents why operation navigation, typed resource references, proven
derivation, complete contract equivalence and governed overlap are not
interchangeable kinds of relationships.

It evaluates three alternatives and **recommends, but does not ratify,**
separating weak navigation hints from independently verified typed
scientific relationships. Proposed shadow metadata and a staged,
reversible compatibility migration remain explicitly contingent on
maintainer approval. [Issue #17](https://github.com/denishdholaria/BrAPI-genX/issues/17)
contains the current evidence and recommended decision.

## Actual locally executed verification and repository inspection

On 2026-11-24, the following isolated local suites were rerun with success:

| Local suite | Passing tests | Evidence |
|---|---:|---|
| Mission 013 registry-only per-edge drift detection | 13 | `/mnt/data/brapigenx_mission013` |
| Mission 014 historical-provenance classifier | 11 | `/mnt/data/brapigenx_mission014` |
| Mission 015 live review-queue reporter | 12 | `/mnt/data/brapigenx_mission015` |
| Mission 016 terminal publication guard | 17 | `/mnt/data/brapigenx_mission016` |
| **Total** | **53** | Isolated/unit test evidence; not full repository integration |

Also compiled the Mission 016 Python modules with
`python -m py_compile`. The GitHub connector independently confirmed
the committed Mission 016 helper/test blob hashes match those tested
locally byte-for-byte.

A separate current GitHub ledger read confirmed **153 unique retained
identities**, of which **51** are `requires-decision` and **102** remain
`inherited-unreviewed`. No ledger identities or active registry links
were added, removed or reclassified by these missions.

**Not executed:** the actual complete repository's full governance suite,
three new integration tests, historic Git worktree baseline-drift gate,
endpoint-artifact generation check, reference server, independent consumer
or hosted GitHub Actions Continuous Integration (CI). The maintainer
reports the monthly hosted minutes budget exhausted until its expected
reset on 2026-12-01. No hosted-pass claim is made.

## Authority and handoff

- No official Breeding API (BrAPI) version 2.1 source contract,
  GenX public route, wire schema or Request for Comments (RFC)
  maturity status changed.
- Terminal link removal requires explicit maintainer authority and
  proof tied to the exact relationship; a syntactically followable
  authorization string is insufficient real-world evidence.
- A machine-readable relationship taxonomy is **only a proposed design**.
  Do not automatically rewrite catalogue fields or infer scientific
  relationships from source operation names.
- **Next bounded non-policy task:** run the three new repository-level
  mutations in a full checkout and fix any actual discrepancies.
  The existing full semantic-neighbor governance and source/registry
  drift checks are required before claiming conformance.
- **Next maintainer hinge:** choose the legacy `semanticNeighborIds`
  interpretation and exact authorization-evidence scheme
  (issues #17 and #20).
- **Parallel technical track:** RFC-154 (Request for Comments 154)
  BreedingPipeline behavioral conformance for immutable revision
  concurrency, authority checks and quantitative target semantics.

**Milestone:** cross-file publication consistency has a tested
isolated guard and committed integration mutations; a clear,
non-normative scientific-relationship architecture decision package
is ready for review. Full behavioral conformance remains unverified.
