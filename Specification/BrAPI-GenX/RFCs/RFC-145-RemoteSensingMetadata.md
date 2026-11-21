# RFC-145 — Remote Sensing Metadata (M)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (M).

## 1. Problem

BrAPI v2.1 has no place to record remote sensing metadata. Remote sensing
records circulate without a stated platform, sensor, CRS, or provenance, so
they cannot be used for remote sensing analysis.

## 2. Object

`RemoteSensingMetadata` — one immutable remote sensing metadata record, with
its platform, sensor, acquisition date, CRS, resolution, and provenance.

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

- A published `remoteSensingMetadataDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.

## 6. Deferred questions

- D-433: Should `resolution` be required? (Current: optional.)
- D-434: Should `platform` be a controlled vocabulary? (Current: free-form string.)
- D-435: Should records link to GenX `ResearchAsset`? (Current: no link.)

## 7. Classification

Primary domain: null (cross-cutting M).
Cross-cutting: C1, C2, C3 (POST), C6, C9.
