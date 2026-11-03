# BrAPI-GenX — Independent Architecture and Specification Assessment

**Assessment date:** 3 November 2026  
**Repository:** `denishdholaria/BrAPI-genX`  
**Branch:** `main`  
**Reviewed commit:** `6c09dff4c8f68fc89df541fc1fdcb09abc95e30c`

## Executive verdict

BrAPI-GenX is a substantial independent specification initiative with a credible engineering foundation. It is **not yet ready for standardisation, external adoption claims, or a stable release**. The immediate risk is not lack of files or code. It is the gap between the breadth of the specification corpus and the depth of its domain semantics, governance, and independent interoperability evidence.

Do not restart the project and do not delete the generated work. Freeze bulk expansion, bring the documentation and registries back into alignment, establish a specification-quality bar, then deepen a small number of scientifically important modules.

The assessment separates:

1. **Domain correctness** — whether a resource captures a real and well-bounded breeding or scientific concept.
2. **Contract completeness** — whether identifiers, types, cardinalities, constraints, relationships, lifecycle, operations, errors, and examples are sufficiently precise.
3. **Interoperability evidence** — whether independent systems can exchange and interpret the same data without BijMantra-specific assumptions.

These are different dimensions and must not be combined into one completion percentage.

## Repository facts verified

- The private GitHub repository is accessible; `main` is the default branch.
- Reviewed commit: `6c09dff4c8f68fc89df541fc1fdcb09abc95e30c`, pushed on 2 November 2026.
- The repository tree contains 2,339 entries, including 1,900 files and 439 directories.
- `Specification/BrAPI-GenX/` contains approximately 1,455 tracked entries and a numbered RFC series through RFC-155.
- The Ambika ideal-module catalog declares 24 domain groups, 47 capability packs, and 402 modules. These are catalogue records, not completed GenX specifications or implementation evidence.
- The endpoint registry checker reports 201 BrAPI v2.1 operations and 462 proposed GenX operations. `Inventory/README.md` separately reports 249 BrAPI v2.1 routes; these may use different counting scopes, but the repository should define and reconcile the difference explicitly.
- The registry and endpoint catalogue include stable identifiers, source paths, semantic metadata, and checks for route and operation identity.

## What is working well

### 1. Separation from official BrAPI

The proposal consistently says it is independent, additive, optional, and non-normative. Keeping official BrAPI v2.1 contracts frozen and using `/genx/v1/` for GenX-native routes is a sound compatibility boundary.

### 2. Domain taxonomy

The D1–D7 scientific-domain model and C1–C9 cross-cutting-capability model are conceptually strong. Separating scientific ownership from cross-cutting concerns such as provenance, execution, terminology, and security avoids treating every technical capability as a scientific domain.

### 3. Endpoint identity and traceability

The stable `catalogId` metadata, operation identifiers, full route identity, semantic-neighbour records, and fail-closed registry checks are valuable. They reduce accidental route collisions and semantic equivalence assumptions.

### 4. The original core RFCs are materially stronger

RFC-003 (Seed-Lot Ledger) is a good example. It explains the problem against the existing BrAPI `SeedLotTransaction`, distinguishes the wire contracts, uses fixed-scale decimal strings for quantities, defines ordering and replay/conflict behavior, records limitations, and includes falsifiers. It also correctly warns against automatically mirroring movements into both data streams before D-20 is resolved.

### 5. Current automation is useful

At the reviewed commit, both the GenX conformance workflow and the specification-build workflow succeeded:

- GenX conformance run: https://github.com/denishdholaria/BrAPI-genX/actions/runs/41497950148
- Specification build run: https://github.com/denishdholaria/BrAPI-genX/actions/runs/41497950252

The live reference-server job reported 21 static probes and 28 live probes passing. The static endpoint identity probe counted 462 GenX operations. This is meaningful evidence for the checks actually run.

## Main findings and risks

### P0 — Project identity and release status need correction

The repository's identity documents describe “Official BrAPI v3” as the community's official third major version. The official BrAPI specification site currently identifies v2.1 as the latest stable release and treats new-concept previews as work subject to change. Do not claim a released or endorsed v3 until the community publishes one.

