# RFC-145 — Remote Sensing Metadata (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

GenX proposes separately identified remote-sensing **metadata** for
discovery alongside official BrAPI version 2.1 resources. A scientifically
usable image product also requires a source raster, footprint, calibrated
bands, timing, spatial reference and processing provenance. The current
candidate requires none of those fields except record identity, so the
presence of a catalogue record is not evidence of image usability.

## 2. Object

`RemoteSensingMetadata` — one proposed immutable discovery record.
Platform, sensor, acquisition date, coordinate reference, resolution and
provenance are optional; no source raster or acquisition quality is required.

## 3. Endpoints

- `GET /genx/v1/remote-sensing-metadata` (`genxListRemoteSensingMetadata`)
- `POST /genx/v1/remote-sensing-metadata` (`genxRegisterRemoteSensingMetadata`)
- `GET /genx/v1/remote-sensing-metadata/{remoteSensingMetadataDbId}` (`genxGetRemoteSensingMetadata`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- A record is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- `remoteSensingMetadataDbId` is proposed to be immutable; registration
  requires this identifier only.
- Replay is a draft contract: same id + identical body replays; same id +
  different body → 409, subject to independent service verification.
- Corrections are proposed as additional records linked by `supersedes`.
- `platform`, `sensor`, `acquisitionDate`, `crs`, `resolution`, and
  provenance are optional; none verifies calibrated/georeferenced imagery.

## 6. Deferred questions

- D-433: Should `resolution` be required? (Current: optional.)
- D-434: Should `platform` be a controlled vocabulary? (Current: free-form string.)
- D-435: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
