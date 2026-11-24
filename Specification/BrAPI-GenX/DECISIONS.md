# BrAPI GenX — Decision Log

> **Governance:** decision-identifier policy, authority rules, and the unresolved
> decision inventory are maintained in
> [`docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md`](../../docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md).
> RFC-local questions use `RFC-NNN-QN` and do not reuse global `D-` identifiers.

Companion to RFC-001…RFC-007. This register records deferred decisions,
reviewable drafting decisions, and decisions accepted by the BrAPI-GenX project
maintainer. It is the authoritative record of decision status.

Status of the proposal as a whole: **draft, not accepted, not normative**.
Nothing here changes V2.1.

## Part A — Deferred (requires authorization)

| ID | Question | Source | Evidence available | What resolves it |
|---|---|---|---|---|
| D-01 | HTTP status for same-key/different-body conflicts (`409` proposed) | RFC-001 §8 | Reference server uses `409` + plain text (L-02 etc. green) | Community agreement + `Error_Handling.md` amendment |
| D-03 | OIDC tenant-claim name and scope vocabulary | RFC-001 §8 | None implemented (reference server: auth `none`) | Operator identity decision + second implementation |
| D-04 | Wiring GenX into `generator/`, `BrAPI-Schema/`, `Generated/` | RFC-001 §8 | GenX dir proven inert to the V2.1 build (Slice H) | Operator build decision |
| D-05 | Term/model version ordering and comparison | RFC-002 §5 | Omitted-version reads use creation recency | Community versioning rule |
| D-06 | Versioned Trait/Method/Scale references | RFC-002 §5 | Referenced by SHOULD-namespaced IDs only | Follow-up RFC with ontology evidence |
| D-07 | Atomic multi-lot transfers | RFC-003 §5 | Single-entry atomicity only | Follow-up RFC (single-writer analysis required) |
| D-08 | Unknown-lot behavior (auto-provision vs `404`) | RFC-003 §5 | Reference auto-provisions | Community behavior mandate |
| D-09 | Model approval/governance behind `revoked` | RFC-004 §5 | Flag is a record; no process | Governance RFC with stakeholder input |
| D-10 | Artifact transport (inline/URL/chunking/signing) | RFC-004 §5 | Digest standardized; transport not | Transport RFC with implementer evidence |
| D-11 | GenX slice/query API over matrices | RFC-005 §5 | htsget is the current answer | Demand evidence from htsget deployments |
| D-12 | Byte-retrieval authorization (DRS Passports vs bearer) | RFC-005 §5 | Access service decides today | DRS deployment experience |
| D-13 | DOI minting flows | RFC-006 §5 | Identifiers asserted, never minted | DataCite practice + pilot |
| D-14 | Restricted-access request/approval protocols | RFC-006 §5 | Contract named, not implemented | Policy + pilot |
| D-15 | Embargo hiding metadata vs whole-record denial | RFC-006 §5 | Reference denies whole record (L-20) | Community privacy review |
| D-16 | Device/sensor registration and identity | RFC-007 §5 | Opaque IDs only | Registry RFC with deployment evidence |
| D-17 | Alert rules, evaluation, delivery | RFC-007 §5 | Prototype vocabulary exists, not standardized | Follow-up RFC |
| D-18 | Gap-filling, resampling, timezone-of-record | RFC-007 §5 | None; servers document their own | Statistical review + RFC |
| D-19 | Pangenome graph encodings (no format value claimed) | RFC-005 §5 | None | Format specification maturity |
| D-20 | Relationship, mapping, authority, and double-counting rules between V2.1 `SeedLotTransaction` and GenX `LotLedgerEntry` | RFC-003 §1/§3; ENDPOINT-IDENTITY.md | Structurally different contracts describe overlapping real-world material movements; no proven shared event identity or one-to-one mapping | Community and implementer decision defining authority, event correlation, mapping loss, and safe dual-read/dual-write behavior |

### RFC-008 local questions — unresolved, non-normative

These questions belong to SelectionDecision and do **not** reuse the global
D-21/D-22/D-23 decisions on capability negotiation and security. The
globally assigned decision numbers retain their original meanings.

| Local question | Topic | Current candidate behavior | Authority |
|---|---|---|---|
| RFC-008-Q1 | Scope to Program versus optional Trial/Study | Program required; Study optional | Maintainer decision pending |
| RFC-008-Q2 | Required Observation evidence for selection | Linked Observation evidence optional | Maintainer decision pending |
| RFC-008-Q3 | Authority to supersede an actual verdict | Decision-maker versus other authorized breeder unresolved | Maintainer decision pending |

Source: `Specification/BrAPI-GenX/RFCs/RFC-008-Selection-Decisions.md`.
This ID reconciliation does not accept a scientific or security policy.

