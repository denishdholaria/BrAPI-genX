# Mission 078 — Relatedness matrix and pedigree evidence boundaries

**Prepared parent:** `8548cd8a1b7762a999d0fa16911da1f61986f781` (Mission 077), 2026-11-24.  
**Scope:** source-grounded documentation and guard tests for three `STRUCTURAL_DRAFT` GenX modules. No official Breeding Application Programming Interface (BrAPI) version 2.1 contract, GenX wire schema, endpoint identity, governed relation, registry, maturity or scientific policy change.

## Findings and source evidence

1. **KinshipMatrix** (RFC-052, D-154–D-156): response requires `kinshipMatrixDbId`, `analysisMethodDbId`, and `status`; registration requires the first two. `matrixRef`, `matrixDigest`, `jobDbId`, `studyDbId`, and provenance are all optional. The SHA-256 (Secure Hash Algorithm 256-bit) digest field has no schema-enforced pattern or automatic content check. Sample order, estimator identity/version, relationship scale and matrix dimensions are not defined. D-155's prior description of a GenomicDataset link as optional is inaccurate: no `genomicDatasetDbId` exists in the candidate schema.
2. **GenomicRelationship** (RFC-056, D-166–D-168): response requires `genomicRelationshipDbId`, `analysisMethodDbId`, and `status`; registration requires the first two. `matrixRef`, an opaque `digest`, job, study and provenance remain optional. A payload location cannot demonstrate a verified genomic relationship computation without a sample order, genotype source, relatedness estimator, allele-frequency baseline or reproducible method. D-167 asks about an unmodelled dataset link. GenomicRelationship and KinshipMatrix are not declared equivalent merely because both may reference a matrix.
3. **PedigreeAnalysis** (RFC-060, D-178–D-180): response requires `pedigreeAnalysisDbId`, `analysisMethodDbId`, and `status`; registration requires the first two. `pedigreeMetrics` is an optional untyped object. Neither pedigree source, completeness nor estimand and uncertainty are mandated. Official BrAPI Germplasm resource identities and ancestry remain authoritative. No GenomicDataset linkage is modelled, despite D-179.

## Changes

- Three previously placeholder `GroupDescription.md` files now contain source-linked limitations and explicit draft maturity.
- Three module READMEs and their matching RFCs were qualified to distinguish storage metadata from scientific validity, resource identity, method execution, and cross-method comparison.
- `Scripts/check_genx_group_descriptions.py` now guards **124 of 156** modules on the stacked branch (**32 remain deferred**).
- The existing group-description regression suite contains a source-derived test for required/optional fields, opaque matrix payload identity and pedigree metrics, unmodelled dataset/version linkage, and preservation of official Germplasm.

## Verification and boundaries

All 24 local links across the three new group descriptions resolve in GitHub. This is source-link and static-diff evidence, not execution of the complete Python tests. At minimum, run:

```sh
python Scripts/test_genx_group_descriptions.py
python Scripts/check_genx_group_descriptions.py
python Scripts/checkEndpointRegistry.py
python Scripts/auditEndpointRegistrySourceConsistency.py --strict
python Scripts/generateEndpointArtifacts.py --check
python Scripts/checkGenXConformance.py
```

Do not upgrade maturity, ratify D-154–D-156/D-166–D-168/D-178–D-180, or assert kinship/pedigree/genomic relatedness equivalence based on this documentation review.
