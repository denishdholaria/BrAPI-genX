# Mission 048 — Observation, quality and missingness proposal boundary

**Date:** 2026-11-24
**Prepared parent:** `048115db0cd9728280ed6c91a0eaf56c89e73b6d`
**Scope:** RFC-110/111/112 source corrections, three candidate GroupDescriptions and evidence guards; no source schema changes.

Official BrAPI version 2.1 already represents Observations, including optional value, timestamp, observation-unit, study, variable and collector context. GenX QualityFlag is a free-form optional flag record without observation identity. ValueMissingness has independently optional `value` and boolean `missing` fields; no specified cross-field invariant determines whether `missing=true` and a value can coexist, how absence of both is interpreted, or whether imputation/correction is represented. CaptureWorkflow only has optional `workflowType` metadata, not a state machine or executable capture definition.

All three RFCs previously implied typed links to official observations absent from source schemas. These assertions were corrected without inventing approved links, quality policy or a missingness algorithm. D-328–D-336 remain open.

Three new evidence-backed descriptions increase the guarded inventory to **39 of 156** (117 deferred), and the explicit unratified-link ledger now covers **18** observations. Regression tests pin the source distinctions. No official BrAPI source, GenX schema, endpoint registry, scientific decision, operation or maturity was altered. Full hosted verification remains required at integration.
