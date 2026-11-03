# BrAPI-GenX — Decision Ownership Matrix

**Status:** Phase 1A planning. No decision is accepted by this document.
**Companion:** `docs/assessment/BRAPI-GENX-PHASE-1A-DECISION-DEPENDENCY-REVIEW.md`

Authority categories: M = Repository maintainer; T = Technical architecture;
S = Scientific/domain; C = Standards/community; Sec = Security/operational;
J = Joint.

| ID | Title (short) | Status | Category | Accountable | Required reviewers | Required evidence | Dependencies |
|---|---|---|---|---|---|---|---|
| D-01 | HTTP status for same-key/different-body conflicts | Deferred | T (with C for normative status code) | Maintainer | Implementers, community | Reference behaviour + Error_Handling amendment | None |
| D-02 | JSON canonical form feeding digests | Deferred | T + C (normative) | Maintainer + community | Implementers (Python/TS), security | Cross-language corpus, JCS evaluation, migration plan | None (root) |
| D-03 | OIDC tenant-claim name and scope vocabulary | Deferred | Sec + M | Maintainer + security | Identity provider operators | Identity-provider evidence, second implementation | D-25 (tenant scope) |
| D-04 | Wiring GenX into generator/BrAPI-Schema/Generated | Deferred | M (operator build decision) | Maintainer | Build/infra | Build evidence (Slice H) | None |
| D-05 | Term/model version ordering and comparison | Deferred | S + T | Maintainer | Domain experts | Versioning rule proposal | None |
| D-06 | Versioned Trait/Method/Scale references | Deferred | S + C | Maintainer + community | Ontology experts | Ontology evidence | D-05 |
| D-07 | Atomic multi-lot transfers | Deferred | S + T | Maintainer | Domain experts | Single-writer analysis | D-20 |
| D-08 | Unknown-lot behaviour (auto-provision vs 404) | Deferred | S + C | Maintainer + community | Implementers | Behaviour mandate | None |
| D-09 | Model approval/governance behind `revoked` | Deferred | S + Sec | Maintainer | Governance stakeholders | Governance RFC | None |
| D-10 | Artifact transport (inline/URL/chunking/signing) | Deferred | T + Sec | Maintainer | Implementers | Transport RFC + evidence | None |
| D-11 | GenX slice/query API over matrices | Deferred | S + T | Maintainer | htsget deployments | Demand evidence | None |
| D-12 | Byte-retrieval authorization (DRS vs bearer) | Deferred | Sec | Maintainer + security | DRS operators | DRS deployment experience | D-22 |
| D-13 | DOI minting flows | Deferred | S + C | Maintainer + community | DataCite practice | Pilot evidence | None |
| D-14 | Restricted-access request/approval protocols | Deferred | Sec + C | Maintainer + security | Policy reviewers | Policy + pilot | D-22 |
| D-15 | Embargo hiding metadata vs whole-record denial | Deferred | Sec + C (privacy) | Maintainer + community privacy review | Privacy reviewers | Community privacy review | D-22 |
| D-16 | Device/sensor registration and identity | Deferred | S + T | Maintainer | Deployment evidence | Registry RFC | None |
| D-17 | Alert rules, evaluation, delivery | Deferred | S + T | Maintainer | Implementers | Follow-up RFC | None |
| D-18 | Gap-filling, resampling, timezone-of-record | Deferred | S | Maintainer | Statistical reviewers | Statistical review + RFC | None |
| D-19 | Pangenome graph encodings | Deferred | S + C | Maintainer + community | Format spec maturity | Format specification maturity | None |
| D-20 | SeedLotTransaction vs LotLedgerEntry relationship | Deferred | S + C (BrAPI overlap) | Maintainer + community | Implementers, BrAPI community | Authority, event correlation, mapping, dual-read/write | None (root for overlap) |
| D-21 | Capability-to-operation mapping and version tokens | Deferred | T + C | Maintainer + community | Implementers | Mapping shape, operation-ID stability, token negotiation | None |
| D-22 | Security meaning of capability scopes and auth profiles | Deferred | Sec (with T) | Maintainer + security | Security specialists | Scope/auth-profile semantics, enforcement, denial behaviour | None (root for security) |
| D-23 | Advertised asynchronous job types | Deferred | T + C | Maintainer + community | Implementers | Requiredness, compatibility, token namespace/versioning | D-21 |
| D-24 | Idempotency request equivalence and header/body precedence | Deferred | T + Sec + C (API contract) | Maintainer + community | Implementers | Equivalence selection, header/body precedence | D-02 |
| D-25 | Idempotency namespace, retention, expiry, durability | Deferred | T + Sec + operational policy | Maintainer + security + operators | Retention, durability, multi-replica behaviour | D-24, D-03 (tenant) |

### Additional: RFC-local questions (RFC-NNN-Q1..Q3)

~415 RFC-local questions follow the template pattern (requiredness, controlled
vocabulary, ResearchAsset link). They are not centrally registered. Accountable
authority: repository maintainer (for governance migration) + per-RFC scientific
authority for the substantive question. Required evidence: per-RFC domain review.

### Approval route summary

- Repository-maintainer decisions: D-04, D-16 (identity registration), naming.
- Technical architecture: D-02, D-10, D-11, D-21, D-23, D-24 (implementation).
- Scientific/domain: D-05, D-06, D-07, D-08, D-09, D-17, D-18, D-19, D-20.
- Standards/community: D-06, D-13, D-19, D-20, D-21, D-23, D-24 (normative).
- Security/operational: D-03, D-12, D-14, D-15, D-22, D-25.
- Joint: D-07, D-09, D-20, D-24, D-25 (multiple authorities).

Where the accountable owner is not yet assigned, this is recorded as
"Maintainer (unassigned)" — no person or committee has been invented.