# Mission 046 — Plot and experimental design authority review

**Date:** 2026-11-24
**Prepared parent commit:** `9275ac6557ede9cdd9b6cd86d26bf9307eaa1535`

Official BrAPI v2.1 ObservationUnitLevel already models a plot level. Trials already comprise multiple studies. GenX Plot, FieldBook and TrialNetwork are STRUCTURAL_DRAFT metadata proposals, not a substitute for an official plot identity, capture-definition schema or multi-location trial membership.

The three existing RFCs contained incorrect claims that BrAPI lacks those basic features or that links to official Study/Location identifiers already exist in the candidate schema. These were corrected; no typed external linkage or biologically meaningful equality was invented. Outstanding decisions D-319–D-327 remain open.

Three group descriptions were written from real candidate schemas and incumbent BrAPI source documents. A pinned guard and regression checks protect them. Reviewed groups rise to **33/156**, leaving **123** deferred; twelve unratified-link evidence observations are checked.

**No official BrAPI sources, GenX wire schemas, operation routes, generated catalogues, endpoint registry identities, maturity decisions or scientific approvals changed.** Hosted static/live and specification generation remain required before asserting full verification.
