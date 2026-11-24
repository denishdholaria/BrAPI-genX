# Mission 010 — RFC-154 Candidate Query-Parameter Identity Assurance

**Date:** 2026-11-24  
**Inspected baseline:** `a974f83c8689b681dee39df895d362afe585aec4`  
**Status:** bounded static conformance hardening; **no new normative policy**.

## Concrete defect and safety impact

The existing `Scripts/check_breeding_pipeline_api_contract.py` converts
OpenAPI (Open Application Programming Interface) list endpoint parameters
into a dictionary keyed by `name` via `parameter_map`.
If a wire contract inadvertently defines the same query parameter twice, the
dictionary retains only the last declaration and the existing authority-pair
checks could pass without detecting the ambiguous duplicate.

That is especially consequential for the authority-qualified filters in
`PopulationAdvancement` and `SelectionDecisions`, where `programDbId`
must be paired with `programServer`, and analogous study, population and
germplasm references must not be resolved by guesswork.

## Implemented scope

- Added `require_unique_parameter_names` in the existing BreedingPipeline
  source contract checker, before any parameter-map deduplication.
- It rejects duplicate explicit `(in, name)` combinations and duplicate
  parameter `$ref` declarations, while preserving identically named
  parameters in *different* locations (for example, path and query).
- Applied to PopulationAdvancement GET and SelectionDecisions GET filter
  parameter lists. Other routes are not covered by this bounded fix.
- Added six isolated mutation/positive tests in
  `Scripts/test_breeding_pipeline_parameter_duplicates.py`.
- Integrated those tests into both current GitHub Actions validation workflows,
  subject to the maintainer-reported monthly minutes limit.

## Verification boundary

Six local tests of a byte-identical extracted helper implementation passed
against synthetic parameter lists on 2026-11-24. This is **helper-unit evidence**,
not proof that the full checker or service has passed. The two checked-in
operation YAML (YAML Ain't Markup Language) sources were also inspected through
the repository connector and their explicit parameter names were unique at the
inspected commit.

**Pending:** execute `python Scripts/check_breeding_pipeline_api_contract.py`,
`python Scripts/test_breeding_pipeline_parameter_duplicates.py` and the
complete source/fixture/registry verification suite from a checked-out
repository. Hosted workflows are blocked until the reported December 1 budget
reset, and an independent implementation is still required for behavioral
conformance.

The schema layout, operation IDs, routes, governance decisions, RFC maturity,
CAS (Compare-and-Set) concurrency profile and official BrAPI v2.1 source files
remain unchanged. The broader RFC-154 authority, lifecycle-security, target
Scale validation and independent concurrency gates remain open.
