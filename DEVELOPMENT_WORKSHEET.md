# BrAPI_genX — Development Command Worksheet

**Purpose:** Master work ledger for independent, slice-based development of the BrAPI GenX proposal.  
**Maintainer / technical lead:** OpenAI assistant (independent development lead, as delegated by repository owner).  
**Last reviewed:** 2026-10-15  
**Planning branch:** `work/development-command-worksheet`  
**Baseline branch:** `brapi-V2.1`  
**Repository:** [denishdholaria/BrAPI_genX](https://github.com/denishdholaria/BrAPI_genX)

> **Standards-status guardrail:** The existing GenX documentation explicitly labels GenX as a proposal that is *not accepted and not normative*. This worksheet is a development plan, not community ratification. No entry here changes the status or authority of BrAPI or GenX.

### Terminology

- **BrAPI:** Breeding Application Programming Interface.
- **GenX:** working name for the proposed next-generation BrAPI design surface.
- **RFC:** Request for Comments; here, a numbered design proposal.
- **JSON:** JavaScript Object Notation.
- **JCS:** JSON Canonicalization Scheme.
- **CI:** continuous integration.
- **SHA-256:** Secure Hash Algorithm with a 256-bit digest.
- **UTC:** Coordinated Universal Time.
- **I-JSON:** Internet JSON profile for interoperable JSON data.

---

## 1. Commander's mandate

Independently advance a useful, interoperable plant-breeding standards proposal while preserving the work and authority of the BrAPI community.

I will:

1. Make repository-grounded choices and record why each slice is selected.
2. Work in small, reviewable branches; avoid mixing unrelated slices.
3. Keep established BrAPI V2.1 behavior and files unchanged.
4. Prefer existing, mature standards over bespoke reinvention, but verify their fit for plant-breeding data before proposing adoption.
5. Treat specifications, examples, conformance probes, and independent implementations as one evidence chain.
6. Never describe a prototype or reference test server as production-ready.
7. Separate engineering decisions that can be made locally from decisions that require implementer, governance, security, or BrAPI community authorization.
8. Update this worksheet when evidence changes; mark items blocked when they need external authority rather than silently deciding for the community.

## 2. Repository baseline (observed, 2026-10-14)

| Area | Observed baseline | Development implication |
|---|---|---|
| Default branch | `brapi-V2.1` | Do not use the release-named branch for independent work. |
| BrAPI V2.1 modules | Core, Phenotyping, Genotyping, Germplasm | Preserve these contracts; do not rewrite V2.1 to accommodate GenX. |
| GenX proposal | `Specification/BrAPI-GenX/`, RFC-001 through RFC-007 | Additive, optional proposal under `/brapi/v3/`; status remains non-normative. |
| Decision register | `Specification/BrAPI-GenX/DECISIONS.md` | D-01…D-23 are deferred decisions; A-01…A-12 are reviewable drafting decisions. |
| Conformance authority | `Specification/BrAPI-GenX/Conformance/probes.yaml` | The probe file declares intended conformance; the runner must remain aligned with it. |
| Recorded test evidence | `Conformance/RESULTS.md`, dated 2026-09-07 | Historical recorded evidence is strong, but must be rerun before asserting the current baseline. |
| Existing conformance results | Recorded 20/20 static probes; 48/48 live probes against Python reference server; 13/13 applicable live probes against TypeScript/Bun server; 9/9 differential steps agree. | Keep this evidence and extend it, rather than replacing it with unverified claims. |
| Known cross-runtime boundary | Python and TypeScript digest agreement was recorded for ASCII payloads; non-ASCII escaping differs. This is tracked as D-02. | Candidate first standards slice: canonicalization and digest interoperability. |
| Reference-server limits | In-memory, single-process prototypes; no effective authentication or durable persistence. Some concurrency and production behaviors are explicitly unproven. | Production architecture is a later, separately evidenced workstream. |
| Visible existing workflow | `.github/workflows/generate-schema.yml` builds and compares generated specification artifacts. It does not visibly invoke the GenX conformance runner. | Add a dedicated conformance gate as an enabling task; do not tangle it with artifact generation. |
| Governance state | No pull requests or open issues were returned by the repository connector during the initial survey. | This is not evidence of community consensus. |

### Primary files used for this baseline

- [GenX overview](Specification/BrAPI-GenX/README.md)
- [Endpoint identity guardrails](https://github.com/denishdholaria/BrAPI_genX/blob/work/endpoint-identity-clarity/Specification/BrAPI-GenX/ENDPOINT-IDENTITY.md)
- [Machine-readable route-overlap register](https://github.com/denishdholaria/BrAPI_genX/blob/work/endpoint-identity-clarity/Specification/BrAPI-GenX/Conformance/endpoint-overlaps.yaml)
- [Recorded endpoint-identity test evidence](https://github.com/denishdholaria/BrAPI_genX/blob/work/endpoint-identity-clarity/Specification/BrAPI-GenX/Conformance/RESULTS.md#run-14--explicit-endpoint-meaning-and-non-equivalence-boundaries)
- [Decision register](Specification/BrAPI-GenX/DECISIONS.md)
- [Adoption guide](Specification/BrAPI-GenX/ADOPTION.md)
- [GenX conformance probes](Specification/BrAPI-GenX/Conformance/probes.yaml)
- [Recorded conformance results](Specification/BrAPI-GenX/Conformance/RESULTS.md)
- [GenX skeleton proposal](Specification/BrAPI-GenX/RFC-001-GenX-Skeleton.md)
- [Existing schema-generation workflow](.github/workflows/generate-schema.yml)

## 3. Non-negotiable engineering and standards guardrails

- **V2.1 remains frozen.** No GenX slice may change V2.1 request/response semantics.
- **GenX stays optional and additive.** A V2.1 client/server must not be made dependent on GenX-only behavior.
- **No silent normative upgrades.** A locally preferred design does not become a community decision by being implemented.
- **No premature generator wiring.** D-04 remains deferred; do not wire GenX into `generator/`, `BrAPI-Schema/`, or generated release artifacts without an explicit decision.
- **No implicit authentication claims.** A Bearer header accepted by a test server is not proof that authorization is enforced.
- **No test-only success claims.** Every report must distinguish static validation, reference-server tests, independent implementation agreement, external-server evidence, and production evidence.
- **One slice, one branch, one reviewable result.** Keep changes scoped; do not mix generated artifacts with hand-authored contracts.
- **Every slice needs falsifiers.** State what evidence would prove the proposed behavior incorrect, not only what should pass.
- **External standards are referenced, not copied wholesale.** Check scope, maturity, license, interoperability, and semantics before adopting an external specification.

## 4. Slice workflow

Each slice follows this sequence:

1. **Frame:** state the problem, hypothesis, non-goals, dependencies, and decision authority.
2. **Inspect:** read the relevant RFCs, definitions, probes, fixtures, recorded evidence, and external standards.
3. **Specify:** write the behavior and edge cases before implementing a test or prototype.
4. **Prove:** add deterministic fixtures and falsifiable tests; where practical, use independently written implementations.
5. **Review:** examine backward compatibility, security implications, data semantics, and unresolved governance questions.
6. **Record:** update the relevant decision/RFC only at the appropriate status; update this worksheet with evidence and follow-on work.
7. **Gate:** recommend merge, revise, or block. Do not treat a green prototype test as community acceptance.

### Definition of done for an individual slice

A slice is not complete until it has: (a) scoped change set; (b) explicit acceptance criteria; (c) repeatable tests or documented reason they cannot run; (d) evidence and known limitations; (e) backward-compatibility assessment; (f) decision status and required external approvals; and (g) a clear next step.

## 5. Master development worksheet

Priority guide: **P0** = foundational or blocks reliable progress; **P1** = high-value follow-on; **P2** = depends on additional evidence or stakeholder policy. Statuses: **PLANNED**, **ACTIVE**, **BLOCKED**, **DONE**.

| Slice | Priority | Workstream | Objective / bounded output | Depends on | Governance gate | Status |
|---|---:|---|---|---|---|---|
| CMD-00 | P0 | Development control | Establish this worksheet, status vocabulary, guardrails, and evidence ledger. | Repository inspection | None | DONE (worksheet established) |
| ENG-01 | P0 | Conformance automation | Dedicated continuous-integration workflow runs endpoint mutation tests, static conformance, and all live probes against an in-memory reference server, separately from schema generation. A future independent-implementation/differential run remains planned. | Existing runner, fixtures, and GenX test server | Engineering proposal only; no normative change | VERIFIED on review head `0cb3db23879b47e82d7bd10da61aa398bd0b04fd`: 12 mutation tests, 21 static probes, 28 live probes passed in [run 38561330221](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38561330221). The single-commit review head `0cb3db23879b47e82d7bd10da61aa398bd0b04fd` has now passed both [conformance run 38561330221](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38561330221) and [schema-generation/build run 38561324427](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38561324427). |
| ENG-02 | P0 | Endpoint identity and semantic collision guardrails | Stable action-specific operation IDs for every GenX operation; explicit full-path/schema/action catalogue; exact route-overlap registry; semantic-neighbor ledger; fail-closed static checks and mutation tests. GenX variable-term route is now `/brapi/v3/variable-terms`, intentionally distinct from V2.1 `/brapi/v2/variables`. | Endpoint YAMLs/schemas, V2.1 contracts, endpoint catalogue, overlap register, reference server | Engineering guardrail only; D-20 remains unresolved and requires implementer/community review | VERIFIED on one-commit review head `0cb3db23879b47e82d7bd10da61aa398bd0b04fd`: 12 mutation tests, 21 static probes, 28 live probes passed; the full schema-generation/build passed on the current one-commit review head; draft review request #1 is open |
| STD-01 | P0 | Scientific provenance and digest integrity | Resolve the known canonical JSON / digest interoperability boundary, define field-level preimages, and recommend an evidence-backed profile. D-02 remains open until authorized. | ENG-02 endpoint identities; current Python/Bun implementations; digest field scope inventory | **Community/implementer review required before adopting a normative rule** | ACTIVE — corpus, field inventory, option comparison, and cross-runtime mutation tests are complete; JCS remains only a candidate. [Draft PR #2](https://github.com/denishdholaria/BrAPI_genX/pull/2), [Run 18](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687419662). |
| STD-02 | P1 | Provenance envelope | Specify the exact digest scope, evidence-link semantics, algorithm/version identity, uncertainty, and safe handling of unknown fields. Keep result provenance portable across breeding tools. | STD-01; RFC-001 | Review of any schema semantics that affect interoperability | PLANNED |
| STD-03 | P1 | Asynchronous jobs | Tighten lifecycle transitions, idempotency scope/retention, error envelope, cancellation races, expiration and retrieval guarantees. Add mixed-key/type concurrency evidence. | ENG-01; RFC-001; D-01 and D-02 evidence | D-01 needs community agreement before claiming settled status | PLANNED |
| STD-04 | P1 | Capability negotiation | Make advertised capabilities resolve to exact operations and accepted job-type tokens; define safe version matching and preserve V2.1-only fallback. | ENG-01; endpoint identity; ServerInfoV3 and Jobs contracts | D-21: route/version mapping; D-22: security scopes/auth profiles; D-23: job-type advertisement/compatibility. All require appropriate implementer/community review. | ACTIVE — operation mapping and `jobTypes[]` remain optional experimental metadata. [Draft PR #3](https://github.com/denishdholaria/BrAPI_genX/pull/3), [Run 17](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38690043457), [build](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38690043404). |
| DOM-01 | P1 | Ontology governance | Clarify term/version ordering, immutability, supersession, and versioned Trait/Method/Scale references. | RFC-002; D-05, D-06 | Community ontology/versioning review | PLANNED |
| DOM-02 | P1 | Seed-lot ledger | Analyze unknown-lot behavior and atomic multi-lot transfer needs; preserve append-only audit semantics and exact quantities. | RFC-003; current ledger probes | D-07/D-08 require implementer agreement | PLANNED |
| DOM-03 | P1 | Model registry and inference | Define model approval/revocation governance and interoperable artifact transport without conflating registration with trusted execution. | RFC-004; STD-01/02; D-09/D-10 | Governance and security review | PLANNED |
| DOM-04 | P1 | Variant matrix references | Validate external-format references, content digests, retrieval and authorization boundaries; keep bulk genomic data outside the API envelope. | RFC-005; STD-01; D-11/D-12/D-19 | Genomics implementer and access-control review | PLANNED |
| DOM-05 | P2 | FAIR packages | Resolve identifier minting, restricted-access workflow, and embargo metadata visibility. | RFC-006; provenance and digest decisions | Repository/policy and privacy review; D-13–D-15 | PLANNED |
| DOM-06 | P2 | Sensor telemetry | Define sensor identity, timestamp/time-zone policy, quality flags, aggregation semantics, and gap handling. | RFC-007; D-16–D-18 | Scientific/statistical and implementer review | PLANNED |
| ADOPT-01 | P1 | Adopter kit | Publish versioned conformance commands, fixtures, minimal client examples, migration guidance, and a clear proposal-status statement. | Stable core contracts and ENG-01 | Documentation review; no implied acceptance | PLANNED |
| PILOT-01 | P2 | External validation | Seek independent implementations or staging-server tests and record deviations without treating one implementation as normative. | Stable relevant slices; willing implementers | External participation required | BLOCKED (no external implementer evidence yet) |

## 6. Priority sequence — endpoint identity first, digest interoperability second

### Active slice: ENG-02 — endpoint identity and semantic collision guardrails

The highest-risk confusion discovered so far was semantic overlap: V2.1 `/brapi/v2/variables` returns `ObservationVariable`, while the initial GenX proposal reused relative `/variables` for `VariableTerm` with different schema and write semantics. I changed the proposal to `/brapi/v3/variable-terms` so route names themselves signal the distinction. Separately, V2.1 `SeedLotTransaction` and GenX `LotLedgerEntry` both describe seed-lot movements but have no proven mapping. Humans, AI agents, logs, and generated clients must not infer equivalence from a shortened route, similar noun, or shared field names.

The implementation branch is [`work/endpoint-identity-clarity`](https://github.com/denishdholaria/BrAPI_genX/tree/work/endpoint-identity-clarity). It adds stable operation IDs to all 21 current GenX operations, the endpoint identity guide and catalogue (each operation requires a meaning and “boundary / do not infer” note), a machine-readable cross-generation overlap register, static probe S-21, a fail-closed checker, twelve mutation tests, and separate static and live-reference-server CI jobs. The latest result is [Conformance/RESULTS.md, Run 14](https://github.com/denishdholaria/BrAPI_genX/blob/work/endpoint-identity-clarity/Specification/BrAPI-GenX/Conformance/RESULTS.md#run-14--explicit-endpoint-meaning-and-non-equivalence-boundaries); The review branch has been compacted to one commit (`0cb3db23879b47e82d7bd10da61aa398bd0b04fd`) without changing the project tree: its tree SHA exactly matched the previously tested `a3e881549e9fb913de978805cf79767c75d945fb`. The new conformance run [38561330221](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38561330221) passed 12 mutation tests, 21 static probes, and 28 live probes. Schema generation/build passed on the identical tree in [run 38560852819](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38560852819); a fresh run against the one-commit revision is in progress. [Draft pull request #1](https://github.com/denishdholaria/BrAPI_genX/pull/1) is open; it is mergeable but not merged.

#### ENG-02 acceptance criteria

- Every GenX operation has one stable, unique `operationId` in an action-plus-resource form, a non-empty summary, and a substantive description.
- The stable identity used by documentation, tests, logs, generated clients, and agents includes API generation/base path, HTTP method, full route template, operation ID, request/response schema names, effects, identity/version semantics, and relevant authorization context.
- Every exact method/path overlap between V2.1 and GenX is registered with a relationship class and plain-language description; added or stale entries fail the static check.
- Semantically adjacent resources are reviewed even when paths differ. D-20 keeps `SeedLotTransaction` ↔ `LotLedgerEntry` equivalence, mapping and double-count behavior unresolved, prohibiting implicit assumptions.
- No frozen V2.1 contracts, generated release artifacts, or generator wiring are changed.
- Static and live workflows pass; deliberate mutations to remove an operation ID, duplicate an ID, create an unregistered overlap, stale the register, or desynchronize the catalogue all fail.

#### Immediate ENG-02 verification checklist

- [x] Ran the static workflow and inspected the recorded result.
- [x] Confirmed the renamed variable-term route removed the three `/variables` overlaps; only the intended `GET /serverinfo` relative-path overlap remains registered.
- [x] Static probe S-21 matched all 21 operation IDs to the endpoint YAML and human catalogue.
- [x] The checker validates the seven semantic-neighbor records for completeness, unique IDs, and recognized risk values.
- [x] Twelve mutation tests proved covered invalid states fail, including missing meaning/boundary text; the valid control passed.
- [x] All 28 live probes passed against the in-memory reference server, including variable-term replay and conflict behavior.
- [x] Confirmed schema-generation/build passed on the current one-commit review head in [run 38561324427](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38561324427).
- [x] Opened draft pull request [#1](https://github.com/denishdholaria/BrAPI_genX/pull/1) for review; it remains unmerged. Do not convert to ready or merge until domain semantics, D-20, and broader interoperability/governance are reviewed.

### Active slice: STD-01 — digest interoperability evidence and remaining decision

Phase 1 now has an experimental, technology-neutral corpus at [digest-vectors.json](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-01-digest-vectors/Specification/BrAPI-GenX/Conformance/digest-vectors.json), a [digest scope inventory](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-01-digest-vectors/Specification/BrAPI-GenX/Conformance/DIGEST-SCOPE-INVENTORY.md), a [candidate decision brief](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-01-digest-vectors/Specification/BrAPI-GenX/Conformance/DIGEST-DECISION-BRIEF.md), and independent Python and TypeScript/Bun runners. [Run 18](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687419662) passed 12 structured-JSON vectors, 2 exact-byte cases, 5 rejection-policy cases (four JSON/JCS input constraints plus one conservative numeric guard), and 2 legacy divergence diagnostics in both runtimes; five corpus mutations were rejected in each runtime (10 mutation checks). The same run passed 12 endpoint-identity mutation tests, 21 static probes, and 28 live probes. These results do not resolve D-02 or migrate the reference servers. The code-review request is [draft PR #2](https://github.com/denishdholaria/BrAPI_genX/pull/2).



### Why this slice is first

GenX uses digests across provenance, model artifacts, variant matrices, and other payload references. The existing cross-runtime exercise narrowed the remaining discrepancy to non-ASCII serialization: the Python reference uses escaped Unicode output in its current canonicalization helper, while the TypeScript implementation emits UTF-8 characters directly. If the canonical byte sequence is not fully specified, equivalent scientific records can produce different digests across implementations.

This problem is central, cross-cutting, reproducible, and bounded. It is a better first standards slice than introducing another domain object.

### STD-01 hypothesis

A precise, testable canonicalization contract plus published golden vectors can make digest computation deterministic across independent runtimes without altering BrAPI V2.1.

### STD-01 first deliverables

1. A candidate comparison note covering JSON Canonicalization Scheme (JCS, RFC 8785), its input constraints and trade-offs, and any practical alternatives.
2. A technology-neutral corpus of canonical input → exact canonical bytes → expected SHA-256 digest vectors.
3. Edge-case coverage for:
   - object-key order and insignificant whitespace;
   - ASCII, non-ASCII and escaped strings;
   - Unicode code-point preservation (do not assume normalization);
   - numeric formatting, negative zero, exponent notation, and large-integer precision;
   - nested objects, arrays, nulls, booleans and empty values;
   - duplicate property names and invalid/non-I-JSON input;
   - the distinction between exact decimal quantities represented as strings and measurement values represented as JSON numbers.
4. Independent Python and TypeScript/Bun verification of the same vector corpus; keep the expected values independently calculated or checked against a trusted implementation.
5. A recommendation with options, compatibility impacts, migration considerations, and an explicit list of unresolved decisions.

### STD-01 candidate to evaluate, not pre-approve

RFC 8785 (JCS) is a serious candidate because it specifies deterministic property sorting and primitive serialization for hashable JSON. It is an **Informational RFC, not an Internet Standards Track specification**, and it imposes I-JSON / IEEE 754 double-precision constraints. The evaluation must therefore test fit for scientific data rather than adopting it merely because it exists. In particular, high-precision quantities may need string representations, and Unicode is preserved as supplied rather than normalized.

Reference: https://datatracker.ietf.org/doc/html/rfc8785

### STD-01 acceptance criteria

- Same logical JSON input produces the same canonical UTF-8 bytes and SHA-256 digest in the supported independent runtimes.
- Vectors cover all declared edge classes and fail when a deliberate mutation is introduced.
- The rule is explicit enough that a third implementation can pass without copying Python or TypeScript implementation details.
- No changes to BrAPI V2.1 behavior or existing V2.1 module definitions.
- Findings distinguish a proposed local recommendation from an authorized standards decision.
- If no candidate provides acceptable scientific and cross-language behavior, document the gap and stop rather than quietly inventing an underspecified rule.

### STD-01 explicitly out of scope

- Ratifying D-02 on behalf of the BrAPI community.
- Rewriting all reference-server or scientific compute implementations.
- Wiring GenX into the existing V2.1 generator pipeline (D-04 remains deferred).
- Claiming cryptographic authenticity from a bare digest; a digest detects byte/content mismatch only when the expected digest itself is trusted.
- Production key management, signing, or authorization.

### STD-01 falsifiers / stop conditions

- Supported runtimes cannot produce identical canonical bytes from the same accepted input under the candidate rule.
- Edge cases require undocumented runtime-specific behavior.
- The candidate changes the meaning of accepted scientific values or silently rounds precision-sensitive numbers.
- A proposed migration would invalidate existing digests without a practical versioning/migration strategy.
- The solution depends on silently changing existing V2.1 schemas or semantics.

## 7. STD-01 execution checklist (active; D-02 remains unresolved)

- [x] Inspect current digest-bearing schemas and prose; record each discovered digest field, scope, and unresolved preimage questions in [DIGEST-SCOPE-INVENTORY.md](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-01-digest-vectors/Specification/BrAPI-GenX/Conformance/DIGEST-SCOPE-INVENTORY.md).
- [x] Read the D-02 discussion and compare the current canonicalization functions in the Python and TypeScript/Bun reference servers; legacy serialization differences are now captured by reproducible diagnostics.
- [x] Create the experimental candidate vector corpus in dedicated branch `work/std-01-digest-vectors`; no V2.1 files or generated outputs changed.
- [x] Add automated Python and TypeScript/Bun tests against the same vectors; both passed in [run 38686137872](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38686137872).
- [x] Add cross-runtime mutation tests and record exact results: five mutations (wrong canonical bytes, wrong structured digest, wrong exact-byte digest, missing required edge vector, duplicate vector ID) rejected in Python and TypeScript/Bun; [Run 18](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687419662).
- [x] Write [DIGEST-DECISION-BRIEF.md](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-01-digest-vectors/Specification/BrAPI-GenX/Conformance/DIGEST-DECISION-BRIEF.md) comparing legacy behavior, RFC 8785/JCS, custom canonicalization, and exact-byte hashing, with migration and review questions.
- [x] Update this worksheet with the branch, review request, and automated evidence links.
- [ ] Stop at the governance gate before presenting a normative decision as settled.

## 8. Decision / evidence ledger

| Date | Entry | Evidence / outcome | Resulting action |
|---|---|---|---|
| 2026-10-14 | Initial repository assessment | Read GenX overview, decision register, adoption guide, RFC-001, conformance probe manifest, recorded results, reference-server sources, differential checker, Gradle generator tasks, and the schema-generation workflow. | Preserve existing foundation; do not restart or rewrite completed work. |
| 2026-10-14 | Sequence the next slices | Endpoint identity and semantic collision safety is the immediate P0 risk; digest interoperability remains a foundational slice after the endpoint identity gate. RFC 8785 is a candidate, not a predetermined decision. | ENG-02 active; STD-01 queued, with D-02 open until authorized. |
| 2026-10-14 | Create master worksheet | Added on `work/development-command-worksheet`, separate from `brapi-V2.1`. | Use this file as the single work queue and status ledger for future slices. |
| 2026-10-15 | STD-04 phase 1 — ServerInfoV3 operation and job-type mapping | Added optional experimental `operations[]` and `jobTypes[]`, a capability registry, static/live drift checks, and a 29-case mutation suite. [Draft PR #3](https://github.com/denishdholaria/BrAPI_genX/pull/3), [Run 17](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38690043457). | Keep D-21 (operation mapping/version tokens), D-22 (security scopes/auth profiles) and D-23 (job type policy) open pending appropriate review. |
| 2026-10-15 | STD-01 phase 1 — digest evidence and proposed trade-offs | Shared corpus, field-level scope inventory, non-normative option comparison, and cross-runtime mutation tests now exist on `work/std-01-digest-vectors`. [Run 18](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38687419662) passed all candidate vectors, 10 mutation checks, 12 endpoint-identity mutation tests, 21 static probes, and 28 live probes. Draft [PR #2](https://github.com/denishdholaria/BrAPI_genX/pull/2) remains open. | Keep D-02 open. Next: review the exact preimage and migration questions with implementers/community; only then select/version the candidate profile and migrate GenX helpers. |



## 10. BijMantra cross-repository evidence register (added 2026-10-14)

Purpose: use BijMantra as an implementation-evidence corpus for discovering practical interoperability problems and candidate use cases. It is **not** the authority for BrAPI, and product-specific behavior must not be promoted into GenX without external standards and implementer review.

### Repositories inspected

- Private primary source: [denishdholaria/bijmantraorg](https://github.com/denishdholaria/bijmantraorg), default branch `main`, private, repository access verified.
- Public comparison repository: [denishdholaria/bijmantra](https://github.com/denishdholaria/bijmantra), default branch `sustainable-path`, public, repository access verified.
- Standards proposal: [denishdholaria/BrAPI_genX](https://github.com/denishdholaria/BrAPI_genX), default branch `brapi-V2.1`.

The current private BijMantra repository README describes a pre-production Rust cellular capability fabric, with the legacy Python code retained as requirements and collision evidence. The public repository is an older, different tree with legacy implementation emphasis. Treat them as different snapshots, not as interchangeable or presumed synchronized sources. Use private `main` for current repository-grounded observations unless a task specifically asks about the public branch.

### Verified source observations

| Evidence ID | Observation | Source | Standards implication |
|---|---|---|---|
| BM-E01 | The private project separates BrAPI V2 endpoints from other BijMantra APIs and capability-owned Rust contracts. Its architecture says BrAPI is an adapter, not the authoritative writer. | `AGENTS.md`, `ADR-001-rust-cellular-capability-fabric.md`, `docs/architecture/API-OWNERSHIP.md` | GenX should define interoperable wire contracts, not impose any single server's internal service/cell/database architecture. |
| BM-E02 | A committed audit dated 2026-10-01 reports 241 BrAPI-declared paths/operations in its counting convention, of which 238 were mounted; it separately reports 1,069 live-mounted routes excluding tests and 1,847 legacy Python HTTP method/path operations. | `docs/2026-10-01-report-python-rust.md` | These are source-reported counts, not independently recomputed here. Endpoint/operation/route must be defined before making count-based claims. Optional dependencies and duplicate method/path pairs can alter observed mounted surface. |
| BM-E03 | The same audit reports five duplicate method/path pairs, including duplicate `GET /brapi/v2/serverinfo`. | Same audit | Test generators and conformance tools should detect duplicate operation registration, route shadowing, and runtime/schema drift. This is a potential conformance-harness improvement, not evidence of a BrAPI standards defect. |
| BM-E04 | BijMantra's BrAPI response transport has generic envelopes and many untyped `any` payloads; some canonical domain types are orphaned or duplicated across layers. | `.ai/decisions/R7-evidence-pack-domain-type-ownership.md`, `.ai/decisions/E-evidence-pack-api-ownership.md` | Standards fixtures should assert full schema/type semantics, not only envelope shape. Distinguish domain types, transport DTOs, persistence rows, and UI projections. |
| BM-E05 | BijMantra records real implementation gaps between legacy endpoints and current cell-owned contracts, including route-shape drift, missing methods, differing shapes, and unclear route ownership. | `docs/architecture/API-OWNERSHIP.md`, `.ai/tasks/RUST-FIRST-ROUTE-INVENTORY.md` | Prioritize a machine-readable conformance and operation-inventory gate that compares declared contract, actual mounted route, and behavior. Keep adapter conformance separate from internal persistence semantics. |
| BM-E06 | Scientific results in the Rust platform can carry input digests, worker digests, method/job identity, and explicit recomputation checks; the polyglot worker documents deterministic results accepted only when Rust recomputation matches. | `platform/boundary-polyglot/openapi/polyglot-v1.json`, `.ai/tasks/RUST-BACKEND-IMPLEMENTATION-PLAN.md` | Valuable use case for the digest slice: define exactly what is digested, canonical bytes, algorithm identifier/version, provenance scope, and independent verification. A digest alone is not an authenticity guarantee. |
| BM-E07 | The REEVU selection-evidence workflow records source cell, endpoint, schema version, response digest, and a query digest over request context and ordered source digests. | `.ai/decisions/REEVU-SELECTION-EVIDENCE-FREEZE.md` | Use as a concrete provenance/evidence-linking scenario for testing GenX proposals; do not standardize its product-specific query formula without a general requirement and review. |
| BM-E08 | The private project explicitly requires scientific method traceability: problem/estimand → model/formula/convention → implementation → validation → runtime provenance. | `.ai/skills/BIJMANTRA-SCIENTIFIC-REFERENCE-TRACEABILITY.md` | Add scientific reproducibility examples and method-identity questions to GenX provenance evaluation; separate scientific validity evidence from software-level digest integrity. |
| BM-E09 | The existing GenX decision register already documents that reference servers lack durable persistence and effective authentication, and that mixed concurrency/expiry behavior remains under-tested. | `Specification/BrAPI-GenX/DECISIONS.md`, `Conformance/RESULTS.md` | The next work should improve the contract and reproducible tests before any production server architecture is prescribed. |
| BM-E10 | The initial GenX draft reused relative `/variables` for a different resource contract; the feature branch removes this exact collision by using `/brapi/v3/variable-terms`. The catalogue now requires an explicit meaning and “boundary / do not infer” note. V2.1 `SeedLotTransaction` and GenX `LotLedgerEntry` remain semantically adjacent but unproven equivalents. | V2.1 `ObservationVariables/Variables_GET_POST.yaml`; GenX `RFC-002-Variable-Term-Governance.md`, `RFC-003-Seed-Lot-Ledger.md`, `ENDPOINT-IDENTITY.md` | Use full generation-qualified routes, stable operation IDs, schema names and effect descriptions; route distinction does not resolve the separately deferred inventory-event mapping. |

### Cross-repository use rules

1. BijMantra implementation is a **case study and potential test fixture source**, never the normative authority.
2. Reuse only abstract, generalizable requirements: stable identity, digest verification, evidence links, idempotent writes, explicit ownership, predictable error handling, and operation-to-contract conformance.
3. Do not copy BijMantra's Rust cell topology, route names, proprietary contracts, product verdict enums, or current application DTOs into GenX unless they solve a demonstrated multi-implementer problem.
4. The private repository's source-available/license policy applies to its code. For standards work, prefer newly authored examples and behavior-level descriptions; do not copy implementation source or substantial private-repository text into GenX. Verify licensing before reusing any implementation artifact.
5. Every cross-repository claim must identify source path, ref/commit where known, and whether it is source-reported, directly inspected, inferred, or independently tested.
6. The public and private BijMantra repos differ materially in branch and architecture state. Never infer one mirrors the other; confirm each repository's current branch and tree for the question at hand.

### Revised priority decision

**STD-01 remains the next foundational standards slice after ENG-02**, and its test corpus will include a scientific-evidence workflow modeled abstractly on the BijMantra source-digest pattern:
- source endpoint and contract/schema version;
- exact response bytes versus canonicalized parsed JSON (a choice that must be explicit);
- digest algorithm and canonicalization identifier/version;
- ordered versus set semantics for multiple sources;
- request/query digest scope and tenant/actor context boundaries;
- recomputation or independent-verification evidence;
- behavior when a source is unavailable, changed, redacted, or no longer resolvable.

Before declaring canonicalization complete, compare two distinct questions: (1) stable hashes of structured JSON values, and (2) integrity hashes of exact retrieved evidence bytes. Do not assume those are the same operation or should share a single canonicalization rule.

### Priority update — endpoint identity and contract drift

The master queue above places ENG-02 at P0. The endpoint identity slice has passing mutation, static, live, and schema-generation evidence; draft pull request [#1](https://github.com/denishdholaria/BrAPI_genX/pull/1) remains unmerged. STD-01 has since advanced independently on `work/std-01-digest-vectors`, with draft pull request [#2](https://github.com/denishdholaria/BrAPI_genX/pull/2); its cross-runtime candidate corpus is verified, but D-02 remains open. STD-04 is now under draft review in [PR #3](https://github.com/denishdholaria/BrAPI_genX/pull/3). The active branches are engineering proposals, not community acceptance.

### Evidence still required

- Recompute the BrAPI-specific operation inventory against the current private repository commit and distinguish route objects, unique paths, method/path operations, declared OpenAPI operations, and actually mounted handlers.
- Inspect exact response/schema validation behavior for representative operations in BijMantra's live BrAPI adapter; the route-count report alone does not prove conformance.
- Find or generate independent golden vectors for provenance digests, including non-ASCII values, exact-response hashing, number precision, and reordered object properties.
- Do not treat a BijMantra-only implementation pass as evidence of community acceptance.


### Active slice: STD-04 — capability negotiation boundary

Branch: [`work/std-04-capability-negotiation`](https://github.com/denishdholaria/BrAPI_genX/tree/work/std-04-capability-negotiation)  
Draft review: [PR #3 — Explicit capability operation mapping](https://github.com/denishdholaria/BrAPI_genX/pull/3)

The audit found that a capability name plus `methods[]` is not enough to identify an exact endpoint. `provenanceEnvelope` is an embedded schema, not a standalone route, but the earlier example advertised GET/POST in a way that could lead an agent to invent such a route. Capability-version tokens, advertised scopes, and auth-profile semantics were also ambiguous.

The branch proposes an **optional and experimental** `operations[]` mapping: full `/brapi/v3` route template, HTTP method, and stable OpenAPI operation ID. `methods[]` is a set summary of the methods in that map; it does not imply every method works on every route. The machine-readable registry is [capability-registry.json](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-04-capability-negotiation/Specification/BrAPI-GenX/Conformance/capability-registry.json), and the review note is [CAPABILITY-NEGOTIATION.md](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-04-capability-negotiation/Specification/BrAPI-GenX/ServerInfoV3/CAPABILITY-NEGOTIATION.md).

The current capability slice has [conformance run 38690043457](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38690043457): 29 capability-negotiation mutation tests, 12 endpoint-identity mutation tests, 22 static probes and 29 live probes passed, with zero failures or skips. Schema/specification validation succeeded; the latest full generation result is being rechecked in [run 38690043404](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38690043404). Run details are in [Conformance/RESULTS.md, Run 17](https://github.com/denishdholaria/BrAPI_genX/blob/work/std-04-capability-negotiation/Specification/BrAPI-GenX/Conformance/RESULTS.md#run-17--supported-job-type-advertisement-and-runtime-drift-guard).

- **Job-type discovery gap:** `JobNewRequest.jobType` requires a server-supported token, but the old `jobs` capability only advertised HTTP methods. Experimental `jobs.jobTypes[]` now lists the exact accepted runtime tokens (`germplasm_search`, `analysis`, `inference`); `export` is not advertised by this prototype. Static and live checks compare advertised values to the capability registry and actual submission validator.
- **Mutation evidence:** 29 capability-negotiation tests cover malformed/duplicated job type lists and registry/runtime drift in addition to route map, version, method, scope and auth-profile failure cases. This adds evidence for internal consistency only; it does not establish third-party interoperability or authentication.
- **D-23 — job type advertisement and compatibility:** maintainers/implementers must decide whether the list is required in future profiles, behavior for older servers where it is absent, exact case/namespace semantics, and naming/version/deprecation rules.

#### STD-04 decision boundary

- **D-21 — capability-operation mapping and version semantics:** implementers and standards maintainers must decide whether `operations[]` becomes part of ServerInfoV3, whether it is optional/required, how operation IDs are governed as wire identifiers, and how exact version tokens and unknown/duplicate capabilities are handled.
- **D-22 — scopes and authentication profiles:** security/operators must define required scopes versus issuer-provided scopes, meaning of missing/empty scope lists, `none` profile semantics, per-operation authorization requirements, enforcement, and denial behavior. The in-memory server accepts and ignores bearer tokens; none of these tests prove authorization.

No V2.1 contract files or generator wiring were changed. Keep PR #3 draft/unmerged pending design, security and community review. The next engineering step is to keep auditing other contract boundaries, while the governance-specific parts of D-21/D-22 remain deferred rather than guessed.

## 9. Commander's operating rule

Advance one active slice at a time unless parallel work is strictly independent. Every new slice must declare its expected artifact, acceptance evidence, dependencies, and authority boundary before implementation begins. When evidence conflicts with the plan, update the plan; do not force the evidence to match it.

## 10. Consolidation checkpoint (2026-10-16)

This section supersedes stale branch/PR status entries above. Historical branch names and run evidence are retained; status below reflects the completed consolidation.

### Merged to `brapi-V2.1`

| Change | Pull request / commit | Status |
|---|---|---|
| Endpoint identity catalogue, semantic collision guards, exact endpoint naming and overlap checks | [PR #1](https://github.com/denishdholaria/BrAPI_genX/pull/1), commit `f4d654b652088c2a7eac2108d4f70ae72fcc98c7` | Merged |
| Experimental digest interoperability corpus, capability-to-operation registry, job-type advertisement checks, and job-idempotency concurrency evidence | [PR #4](https://github.com/denishdholaria/BrAPI_genX/pull/4), commit `cca320df1934a1135763b63b8019c3ef43554409` | Merged |

### Superseded pull requests and preserved source branches

- PR #2, **[Superseded] STD-01 — Digest interoperability golden vectors**, was closed after its changes were incorporated into PR #4.
- PR #3, **[Superseded] STD-04 — Explicit capability operation mapping**, was closed after its changes were incorporated into PR #4.
- `work/std-01-digest-vectors`, `work/std-04-capability-negotiation`, `work/std-03-idempotency-contract`, and `work/endpoint-identity-clarity` are retained as historical source branches; do not merge independently.
- `work/std-03-job-idempotency-semantics` is an archival branch. Its tip is the old endpoint-identity base and has no unique job-idempotency implementation. The idempotency tests actually landed through PR #4 from `work/std-03-idempotency-contract`.
- `work/integrated-genx-evidence` is the integration source branch for PR #4. Main now contains its consolidated work; preserve the branch as provenance until ordinary branch-retention policy decides otherwise.

### Current continuous-integration evidence

- [PR #4 conformance run 38869958077](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38869958077): **success**. Static and live conformance both passed, including endpoint-identity mutations, capability-negotiation mutations, idempotency concurrency, Python and TypeScript/Bun digest vectors, digest mutation resistance, and static/live probes.
- [PR #4 schema-generation run 38869952712](https://github.com/denishdholaria/BrAPI_genX/actions/runs/38869952712): **success**. Build, conversion, validation, OpenAPI/GraphQL/OWL generation, comparison, generated-diff summary, and report completed successfully.
- The follow-up checks on merge commit `cca320df1934a1135763b63b8019c3ef43554409` are recorded as conformance success and schema generation still in progress at the time of this worksheet update.

### Deferred decisions; do not infer acceptance from passing tests

- **D-02 — digest canonicalization and field preimages:** experimental candidate vectors pass, but RFC 8785/JCS is not adopted and existing reference-server canonicalizers were not migrated.
- **D-21 — capability-to-operation mapping/version token semantics:** open.
- **D-22 — scope/authentication-profile semantics and enforcement:** open; the in-memory prototype does not provide effective authentication/authorization.
- **D-23 — job-type advertisement, compatibility, versioning, and deprecation:** open.
- **D-24 — idempotency request-equivalence rule and header/body key precedence:** open; prototype canonicalizes parsed JSON, while existing prose describes byte-identical bodies.
- **D-25 — idempotency key namespace, retention, expiry, and durable/multi-replica guarantees:** open; prototype state is process-local.

### Release workflow repair

The schema-generation workflow's automatic commit step previously failed with HTTP 403, and a whitespace-check step failed on trailing whitespace emitted by the generated GraphQL file. The workflow on `brapi-V2.1` now declares explicit `contents: write` permissions for the release-branch commit path, guards artifact commits to release branches, and reports generated artifact differences rather than failing on generator-emitted whitespace. PR #4's schema-generation workflow passed with that policy. No generated BrAPI V2.1 artifacts were intentionally changed by this proposal.

### Next-step queue

1. Keep V2.1 contracts and generated release artifacts frozen.
2. Obtain community, implementer, and security review before resolving D-02 or D-21–D-25.
3. For additional engineering, create one narrowly scoped branch at a time from the current `brapi-V2.1` head, run the combined static/live suite plus schema generation, and update this worksheet only after verifying the exact commit and workflow results.
4. Do not delete historical branches automatically; close superseded pull requests and retain branches until explicit repository-retention cleanup.

