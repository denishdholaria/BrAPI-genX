# BrAPI-GenX — Missions 013–015 Engineering Closeout

**Date:** 2026-11-24  
**Starting `main`:** `8d3e6840ae4522734440b46f8b779c13a47033a3`  
**Verified final implementation commit:** `f06a4f2133ae12ef3fc1d197dea1f8e82c8ddd95`  
**Status:** source-history root-cause investigation and three bounded engineering deliverables committed to `main`. Tests are isolated/local; hosted checks and full-repository suites are pending.

## Mission 013 — Explain the inherited neighbor concentration; allow safe drift remediation

**Commit:** [`2b5f033f316a9da6345d1041e742f0b809a90fae`](https://github.com/denishdholaria/BrAPI-genX/commit/2b5f033f316a9da6345d1041e742f0b809a90fae).

- Identified Git history showing direct historical additions of questionable registry-only cross-module neighbors in individual 2026-11-02 module-creation commits. The checked-in documentation generator reads the registry and renders its relationship metadata; it does not establish biological equivalence.
- Did **not** determine the specific generator template, authoring agent or decision process that chose those targets. The common repeated third-neighbor pattern is evidence for a templating **hypothesis**, not verified causation.
- Fixed `Scripts/check_registry_drift_regression.py`: old regression logic compared entire `registryOnlyNeighbors` arrays atomically, falsely treating removal of one existing bad link as newly introduced drift. Comparison is now per `catalogId`, `module`, `neighbor` edge with multiset cardinality and malformed-input checks.
- **13 isolated regression tests passed**. Actual local bytes match the committed Git blobs:
  - Checker: `f97e8431fa6a9bd15969c6fd2f91e05561b11bc7`
  - Test: `5bb93bc4f8075ed2c8559d4d2d2c94afe7ae3eb5`

[Root-cause analysis](./BRAPI-GENX-MISSION-013-REGISTRY-NEIGHBOR-ROOT-CAUSE.md).

## Mission 014 — Retain lineage through a future authorized rejection or supersession

**Commit:** [`89a3b5dda27887908ec80a4eacb000ee060b0290`](https://github.com/denishdholaria/BrAPI-genX/commit/89a3b5dda27887908ec80a4eacb000ee060b0290).

- Corrected canonical validator classification: an original baseline ledger ID does not become a **new** relationship merely because its active registry-only link was subsequently removed.
- Original IDs absent from current registry are permitted to retain their immutable historical provenance only with terminal `rejected` or `superseded` status. Existing canonical authorization, transition, successor, evidence and completeness checks remain in effect.
- Truly new relationships cannot borrow `inherited-unreviewed` or `inherited-registry-only` to evade scrutiny.
- New pure helper `Scripts/semantic_neighbor_lineage.py` plus **11 isolated positive/mutation tests passed**; the full canonical validator was **not** run against a historical full checkout.
- Both tested files were verified byte-identical to Git blobs:
  - Helper: `835d481b98d40739e6a59faf35008de55265b7ec`
  - Test: `b12c12d9a6d2d2c0f09d0e0300b3417904629f87`.

[Lineage-retirement assessment](./BRAPI-GENX-MISSION-014-HISTORICAL-NEIGHBOR-LINEAGE.md).

## Mission 015 — Stop relying on a stale review-queue snapshot

**Commit:** [`f06a4f2133ae12ef3fc1d197dea1f8e82c8ddd95`](https://github.com/denishdholaria/BrAPI-genX/commit/f06a4f2133ae12ef3fc1d197dea1f8e82c8ddd95).

- Added a read-only live ledger reporter with Markdown, `--json`, and `--check` output modes, reflecting **actual** per-source/per-target review status.
- Mixed reviewed/unreviewed groups remain visible and every count clearly distinguishes triage from scientific acceptance.
- Prevents silent reliance on the pinned 2026-11-23 markdown snapshot by pointing readers to the new command.
- **12 isolated local tests passed**; committed Git blobs match:
  - Reporter: `e0cfdcc8166cd54f1496f2f50622ec176644cacb`
  - Test: `1228f4c4b397822f5842e1f180e14516fba684d2`.
- Static conformance workflow now watches both scripts and runs the live inventory `--check` and its tests. Hosted execution remains pending.

[Live queue report design](./BRAPI-GENX-MISSION-015-LIVE-REVIEW-QUEUE.md).

## Repository-backed status inspection after integration

The current GitHub ledger, source-tracked file tree and status inventory were inspected through the GitHub connector after commit `f06a4f2`:

| Measure | Verified observed count |
|---|---:|
| Original relationship identities retained | 153 |
| Distinct ledger IDs | 153 |
| Source-module/target-operation groups | 51 |
| Groups with links still unreviewed | 34 |
| `requires-decision` links | 51 |
| `inherited-unreviewed` links | 102 |
| Links to `genxRegisterGenomicDataset` | 120 |
| Of those genomic target links, unreviewed | 99 |
| Normatively accepted or rejected by these missions | 0 |

This independent repository data inspection is distinct from running
`report_semantic_neighbor_inventory.py` on the *full checked-out repository*;
the latter was **not** executed in the current environment.

## Actually executed local verification

All tests were executed in isolated local copies of the corresponding
source modules, with byte-for-byte Git blob verification on the committed
files. Commands used:

```sh
cd /mnt/data/brapigenx_mission013
python -m unittest -v test_registry_drift_regression.py
python -m py_compile check_registry_drift_regression.py test_registry_drift_regression.py

cd /mnt/data/brapigenx_mission014
python -m unittest -v test_semantic_neighbor_lineage.py
python -m py_compile semantic_neighbor_lineage.py test_semantic_neighbor_lineage.py

cd /mnt/data/brapigenx_mission015
python -m unittest -v test_semantic_neighbor_inventory.py
python -m py_compile report_semantic_neighbor_inventory.py test_semantic_neighbor_inventory.py
```

**36/36 local tests passed** across the three missions. This is
**not** a claim that the entire endpoint registry, historical baseline
worktree, canonical 153-entry ledger validator, full repository conformance
suite or an independent scientific service has been tested end to end.

## Scope, governance and next actions

- No modification to official Breeding API (BrAPI) version 2.1 sources,
  GenX public wire schemas/routes, 153 active registry neighbor edges, or
  Request for Comments (RFC) maturity decisions.
- The user reports the GitHub Actions monthly minutes budget exhausted,
  with an expected reset on **2026-12-01**. Hosted Continuous Integration
  (CI) must be rerun after the actual budget reset; do not treat pre-job
  failures as test regressions.
- The historical drift cleanup path is now structurally improved **but no
  actual scientific-policy rejection was authorized or performed**.
- **Next scientific governance hinge:** define what `semanticNeighborIds`
  is intended to mean: operation-level discovery, typed scientific resource
  relationships, or editorial navigation. Do not infer scientific
  equivalence from an operation-neighbor association.
- Maintainer questions and this new evidence are tracked in
  [GitHub issue #17](https://github.com/denishdholaria/BrAPI-genX/issues/17).
- The next independent conformance track remains RFC-154:
  authenticated authority resolution, target Scale validation, immutable
  revision compare-and-set races, and provenance/lifecycle auditing.
  Static fixtures alone cannot establish the behavioral guarantees.

**Milestone:** the actual introduction point of suspicious links is
documented, two blockers to safe authorized cleanup are corrected, and
the remaining review queue is available from live ledger status rather
than historical documentation snapshots.
