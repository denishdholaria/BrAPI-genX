# Mission 094 — Parent candidacy versus selection verdict authority

**Parent:** Mission 093 branch head `4a5c8705b6282f20e9aea87b3537ecab8ea80917`. **Scope:** evidence review only, not a new or approved breeding-operations specification.

## Contract comparison

| Dimension | ParentCandidateSelection (RFC-028) | SelectionDecision (RFC-008) |
|---|---|---|
| Required verdict | Boolean `selected` | `decision` enum: selected/rejected/deferred/advanced |
| Required context | Raw string `programDbId` and `candidateGermplasmDbId` | Authority-qualified `programReference`; candidate reference optional |
| Required chronology | None | `decisionDate` in date format |
| Required person, rationale, evidence | None | None |
| Required response lifecycle `status` | Yes | No |
| Typed reciprocal link | None | None |

The ParentCandidateSelection draft previously claimed a *currently optional* link to SelectionDecision in D-83. It has **no link at all**. Parent-specific Boolean `false` cannot be mapped losslessly to rejected versus deferred or other general selection states. Conversely, the broader verdict may omit a candidate Germplasm, so it is not automatically a parent-candidate outcome.

Official Breeding Application Programming Interface (BrAPI) version 2.1 PlannedCross and Cross schemas already model parents and parent role through CrossParent. A candidate selection is neither a PlannedCross nor a performed cross; no decision authorizes a pollination automatically. BreedingPipeline schemes describe process definitions; they do not establish that a candidate verdict was authorized.

## Provenance, authority and open governance

The richer SelectionDecision resource has required `programReference` with explicit issuing-server context, but optional decision-maker identity, linked Observations, rationale, candidate and provenance. The ParentCandidateSelection raw Program/Germplasm strings do not include issuing-server context. Neither establishes cross-server authorization or mandatory evidence review.

D-81–D-83 and RFC-008-Q1–Q3 remain unresolved. No relationship, automatic mapping, replacement, deletion, synchronization, scientific maturity or production conformance is approved.

## Changes and verification

- Two title-only GroupDescriptions replaced; two module overviews and RFC-028/RFC-008 corrected; source-derived tests protect the differing requiredness, authority fields, official Cross parent semantics and missing relationship.
- Expected reviewed descriptions: **149/156** and 7 deferred, conditional on integration after Mission 093.
- No official BrAPI version 2.1 source, GenX wire schema, endpoint registry, operation identity or maturity register is modified.

```sh
python Scripts/check_genx_group_descriptions.py
python Scripts/test_genx_group_descriptions.py
python Scripts/report_genx_evidence_coverage.py --check
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Hosted static conformance, live reference conformance and specification generation must succeed on the final PR head; this assessment does not assert that they already passed.
