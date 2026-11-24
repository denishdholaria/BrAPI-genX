# Mission 014 — Historical Semantic-Neighbor Retirement Safety

**Date:** 2026-11-24  
**Parent `main`:** `2b5f033f316a9da6345d1041e742f0b809a90fae`  
**Authority:** existing original 153 semantic-neighbor ledger IDs and the
project's maintainer-governed terminal decisions.

## Defect

The canonical semantic-neighbor validator previously decided whether a
relationship was historically inherited **solely by comparing it with the
current** registry-only operation-neighbor set. After an otherwise
authorized `rejected`/ `superseded` decision removed an invalid link
from the registry, its immutable ledger record became absent from that
current set and was incorrectly categorized as a **new, invented**
relationship. The validator then prohibited its original
`inherited-registry-only` provenance, making honest historical retention
and cleanup mutually contradictory.

Mission 013 repaired the companion drift gate to allow partial removal.
This mission corrects the canonical governance classification separately.

## Implementation

Extracted a small pure provenance classifier into
`Scripts/semantic_neighbor_lineage.py`. Given an entry, the set of
current registry-only pairs, and the **existing pinned baseline of original
153 IDs**, it makes the following distinctions:

- A relationship still in the current inherited set passes lineage
  classification (other validators still review statuses and links).
- An **original baseline ID** absent from the active registry requires the
  reviewed terminal status `rejected` or `superseded`. It retains its
  original inherited provenance and immutable ledger ID.
- A genuinely new non-inherited relationship still cannot claim
  `inherited-unreviewed` status or reuse `inherited-registry-only`
  provenance, and must have a nonempty rationale.

**Crucial:** the helper does **not** authorize terminal status. The canonical
validator still checks `authorizationReference`, legal status transitions,
rationale, successor resolution for `superseded`, registry consistency,
canonical IDs, and all original IDs' retention.

The standard conformance workflow now runs
`Scripts/test_semantic_neighbor_lineage.py` and watches changes to both
new scripts. The actual current ledger and registry are unchanged.

## Verification

Executed against the exact helper and test content in an isolated local
Python environment:

```sh
cd /mnt/data/brapigenx_mission014
python -m unittest -v test_semantic_neighbor_lineage.py
python -m py_compile semantic_neighbor_lineage.py test_semantic_neighbor_lineage.py
```

**11/11 tests passed.** They cover retention, an authorized-terminal-state
shape after registry removal, removal without terminal status, genuinely new
relationships spoofing inherited provenance, unknown rationale types, and
documented non-inherited relationships. The helper deliberately defers
authorization enforcement to the canonical validator.

**Not yet verified:** integration against the full historical Git checkout,
the original 153-entry ledger validator, or an independently implemented
service. A real terminal disposition must not be enacted until maintainer
approval is recorded. Hosted GitHub Actions remain blocked by the reported
monthly minutes budget until the anticipated 2026-12-01 reset.

## Preservation

No official Breeding API (BrAPI) version 2.1 contract, GenX public route,
wire schema, registry edge, ledger ID, or Request for Comments (RFC) maturity
was changed. This is governance infrastructure only.