The GenX OpenAPI metadata uses `3.0-draft`. This risks conflating GenX's independent release number with the official BrAPI major version. Define an independent GenX proposal/release scheme, such as `0.x.y`, and state the BrAPI compatibility target separately.

The GenX metadata also advertises `https://test-server.brapi.org/genx/v1` as its server. The official BrAPI server directory documents the community test server for official BrAPI routes, not a GenX deployment. Remove this server URL unless the community has explicitly deployed and authorised the GenX surface there. Use a clearly labelled local/reference server or a GenX-controlled deployment instead.

### P0 — Documentation and generated-catalogue drift

The repository's own current checks show 462 proposed GenX operations, but `Specification/BrAPI-GenX/README.md` still says 21. `Inventory/README.md` describes only the original small set of GenX modules and says D1, D2, D4, and D5 have no GenX specifications, although later modules have since been added. `DEVELOPMENT_WORKSHEET.md` still describes an October baseline, the old `BrAPI_genX` repository name, a `brapi-V2.1` branch baseline, and only RFC-001 through RFC-007.

The current conformance results document is also historical: its recorded runs stop in October, while the reviewed repository head is 2 November. Keep historical test results, but publish a current, commit-pinned status report and clearly separate historical evidence from current branch evidence.

There is a related governance issue: the central `DECISIONS.md` has D-01 through D-25, while newer RFCs introduce local-looking decision IDs such as D-448 through D-462. RFC-153 and RFC-155 both reuse D-460, D-461, and D-462 for different questions. Adopt one globally unique decision-ID mechanism or use RFC-scoped question IDs (for example, `RFC-155-Q1`).

### P1 — The long tail of RFCs is not yet at the depth of the original core

A sample of newer RFCs (including RFC-150 and RFC-152 through RFC-155) shows a short, highly templated structure: a generic problem statement, a one-paragraph object definition, three standard operations, generic immutability/replay rules, and a few deferred questions. That is a useful scaffold, but it is not enough to define an interoperable scientific contract.

For example:

- **BreedingPipeline:** the project index describes ordered stage gates, but the schema has only a single `pipelineStage` string. It does not model an ordered collection of stages, gate criteria, transitions, or stage-specific evidence. The request requires only an identifier; the breeding-program reference, pipeline type, stage, and target trait are optional. Several semantic fields are unbounded strings.
- **RemoteSensingMetadata:** the sampled schema has platform, sensor, acquisition date, coordinate reference system, and resolution, but the date and coordinate reference system are unformatted strings and the resolution is an untyped string such as `10m`. It lacks the typed relationships and constraints needed for reliable cross-system interpretation of acquisition, sensor, product, spatial footprint, and processing context.
- **SchemaMapping:** mapping rules are represented as a free-text string (example: `field1->fieldA`). The contract does not yet define a mapping language, schema-version references, execution semantics, validation, or transformation failure behavior.
- **ConformanceProbe:** expected and actual responses are strings rather than structured request/response evidence. More importantly, it is not yet clear why conformance-test artefacts should be a standard breeding-data resource rather than a tooling concern.
- **CapabilityNegotiation:** the proposal introduces a stored negotiation record, but the need for a persistent domain resource should be justified against the existing capability-advertisement/negotiation contract.

This does not mean these concepts are invalid. It means each requires domain analysis before its schema can be called complete.

### P1 — Ambika is a domain catalogue, not an API-generation checklist

Ambika explicitly describes itself as a target-state domain catalogue and governance instrument, not an endpoint roadmap, implementation inventory, or evidence that capabilities are implemented. A module boundary in Ambika does not automatically imply a public API resource.

Use Ambika to discover candidate responsibilities and ownership boundaries. For every proposed GenX resource, separately establish:

- a cross-organisation interoperability use case;
- the authoritative domain fact and its lifecycle owner;
- why BrAPI v2.1 resources are insufficient, including adjacent concepts and any non-equivalence;
- external standards or vocabularies that should be reused;
- identifiers, relationships, units, cardinality, constraints, and temporal/spatial semantics;
- which operations are truly needed by independent implementers.

