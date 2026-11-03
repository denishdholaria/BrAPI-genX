# BrAPI-GenX

**BrAPI-GenX** is an independently governed project for developing, exploring, and
extending approaches to breeding data interoperability. It builds on the plant
breeding community's standards while distinguishing its own extensions,
experimental capabilities, and independently developed features.

BrAPI-GenX is **not** the official BrAPI specification, an officially endorsed
BrAPI release, or a replacement for the community's specification. Official
BrAPI terminology, version identifiers, and routes remain intact.

## Identity and naming

The canonical identity and naming standard is
[`docs/project/PROJECT_IDENTITY.md`](./docs/project/PROJECT_IDENTITY.md). In
summary:

- Official project name: **BrAPI-GenX**
- Repository slug / technical identifier: `brapi-genx`
- Rust module identifier: `brapi_genx`
- Configuration prefix: `BRAPI_GENX_`
- OpenAPI specification title: **BrAPI-GenX API**
- GenX-native API namespace: **`/genx/v1/`**

Legacy and provisional names are retired as active identities. Historical
references may be preserved for attribution, migration, or compatibility.

## Relationship with official BrAPI

- **BrAPI** — the established community-driven Breeding Application Programming
  Interface specification and ecosystem.
- **Official BrAPI** — latest stable release is **v2.1** (brapi.org, released
  2022-07-01). "BrAPI v3" is not an officially released major version; the
  community's "New Concept Preview" documentation is explicitly subject to
  change. BrAPI-GenX must not claim or imply official v3 status.
- **BrAPI-GenX** — this independently governed project.

GenX-native endpoints use `/genx/v1/`. Official BrAPI-versioned routes are used
only where they implement the corresponding official specification and that use
is justified by actual compatibility requirements. GenX never redefines an
official BrAPI route or version identifier to represent a proprietary extension.

## Repository layout

- `Specification/` — endpoint registry, OpenAPI specifications, generated
  catalogues, and crosswalks.
  - `Specification/BrAPI-GenX/` — GenX proposal specifications (non-normative
    until explicitly accepted).
  - `Specification/BrAPI-GenX/Conformance/` — probes, fixtures, and the
    machine-readable domain classification registry.
  - `Specification/BrAPI-GenX/Inventory/` — generated endpoint-to-class inventory.
  - `Specification/BrAPI-GenX/AMBIKA-GAP-REGISTER.md` — gap analysis against the
    Ambika ideal module catalog.
- `Scripts/` — generation and conformance-check scripts.
- `docs/project/PROJECT_IDENTITY.md` — authoritative identity and naming standard.
- `generator/`, `Wiki/`, `docker/` — supporting tooling and documentation.

## Status

BrAPI-GenX specifications are **proposals** unless explicitly accepted and
ratified. They are additive and optional: a client using official BrAPI must
keep working against a GenX-aware server, and a GenX client must tolerate a
server that does not implement a GenX object. Nothing here changes official BrAPI
v2.1 behavior.

## Validation

From the repository root:

```bash
python3 Scripts/checkGenXEndpointCatalog.py
python3 Scripts/checkEndpointRegistry.py
python3 Scripts/checkGenXConformance.py
```

The first two validate catalogue/registry consistency. The third runs static
conformance probes; live probes require `--server`.

## Versioning

BrAPI-GenX has an independent versioning policy. Its version must not be confused
with the version of the official BrAPI specification. Compatibility, extensions,
experimental endpoints, and breaking changes are managed under this independent
policy. See `docs/project/PROJECT_IDENTITY.md`.

## Contribution guidance

- Preserve official BrAPI terminology and identifiers.
- Do not introduce competing aliases or provisional names.
- Classify every new GenX module, schema, and operation in
  `Specification/BrAPI-GenX/Conformance/domain-classification.yaml`.
- Follow the GenX module pattern and run the checks above before submitting.