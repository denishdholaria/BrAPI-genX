# BrAPI-GenX — Decision Governance Register

**Status:** Phase 0 governance foundation.
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

## 4. Unresolved decision inventory (verified)

The following deferred decisions remain unresolved and must not be silently
standardised from prototype behaviour:

| ID | Subject | Source | Required authority |
|---|---|---|---|
| D-01 | HTTP status for same-key/different-body conflicts | RFC-001 §8 | Community |
| D-02 | JSON canonical form feeding digests (JCS) | RFC-001 §8 | Community/implementer |
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
| D-24 | Idempotency request equivalence and header/body precedence | Jobs | Community |
| D-25 | Idempotency namespace, retention, expiry, durability | Jobs | Community |
| RFC-153-Q1..Q3 | CapabilityNegotiation local questions | RFC-153 | Maintainer |
| RFC-155-Q1..Q3 | ConformanceProbe local questions | RFC-155 | Maintainer |

## 5. Digest interoperability note

Passing a candidate digest corpus does not automatically resolve the normative
digest contract. D-02 remains deferred pending community/implementer review of
canonicalization, field-level preimage scope, numeric precision, rejection
policy, and migration/versioning.

## 6. Authentication note

The reference implementation has historically lacked effective authentication and
authorization. Token acceptance must be distinguished from token validation,
authorization, and tenant enforcement. The prototype must not be described as
secure.

## 7. Collision repair record

D-460/D-461/D-462 were reused between RFC-153 and RFC-155 for different
questions. They have been renamed to `RFC-153-Q1..Q3` and `RFC-155-Q1..Q3`
respectively. Historical references in `Conformance/RESULTS.md` are preserved.