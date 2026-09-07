# BrAPI GenX — Decision Log

Companion to RFC-001…RFC-007. Two lists: decisions the proposal **defers**
(need community or operator authorization — not taken here), and decisions
taken autonomously while drafting (visible here for review and reversal).

Status of the proposal as a whole: **draft, not accepted, not normative**.
Nothing here changes V2.1.

## Part A — Deferred (requires authorization)

| ID | Question | Source | Evidence available | What resolves it |
|---|---|---|---|---|
| D-01 | HTTP status for same-key/different-body conflicts (`409` proposed) | RFC-001 §8 | Reference server uses `409` + plain text (L-02 etc. green) | Community agreement + `Error_Handling.md` amendment |
| D-02 | JSON canonical form feeding digests | RFC-001 §8 | Runner/server both use sorted-keys, compact separators | Community pick; then pin in all schemas |
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

## Part B — Taken autonomously (reviewable)

These were decided during drafting because a defensible answer existed. Each
is reversible without breaking the rest; objections belong against the ID.

| ID | Decision | Rationale |
|---|---|---|
| A-01 | GenX lives under `/brapi/v3/`, V2.1 frozen | Community major-version convention |
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

- Static: 20 probes green. Live: 24 probes green vs the reference server
  (`Scripts/genx_test_server.py`), plus L-06 vs the v21 profile.
- Eight recorded runs in `Conformance/RESULTS.md`; every static check has
  /tmp mutation evidence proving fail-closed behavior, and L-24 proves
  single-effect idempotency under 8-thread concurrency (control: 8 keys → 8 jobs).
- Footprint: only `Specification/BrAPI-GenX/` and two new `Scripts/` files;
  zero changes to V2.1 modules, `BrAPI-Schema/`, `generator/`, `Generated/`.
