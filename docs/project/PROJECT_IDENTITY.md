# BrAPI-GenX — Project Identity and Naming Standard

## 1. Canonical identity

- **Official project name:** BrAPI-GenX
- **Project identity:** BrAPI-GenX
- **Repository slug:** brapi-genx
- **Rust package / crate name:** brapi-genx
- **Rust module identifier:** brapi_genx
- **Configuration prefix:** `BRAPI_GENX_`
- **Environment variables:** `BRAPI_GENX_*`
- **Documentation title:** BrAPI-GenX
- **OpenAPI specification title:** BrAPI-GenX API
- **GenX-native API namespace:** `/genx/v1/`
- **Git references and technical identifiers:** brapi-genx

BrAPI-GenX is the single canonical project identity. Legacy names (BrAPI-Den,
BrAPI_Den, brapi_den, BrAPI GenX, brapi-genx variants used as provisional names)
are retired as active identities. Historical references may be preserved for
attribution, migration, or compatibility.

## 2. Naming conventions

1. Use `BrAPI-GenX` in all human-readable documentation, presentations,
   specifications, and references.
2. Use `brapi-genx` for repository slugs, Rust package names, technical package
   identifiers, and filesystem naming where appropriate.
3. Use `brapi_genx` where programming-language conventions require underscores.
4. Use `BRAPI_GENX_` for environment-variable prefixes and configuration constants.
5. Do not introduce alternative spellings or additional provisional names.

## 3. Relationship with official BrAPI

- **BrAPI** is the established community-driven Breeding Application Programming
  Interface specification and ecosystem.
- **Official BrAPI v3** is the community's official third major version, governed
  by the BrAPI community.
- **BrAPI-GenX** is an independently governed project for developing, exploring,
  and extending approaches to breeding data interoperability.

BrAPI-GenX must not present itself as the official successor to BrAPI, an
officially endorsed BrAPI release, or a replacement for the community
specification. It maintains compatibility with official BrAPI specifications
where applicable, while distinguishing its own extensions, experimental
capabilities, and independently developed features.

## 4. API namespace and versioning

- GenX-native API endpoints use `/genx/v1/`.
- Official BrAPI-versioned routes are used only where they implement the
  corresponding official specification and their use is justified by actual
  compatibility requirements.
- Never redefine an official BrAPI route or version identifier to represent a
  proprietary GenX extension.
- BrAPI-GenX has an independent versioning policy. Its version must not be
  confused with the version of the official BrAPI specification.
- Compatibility, extensions, experimental endpoints, and breaking changes are
  managed under this independent policy.

## 5. Legacy naming and migration policy

- Legacy names are retired as active identities.
- Historical records are not modified merely to make terminology appear current.
- Where legacy environment variables or identifiers must remain supported,
  introduce a controlled compatibility and deprecation strategy.
- Official BrAPI terminology and version identifiers remain intact.

## 6. Branding and attribution

The project should be recognised for its engineering, scientific value,
openness, and contribution to the plant breeding community. Founder attribution
is welcome, but personal recognition is not the primary objective.