# RFC-075 — Field Boundary (Field Agronomy)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-029 (Crop Cycle), RFC-069 (Farm), `../CLASSIFICATION.md` (D6).

## 1. Problem

Official BrAPI version 2.1 already records geographic coordinates for Locations. A distinct operational field-boundary history could represent field splits and revisions, but the current proposed record carries only optional `fieldDbId`, version label, and geometry URI without a canonical BrAPI Location or GenX Farm identity mapping.

## 2. Object

`FieldBoundary` — one immutable record of an operational field boundary version,
with its field linkage, version label, geometry reference, and provenance.

## 3. Endpoints

- `GET /genx/v1/field-boundaries` (`genxListFieldBoundaries`)
- `POST /genx/v1/field-boundaries` (`genxRegisterFieldBoundary`)
- `GET /genx/v1/field-boundaries/{fieldBoundaryDbId}` (`genxGetFieldBoundary`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The candidate has an optional free-string `fieldDbId` but no typed official BrAPI `Location` or GenX `Farm` reference. It cannot establish either resource's identity or boundary ownership.
- A boundary record is not a BrAPI Location and must not be treated as one.
- Geometry bytes are not transported by this API. The record optionally names an external geometry URI but provides no required format, checksum, retrieval operation or verification guarantee.

## 5. Invariants

- A published `fieldBoundaryDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional versions linked by `supersedes`.
- New geometry under an existing identity requires a new record; silent
  replacement is forbidden.
- A record does not imply that the boundary is validated, authoritative, or
  legally registered.

## 6. Deferred questions

- D-223: Should `geometryUri` be required, or may a boundary record exist
  before its geometry is published? (Current: optional.)
- D-224: Should the API define a standard geometry format/CRS, or inherit from
  the referenced Location? (Current: no format/CRS field.)
- D-225: Should boundary history be a first-class chain via `supersedes`, or a
  separate history endpoint? (Current: `supersedes` only.)

## 7. Classification

Primary domain: D6 — Field Agronomy and Crop Operations.
Cross-cutting: C1, C2, C3 (POST), C6, C9.
