# RFC-032 — Image Metadata (Phenotyping)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), `../CLASSIFICATION.md` (D4).

## 1. Problem

Official BrAPI version 2.1 already defines `Image` metadata, including
`imageTimeStamp`, `imageWidth`, `imageHeight`, `imageLocation`,
`observationUnitDbId` and `additionalInfo`. GenX proposes a **separate**
capture-context lifecycle and cannot assert that existing BrAPI Images lack
metadata. The candidate does not itself validate camera calibration,
capture correctness, scientific content or links to an authority-matched
Image or Study.

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
- `imageDbId` is a required string referencing an official BrAPI Image;
  `studyDbId` and `observationUnitDbId` are optional strings.
  No server-context join or synchronization with overlapping official Image
  metadata is established by this schema.
- Image metadata is not a BrAPI Image and must not be treated as one.

## 5. Invariants

- A published `imageMetadataDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional records linked by `supersedes`.
- `imageDbId` and `capturedAt` are required, with the registration
  identity; `camera`, `resolution`, study, observation unit and provenance
  are optional.
- `resolution` is an unstructured string; image dimensions already
  exist in official BrAPI ImageNewRequest.
- A record does not imply a complete image repository, validated
  sensor calibration, verified original image, or a scientifically
  interpretable phenotype.

## 6. Deferred questions

- D-93: Should `imageDbId` be required? (Current: required.)
- D-94: Should image metadata link to GenX `PhenotypeCapture`? (Current:
  no `phenotypeCaptureDbId` field is modelled.)
- D-95: Should resolution be a structured quantity? (Current: string.)

## 7. Classification

Primary domain: D4 — Phenotyping and Plant Observations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.