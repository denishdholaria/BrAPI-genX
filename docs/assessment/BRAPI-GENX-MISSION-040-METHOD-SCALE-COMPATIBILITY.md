# Mission 040 — BrAPI v2.1 Method/Scale compatibility and provenance audit

**Date:** 2026-11-24
**Inspected main:** `12cd9441fefe1467ff99c80204c10243fe2a43a8`
**Scope:** editorial RFC/readme corrections for RFC-087 and RFC-017, two source-backed group descriptions, checker pinning, regression tests. No source schema or route changes.

## Confirmed overlapping standard surface

The repository preserves official BrAPI v2.1 `Specification/BrAPI-Phenotyping/Scales` and `Specification/BrAPI-Phenotyping/Methods` operations and schemas. Official Scale already handles units, value types and acceptable values; Method is likewise a first-class resource. Therefore the earlier RFC-087 assertion that BrAPI v2.1 has no place to record scales is factually misleading. Any proposed GenX record requires a demonstrated distinct workflow rather than a claim that the incumbent feature is missing.

## Changes and non-decisions

- RFC-087 and MeasurementScale README now acknowledge the real official Scale, and disclaim any tested identity mapping or necessity of a distinct object. The former RFC-087 claim of an existing `VariableTerm` reference was corrected to match its source schema (none defined; D-261 open).
- RFC-017 and MeasurementMethods README acknowledge official `Methods` endpoints. The assertion that the GenX record references official Method/Scale was corrected; the schema currently has no such typed link (D-49 open).
- Two group descriptions explain the proposal fields, official authority, limits and unresolved decisions D-259–D-261 and D-48–D-50.
- The group-description audit pins 17 reviewed modules out of 156; 139 stay deferred.
- Regression tests assert official `/scales` and `/methods` source operations exist and safeguard against reintroducing the false missing-scale claim.

## Verification

Direct referenced Markdown links verified against the inspected main repository tree; source fields checked against actual local OpenAPI schemas and operation definitions. Full hosted governance/generation will run on the committed tree. This assessment is not a statement of hosted success until Actions report it.

**No official BrAPI v2.1 sources, GenX endpoints, schema fields, generated files, RFC maturity status, or scientific mapping decisions were changed.**