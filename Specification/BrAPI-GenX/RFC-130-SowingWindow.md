# RFC-130 — Sowing Window (O)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (O).

## 1. Problem

BrAPI v2.1 has no place to record sowing windows. Sowing advisories
circulate without a stated window type, dates, region, or provenance, so
they cannot be used for planting decisions.

## 2. Object

`SowingWindow` — one immutable sowing window record, with its window type,
recommended dates, region/zone, crop type, and provenance.

## 3. Endpoints

- `GET /genx/v1/sowing-windows` (`genxListSowingWindows`)
- `POST /genx/v1/sowing-windows` (`genxRegisterSowingWindow`)
- `GET /genx/v1/sowing-windows/{sowingWindowDbId}` (`genxGetSowingWindow`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `sowingWindowDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-388: Should `endDate` be required? (Current: optional.)
- D-389: Should `windowType` be a controlled vocabulary? (Current: free-form string.)
- D-390: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting O).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
