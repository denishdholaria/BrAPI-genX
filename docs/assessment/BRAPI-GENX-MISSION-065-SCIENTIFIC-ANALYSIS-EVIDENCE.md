# Mission 065 — Analysis method and numerical-result evidence boundaries

**Prepared parent:** `9671f592b6aaa12797e8396c37e84d7fba67f910`.
**Scope:** four source-backed group descriptions, review pinning and regression test.

- AnalysisMethod is a candidate immutable method/version registry, but optional input/output contracts and implementation references do not by themselves provide executable science, verified repeatability or enforced revocation.
- AnalysisResult requires an analysisMethodDbId but does not require the exact methodVersion or job link; resultData and uncertainty remain optional objects.
- MixedModelResult has optional untyped varianceComponents and blupValues; genetic covariance assumptions, genotype reference identities, uncertainty and trait scales are not constrained.
- PcaResult has optional component and explainedVariance objects with no specified scores/loadings axis, normalization or model provenance.

All four remain STRUCTURAL_DRAFT; the decisions D-24–26, D-133–135, D-142–144 and D-157–159 remain open. No scientific validation, independent service conformance, normative approval, route, OpenAPI schema or official BrAPI v2.1 contract is modified.

Verification: checked all direct relative evidence links against the prepared-parent tree; regression checks added to the existing group-description test suite. Hosted workflows must pass on integrated commit before full verification is claimed.
