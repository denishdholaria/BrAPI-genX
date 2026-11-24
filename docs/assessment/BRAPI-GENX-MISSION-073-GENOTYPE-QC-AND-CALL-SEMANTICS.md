# Mission 073 — Genotype QC evidence and call interpretation scope

**Prepared parent:** `c89a1175974529088b8af5e85051c8f1c868c7e1` (Mission 072), 2026-11-24.
**Scope:** review and safeguard two draft GenX genotyping groups, with source-backed wording corrections only. No official BrAPI source, candidate wire-schema, operation, registry, maturity or scientific policy change.

## Findings

1. The `GenotypeQcReport` registration request requires only its record identity. Both proposed dataset/import identifiers are optional string fields. The optional `metrics` object has no required per-metric keys, value constraints, scientific interpretation, or verdict. An arbitrary metric object does not establish a passed or released genotype set. `D-190`–`D-192` remain unresolved.
2. The `GenotypeCallSemantics` registration request requires only record identity. The `callSetDbId` string is optional, and `missingCallPolicy`, `zygosityEncoding` and `confidenceThreshold` are optional. No range constraint or harmonized vocabulary guarantees comparable genotyping calls. Official BrAPI 2.1 `GET /brapi/v2/callsets` is preserved. `D-214`–`D-216` remain unresolved.
3. Both RFCs formerly made unconditional statements about references to other objects; the corresponding candidate fields exist but their presence and resolution are not required or independently proven. We qualify those links as optional, without reclassifying them as absent.

## Assurance work

Pin two source-linked `GroupDescription.md` documents, qualify RFC-064/RFC-072 and corresponding README claims, and add schema-derived regression checks on required and optional fields, official CallSets route and unresolved decisions. Documentation evidence coverage becomes **113 of 156** reviewed, 43 deferred, subject to repository checker and hosted verification.

This does not warrant normative maturity, referential integrity, data-readback authenticity, laboratory quality approval, standardized genotype transformations or independent persistent-service conformance.
