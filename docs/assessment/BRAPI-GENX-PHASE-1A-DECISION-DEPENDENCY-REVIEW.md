# BrAPI-GenX — Phase 1A Decision Dependency Review

**Status:** Phase 1A planning. No implementation or normative decision is
authorized by this document.
**Baseline:** `planning/phase-1a-decision-review` from `548d00ba` (Phase 0 + assessment commit).
**Phase 0 baseline commit:** `e65b1d89825c137eec0ddefedad117c3108f1586`.

> **Ratification update (2026-11-03):** This is a historical Phase 1A planning record. D-02, D-24, and D-25 have since been accepted by the BrAPI-GenX project maintainer; D-22 remains open, except that D-24 now requires fresh authentication and authorization before replay disclosure. Implementation and conformance remain pending.

## 1. Executive summary

Phase 0 established governance, quality, and maturity foundations. Phase 1A
inspects the unresolved decision space and determines what must be decided, in
what order, and by whom before any scientific specification pilot is developed.

Key findings:

- The central `DECISIONS.md` registers D-01…D-25 (25 decisions). Beyond these,
  approximately 415 additional `D-NNN` identifiers appear in RFC deferred-question
  sections (D-26…D-459), but are **not** centrally registered. These are
  RFC-local questions masquerading as global identifiers — a governance gap
  first identified in Phase 0 (CON-004).
- The critical decision clusters are: (1) digest canonicalization + idempotency
  (D-02, D-24, D-25); (2) security/authorization (D-22); (3) scientific
  authority/BrAPI overlap (D-20); (4) capability advertisement (D-21, D-23).
- The minimal critical path is: D-02 (digest) → D-24 (equivalence) → D-25
  (scope/retention/durability), with D-22 (security) and D-20 (scientific
  overlap) as parallel prerequisite clusters.
- Phase 1B implementation is **not** authorized by this document.

## 2. Verified baseline

- Repository root: `/home/dennis/src/reevuLabs/Bijmantra-Project/brapi-genx`
- Remote: `denishdholaria/BrAPI-GenX`
- Phase 0 commit: `e65b1d89825c137eec0ddefedad117c3108f1586`
- Current HEAD at start: `548d00ba51fea0ba4750de9930a4116a83b255c1`
- Closeout report: `docs/assessment/BRAPI-GENX-PHASE-0-CLOSEOUT.md` (present)
- Working tree: clean.

## 3. Complete decision inventory

### 3.1 Centrally registered decisions (D-01…D-25)

Source: `Specification/BrAPI-GenX/DECISIONS.md` Part A (deferred) and the
"Additional deferred decisions" section (D-21…D-25). At the time of this
review all 25 were unresolved (status DEFERRED). The current status is recorded
in `DECISIONS.md` and summarized in
`docs/governance/BRAPI-GENX-DECISION-GOVERNANCE.md`.

### 3.2 Autonomous decisions (A-01…A-12)

Status: TAKEN (reviewable, reversible). Not unresolved; listed for traceability.

### 3.3 RFC-local questions (RFC-NNN-QN / legacy D-NNN)

Approximately 415 additional `D-NNN` identifiers appear in RFC "Deferred
questions" sections (D-26…D-459). They follow a template pattern:
(1) Should field X be required? (2) Should field Y be a controlled vocabulary?
(3) Should records link to GenX `ResearchAsset`? These are not centrally
registered. Per the Phase 0 decision governance policy, they should be
reclassified as `RFC-NNN-QN`. This is a governance task, not a scientific
decision, but it is not performed in Phase 1A.

### 3.4 Count summary

- Centrally registered deferred: 25 (D-01…D-25)
- Autonomous (taken): 12 (A-01…A-12)
- RFC-local questions: ~415 (D-26…D-459, to be reclassified)
- RFC-scoped (already migrated): 6 (RFC-153-Q1..Q3, RFC-155-Q1..Q3)

Total decision references: ~458.

## 4. Critical decision clusters

### Cluster 1 — Digest canonicalization and idempotency (D-02, D-24, D-25)

**D-02 — JSON canonical form feeding digests.** The digest is used to bind
provenance and detect mutation. The exact preimage (which fields, in what
order, how numbers/Unicode/nulls are represented) is unspecified. JCS (RFC 8785)
is a candidate, not a decision. Current evidence: Python and TypeScript/Bun
candidate corpora (12 structured vectors, 2 exact-byte, 5 rejection-policy, 2
legacy-divergence, 10 mutation failures) — exploratory, not normative.

**D-24 — Idempotency request equivalence.** RFC prose says byte-identical
bodies; the Python prototype parses JSON and compares a canonicalized object,
making whitespace/property order irrelevant. Header/body key precedence is
unspecified. This directly depends on D-02's canonicalization choice.

**D-25 — Idempotency scope, retention, expiry, durability.** Key namespace
(tenant/actor/operation/endpoint), retention, reuse rules, TTL, expiry/conflict
behaviour, and survival across restart/replicas are unspecified. Depends on
D-24's equivalence definition and on operational policy.

