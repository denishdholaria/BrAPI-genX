# BrAPI-GenX — Phase 0 Assessment

**Date:** 2026-11-03
**Repository:** `denishdholaria/BrAPI-genX`
**Branch:** `assessment/phase-0-consolidation`
**Baseline commit:** `6c09dff4c8f68fc89df541fc1fdcb09abc95e30c`
**Assessment type:** Phase 0 consolidation and remediation (no new RFC or endpoint generation).

## 1. Overall project assessment

BrAPI-GenX is a substantial, independently governed specification initiative with a
credible engineering foundation: a master endpoint registry with stable catalogue
identifiers, generated catalogues, a domain classification registry, conformance
probes and fixtures, and 155 numbered RFCs. It is **not yet ready for
standardisation, external adoption claims, or a stable release**. The immediate
risk is the gap between the breadth of the specification corpus and the depth of
its domain semantics, governance, and independent interoperability evidence.

This Phase 0 work freezes bulk expansion and re-establishes a controlled,
reviewable, quality-governed foundation.

## 2. Verified repository baseline

| Item | Value |
|---|---|
| Repository remote | `https://github.com/denishdholaria/BrAPI-genX.git` |
| Default branch | `main` |
| Baseline commit SHA | `6c09dff4c8f68fc89df541fc1fdcb09abc95e30c` |
| Working branch | `assessment/phase-0-consolidation` |
| Local uncommitted changes at start | one untracked file `BrAPI-GenX_Assessment_2026-11-03.md` (preserved) |
| RFC documents | 155 (RFC-001 … RFC-155, no gaps, no duplicates) |
| Resource directories | 158 (under `Specification/BrAPI-GenX/`, excluding `Inventory`) |
| Schema files (YAML) | 967 (repository-wide, includes V2.1) |
| Schema files (JSON) | 145 |
| Endpoint registry entries | 663 (201 BrAPI v2.1 + 462 proposed GenX) |
| Conformance fixtures | 32 |
| Domain classification modules | 158 |
| Ambika catalogue (read-only input) | 24 domain groups, 47 capability packs, 402 modules |

Counting rules: an API operation is one HTTP method on one route. The registry
counts 201 BrAPI v2.1 operations and 462 proposed GenX operations. The legacy
inventory separately counts 249 BrAPI v2.1 routes from the Bijmantra backend;
these are different scopes (official spec routes vs. legacy implementation
routes) and are not reconciled into a single number. See consistency register.

## 3. Architecture strengths

1. Separation from official BrAPI: GenX stays additive and optional, with
   `/genx/v1/` namespace and frozen V2.1 contracts.
2. Domain taxonomy (D1–D7 + C1–C9) is conceptually strong.
3. Endpoint identity and traceability: stable `catalogId`, operation IDs, full
   route identity, semantic-neighbour records, fail-closed registry checks.
4. Original core RFCs (RFC-001…RFC-007) are materially stronger than the long
   tail (e.g. RFC-003 Seed-Lot Ledger).
5. Automation is useful: conformance, endpoint catalogue, registry checks, and
   generated artefacts all pass at baseline.

## 4. Critical deficiencies

1. **Standards identity confusion.** `PROJECT_IDENTITY.md` and root `README.md`
   described "Official BrAPI v3" as a released community major version. Official
   BrAPI latest stable release is v2.1 (brapi.org). Corrected in Phase 0.
2. **Documentation drift.** `Specification/BrAPI-GenX/README.md` claimed 21 GenX
   operations while the registry reports 462. `Inventory/README.md` said D1/D2/D4/D5
   had no GenX specs despite many newer RFCs. `DEVELOPMENT_WORKSHEET.md` is stale.
3. **Decision-identifier collisions.** `DECISIONS.md` covers D-01…D-25 plus
   D-21…D-25 additions, while RFCs use D-001…D-462. D-460/D-461/D-462 were
   reused between RFC-153 and RFC-155; renamed to RFC-scoped IDs in Phase 0.
4. **Generic/placeholder RFCs.** Newer RFCs (e.g. RFC-145, RFC-152, RFC-154,
   RFC-155) are short, templated, and lack scientific depth. See maturity
   register.
5. **Security overstated.** Reference server accepts/ignores bearer tokens; no
   effective authorization. Must not be described as secure.
6. **S-22 discrepancy.** Conformance README/RESULTS reference an S-22 guardrail
   not registered in `probes.yaml`.
7. **Versioning terminology.** OpenAPI metadata used `3.0-draft`, conflating GenX
   with official BrAPI major version; corrected to `0.1-draft`. Server URL pointed
   at an unauthorised official test server; corrected to local reference.

## 5. Main risks

- Unverified interoperability claims if generic RFCs are treated as complete.
- Ambika module count (402) being misread as a mandatory endpoint backlog.
- Historical conformance results being mistaken for current evidence.
- AI agents inventing endpoints or ratifying decisions without authority.

## 6. Evidence

- Baseline validation (run 2026-11-03): `checkEndpointRegistry.py` passed
  (201 v2.1 + 462 GenX). `checkGenXEndpointCatalog.py` passed. `checkGenXConformance.py`
  reported 0 failures, 28 skipped (live probes need a server). `generateEndpointArtifacts.py --check`
  exited 0. `checkNullableConsistency.py` reported 24 mismatches in V2.1 schemas
  (pre-existing, out of GenX scope; documented, not fixed).
- Official BrAPI status: brapi.org lists v2.1 as latest stable release (released
  2022-07-01); "New Concept Preview" is explicitly subject to change.

## 7. Priority ranking

- P0 (critical): identity correction, decision-id collision, registry drift.
- P1 (high): generic RFC depth, security ambiguity, stale docs.
- P2 (medium): missing validation, test coverage, schema details.
- P3 (low): naming, formatting, presentation.

## 8. Recommended next steps

1. Complete Phase 0 deliverables (consistency register, coverage matrix, quality
   standard, maturity register, decision governance, worksheet, READMEs, backlog).
2. Run full validation and record commit-pinned evidence.
3. Do not begin Phase 1 until acceptance criteria are met.
4. Phase 1 should deepen a small number of scientifically important modules
   (e.g. RFC-003-style depth) rather than expand endpoint count.