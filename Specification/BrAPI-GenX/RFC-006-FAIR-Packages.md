# RFC-006: FAIR Exchange Packages

- Status: **proposal** (not accepted, not normative, grants no implementation authority)
- Builds on: RFC-001 (compatibility law, `ProvenanceEnvelope`, evidence links)
- Scope: a metadata envelope that makes any GenX payload findable, licensed,
  and embargo-aware
- Non-scope: DOI minting, license negotiation, access-approval workflows,
  repository storage — the package links to these, it does not implement them

## 1. Problem

Every GenX object so far is retrievable but not publishable: nothing names a
license, nothing carries a persistent identifier, nothing expresses an
embargo, and nothing binds a set of payloads into one citable unit. Federated
use (FAIDARE-style discovery, genebank networks, Data Trustee models) needs
exactly that layer — and it needs it as an envelope around existing payloads,
not as fields copied into every object.

Reference experience (BijMantra federated-asset work, pre-production
research, cited as evidence only): assets are registered with FAIR metadata,
JSON-LD context, W3C PROV provenance, DataCite DOI links, licenses, and
explicit promotion states; uninstall/revoke preserves records while denying
access. RFC-006 standardizes the wire half: the package and its access
contract. Minting, storage, and approvals stay outside.

## 2. Object — FAIRPackage

Files: `FAIR/Schemas/FAIRPackage.yaml`,
`FAIR/Schemas/FAIRPackageNewRequest.yaml`,
`FAIR/FairPackages_GET_POST.yaml`,
`FAIR/FairPackages_PackageDbId_GET.yaml`.

Purpose: bind payload references into one licensed, identified,
embargo-aware, citable unit.

Fields: `packageDbId` (`{authority}:package:{localId}`, required), `title`
(required), `description?`, `identifiers[]` (`{type: DOI|HANDLE|URL, value}`,
at least the primary citation link), `license` (SPDX expression, required —
FAIR R1.1), `accessRights` (`open`|`embargoed`|`restricted`, required),
`embargoUntil?` (date-time; servers MUST deny payload reads with `403` before
expiry), `keywords[]?`, `creators[]?`, `publisher?`, `publicationYear?`,
`payloadRefs[]` (reuses `EvidenceLink`: endpoint, schemaVersion,
responseDigest, queryDigest), `provenance?` (`ProvenanceEnvelope` — curation
history).

Responsibilities: citation identity, license, access contract, payload
binding. Non-responsibilities: minting DOIs (DataCite/Handle external);
storing payload bytes (payload services own them); deciding access requests
(`restricted` names the contract, it does not implement approvals).

Invariants:

1. Same `packageDbId` + identical body replays the existing record. Same id
   + different body is rejected with `409`. In particular the `license` of a
   published package never silently changes.
2. `embargoUntil` in the past or absent with `accessRights: open` serves
   payloads. Before expiry, payload reads are denied with `403`; metadata
   (title, identifiers, license, embargo date) stays readable so the package
   remains findable while embargoed.
3. `identifiers` of type `DOI` match `^10\.\d{4,}/.+`. Identifiers are
   asserted links; resolution is the identifier system's business.

## 3. Endpoints

- `POST /genx/v1/fair-packages` (`genxRegisterFairPackage`) with `FAIRPackageNewRequest` → `200` + single
  package (create, replay, or `409` conflict with plain-text body).
- `GET /genx/v1/fair-packages` (`genxListFairPackageMetadata`) with `accessRights?`, `license?` filters + standard
  pagination → list of packages (metadata only, never payload bytes).
- `GET /genx/v1/fair-packages/{packageDbId}` (`genxGetFairPackageMetadata`) → single package metadata, or `403`
  while its payloads are embargoed... precisely: metadata always serves;
  servers MUST NOT serve `payloadRefs` resolution while embargoed. Since this
  API serves metadata (not bytes), the `403` applies to any future payload
  expansion — the reference server returns `403` for the whole record while
  embargoed to prove the gate exists. (Honest limitation, see §5.4.)

## 4. Hypothesis, falsifier, verification

- Hypothesis: any consumer can cite a fixed set of payloads under a license,
  verify the binding by digest, and be refused before embargo expiry.
- Falsifier: a mutated license under a published id; an embargoed payload
  served early; a payload binding whose digest does not resolve.
- Verification: static probes S-17/S-18 plus live probes L-18–L-20 in
  `Conformance/probes.yaml` against the reference test server.

## 5. Explicit unknowns and requires-decision

1. `requires decision`: DOI minting flows (who mints, when, draft vs
   registered states) — identifiers are asserted here, never minted.
2. `requires decision`: restricted-access request/approval protocols.
3. `requires decision`: whether embargo should hide metadata fields beyond
   payload binding (reference denies the whole record; metadata-visible is
   the gentler alternative).
4. `assumption`: the reference server's whole-record `403` stands in for
   payload-level denial because this API serves metadata only.
5. `unknown`: cross-repository package federation and deduplication.

## 6. File map

```text
Specification/BrAPI-GenX/
  RFC-006-FAIR-Packages.md   this document
  FAIR/README.md + GroupDescription.md
    + Schemas/FAIRPackage.yaml + Schemas/FAIRPackageNewRequest.yaml
    + FairPackages_GET_POST.yaml + FairPackages_PackageDbId_GET.yaml
```
