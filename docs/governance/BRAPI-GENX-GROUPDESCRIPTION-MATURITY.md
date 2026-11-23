# BrAPI-GenX GroupDescription Maturity Guardrail

**Status:** mandatory structural gate for GenX modules.

## Rule

`GroupDescription.md` is a governed, maturity-aware artifact.

1. Source of maturity truth: `docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md`,
   interpreted through the RFC documents under
   `Specification/BrAPI-GenX/RFCs/`. An RFC is mature when its maturity status
   is `CONTRACT_VALIDATED` or `SEMANTICALLY_REVIEWED`.
2. Only modules whose RFC is mature may carry a non-trivial `GroupDescription.md`
   (more than the title line).
3. For mature modules, `GroupDescription.md` must contain substantive content
   beyond the title line. An empty or title-only description fails validation.
4. Structural-draft modules remain title-only. They are not required, and must
   not be forced, to invent content.
5. Provenance-only embedded contracts (`Core/Provenance/`) are exempt from the
   substantive-content requirement; they remain title-only.

## Enforcement

`Scripts/specification_structure.py` derives the mature module set from the
maturity register and RFC module references, and validates each mature module's
`GroupDescription.md`. `Scripts/test_specification_structure.py` covers
positive and negative mutation cases.