# BrAPI-GenX — Missions 019, 020, 022 and 025 Engineering Handover

**Date:** 2026-11-24  
**Starting `main`:** `a9f225f5da4d8037b427b7675a023b56a5fad2ca`  
**Last inspected implementation head:** `a9e9f70378c736dca61e44f7313caf3c0642d42f`  
**Status:** three bounded implementation deliverables integrated on main; full-checkout and independent service checks explicitly pending.

## Mission 019 — Verification debt: partial completion, hard limitation recorded

Attempted to obtain a complete local repository checkout, including
`Specification/ENDPOINT-REGISTRY.json` (2,449,266 bytes) and the pinned Git
baseline revisions. The isolated execution environment cannot resolve
`github.com` for a Git clone; the GitHub connector does expose the repository
tree and individual source files but rejects the oversized 2.45 MB registry
content. Thus the complete checkout cannot be constructed locally through
the available mechanisms.

The three new Mission 017 canonical governance mutation tests were **not
run** in this session. The full historical worktree drift check, generated
catalogue check, and complete source/registry integrity suite also remain
unexecuted. No passing hosted Continuous Integration (CI) run is asserted.
Hosted GitHub Actions minutes remain exhausted according to the maintainer
until their anticipated December 1, 2026 reset.

**Verification actually performed:** isolated local script suites (see table),
direct source-code inspection through the GitHub connector, exact tested
script blob comparisons and current GitHub ledger status check.

## Mission 022 — Executable consumer provenance