## Part B — Taken autonomously (reviewable)

These were decided during drafting because a defensible answer existed. Each
is reversible without breaking the rest; objections belong against the ID.

| ID | Decision | Rationale |
|---|---|---|
| A-01 | GenX lives under `/genx/v1/`, V2.1 frozen | Community major-version convention |
| A-02 | Zero shadowing of V2.1/shared component names (S-01 enforces) | Caught 2 real collisions (`AuthorizationToken`, `OntologyTerm`) |
| A-03 | `VariableTerm`, not `OntologyTerm`, for the governance object | V2.1 Genotyping owns `OntologyTerm` (GA4GH label, different semantics) |
| A-04 | Replay returns `200`, first submit `202` | Distinguishes replay observably; L-probes assert it |
| A-05 | Decimal strings for inventory, floats for telemetry | Money-vs-measurement distinction (RFC-003 §5 vs RFC-007 §5) |
| A-06 | No PUT/DELETE on ledger entries, terms, models, matrices, packages | Correction-by-new-record preserves history; deprecation is explicit |
| A-07 | Inference via Jobs, not a new endpoint | RFC-001 lifecycle reused; no new surface |
| A-08 | Reference `outputs.echo` stub for inference | Proves digest binding only; documented as not-a-model |
| A-09 | Whole-record `403` for embargoed packages (reference behavior) | Stands in for payload-level denial; flagged as D-15 |
| A-10 | Omitted `version` reads return most-recently-created | Deterministic without deciding D-05 |
| A-11 | Static fixtures use `institute-a:*`, live runs use `test-*` ids | No collision between checked-in examples and test runs |
| A-12 | `TelemetryBatchResult` under `components.schemas`, not `responses` | It is a result object; S-01 proved the original placement dangling |

## Historical verification state (original RFC-001–RFC-007 drafting snapshot)

The counts below describe an earlier recorded verification snapshot, **not**
the current branch or the latest registered probe manifest. The authoritative
probe list is `Conformance/probes.yaml` (currently S-01–S-21 and L-01–L-28);
`Conformance/RESULTS.md` retains the later dated run records.

- At this historical snapshot: 20 static probes and 28 live probes passed against
  the reference server (`Scripts/genx_test_server.py`), with subsets against
  the v21 profile and TypeScript server.
- The then-recorded eleven runs included static mutation evidence; L-24 checked
  single-effect idempotency under 8-thread concurrency (control: 8 keys → 8 jobs).
- A second, black-box TypeScript/Bun implementation passes 13/13 applicable
  live probes (run 9), including cross-runtime digest agreement.
- Footprint: only `Specification/BrAPI-GenX/` and two new `Scripts/` files;
  zero changes to V2.1 modules, `BrAPI-Schema/`, `generator/`, `Generated/`.


## Additional decision inventory identified during branch review (2026-10-16)

| ID | Question | Source | Evidence available | What resolves it |
|---|---|---|---|---|
| D-21 | ServerInfoV3 capability-to-operation mapping and version-token semantics | RFC-001 §6; ServerInfoV3 schema; CAPABILITY-NEGOTIATION.md | `methods` alone cannot identify routes; `provenanceEnvelope` is an embedded contract. An optional `operations[]` route map is proposed and tested on a branch. | Community/implementer review of mapping shape, requiredness, public operation-ID stability, exact-token negotiation, and unknown/duplicate capability handling |
| D-22 | Security meaning of capability scopes and authentication profiles | RFC-001 §6; ServerInfoV3 schema; CAPABILITY-NEGOTIATION.md | Capability `scopes` and auth-profile `scopes` are semantically ambiguous. The prototype accepts and ignores bearer tokens and has no effective authorization. D-24 now separately requires fresh authentication and authorization before any idempotency replay result is disclosed. | Security/operator review of required versus issued scopes, missing/empty scopes, `none` profile semantics, per-operation enforcement, denial behavior, and independent verification. D-22 remains deferred except for the D-24 replay-security dependency. |
| D-23 | How supported asynchronous `jobType` tokens are advertised and versioned | Jobs schemas; ServerInfoV3 schema; CAPABILITY-NEGOTIATION.md | Optional experimental `jobs.jobTypes[]` lists prototype-supported tokens and is checked against runtime validation. | Implementer/community review of requiredness, older-server compatibility, exact token namespace/case, versioning/deprecation, and a second implementation |
| D-24 | Idempotency request equivalence and key-source precedence | RFC-001 §8; `Core/Jobs/Schemas/JobNewRequest.yaml`; reference submit handler | **Accepted 2026-11-03.** Historical issue: RFC prose says byte-identical bodies, while the Python prototype parses JSON and compares a canonicalized object. The accepted resolution separates lookup identity from request fingerprint; see Part C. | Implementation, security review, operation-specific fingerprint definitions, conformance evidence, and legacy compatibility work remain pending. |
| D-25 | Idempotency namespace, retention, expiry, and deployment guarantee | RFC-001 §8; Jobs schemas; prototype store | **Accepted 2026-11-03.** Historical issue: the key map is process-local and not durable across restart or replicas. The accepted resolution requires durable shared production state and separate response/tombstone retention; see Part C. | Implementation, retention policy selection, recovery evidence, and production conformance verification remain pending. |

