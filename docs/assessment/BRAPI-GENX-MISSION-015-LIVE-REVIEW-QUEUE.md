# Mission 015 — Live Semantic-Neighbor Work Queue

**Date:** 2026-11-24  
**Baseline `main`:** `89a3b5dda27887908ec80a4eacb000ee060b0290`  
**Purpose:** replace misleading reliance on the Mission 006 pinned inventory
with deterministic read-only status reporting. The authoritative data remains
`Specification/BrAPI-GenX/Conformance/semantic-neighbor-review.yaml`.

## Deliverables

- `Scripts/report_semantic_neighbor_inventory.py` reads the current ledger and
  produces Markdown by default, full deterministic `--json`, or read-only
  concise `--check`. It groups by actual `(sourceModule, targetOperationId)`,
  not by guessed scientific equivalence. The queue retains partially reviewed
  groups and distinguishes total links from unreviewed link counts.
- Fail-closed validation of missing/duplicate IDs, unknown review states,
  malformed entries, and incorrect declared `entry_count`.
- `Scripts/test_semantic_neighbor_inventory.py`: **12 isolated local
  unit/mutation tests** including mixed-status group handling, order
  independence, malformed data, and read-only command behavior.
- Static conformance workflow integration for `--check` and the tests.
- Updated the Mission 006 snapshot heading to link users to the live
  command rather than silently presenting obsolete counts.

## Expected current context

At the inspected baseline the original 153 links remain, with
**51 requires-decision** and **102 inherited-unreviewed**. This assessment
does not freeze those numbers as invariants: the script reports whatever
valid statuses the ledger contains in subsequent commits.

The command's `reviewedOrDecisionPending` count includes
`requires-decision`, `evidence-backed-proposed`, `rejected` and
`superseded`, and is **not** a claim that any relationship is scientifically
accepted or normatively specified.

## Actual verification and limitations

Local isolated execution:

```sh
cd /mnt/data/brapigenx_mission015
python -m unittest -v test_semantic_neighbor_inventory.py
python -m py_compile report_semantic_neighbor_inventory.py test_semantic_neighbor_inventory.py
```

**12/12 tests passed**, plus Python compilation; the locally tested files
are compared to their committed Git object hashes after the commit.
A separate full repository checkout with 153 real entries and the hosted
workflows have **not** been executed in this session. Hosted GitHub Actions
minutes remain unavailable until the maintainer-reported reset on 2026-12-01.

No change to official Breeding API (BrAPI) version 2.1 source contracts,
public GenX schemas, endpoint registry relationships, or Request for Comments
(RFC) statuses. No scientific or terminal decision is inferred by a count.
