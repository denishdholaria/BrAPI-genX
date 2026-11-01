# RFC-032 — Image Metadata (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `CLASSIFICATION.md` (D4).

## 1. Problem

BrAPI v2.1 standardizes images but not image metadata: capture details,
camera, resolution, and provenance. Without this record, image provenance and
capture context cannot be audited or linked to studies.

## 2. Object

`ImageMetadata` — one immutable image metadata record.

## 3. Endpoints

- `GET /genx/v1/image-metadata` (`genxListImageMetadata`)
- `POST /genx/v1/image-metadata` (`genxRegisterImageMetadata`)
- `GET /genx/v1/image-metadata/{imageMetadataDbId}` (`genxGetImageMetadata`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Image metadata references BrAPI Image, Study, and ObservationUnit by
  identifier; it does not duplicate those resources.
- Image metadata is not a BrAPI Image and must not be treated as one.

## 5. Invariants

- A published `imageMetadataDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `imageDbId` and `capturedAt` are required.
- A record does not imply a complete image repository.

## 6. Deferred questions

- D-93: Should `imageDbId` be required? (Current: required.)
- D-94: Should image metadata link to GenX `PhenotypeCapture`? (Current:
  optional, not required.)
- D-95: Should resolution be a structured quantity? (Current: string.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.