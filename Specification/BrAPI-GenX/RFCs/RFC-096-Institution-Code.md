# RFC-096 — Institution Code (Reference Data)

- Status: proposal, non-normative.
- Supersedes: none.
- Related: RFC-001 (GenX skeleton), RFC-002 (Variable Term Governance), `../CLASSIFICATION.md` (cross-cutting).

## 1. Problem

Official BrAPI version 2.1 Germplasm already carries holding and donor institute codes. Multi-Crop Passport Descriptors (MCPD) version 2.1 defines an INSTCODE convention governed through the Food and Agriculture Organization (FAO) World Information and Early Warning System (WIEWS). This GenX proposal is an unproven additional metadata record, not a replacement for externally issued identifiers.

## 2. Object

`InstitutionCode` — one immutable institution and collection code entry, with
its code, name, and provenance.

## 3. Endpoints

- `GET /genx/v1/institution-codes` (`genxListInstitutionCodes`)
- `POST /genx/v1/institution-codes` (`genxRegisterInstitutionCode`)
- `GET /genx/v1/institution-codes/{institutionCodeDbId}` (`genxGetInstitutionCode`)

## 4. Compatibility law

- Additive and optional. A V2.1 client keeps working against a GenX server.
- A GenX client tolerates a server that does not implement this object.
- No change to BrAPI v2.1 paths, schemas, or operationIds.
- The candidate defines no typed official BrAPI Germplasm or WIEWS institute reference, and its optional code cannot be treated as externally verified. The proposed link to GenX TaxonName under D-288 is not implemented or scientifically established.
- An entry is not a BrAPI data resource and must not be treated as one.

## 5. Invariants

- A published `institutionCodeDbId` record never mutates in place.
- Replay: same id + identical body replays; same id + different body → 409.
- Corrections are recorded as additional entries linked by `supersedes`.
- A record does not imply that the code is validated or endorsed.

## 6. Deferred questions

- D-286: Should `code` be required? (Current: optional.)
- D-287: Should `name` be required? (Current: optional.)
- D-288: Should entries link to GenX `TaxonName`? (Current: no link.)

## 7. Classification

Primary domain: (none, cross-cutting).
Cross-cutting: C1, C2, C3 (POST), C4, C9.