The above additions record open questions found during implementation review.
Except for the accepted D-24 and D-25 resolutions recorded below, they do not
settle contract decisions. The reference server and its tests are evidence for
one prototype only, not a normative or production guarantee.

## Part C — Accepted BrAPI-GenX architectural decisions

**Approval authority:** BrAPI-GenX project maintainer.
**Approval date:** 2026-11-03.
**Authority boundary:** These are internal BrAPI-GenX architectural decisions. They do not claim implementation completion, production conformance, external standards adoption, or official BrAPI community endorsement.

### D-02 — Digest canonicalization and purposes (`ACCEPTED`)

**Original question and context.** What JSON canonical form feeds digests? The historical evidence was an exploratory Python and TypeScript/Bun candidate corpus; the historical alternatives included exact-byte hashing, JCS, and a custom profile. No existing helper was migrated as part of that evidence.

**Resolution and requirements.** BrAPI-GenX distinguishes a raw-byte digest for exact bytes, a canonical JSON digest for generic JSON, and an optional, domain-specific scientific semantic fingerprint. Generic canonical JSON uses unmodified JCS from RFC 8785, identified as `JCS-RFC8785`. JCS inputs reject duplicate object properties and non-finite numbers; Unicode is not normalized automatically; and JCS numeric constraints apply. High-precision scientific decimals use strings where their domain contract requires it. Unit conversion, decimal rounding, Unicode normalization, and other scientific transformations are outside generic JCS and require an explicit domain contract. Digest purpose and canonicalization method must be identifiable.

**Deferred and pending.** This decision does not choose a universal cryptographic digest algorithm (existing SHA-256 evidence is not such a selection), create a universal semantic fingerprint, or define every field-level preimage. JCS implementation, operation/domain preimages, and cross-language conformance evidence remain pending. D-24 may use the approved canonical JSON approach for its canonical request payload where appropriate.

### D-24 — Idempotency identity, equivalence, and replay (`ACCEPTED`)

**Original question and context.** What makes requests equivalent and how are header/body keys reconciled? Historically, RFC prose said byte-identical bodies while the Python prototype compared a parsed, Python-canonicalized object and silently preferred a non-empty header key.

**Resolution and requirements.** Lookup identity is `idempotency_namespace + idempotency_key`, distinct from the request fingerprint `stable_genx_operation_id + relevant_request_context + canonical_request_payload`. The namespace is `tenant_id + authenticated_client_id + effective_principal_id + stable_genx_operation_id`; operation identifiers are logical GenX identifiers, not route strings. Same namespace/key plus same fingerprint is a retry/replay candidate; same namespace/key plus a different fingerprint is conflicting reuse; different namespaces, including different tenants, remain distinct. Equal header/body keys are permitted; different values are rejected with HTTP 400; the header remains the authoritative transport mechanism. Every replay requires fresh authentication and authorization before result disclosure; a key grants no access right and unauthorized handling must not disclose another record.

**Deferred and pending.** The exact fingerprint fields are operation-specific; only materially relevant context belongs in them. D-24 does not complete D-22, select every replay response status, or settle every legacy body-key outcome. Implementation, security review, deterministic concurrency, operation-specific contracts, and conformance evidence remain pending. D-25 provides its durable lifecycle requirements.

### D-25 — Idempotency scope, retention, and durability (`ACCEPTED`)

**Original question and context.** What namespace, retention, expiry, and deployment guarantee apply? Historically, the prototype used a process-local map with no restart/replica guarantee and unspecified retention.

**Resolution and requirements.** Production-conforming implementations require durable shared idempotency state, atomic claim/create, namespace-scoped uniqueness, restart recovery, and duplicate recognition within documented retention. Process-local maps and locks are development/reference-only. Where record and business mutation share a transactional store, they must be coordinated atomically; other boundaries require documented coordination and recovery. External effects require appropriate mechanisms, but BrAPI-GenX does not promise universal exactly-once execution. Full-response and tombstone retention are distinct; discarding a response must not re-enable execution while the tombstone remains. Implementations must document retry window, both retention periods, expiry/key-reuse behaviour, recovery implications, and extensions.

**Deferred and pending.** No database technology or numeric minimum retention duration is selected, and no universal external-effect mechanism is mandated. Implementation, durable multi-instance/failure testing, recovery design, and retention-policy documentation remain pending. D-22 remains open for the broader security architecture.

