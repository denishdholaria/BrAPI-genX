# BrAPI-GenX — Missions 011–012 Autonomous Engineering Closeout

**Date:** 2026-11-24  
**Starting `main`:** `52f3237d77572896b6571dd37db6996233304f31`  
**Last inspected implementation commit:** `68abc0e7b528bb1d51dccb531a18b327dc94ff2f`  
**Status:** two bounded engineering slices integrated into `main`. Source-contract review and isolated tests only, no normative acceptance.

## Mission 011 — Eliminate false rejection of later governance review states

**Commit:** [`5a84edd83b6c4feae53ae2a04bba889aef00feef`](https://github.com/denishdholaria/BrAPI-genX/commit/5a84edd83b6c4feae53ae2a04bba889aef00feef).

`Scripts/check_scientific_contract_boundaries.py` previously failed when a
reviewed link advanced from `requires-decision` to any later allowed status.
The checker now regards `requires-decision`, `evidence-backed-proposed`,
`rejected`, and `superseded` as reviewed statuses, while rejecting regression
to `inherited-unreviewed` and unknown statuses.

**Safety boundary:** this auxiliary checker does not authorize a rejected or
superseded status; the canonical
`Scripts/check_semantic_neighbor_governance.py` retains authority
reference requirements and legal transition enforcement. Assessment citations,
three-operation group identity and source-schema field checks remain enforced.

Three tests were added to the previous twelve. Local isolated execution:

```sh
cd /mnt/data/brapigenx_mission011
python -m unittest -v test_scientific_contract_boundaries.py
python -m py_compile check_scientific_contract_boundaries.py test_scientific_contract_boundaries.py
```

**Result: 15/15 tests passed**, Python compilation passed.
The GitHub connector independently confirmed that committed script blob hashes
matched the locally tested byte content:

- checker: `2ebe01427776451eb7698598952407749e1de35b`;
- tests: `74cfb1a71fe109eca8bea229331b3e2d258363bb`.

**Not claimed:** the full repository conformance suite, canonical validator
execution, independently observed runtime behavior, or hosted validation.

## Mission 012 — Source-contract triage of field experiments and capture

**Commit:** [`68abc0e7b528bb1d51dccb531a18b327dc94ff2f`](https://github.com/denishdholaria/BrAPI-genX/commit/68abc0e7b528bb1d51dccb531a18b327dc94ff2f).

Five source/target groups were reviewed against existing schemas, including
official BrAPI data ownership considerations:

| Inherited group | Scientific boundary requiring clarification |
|---|---|
| Farm → CropCycle | A farm/site and a seasonal crop episode are distinct; authoritative Location membership and timing remain unspecified |
| Plot → FieldScouting | Plot identity and field-level notes differ; use official ObservationUnit identity where the underlying fact is an experimental unit |
| TrialNetwork → FieldScouting | Multi-environment trial organization is not an actual scouting observation; Trial/Study/Location authority remains separate |
| TreatmentAssignment → FieldScouting | Assigned treatment, actual application and observed exposure/response are distinct scientific facts |
| CaptureWorkflow → VariableTerms | Data-capture workflow and a versioned observation-variable definition have separate lifecycles |

[Detailed assessment and five open questions](./BRAPI-GENX-MISSION-012-FIELD-EXPERIMENT-NEIGHBOR-REVIEW.md).
[Maintainer decision issue #19](https://github.com/denishdholaria/BrAPI-genX/issues/19).

Each of the 15 source-operation-level references was moved from
`inherited-unreviewed` to `requires-decision` with specific rationale,
open question, source schema, target schema and assessment path.

### Repository-backed verification performed

After the commit, the GitHub repository tree and the current and baseline
governance ledgers were compared independently:

- **153** original stable IDs retained with **153 unique IDs**;
- exactly **15** changes, each `inherited-unreviewed → requires-decision`;
- no other status transitions or new/deleted relationship IDs;
- all **51 reviewed entries** have nonempty rationale and open question,
  existing source-schema paths, existing target-schema paths, and tracked
  assessment document paths;
- all five new source modules match the planned batch.

No script execution against the full checked-out repository was performed
for this ledger audit; the comparison was of connector-returned repository
bytes and tree objects. The separate 15 local tests above cover the
isolated evidence gate, not a deployed service.

## Resulting governance inventory

| Status | Count |
|---|---:|
| `requires-decision` | 51 |
| `inherited-unreviewed` | 102 |
| Total original links | 153 |
| Normatively approved or terminally rejected in Missions 011–012 | 0 |

The existing 51 source-module/target-operation group inventory remains the
scientific review work queue, not evidence of an accepted data model.

## Preservation, dependencies and next logical work

- Official Breeding API (BrAPI) version 2.1 sources are unchanged.
- GenX public routes, operation identifiers, production data models, endpoint
  registry associations and maturity statuses are unchanged.
- The changes do not endorse semantically equivalent operations, infer causal
  relationships, or approve scientific policy.
- Hosted Continuous Integration (CI) is not available because the maintainer
  reports an exhausted monthly GitHub Actions minutes budget, expected to
  reset **2026-12-01**. Rerun all repository checks once available.
- Continue bounded review of the **102** inherited-unreviewed relationships
  with source-schema evidence and specific falsifiable science claims.
- Preserve a separate RFC-154 (Request for Comments 154) track for
  independent-service compare-and-set concurrency, publication/withdrawal
  authorization and validated quantitative Scale evidence; do not promote
  its normative maturity on static fixtures alone.

**Milestone boundary:** one incorrectly strict regression condition fixed,
15 local tests passed, 15 scientifically distinct operation-neighbor records
audited and traceably advanced. Scientific decisions and deployment
conformance remain open.
