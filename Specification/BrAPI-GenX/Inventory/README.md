# BrAPI-GenX Endpoint Inventory (generated from Bijmantra legacy backend)

- Status: **generated working inventory / proposal**, non-normative. Review required.
- Source: `bijmantraOrg/backend` FastAPI app (brain-wired modules), extracted 2026-11-01.
- Scope: all registered HTTP routes (auth, BrAPI v2.1, product `/api/v2/*`). Socket.IO and static mounts excluded.
- Purpose: give a single organized view of ~1,849 legacy endpoints, map them to the proposed
  BrAPI-GenX scientific domain classes (D1–D7) and cross-cutting capabilities (C*), and expose
  clashes/duplicates so GenX specs can be planned without guessing.

## Totals

| Source | Endpoints |
|---|---:|
| BrAPI v2.1 (`/brapi/v2`) | 249 |
| Product (`/api/v2`) | 1,591 |
| Auth (`/api/auth`) | 8 |
| OpenAPI metadata | 1 |
| **Total** | **1,849** |

## By proposed BrAPI-GenX class

| Code | Class | Endpoints | Share |
|---|---|---:|---:|
| P | Platform / non-scientific (app, auth, infra, collaboration, UI, AI, etc.) | 836 | 45.2% |
| D2 | Breeding Programs & Experimental Design | 240 | 13.0% |
| D3 | Genotyping & Molecular Genomics | 164 | 8.9% |
| D5 | Environment, Agroecology & Field Context | 160 | 8.6% |
| D7 | Scientific Analysis, Models & Derived Evidence | 127 | 6.9% |
| D4 | Phenotyping & Plant Observations | 124 | 6.7% |
| D6 | Crop Production & Material Operations | 94 | 5.1% |
| D1 | Germplasm & Biological Resources | 76 | 4.1% |
| C4 | Terminology & Semantic Governance | 19 | 1.0% |
| C1 | Identity, versioning & capability negotiation | 9 | 0.5% |

Machine-readable: `by_class.csv`.

## By module (top 25 by endpoint count)

| Module | Endpoints |
|---|---:|
| future | 114 |
| vision | 54 |
| brapi-v2:search | 48 |
| devguru | 41 |
| crop-calendar | 40 |
| weather | 28 |
| chat | 24 |
| ai-configuration | 22 |
| collaboration-hub | 22 |
| seed-bank | 22 |
| resources | 19 |
| dispatch | 18 |
| sensors | 18 |
| prahari | 18 |
| data-quality | 17 |
| genotyping | 17 |
| reports | 17 |
| licensing | 17 |
| data-sync | 16 |
| dus | 16 |
| audit | 16 |
| trial-planning | 16 |
| harvest | 15 |
| teams | 15 |
| chaitanya | 15 |

Full list: `by_module.csv` (219 modules).

## GenX coverage vs legacy demand

Existing GenX modules and their primary class:

| GenX module | Class | Legacy endpoints in same class (approx.) | Status |
|---|---|---:|---|
| Genomics / VariantMatrix | D3 | 164 | Spec exists; legacy genomics surface is large (genotyping, markers, variants, etc.) |
| LotLedger / LotLedgerEntry | D6 | 94 | Spec exists (seed-lot ledger only) |
| Models / ModelArtifact | D7 | 127 | Spec exists (model registry only) |
| Telemetry / TelemetryPoint | D4/D5 (context) | 284 (D4+D5) | Spec exists (generic point) |
| VariableTerms / VariableTerm | C4 | 19 (+ BrAPI variables/traits/methods/scales/ontologies) | Spec exists |
| Jobs / Job | C3 | — (cross-cutting) | Spec exists |
| ServerInfoV3 | C1 | 9 (+ BrAPI serverinfo) | Spec exists |
| FAIR / FAIRPackage | C5 | 3 (fair-metadata) | Spec exists |
| Provenance / ProvenanceEnvelope | C2 (embedded) | — | Embedded only, no endpoints |

Classes with **no GenX spec yet** but significant legacy surface:
- **D1** Germplasm & Biological Resources — 76 endpoints (seed-bank, passport, grin, germplasm search/comparison)
- **D2** Breeding Programs & Experimental Design — 240 endpoints (trials, crosses, nursery, selection, breeding pipeline, doubled haploids, gxe, stability)
- **D4** Phenotyping & Plant Observations — 124 endpoints (phenotype, observations, image/vision, DUS, crop-health)
- **D5** Environment, Agroecology & Field Context — 160 endpoints (weather, sensors, IoT, field layout, crop calendar, carbon/emissions)

## Clashes / duplicates detected

Exact duplicate method+path registrations (4):
- `POST /api/v2/crop-calendar/events` (×2)
- `GET /api/v2/crop-calendar/events` (×2)
- `GET /api/v2/crop-calendar/growth-stages` (×2)
- `GET /api/v2/audit/security` (×2)

These are the same kind of collision BrAPI-GenX `ENDPOINT-IDENTITY.md` guards against. Resolve before promoting any of them into a GenX spec.

## Where to work next (suggested)

1. **Spec the missing scientific domains first**: D1, D2, D4, D5 (in that order of legacy mass and standards gap). D2 has the largest un-spec'd surface (240) and the most BrAPI v2 overlap (trials/studies/programs/crosses).
2. **Deepen existing GenX modules** where legacy surface is large: D3 (genotyping/markers/variants), D6 (seed-bank, inventory, harvest, warehouse), D7 (analytics, breeding-value, selection-decisions, GWAS/QTL).
3. **Do not force the 836 platform endpoints into scientific GenX classes.** Keep them as BrAPI-GenX platform extensions or leave them in the product API; classify them as `P` / cross-cutting (C9 security, C3 jobs, C5 FAIR where applicable).
4. **Resolve the 4 duplicate routes** and any semantic overlaps with BrAPI v2 (see `Conformance/endpoint-overlaps.yaml` pattern) before adding new operationIds.
5. **Use `Conformance/domain-classification.yaml`** as the registry template; every new GenX module/schema/operation must be classified or explicitly marked cross-cutting, with no duplicate primary owners.

## Files

- `inventory.csv` — one row per endpoint (method, path, module, proposed class)
- `by_module.csv` — endpoint count per module
- `by_class.csv` — endpoint count per class
- `top_modules.csv` — modules sorted by endpoint count

## Notes / caveats

- Classification is **auto-proposed by module name keywords + manual overrides**; it is not a scientific authority. Review each module before ratifying.
- A module's primary class follows the resource's authoritative meaning; facets are additive and never imply wire compatibility.
- Legacy endpoint counts are implementation evidence only, not parity targets (per ADR-008).
- Telemetry is context-dependent (D4 vs D5); individual readings must be classified by phenomenon, not transport.