The legacy BijMantra endpoint inventory is useful requirements evidence, but it is not a measure of the standard's required scope. Product, user-interface, AI orchestration, authentication, administration, and infrastructure endpoints should not become GenX scientific resources merely because they exist in a local application.

### P1 — Conformance coverage is much narrower than endpoint count

The current live suite passes 28 probes, but those probes exercise the original core surface: jobs, provenance, variable terms, lot ledger, models/inference, variant-matrix references, FAIR packages, and telemetry. The second TypeScript/Bun reference server is documented as covering only the RFC-001 core plus RFC-004 inference subset.

The 462-operation identity check proves that operations have registered identities and that recorded overlaps are accounted for. The static checks also verify references and selected fixture properties. They do not prove the scientific semantics or behavior of the 154-plus newer module contracts.

The latest successful specification-build workflow is not proof that GenX is accepted by the official BrAPI generator: the repository deliberately keeps GenX inert to the frozen v2.1 generation pipeline. Treat the build and conformance results as evidence for their actual scope, not a general standards-conformance claim.

### P1 — Security and durability remain open contract decisions

The repository correctly records unresolved decisions around authentication profiles and scopes (D-22), tenant identity (D-03), digest canonicalisation (D-02), capability mapping (D-21), job-type advertisement (D-23), idempotency equivalence (D-24), and idempotency retention and durability (D-25).

The reference server is explicitly in-memory, single-process, non-durable, and has no effective authentication. It is suitable for exercising prototype behavior, not proving production security, tenancy, durable idempotency, or multi-replica guarantees. These limitations must remain prominent in adoption material.

### P1 — Some new resources need a stronger boundary decision

The proposal should distinguish public scientific interoperability resources from local platform/administrative resources. Examples such as conformance-probe storage, schema-mapping administration, and capability-negotiation history may be more appropriate as implementation tooling or platform APIs unless a clear multi-organisation exchange use case is demonstrated.

## Standards overlap requiring care

BrAPI v2.1 already defines `SeedLotTransaction`. GenX `LotLedgerEntry` is structurally different: the official transaction describes a movement between source and destination seed lots with numeric amount, while the GenX ledger is a per-lot append-only, ordered event using a fixed-scale decimal string, actor/provenance, and replay/conflict semantics.

The GenX RFC correctly recognises this as a semantic overlap, not a proven wire-compatible replacement. Keep D-20 open until there is an explicit event-correlation and authority model, mapping-loss analysis, and safe dual-read/dual-write guidance. Do not silently mirror or double-count the two streams.

Likewise, claims that BrAPI v2.1 has “no place” for a domain concept should be tested against related official resources such as BreedingMethod, Program, Trial, Study, ObservationUnit, Observation, ObservationVariable, Trait, Method, and Scale. “Related but not equivalent” is often the correct answer; the RFC should document why.

## Maturity assessment

| Dimension | Assessment | Rationale |
|---|---|---|
| Project separation and optional namespace | Strong | Clear non-normative stance and `/genx/v1/` boundary |
| Scientific-domain classification | Strong foundation | D1–D7 plus C1–C9 is a useful taxonomy |
| Endpoint identity and registry | Strong engineering | Stable IDs, route checks, semantic links, generated catalogues |
| Original core contracts (RFC-001–007) | Prototype-grade proposal | Better problem framing, invariants, falsifiers, and test evidence |
| Newer domain RFCs | Early draft / scaffold | Many require substantial domain-specific semantics and review |
| Static and live conformance | Good for core scope | 21 static and 28 live checks pass; coverage does not scale to 462 operations |
| Independent implementation evidence | Limited | TypeScript/Bun subset; no external adopter evidence for the long tail |
| Security and durability | Not established | Explicitly unresolved and absent from reference server |
| Documentation/governance freshness | Needs remediation | Conflicting counts, stale inventories, old branch records, duplicate decision IDs |
| Standards-readiness | Not ready | Requires domain review, contract completion, governance, and independent validation |

