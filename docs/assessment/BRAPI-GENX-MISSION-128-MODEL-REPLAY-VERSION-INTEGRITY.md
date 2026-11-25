# Mission 128 — Model replay version integrity

**Status:** implemented; required hosted verification pending.  
**Scope:** registered probe L-12, runner assertion, regression tests and
conformance documentation.  
**Dependencies:** Missions 126–127.  
**Official BrAPI 2.1 and GenX wire-schema changes:** none.

## Defect

L-12 asserted matching model identifiers and versions returned by two
identical registrations. An implementation could return the same identity
while appending an additional version or silently changing the original
model's artifact, training-data digest, metrics, or provenance.

## Implementation

L-12 reads GET `/models?modelDbId={modelDbId}` after replay.
The runner requires HTTP 200, exactly one original version,
complete single-page pagination, and equality of all originally submitted
fields, including nested metrics and provenance. The request's initial
modelDbId/modelVersion baseline must match the response identity.
Server-managed additional fields may coexist.

The postcondition uses the same localized collection helper introduced
for variant matrices and FAIR packages. The registered manifest requires
`model_replay_single_version` on the filtered GET. Hosted static conformance
executes `Scripts/test_model_replay_version_integrity.py` and the
workflow-scope guard requires it to remain registered.

## Verification commands

```bash
python Scripts/test_model_replay_version_integrity.py
python Scripts/test_conformance_assertion_manifest.py
python Scripts/test_conformance_workflow_scope.py
python Scripts/checkGenXConformance.py
```

Static and live reference, independent cross-runtime conformance and
specification-generation workflows must all pass before merge.

## Boundaries

This proves a synthetic reference-server model has one visible unchanged
version after replay. It does not prove persistent database uniqueness,
distributed transactions, immutable artifact bytes, the scientific validity
of model metrics, security policies, or external certification. No scientific
maturity promotion is requested.
