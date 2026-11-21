# RFC-070 — Yield Map (Field Agronomy)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-011 (Harvest Records), RFC-029 (Crop Cycle), RFC-066 (Planting Operation), RFC-069 (Farm), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 records harvest observations but has no way to describe a spatial
yield surface. Yield maps are the routine output of combine monitors, remote
sensing pipelines, and yield-model post-processing. Without a record, a map is
an unversioned file with no stated location, crop cycle, harvest source, cell
size, or integrity digest, so results cannot be compared or reproduced.

## 2. Object

`YieldMap` — one immutable reference to a spatial yield surface, with its
location, source harvest record, resolution, storage URI, and digest.

## 3. Endpoints

- `GET /genx/v1/yield-maps` (`genxListYieldMaps`)
- `POST /genx/v1/yield-maps` (`genxRegisterYieldMap`)
- `GET /genx/v1/yield-maps/{yieldMapDbId}` (`genxGetYieldMap`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Yield maps reference BrAPI `Study` and `Location` and GenX `CropCycle` and
  `HarvestRecord` by identifier; they do not duplicate those resources.
- A yield map is not a BrAPI data resource and must not be treated as one.
- Map bytes are not transported by this API. The record names and verifies the
  payload; retrieval uses the referenced storage URI.

## 5. Invariants

- A published `yieldMapDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional versions linked by `supersedes`.
- New bytes under an existing identity require a new `fileDigest` and hence a
  new record; silent payload replacement is forbidden.
- `resolutionM` describes the nominal grid, not a guarantee of accuracy or
  interpolation quality.
- A map record does not imply that the underlying yield was measured, cleaned,
  or validated; that evidence belongs to the referenced harvest record and
  provenance.

## 6. Deferred questions

- D-208: Should `storageUri` and `fileDigest` be required, or may a map record
  exist before its payload is published? (Current: both optional.)
- D-209: Should the map reference an explicit coordinate reference system, or
  inherit one from the covered Location? (Current: no CRS field.)
- D-210: Should the API define a standard interpolation or aggregation method
  for turning point yield data into a surface, or leave that to provenance?
  (Current: provenance only.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
