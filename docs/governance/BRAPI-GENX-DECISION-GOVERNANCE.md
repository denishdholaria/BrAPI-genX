# BrAPI-GenX — Decision Governance Register

**Status:** Phase 0 governance foundation, updated for the 2026-11-03 Cluster 1 maintainer approvals.
**Companion:** `Specification/BrAPI-GenX/DECISIONS.md` (historical decision log).

## 1. Identifier policy

- **Global decisions** (cross-RFC, affecting interoperability/identity/security) use
  `D-NN` (zero-padded two digits is legacy; new global decisions should use
  `D-NNN` with three digits) and must be unique across the entire repository.
  Historical D-01…D-25 retain their identifiers (no renumbering).
- **RFC-local questions** (questions scoped to a single RFC's schema or
  behaviour) use `RFC-NNN-QN` (e.g. `RFC-155-Q1`). They must not masquerade as
  globally unique `D-` identifiers.
- **Autonomous decisions** taken during drafting use `A-NN` (existing A-01…A-12)
  and remain reviewable/reversible.
- Every decision reference must resolve to a record with: question, source,
  evidence, alternatives, compatibility impact, security impact, required
  decision authority, resolution criteria, and status.

## 2. Status vocabulary

`DEFERRED` (requires authorization), `TAKEN` (autonomous, reviewable),
`PROPOSED`, `ACCEPTED` (only by maintainer under explicit governance),
`REJECTED`, `SUPERSEDED`.

## 3. Authority

AI agents may research, analyse, propose, draft, test and implement authorised
engineering changes. They cannot ratify scientific policy, declare community
acceptance, assume maintainer authority, or convert an experimental proposal
into a normative specification. The repository maintainer retains final decision
authority.

## 4. Accepted decision inventory

The BrAPI-GenX project maintainer accepted the following internal architectural
directions on 2026-11-03. Acceptance does not represent implementation,
independent conformance verification, production deployment, or official BrAPI
community endorsement.

| ID | Subject | Status | Approval authority | Remaining work |
|---|---|---|---|---|
| D-02 | Digest purposes and generic canonical JSON | ACCEPTED | BrAPI-GenX project maintainer | JCS implementation, profile/preimage use, cross-language conformance; hash algorithm remains separate |
| D-24 | Idempotency lookup identity, equivalence, key conflict, replay | ACCEPTED | BrAPI-GenX project maintainer | Operation-specific fingerprint contracts, implementation, authorization and concurrency evidence |
| D-25 | Idempotency durability, recovery, and retention architecture | ACCEPTED | BrAPI-GenX project maintainer | Durable implementation, recovery/retention policy, multi-instance and fault evidence |
| D-026 | Advisory operation navigation separated from governed typed scientific relationships | ACCEPTED | BrAPI-GenX project maintainer, 2026-11-24 | Non-breaking shadow model, reader audit and independent semantic validation; no link is automatically accepted |
| D-027 | Exact-record maintainer authorization for terminal semantic-neighbor dispositions | ACCEPTED | BrAPI-GenX project maintainer, 2026-11-24 | Exact-binding validator and maintainer-controlled approval review; register initially empty |

The detailed explanatory record is
[`BRAPI-GENX-CLUSTER-1-APPROVED-DECISIONS.md`](BRAPI-GENX-CLUSTER-1-APPROVED-DECISIONS.md).

## 5. Unresolved decision inventory (verified)

The following deferred decisions remain unresolved and must not be silently
standardised from prototype behaviour:

| ID | Subject | Source | Required authority |
|---|---|---|---|
| D-01 | HTTP status for same-key/different-body conflicts | RFC-001 §8 | Community |
| D-03 | OIDC tenant-claim name and scope vocabulary | RFC-001 §8 | Operator |
| D-04 | Wiring GenX into generator/BrAPI-Schema/Generated | RFC-001 §8 | Operator |
| D-05 | Term/model version ordering and comparison | RFC-002 §5 | Community |
| D-06 | Versioned Trait/Method/Scale references | RFC-002 §5 | Follow-up RFC |
| D-07 | Atomic multi-lot transfers | RFC-003 §5 | Follow-up RFC |
| D-08 | Unknown-lot behavior (auto-provision vs 404) | RFC-003 §5 | Community |
| D-09 | Model approval/governance behind `revoked` | RFC-004 §5 | Governance RFC |
| D-10 | Artifact transport | RFC-004 §5 | Transport RFC |
| D-11 | GenX slice/query API over matrices | RFC-005 §5 | Demand evidence |
| D-12 | Byte-retrieval authorization | RFC-005 §5 | DRS experience |
| D-13 | DOI minting flows | RFC-006 §5 | DataCite practice |
| D-14 | Restricted-access request/approval protocols | RFC-006 §5 | Policy + pilot |
| D-15 | Embargo hiding metadata vs whole-record denial | RFC-006 §5 | Community privacy review |
| D-16 | Device/sensor registration and identity | RFC-007 §5 | Registry RFC |
| D-17 | Alert rules, evaluation, delivery | RFC-007 §5 | Follow-up RFC |
| D-18 | Gap-filling, resampling, timezone-of-record | RFC-007 §5 | Statistical review |
| D-19 | Pangenome graph encodings | RFC-005 §5 | Format maturity |
| D-20 | SeedLotTransaction vs LotLedgerEntry relationship | RFC-003 | Community/implementer |
| D-21 | Capability-to-operation mapping and version tokens | ServerInfoV3 | Community/implementer |
| D-22 | Security meaning of capability scopes and auth profiles | ServerInfoV3 | Security/operator |
| D-23 | Advertised asynchronous job types | Jobs/ServerInfoV3 | Implementer/community |
| RFC-153-Q1..Q3 | CapabilityNegotiation local questions | RFC-153 | Maintainer |
| RFC-155-Q1..Q3 | ConformanceProbe local questions | RFC-155 | Maintainer |

## 6. Digest interoperability note

Passing a candidate digest corpus is not implementation or conformance proof.
D-02 is accepted internally: generic canonical JSON is JCS-RFC8785 and
scientific semantics remain separate. Field-level preimages, hash-algorithm
selection, implementation migration, and cross-language conformance remain
pending.

## 7. Authentication note

The reference implementation has historically lacked effective authentication and
authorization. Token acceptance must be distinguished from token validation,
authorization, and tenant enforcement. The prototype must not be described as
secure. D-24 nevertheless requires fresh authentication and authorization
before a stored idempotency result is disclosed; D-22's broader security
architecture remains unresolved.

## 8. Collision repair record

D-460/D-461/D-462 were reused between RFC-153 and RFC-155 for different
questions. They have been renamed to `RFC-153-Q1..Q3` and `RFC-155-Q1..Q3`
respectively. Historical references in `Conformance/RESULTS.md` are preserved.
