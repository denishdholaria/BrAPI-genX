# Mission 054 — Coordinate geometry, spatial authority and verification boundaries

**Date:** 2026-11-24
**Prepared parent:** `22fc9363f36978b6ccfcd387fe6d17b89214db50`
**Scope:** Source-based, non-normative review of four candidate geospatial modules: LocationGeometry, FieldGeometry, CrsTransform and FieldBoundary.

## Incumbent contract overlap

Official BrAPI version 2.1 `LocationNewRequest` already has `coordinates` referring to a GeoJSON schema and a `coordinateUncertainty` field. It is incorrect to infer that spatial geometry is wholly absent merely because the official operation does not use the proposed GenX resource name.

## Candidate gaps

- LocationGeometry carries optional `locationDbId` (a real string reference field) and `geometryUri`, but no required geometry format, coordinate-reference system, digest, or built-in payload verification. RFC-092 previously claimed the record *verifies* geometry payload; this was corrected. D-274–D-276 remain open.
- FieldGeometry stores an unconstrained object `geometry`, string `crs`, and string `area`, but has no `fieldDbId` or typed Location identity and no geometry validity or area-consistency checks. D-424–D-426 remain open.
- CrsTransform stores optional source/target coordinate reference systems and a free-text `parameters` string; it is not an executable transform and carries no accuracy proof. D-418–D-420 remain open.
- FieldBoundary uses optional `fieldDbId`, `boundaryVersion` and `geometryUri`. The original RFC asserted geometry verification and typed Location/Farm references absent from source schema; these were corrected. D-223–D-225 remain open.

Four evidence-linked group descriptions and scientific non-ownership checks are added. The protected count becomes **49 of 156**; **107 evidence-deferred**. The unratified typed-link inventory becomes **25** with two new ResearchAsset link observations; explicit existing `locationDbId` and `fieldDbId` strings are **not** misclassified as absent.

No official BrAPI source, GenX OpenAPI schema, endpoint route, scientific relationship approval, maturity status, geometry validation policy or independently deployed service was changed. Full hosted checks are required after integration.