## Recommended next actions

### Phase 0 — Freeze expansion and repair the project control plane

1. Pause bulk RFC/schema generation; do not delete existing work.
2. Correct the official BrAPI release wording and the independent GenX version policy.
3. Remove or correct the unverified official test-server GenX URL.
4. Regenerate endpoint catalogues and reconcile README, inventory, worksheet, and conformance status to the reviewed commit.
5. Resolve decision-ID collisions and establish a single decision register with owners, status, rationale, and evidence.
6. Record the real human maintainer/steward and the review authority; do not let a historical agent worksheet imply an institutional standards role.

### Phase 1 — Establish a mandatory RFC/specification quality bar

Every new RFC should include:

1. A real cross-organisation use case and intended adopters.
2. Existing BrAPI coverage analysis, with exact resource/schema/operation references.
3. Domain definitions, authoritative owner, lifecycle, identifiers, and relationships.
4. Field-level types, requiredness, cardinality, units, vocabularies, temporal/spatial semantics, and constraints.
5. Operation behavior, filters, pagination, state transitions, side effects, idempotency, and error semantics.
6. Valid and invalid examples, edge cases, privacy/security implications, and provenance requirements.
7. External standards considered and a reasoned choice to reuse or not reuse them.
8. A compatibility/crosswalk analysis that does not assume equivalence from similar names.
9. Explicit acceptance criteria and falsifiers.
10. Static, schema, behavior, and independent-implementation tests appropriate to the claim.

### Phase 2 — Pilot a small number of high-value domains

Do not standardise 154-plus resource families simultaneously. Select a small pilot set with genuine multi-organisation value. A reasonable review queue is:

- BreedingPipeline / ExperimentalDesign (D2), with an explicit mapping against Program, Trial, Study, and BreedingMethod.
- RemoteSensingMetadata / VegetationIndex / CloudMask (D5/D4), with typed geospatial and sensor semantics.
- PhenotypeCapture / repeated measurements (D4), anchored to existing BrAPI observation concepts.
- SeedLot ledger (D6), only after D-20 is resolved.
- VariantMatrix (D3), with external genomics standards and access-control boundaries.
- Provenance and asynchronous Jobs as cross-cutting contracts, after the open digest, security, and idempotency decisions are resolved.

The pilot set should be narrowed further by scientific stakeholders and prospective adopters before implementation expands.

### Phase 3 — Scale conformance only after the contracts are stable

For each pilot resource, add fixtures for valid and invalid data, schema validation, behavior tests for every operation, mutation tests, pagination and error tests, replay and concurrency tests where relevant, and at least one independent implementation. Keep prototype-server evidence separate from durable, authenticated, multi-tenant deployment evidence.

## Final recommendation

Treat BrAPI-GenX as an **advanced exploratory specification corpus with a useful, partly tested core**, not as a completed next-generation BrAPI standard. The core architecture and engineering controls are worth preserving. The next milestone should be **specification quality and governance consolidation**, not more endpoint generation.

## Review basis and limitations

This was a read-only review of the connected GitHub `main` branch at the commit shown above, plus relevant Ambika catalogue material and official BrAPI sources. I inspected repository structure, selected RFCs and schemas, the endpoint registry/checkers, decision and inventory documents, and current GitHub Actions runs/logs. I did not clone the repository or execute the scripts locally. The module-level examples are representative samples, not a line-by-line scientific review of all 155 RFCs.

Key repository locations:

- https://github.com/denishdholaria/BrAPI-genX/tree/main/Specification/BrAPI-GenX
- https://github.com/denishdholaria/BrAPI-genX/blob/main/Specification/BrAPI-GenX/DECISIONS.md
- https://github.com/denishdholaria/BrAPI-genX/blob/main/Specification/BrAPI-GenX/Conformance/README.md
- https://github.com/denishdholaria/BrAPI-genX/blob/main/Specification/BrAPI-GenX/Inventory/README.md
- https://github.com/denishdholaria/bijmantra-project/tree/main/Ambika/ideal-module-catalog
- https://brapi.org/specification
- https://brapi.org/servers
