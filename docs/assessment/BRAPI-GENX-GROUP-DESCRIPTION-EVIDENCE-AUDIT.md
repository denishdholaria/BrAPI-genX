# GenX Group Description Evidence Audit

**Inspected:** 2026-11-24, starting from `main` `46d94d569f2342001da24eafd9113f47519ca325`.
**Objective:** improve foundational module descriptions without inventing settled scientific facts.

## Findings

The inspected repository tree contains **156** GenX `GroupDescription.md` files; every inspected entry has a Git blob size between 13 and 46 bytes, consistent with a single Markdown heading and no scope explanation. This is not evidence that all 156 modules are finalized. The maturity register classifies many GenX Request for Comments (RFC) as `STRUCTURAL_DRAFT`; even `CONTRACT_VALIDATED` denotes limited fixture evidence, not independent normative acceptance.

**Completed, source-backed descriptions in this review:** nine groups. The first bounded slice wrote Jobs, Provenance, VariableTerms and BreedingPipeline. The second slice wrote LotLedger, Models, FAIR, Telemetry and Genomics. Descriptions cite neighboring local module documentation, schema files, approved architectural decisions or existing RFCs. They distinguish technical design boundaries from unverified security, scientific semantics and production behavior.

**Deliberately left title-only:** 147 candidate groups. The safe follow-up is to assess each against its actual source schema, RFC maturity, official BrAPI overlap, and current open decisions before writing semantics. A heading-only document is preferable to a plausible but fabricated scientific relationship, authority or unit policy. No official BrAPI version 2.1 description was edited.

## Editing criteria for additional descriptions

- Trace substantive claims to the module's own schema and operations, accepted internal decisions, or checked scientific standards.
- Mark the current maturity accurately; distinguish internally accepted architectural decisions from draft public wire contracts.
- State module ownership and explicit exclusions; do not equate an operation-navigation link with typed resource identity or provenance (accepted D-026).
- Avoid inventing identifiers, units, optionality, lifecycle behavior, permissions, thresholds, production guarantees or unsupported cross-module mappings.
- Preserve unresolved decisions prominently rather than silently selecting a scientific answer.
- Write only in the relevant module's `GroupDescription.md` and inspect generated-artifact consumers before changing shared tooling.

## Verification limits

Repository-tree file names and blob sizes were inspected; the selected module `README.md` and related operations/schemas supplied the source-boundary evidence. No full local repository checkout or hosted conformance run was available. Descriptive documentation changes do not constitute scientific conformance, runtime behavior or new normative acceptance.
