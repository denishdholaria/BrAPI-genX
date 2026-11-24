# Mission 053 — Phenotyping capture, annotation and measurement-series shape audit

**Date:** 2026-11-24
**Prepared parent:** `b5967449714aa7b635d17e309b263eebb113d275`
**Scope:** RFC-012/025/044 and module README corrections, three evidence-linked groups, regression safeguards; no wire-schema modification.

## Verified mismatches

- Official BrAPI version 2.1 ObservationNewRequest has a nullable `value` string, permitting non-numerical scale values. Proposed GenX PhenotypeCapture entries use optional nullable `number`. This narrower representation is not a direct general-purpose replacement. RFC-012 proposes a `missingReason` if `qualityFlag=missing`, but the schema does not conditionally require one; `entries` may be empty unless separately validated.
- Proposed MeasurementSeries requires a `measurements` array (possibly empty), and each measurement requires a numeric, non-nullable `value`. The `qualityFlag` enumeration includes `missing`, but no `missingReason` property or null mechanism exists in the entry. The RFC's time-ordering promise is not enforced by an array structure. D-72–D-74 remain open.
- Proposed PhenotypeAnnotation requires study/unit/variable context and a free-text `annotation`; no typed link to GenX PhenotypeCapture is present, contrary to the former RFC D-131 description of an optional link. D-130–D-132 remain open.

Three non-normative group descriptions distinguish metadata fields, scientific validity, reference resolution and independent service conformance. Documentation guard reaches **45 of 156**, **111 deferred**. The typed-link absence evidence manifest rises to **23**; MeasurementSeries requires explicit `schema_file` in its row, since the module directory is named RepeatedMeasurement.

## Non-decisions

No observation value-type change, missingness or correction law, scientific ontology mapping, BrAPI v2.1 source, GenX OpenAPI schema, route, endpoint registry, mature RFC status or independent persistent conformance was introduced. The gaps are to be considered for separately approved future design decisions.

Hosted static/live and specification-generation checks must validate the integrated commit.
