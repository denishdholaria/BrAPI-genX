# Mission 032 — Correct misleading generated semantic-neighbor labels

**Date:** 2026-11-24  
**Starting `main`:** `801bfa7d4dbe2c04548f09fa732e7c09d472559d`  
**Decision basis:** accepted internal D-026, not a new official BrAPI (Breeding API) standard.

## Problem

The canonical generator rendered historical `semanticNeighborIds` as
"Semantic relationship IDs / labels", inviting readers or automated agents
to mistake advisory operation navigation for a verified scientific link.
At the starting revision the master endpoint catalogue had 562 such labels;
the GenX focused catalogue had 462. Both labels are generated from the
unchanged registry. Misrepresentation affects interpretation of contracts.

## Remediation

- Relabel the affected rendered fields as advisory operation neighbors and
  related catalogue IDs with an explicit advisory qualification.
- Add text to both generated catalogue preambles that navigation alone does
  not establish scientific equivalence, common authority, or permission to
  invoke a related operation.
- Regenerate the two affected Markdown artifacts **atomically** with the
  generator change. The BijMantra crosswalk and registry are unchanged.
- Add six focused positive/negative regression cases under
  `Scripts/test_generated_advisory_navigation.py`; enable the test in the
  static conformance workflow.

## Constraints

No `semanticNeighborIds` value, historical ledger entry, OpenAPI route,
schema, decision status, or official BrAPI version 2.1 source is rewritten.
The separate governed `semanticRelationships` block remains intact and
retains its own risk/status labels. This is a corrective presentation update,
not approval of any existing scientific mapping.

## Verification

At preparation, source-level assertions confirmed each existing label's
exact count (master 562, focused 462) before replacement. The full
`python Scripts/generateEndpointArtifacts.py --check` and the newly
introduced regression tests must pass in hosted GitHub Actions on the
resulting `main`. Do not claim green until those runs finish.
