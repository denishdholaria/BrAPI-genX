# Mission 016 — Terminal Semantic-Neighbor Publication Consistency

**Date:** 2026-11-24
**Starting main:** `9fde41015d18e12d915faace493a3cb3dc024261`
**Disposition:** governance consistency hardening only, not a normative scientific mapping decision.

## Concrete defect

The canonical semantic-neighbor validator already requires an authorized
terminal status to retire a grandfathered registry-only neighbor.
However, the opposite inconsistency remained possible: an entry marked
`rejected` or `superseded` could still be published under the source's
active `semanticNeighborIds`. That would mislead a consumer treating the
registry as a navigable catalogue.

## Change

- Extended the existing pure lineage module with
  `terminal_publication_errors(entry, active_neighbors)` to reject a
  terminal ledger disposition that is still published as a live edge.
- Integrated the check into the canonical governance validator, reading
  active (source catalogue ID, target operation ID) pairs from the current
  registry.
- Kept authorization, legal status transitions, successor resolution,
  original 153-ID retention and archive provenance checks unchanged.
- Preserved all active registry links and all current ledger statuses;
  no scientific or normative decision is inferred.

An approved later retirement must update the ledger and registry consistently,
preserving historical identity and carrying maintainer authorization.

## Actual verification

Ran the exact module and tests in the isolated local environment
`/mnt/data/brapigenx_mission016`:

```sh
python test_semantic_neighbor_lineage.py -v
python -m py_compile semantic_neighbor_lineage.py test_semantic_neighbor_lineage.py
```

**17 of 17 tests passed.** Six new cases exercise rejected and superseded
links still published, properly withdrawn terminal links, active nonterminal
links, unrelated sources, and the authorization boundary.

Git object hashes from the tested local files (to match after commit):

- `Scripts/semantic_neighbor_lineage.py` — `3bc9f3d575ee9cc97f63bffd3511cc12c89ed3f3`
- `Scripts/test_semantic_neighbor_lineage.py` — `4ff20db1c98e5f74f4a50e2efe021f2edb06e769`

This is an isolated unit test run, **not** the full repository governance
suite, its historical baseline-checkout verification, or a hosted Continuous
Integration (CI) run. Hosted checks remain blocked by the maintainer-reported
GitHub Actions monthly minutes budget.

No official Breeding API (BrAPI) version 2.1 contract, GenX wire schema,
endpoint identifier, active semantic link, or Request for Comments (RFC)
maturity was changed.