Dependency: D-02 → D-24 → D-25. Resolving D-24 before D-02 risks an
incompatible equivalence definition. Resolving D-25 before D-24 risks retention
rules that don't match the equivalence semantics.

### Cluster 2 — Security and authorization (D-22)

Capability `scopes` and auth-profile `scopes` are semantically ambiguous. The
prototype accepts and ignores bearer tokens; no effective authorization exists.
Security properties that belong in the normative contract vs. implementation
profile vs. deployment guidance must be separated. Requires security/operational
authority, not just a software architect.

### Cluster 3 — Scientific authority and official BrAPI overlap (D-20)

Using RFC-003 Seed-Lot Ledger as the example: `LotLedgerEntry` vs official
BrAPI `SeedLotTransaction` describe overlapping real-world material movements
but are structurally different. No proven shared event identity or one-to-one
mapping exists. This requires community/implementer consultation, not just
internal decision.

### Cluster 4 — Capability advertisement (D-21, D-23)

D-21: capability-to-operation mapping and version-token semantics. `methods`
alone cannot identify routes; an optional `operations[]` map is proposed.
D-23: how supported async `jobType` tokens are advertised and versioned.
Both are experimental and require implementer/community review.

### Cluster 5 — Other deferred decisions (D-01, D-03…D-19)

D-01 (HTTP status for conflicts), D-03 (OIDC tenant claim), D-04 (wiring into
generator), D-05 (version ordering), D-06 (versioned Trait/Method/Scale refs),
D-07 (atomic multi-lot transfers), D-08 (unknown-lot behaviour), D-09 (model
approval governance), D-10 (artifact transport), D-11 (matrix slice/query API),
D-12 (byte-retrieval authorization), D-13 (DOI minting), D-14 (restricted
access protocols), D-15 (embargo hiding vs whole-record denial), D-16 (sensor
registration), D-17 (alert rules), D-18 (gap-filling/resampling/timezone),
D-19 (pangenome graph encodings). Each has its own authority and evidence
requirements as recorded in `DECISIONS.md`.

## 5. Decision dependency model

Directed dependencies (must be resolved before):

- D-02 → D-24 (equivalence depends on canonicalization)
- D-24 → D-25 (retention/durability depends on equivalence)
- D-02 → D-24 → idempotency implementation
- D-22 → security contract finalization (independent of digest cluster)
- D-20 → any claim of BrAPI compatibility for LotLedger (independent)
- D-21, D-23 → capability negotiation finalization (independent of digest)
- D-04 → any wiring into generator/BrAPI-Schema/Generated
- D-03 → tenant-scoped idempotency keys (D-25 sub-question)

Parallel-safe (no dependency):
- D-05, D-06 (versioning) can proceed independently
- D-09, D-10 (model governance/transport) independent
- D-16, D-17, D-18 (telemetry) independent
- D-11, D-12 (matrix) independent
- D-13, D-14, D-15 (FAIR packaging) independent

## 6. Decision critical path

Smallest prerequisite set that unlocks safe scientific specification development:

1. D-02 (digest canonicalization) — blocks provenance/mutation semantics
2. D-24 (idempotency equivalence) — blocks replay/conflict contracts
3. D-25 (idempotency scope/retention/durability) — blocks production claims
4. D-22 (security meaning) — blocks any authorization claim
5. D-20 (BrAPI overlap) — blocks compatibility claims for LotLedger

These five must be resolved (or explicitly deferred with documented
consequences) before Phase 1B implementation of any resource that depends on
provenance, mutation, or BrAPI overlap.

## 7. Evidence gaps

- D-02: no cross-language normative spec; only exploratory corpora.
- D-24: byte-identical vs canonicalized equivalence undecided; header/body
  precedence undecided.
- D-25: no durability/retention requirement defined; prototype is in-memory.
- D-22: no security specialist review; prototype has no auth.
- D-20: no community/implementer consultation recorded.
- D-21/D-23: optional experimental metadata; no second implementation.

## 8. Risks and implications

- Resolving D-24 before D-02 risks an incompatible equivalence definition.
- Treating prototype behaviour as normative (e.g., "409 for conflict") without
  community authorization overstates evidence (Rule 5).
- Treating RFC-local D-NNN as global decisions inflates the apparent decision
  count and obscures ownership.
- Selecting a pilot that depends on unresolved digest/BrAPI-overlap decisions
  would force premature resolution.

## 9. Recommended next actions

1. Adopt the RFC-scoped identifier migration (governance, low risk).
2. Convene the Cluster 1 dependency review (D-02 → D-24 → D-25) with
   implementer input.
3. Schedule D-22 security review with a security specialist.
4. Initiate D-20 community consultation for SeedLot/LotLedger overlap.
5. Select the scientific pilot (see `BRAPI-GENX-SCIENTIFIC-PILOT-SELECTION.md`)
   such that it does not depend on unresolved digest/overlap decisions.

See also: `docs/governance/BRAPI-GENX-DECISION-OWNERSHIP-MATRIX.md`,
`docs/assessment/BRAPI-GENX-SCIENTIFIC-PILOT-SELECTION.md`,
`docs/assessment/BRAPI-GENX-PHASE-1A-ROADMAP.md`.
