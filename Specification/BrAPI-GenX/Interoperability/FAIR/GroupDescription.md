# Group FAIR — Findable, Accessible, Interoperable, Reusable Exchange Packages

**Status:** BrAPI-GenX candidate exchange metadata profile (RFC-006); contract-validation evidence is not proof of independent access-control, transport or preservation conformance.

The `FAIRPackage` candidate provides a metadata envelope for identifying, citing, describing and retrieving a curated set of data payload references. Proposed metadata includes persistent identifiers, declared licensing and access conditions, checksums or digests, provenance and embargo information. Candidate operations register a package and read package metadata; these operations do not themselves issue identifiers or transport every referenced payload.

**Scope boundary:** A registered package is not automatically FAIR-compliant. Digital Object Identifier (DOI) minting, licensing authority, Software Package Data Exchange (SPDX) license interpretation, restricted-access approval, remote byte retrieval, and embargo privacy remain separate responsibilities or unresolved decisions. In particular, access control at the metadata layer must not be mistaken for authorization to download protected underlying data.

**Sources:** [Local module scope](./README.md), [package schema](./Schemas/FAIRPackage.yaml), [candidate operations](./FairPackages_GET_POST.yaml), [RFC-006](../../RFCs/RFC-006-FAIR-Packages.md), and [project decisions](../../DECISIONS.md).
