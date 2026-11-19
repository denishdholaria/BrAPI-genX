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
7. Synchronize RFC-154, open-decision record, module readme, digest implementation documentation, and independent-service behavioral acceptance plan. Do not change official BrAPI v2.1 sources or unrelated operation catalogues.

## Guardrails
- No change to D-22 or D-24.
- Do not ratify §12.8/§12.9 or §12.10.
- Do not modify main, merge PR #5, or mark either PR ready.
- Avoid touching unrelated branch work. Use small commit(s) and preserve all existing content.
- Do not claim remote dereferencing, authorization enforcement, or production CAS execution.
- Maintain the existing non-normative markers.

## Validation
Run the fixture validator and static API contract checker locally if the environment is available. Also run JSON parsing, Python compilation, digest vector tests, Python fixture validation, and relevant specification checks. Report exact commands and outputs. If execution is unavailable, state that clearly.