**Commit:** [`74575b1e8c2ee98e8fd41f7256b6a1c06960166b`](https://github.com/denishdholaria/BrAPI-genX/commit/74575b1e8c2ee98e8fd41f7256b6a1c06960166b).

Added a read-only, deterministic executable source inventory and a
regression check for new unreviewed consumers of
`semanticNeighborIds`, `semanticNeighborCatalogIds`,
`semanticNeighbors` and `registryOnlyNeighbors`. Scanned Python,
JavaScript/TypeScript, Rust and Java-like executable source under
`Scripts/`, `src/` and `generator/`. Seven known script paths have
documented roles: source audit, registry validation, source-contract
validation, drift check, governance validation, documentation generation
and lineage helper.

The scanner does **not** claim dynamic or indirect usage is absent, nor does
it approve scientific interpretation of an operation-level relationship.
**10/10 synthetic local tests passed**; tested Git blobs:

- scanner `782c584b5bdd1c10e79eb97aeec633b5200db71e`;
- tests `b32a3f4c07cdf5f382c9cf5882b9fe526ccf722c`.

[Consumer audit](./BRAPI-GENX-MISSION-022-SEMANTIC-CONSUMER-AUDIT.md).

## Mission 020 — Strict draft-only authorization candidate

**Commit:** [`b8bd6d83261f5bd7458ee2d150c52fbf23f4f27f`](https://github.com/denishdholaria/BrAPI-genX/commit/b8bd6d83261f5bd7458ee2d150c52fbf23f4f27f).

Added an **opt-in**, **non-authorizing** candidate validator enforcing exact
source/target relationship identity, decision action, rationale, proposer,
evidence, timestamp, optional known-ledger membership, successor identity,
and `draft-not-authorized` status. It rejects attempts to include
`authorizationReference` or a fake ratified state in a proposal. The
canonical terminal-decision validator was not modified to accept any
candidate record as an authorization.

**14/14 synthetic local tests passed**, byte-verified:

- validator `01a669876936b5f54b8b5e9e75cd449a5883a7d8`;
- tests `80f93b8eec73b0ce8c2940799fc0f395ff94100f`.

[Draft candidate design](./BRAPI-GENX-MISSION-020-AUTHORIZATION-CANDIDATE-DESIGN.md).
Maintainer authorization mechanism is still undecided in
[issue #20](https://github.com/denishdholaria/BrAPI-genX/issues/20).

## Mission 025 — BreedingPipeline CAS trace evidence, bounded phase

**Commits:** [`fd62caf203a9e43333a98f2e443a0be3a1adb316`](https://github.com/denishdholaria/BrAPI-genX/commit/fd62caf203a9e43333a98f2e443a0be3a1adb316)
and [`687d99c724844423281fd18f926be608e676b26a`](https://github.com/denishdholaria/BrAPI-genX/commit/687d99c724844423281fd18f926be608e676b26a).
Exact test bytes aligned on [`a9e9f703`](https://github.com/denishdholaria/BrAPI-genX/commit/a9e9f70378c736dca61e44f7313caf3c0642d42f).

Built a read-only, offline, implementation-independent **trace verifier**
for five selected D-BP-14 (Compare-and-Set) acceptance scenarios:
`CAS-01`, `CAS-02`, `CAS-03`, `CAS-04`, and `CAS-06`.
It checks expected pointer values, immutable revision fingerprint and
publication state, successful/losing writer outcomes, winning current
pointer, unchanged history for rejected attempts, and observed lifecycle
effects. CAS-06 specifically checks that first-create requests omit the
precondition rather than encode explicit null.

**27/27 synthetic tests passed**, with exact Git blob matches:

- checker `fef4e29ab6597c911c982f64c01e8ea327815c14`;
- tests `154d01ce8da09271170fdfd83dad2aeb84560961`.

This validator **does not perform network calls or test an independently
implemented service**. A fake or incomplete trace can pass its structure
checks. True behavioral conformance still needs authenticated clients,
a real timing barrier, durable readback, event visibility, and transaction
fault injection, plus the remaining CAS-05 and CAS-07 through CAS-16
scenarios. The necessary independent service is a pending external
dependency in [issue #21](https://github.com/denishdholaria/BrAPI-genX/issues/21).

[CAS trace tool](./BRAPI-GENX-MISSION-025-CAS-TRACE-CONFORMANCE-TOOL.md).

## Tests actually rerun (latest tested local versions)

| Suite | Passed | Scope |
|---|---:|---|
| Registry per-edge drift regression | 13 | Isolated Python unit/mutation tests |
| Live review inventory | 12 | Isolated Python unit/mutation tests |
| Historical provenance and terminal publication | 17 | Isolated Python unit/mutation tests |
| Executable consumer regression | 10 | Isolated Python unit/mutation tests |
| Draft decision candidate | 14 | Isolated Python unit/mutation tests |
| BreedingPipeline CAS trace verifier | 27 | Synthetic observation traces |
| **Total** | **93** | **Not full-repository or actual service conformance** |

The GitHub connector independently confirmed each newly committed source
and test file matches its tested local Git blob hash.

## Invariant repository state

After integration the actual GitHub ledger still has:

- **153 original unique relationship identities**;
- **51 `requires-decision`**;
- **102 `inherited-unreviewed`**;
- **zero terminal rejections, supersessions, or scientific approvals
  performed by these missions**.

No official Breeding API (BrAPI) version 2.1 source, public GenX
application programming interface (API) route or schema, Request for
Comments (RFC) maturity state, or current neighbor edge was modified.

## Unresolved decision and execution gates

1. **Issue #17:** ratify or reject the proposed separation of advisory
   operation navigation from typed scientific relationships. **Recommendation:
   approve a separate typed relationship track**, leaving current
   `semanticNeighborIds` historical and advisory pending a staged
   compatibility audit.
2. **Issue #20:** define binding, verifiable maintainer authorization for
   exact relationship/action decisions. **Recommendation: repository-controlled,
   uniquely identified, maintainer-approved decision records matched to
   exact ledger ID and status**, with a documented approval/commit boundary.
   A draft or merely followable URL/RFC label must not grant approval.
3. **Issue #21:** identify and authorize an independent BreedingPipeline test
   deployment and durable state/side-effect inspection to execute actual
   CAS races. No test host, credentials, or access are assumed here.
4. **Mission 019:** rerun full checkout conformance, three Mission 017
   integration mutations, generated-artifact check and pinned historical
   drift baseline as soon as the repository checkout and hosted CI are
   available. The limited local tests cannot replace this.

**Milestone:** consumer governance regression protection, a safe unratified
authorization candidate schema, and a five-scenario portable CAS trace
auditor are integrated without crossing maintainer-only scientific policy
or normative maturity boundaries.
