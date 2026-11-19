# BGX-P1-06 — Contract Quality Follow-on

**Base:** `d739774c7a05bf37ea613b1f00bebd98c4a39f53`
**Branch:** `bgx-p1-06-contract-quality`
**Status:** Candidate engineering work only. RFC-154 remains non-normative. This follow-on also defines a per-target immutable Scale-validation evidence model and its independent-service acceptance plan without adding a new public endpoint.

## Scope
Refine the BreedingPipeline target-scale and authority-reference contract without selecting a production identity provider, permission-token vocabulary, trust registry, or server implementation.

1. Add explicit fixture validation for BrAPI authority base-URI syntax invariants that are safely testable without network access.
2. Add fixture evidence for target-scale validation rules that are independent of a live authority lookup: numeric target requires ObservationVariable; exact decimal syntax; reject impossible locally evidenced scale metadata only if represented as fixture evidence. Do not fabricate Scale fields inside the pipeline contract.
3. Clarify the candidate lifecycle boundary: drafts may carry unresolved scale references only under an explicit unverified state/representation; publication requires successful resolution and validation against ObservationVariable's numerical Scale. Keep this proposal unratified.
4. Keep network trust/dereferencing, DNS rebinding, redirect policy, HTTPS-only production profile, provider and onboarding decisions open.
5. Define immutable evidence binding to pipeline revision + target context + target requirement index; define the JCS preimage while leaving the cryptographic hash algorithm open under D-02.
6. Check category-governed Numerical Scale values against permitted decimal category values as an explicitly unratified candidate rule.
7. Keep the evidence record identity, wire link, endpoint/storage representation and retention as maintainer decisions; do not reuse Genotyping PipelineProvenance.
8. Synchronize RFC-154, open-decision record, module readme, digest implementation documentation, and independent-service behavioral acceptance plan. Do not change official BrAPI v2.1 sources or unrelated operation catalogues.
9. Keep the fixture validator itself tested with mutation-based unit tests; reject ambiguous duplicate JSON keys and non-standard JSON numeric constants without extending the public API contract.

## Guardrails
- No change to D-22 or D-24.
- Do not ratify §12.8/§12.9 or §12.10.
- Do not modify main, merge PR #5, or mark either PR ready.
- Avoid touching unrelated branch work. Use small commit(s) and preserve all existing content.
- Do not claim remote dereferencing, authorization enforcement, or production CAS execution.
- Maintain the existing non-normative markers.

## Validation

From the repository root, run:

```sh
python -m py_compile Scripts/validate_breeding_pipeline_contract_fixtures.py Scripts/test_breeding_pipeline_contract_fixture_validator.py
python Scripts/validate_breeding_pipeline_contract_fixtures.py
python -m unittest discover -s Scripts -p 'test_breeding_pipeline_contract_fixture_validator.py' -v
```

The third command runs the 23-test standard-library mutation regression suite, including authority-filter return-value and invariant regression checks. Execute the existing static API contract checker, digest-vector tests, and relevant specification checks separately. Report exact commands and outputs. The test suite has not been run in the remote GitHub-only editing environment; read-back or JavaScript mirrors are not equivalent to Python execution.

The candidate fixture corpus contains 70 scenarios (16 valid, 54 invalid). Static evidence fixture checks cannot substitute for the independent-service Scale evidence and compare-and-set acceptance plans.