For diagrams, acceptance criteria, evidence requirements, and complete cross-dependencies, see [`BRAPI-GENX-CLUSTER-1-APPROVED-DECISIONS.md`](../../docs/governance/BRAPI-GENX-CLUSTER-1-APPROVED-DECISIONS.md).

### D-026 — Separate advisory navigation from typed scientific relationships (`ACCEPTED`)

**Maintainer direction:** Approved in the ongoing 2026-11-24 BrAPI-GenX development conversation, following the Mission 018 recommendation and issue #17. The architectural direction is accepted **internally**, not on behalf of the official Breeding Application Programming Interface (BrAPI) community.

**Resolution:** Legacy `semanticNeighborIds`, source `x-brapi-genx.semanticNeighbors` and related operation/catalogue navigation labels are **advisory discoverability metadata**. They are not proof of scientific equivalence, shared resource identity, lineage, ownership, unit conversion, authorization or permission to invoke a write operation. A distinct, separately governed typed scientific relationship track is selected for future work. Resource references, directed derivation, operation-contract equivalence and editorial navigation must remain explicitly distinguished.

**Compatibility boundary:** Preserve the existing 153 historical ledger identities and current registry/source names. Adopt a non-breaking shadow proposal mechanism before changing published catalogues or clients. No pending source–target mapping is automatically approved, rejected or deleted. The specific typed relationship schema, evidence sufficiency, identifiers, and migration remain to be validated independently.

**Evidence and alternatives:** `docs/assessment/BRAPI-GENX-MISSION-018-SEMANTIC-RELATIONSHIP-ARCHITECTURE-PROPOSAL.md`; alternatives: keep one ambiguous field, incorrectly treat every link as scientific equivalence, or separate advisory/typed semantics (selected).

**Security and scientific impact:** Prevent algorithms and agents from treating navigation as authorized access or a valid scientific foreign key. Not a live access-control enforcement policy. **Status:** ACCEPTED architectural direction; **not** a normative endpoint specification.

### D-027 — Exact-record maintainer authorization for terminal neighbor decisions (`ACCEPTED`)

**Maintainer direction:** Approved in the 2026-11-24 development conversation, following Mission 020 and issue #20.

**Resolution:** Terminal `rejected` or `superseded` changes to a semantic-neighbor ledger entry require an **explicit, uniquely identified, maintainer-approved repository decision record** bound to the exact `sourceCatalogId -> targetOperationId` identity, intended terminal action, and any successor. An unrelated Request for Comments (RFC) citation, arbitrary web link, or a draft candidate is not an authorization. The record must include rationale, evidence, approval attribution and a traceable immutable GitHub approval reference. The governance validator must fail closed on missing or mismatched records and preserve the original ledger identity through active registry withdrawal.

**Approval authenticity limit:** Plain version-controlled metadata can be forged by an actor allowed to push to the branch. Only the maintainer's controlled review/approval of the *actual decision record* establishes authority. Local schema and identity checks detect mismatches but cannot cryptographically authenticate the approver, replace branch protection or confer consent. The initial approval register intentionally has **no terminal decisions**.

**Compatibility and security impact:** No existing endpoint, registry edge, source schema or scientific relationship is reclassified. A future terminal disposition changes active publication and governance together after a separately recorded decision. This strengthens governance integrity but does not settle broader authentication or security-policy decision D-22.

**Alternatives:** Unconstrained `authorizationReference` (unsafe), generic reviewable markdown with no exact link (ambiguous), or exact record binding with maintainer review (selected). **Status:** ACCEPTED governance architecture, not blanket acceptance of any terminal relationship status.

## Branch reconciliation record (2026-10-16)

- The endpoint-identity foundation was merged to `brapi-V2.1` via PR #1,
  commit [`f4d654b`](https://github.com/denishdholaria/BrAPI_genX/commit/f4d654b652088c2a7eac2108d4f70ae72fcc98c7).
- STD-01 and STD-04 remain non-normative proposal branches. Their last recorded
  conformance runs passed, but must be rerun on the post-consolidation heads
  before either branch is merged.
- `work/std-03-idempotency-contract` contains both job-idempotency tests and
  STD-04 capability-negotiation changes; its branch name understates its
  scope. Do not merge it as a standalone idempotency slice without separating
  and retesting the overlapping work.
- `work/std-03-job-idempotency-semantics` contains no independent commits
  relative to the endpoint-identity base; keep it as an archival branch until
  a clean replacement is prepared or its purpose is explicitly retired.
- `work/development-command-worksheet` contains the development queue and
  cross-repository evidence register. Review its worksheet content before
  merging because it predates some of the later decision-log additions.
