# RFC-069 — Farm (Field Agronomy)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-011 (Harvest Records), RFC-024 (Irrigation Operation), RFC-026 (Fertilizer Application), RFC-029 (Crop Cycle), RFC-066 (Planting Operation), `../CLASSIFICATION.md` (D6).

## 1. Problem

BrAPI v2.1 models Locations and Studies, but it has no farm or site reference.

Agronomic records attach to fields, but a farm is the management unit that
groups fields, owns machinery and water rights, and carries the rotation and
boundary history. Without a farm record, every GenX operation has to repeat
holding metadata or infer it from Location fields, and cross-field accounting
(water, carbon, yield) cannot be scoped reliably.

## 2. Object

`Farm` — one immutable farm or site reference, with the BrAPI Locations that
make it up.

## 3. Endpoints

- `GET /genx/v1/farms` (`genxListFarms`)
- `POST /genx/v1/farms` (`genxRegisterFarm`)
- `GET /genx/v1/farms/{farmDbId}` (`genxGetFarm`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Farms reference BrAPI `Location` by identifier; they do not duplicate
  location geometry, coordinates, or country metadata.
- A farm is not a BrAPI data resource and must not be treated as one.
- A farm record is not a cadastral survey, land title, or legal boundary claim.

## 5. Invariants

- A published `farmDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional versions linked by `supersedes`.
- `totalAreaHa` is in hectares and is the farm's declared area, not the summed
  area of its locations; the two may disagree and the difference is evidence.
- The current `locationDbIds` array does not encode a farm-membership
  interval, polygon overlap or exclusive-partition rule. No current field
  verifies an overlap agreement, so shared location membership cannot be
  interpreted as an accepted land-tenure or boundary relationship.
- `inactive` and `withdrawn` farms remain visible; they are never deleted.

## 6. Deferred questions

- D-205: Should `locationDbIds` be required, or may a farm exist before its
  fields are registered? (Current: optional.)
- D-206: Should farm boundaries be modelled as geometry here, or remain with
  the geospatial module? (Current: no geometry; only Location references.)
- D-207: Should farm records link to an organization or party registry rather
  than carrying a free-text `organization`? (Current: free string.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
