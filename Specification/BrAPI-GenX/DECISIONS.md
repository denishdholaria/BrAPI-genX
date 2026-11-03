# BrAPI GenX — Decision Log

> **Governance:** decision-identifier policy, authority rules, and the unresolved
> decision inventory are maintained in
> [`docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md`](../../docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md).
> RFC-local questions use `RFC-NNN-QN` and do not reuse global `D-` identifiers.

Companion to RFC-001…RFC-007. Two lists: decisions the proposal **defers**
(need community or operator authorization — not taken here), and decisions
taken autonomously while drafting (visible here for review and reversal).

Status of the proposal as a whole: **draft, not accepted, not normative**.
Nothing here changes V2.1.

## Part A — Deferred (requires authorization)

| ID | Question | Source | Evidence available | What resolves it |
|---|---|---|---|---|
| D-01 | HTTP status for same-key/different-body conflicts (`409` proposed) | RFC-001 §8 | Reference server uses `409` + plain text (L-02 etc. green) | Community agreement + `Error_Handling.md` amendment |
| D-02 | JSON canonical form feeding digests | RFC-001 §8 | Experimental Python and TypeScript/Bun candidate corpus covers 12 structured JSON vectors, 2 exact-byte cases, 5 rejection-policy cases, 2 legacy-divergence diagnostics, and 10 mutation failures; no existing helper migrated | Community/implementer review of canonicalization, field-level preimage scope, numeric precision, rejection policy and migration/versioning; explicit ratification |
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

## Verification state

- Static: 20 probes green. Live: 28 probes green vs the reference server
  (`Scripts/genx_test_server.py`), plus applicable subsets vs the v21 profile
  and the TypeScript server.
- Eleven recorded runs in `Conformance/RESULTS.md`; every static check has
  /tmp mutation evidence proving fail-closed behavior, and L-24 proves
  single-effect idempotency under 8-thread concurrency (control: 8 keys → 8 jobs).
- A second, black-box TypeScript/Bun implementation passes 13/13 applicable
  live probes (run 9), including cross-runtime digest agreement.
- Footprint: only `Specification/BrAPI-GenX/` and two new `Scripts/` files;
  zero changes to V2.1 modules, `BrAPI-Schema/`, `generator/`, `Generated/`.


## Additional deferred decisions identified during branch review (2026-10-16)

| ID | Question | Source | Evidence available | What resolves it |
|---|---|---|---|---|
| D-21 | ServerInfoV3 capability-to-operation mapping and version-token semantics | RFC-001 §6; ServerInfoV3 schema; CAPABILITY-NEGOTIATION.md | `methods` alone cannot identify routes; `provenanceEnvelope` is an embedded contract. An optional `operations[]` route map is proposed and tested on a branch. | Community/implementer review of mapping shape, requiredness, public operation-ID stability, exact-token negotiation, and unknown/duplicate capability handling |
| D-22 | Security meaning of capability scopes and authentication profiles | RFC-001 §6; ServerInfoV3 schema; CAPABILITY-NEGOTIATION.md | Capability `scopes` and auth-profile `scopes` are semantically ambiguous. The prototype accepts and ignores bearer tokens and has no effective authorization. | Security/operator review of required versus issued scopes, missing/empty scopes, `none` profile semantics, per-operation enforcement, denial behavior, and independent verification |
| D-23 | How supported asynchronous `jobType` tokens are advertised and versioned | Jobs schemas; ServerInfoV3 schema; CAPABILITY-NEGOTIATION.md | Optional experimental `jobs.jobTypes[]` lists prototype-supported tokens and is checked against runtime validation. | Implementer/community review of requiredness, older-server compatibility, exact token namespace/case, versioning/deprecation, and a second implementation |
| D-24 | Idempotency request equivalence and key-source precedence | RFC-001 §8; `Jobs/Schemas/JobNewRequest.yaml`; reference submit handler | RFC prose says byte-identical bodies, while the Python prototype parses JSON and compares a canonicalized object, making whitespace/property order irrelevant. A non-empty `Idempotency-Key` header takes precedence over body `idempotencyKey`, but the body field still participates in the comparison. | Select exact-byte, named structured-JSON, or normalized-command equivalence; specify header/body precedence and whether the body key participates in equivalence. Preserve D-02/profile-version implications |
| D-25 | Idempotency namespace, retention, expiry, and deployment guarantee | RFC-001 §8; Jobs schemas; prototype store | The key map is process-local and not durable across restart or replicas; retention/reuse rules, tenant/actor scope, and behavior after job expiry are unspecified. | Define key namespace, minimum retention, reuse rules, relationship to job time-to-live (TTL), expiry/conflict behavior, and whether guarantees survive restart or multiple replicas |

The above additions record open questions found during implementation review;
they do not settle these contract decisions. The reference server and its tests
are evidence for one prototype only, not a normative or production guarantee.

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
