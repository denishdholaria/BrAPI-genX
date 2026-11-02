# RFC-071 — Marker Probe (Genomics)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-061 (Assay Design), RFC-062 (Variant Annotation), RFC-064 (Genotype QC), `CLASSIFICATION.md` (D3).

## 1. Problem

BrAPI v2.1 standardizes markers, variants, and call sets but has no place to
record the physical probe (oligo or vendor-defined probe) that targets a marker
on a given genotyping platform. Probe sequences, vendor part numbers, and the
marker linkage they implement are exactly the evidence a reviewer needs to
reproduce an assay or audit a vendor order. Without a probe record, the same
marker can be assayed with different probes across runs and no audit trail.

## 2. Object

`MarkerProbe` — one immutable record of a probe targeting a BrAPI Marker on a
genotyping platform, with its sequence, platform, and provenance.

## 3. Endpoints

- `GET /genx/v1/marker-probes` (`genxListMarkerProbes`)
- `POST /genx/v1/marker-probes` (`genxRegisterMarkerProbe`)
- `GET /genx/v1/marker-probes/{markerProbeDbId}` (`genxGetMarkerProbe`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- Marker probes reference BrAPI `Marker` by identifier; they do not duplicate
  the Marker registry.
- A marker probe is not a BrAPI Marker and must not be treated as one.
- Probe sequences and vendor part numbers are opaque metadata; the API does not
  validate biological correctness.

## 5. Invariants

- A published `markerProbeDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional probes linked by `supersedes`.
- A probe record does not imply that the probe is validated, commercially
  available, or scientifically endorsed.
- `platform` names the platform/vendor context; it is not a BrAPI Location.

## 6. Deferred questions

- D-211: Should `markerDbId` be required, or may a probe be registered before
  its target marker is known? (Current: optional.)
- D-212: Should `probeSequence` be required, or may a vendor withhold the
  sequence? (Current: optional.)
- D-213: Should platform be a controlled GenX terminology instead of a free-form
  string? (Current: free-form string.)

## 7. Classification

Primary domain: D3 — Genotyping and Molecular Genomics.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
