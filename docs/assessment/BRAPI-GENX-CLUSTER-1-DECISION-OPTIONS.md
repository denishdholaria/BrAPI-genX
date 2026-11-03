# BrAPI-GenX — Cluster 1 Decision Options (D-02 / D-24 / D-25)

**Historical status:** DRAFT — NOT APPROVED. Decision-engineering analysis.

> **Ratification update (2026-11-03):** This historical options analysis informed a subsequent BrAPI-GenX maintainer approval of D-02, D-24, and D-25. The approved resolution is in `Specification/BrAPI-GenX/DECISIONS.md`; its detailed explanation is `docs/governance/BRAPI-GENX-CLUSTER-1-APPROVED-DECISIONS.md`. Do not treat the alternatives below as currently undecided.

## 1. D-02 — Digest canonicalization

### Problem
What exact byte sequence is hashed, and under what canonicalization rule, for
provenance binding and (potentially) request equivalence?

### Candidate alternatives

| Option | Description | Strengths | Weaknesses |
|---|---|---|---|
| A. Exact-byte hashing | Hash the raw request body bytes | Simple; tamper-evident | Whitespace/key-order changes alter digest; poor cross-client stability |
| B. Standardized JSON canonicalization (JCS, RFC 8785) | Canonical JSON before hashing | Cross-language standard; deterministic | JCS number handling (IEEE 754) may not suit scientific decimals; Unicode normalization rules fixed |
| C. Versioned canonicalization profile | GenX-defined profile with version id | Evolvable; can tailor to scientific types | Requires governance; risk of fragmentation |
| D. Separate digests per purpose | Different digest for request equivalence vs provenance | Clear semantics; avoids overloading | More complexity; more to specify |

### Historical recommendation and approved outcome
The approved outcome adopts unmodified JCS/RFC 8785 for generic canonical JSON under `JCS-RFC8785`, separates raw-byte/canonical-JSON/scientific-semantic purposes, and leaves semantic fingerprints domain-specific and optional.

### Rejected/deferred
- Treating the Python prototype's `sort_keys` form as the standard (not
  cross-language, not specified).
- Assuming JCS solves scientific decimal representation.

## 2. D-24 — Idempotency request equivalence

### Problem
What makes two requests equivalent for idempotency replay/conflict purposes?

### Candidate alternatives

| Option | Description |
|---|---|
| A. Exact request-byte equivalence | Only byte-identical requests replay |
| B. Canonical request equivalence | Canonicalized JSON comparison (current prototype) |
| C. Operation identity + payload fingerprint | Separate operation identity from payload digest |
| D. Composite model | Key + method + route + canonical payload + tenant |

### Historical recommendation and approved outcome
The accepted model separates lookup identity (`namespace + key`) from the request fingerprint (stable operation ID + relevant context + canonical payload). The namespace is tenant + authenticated client + effective principal + stable GenX operation ID. Different header/body values are rejected with HTTP 400, and every replay needs fresh authentication and authorization.

### Operation-specific follow-up
- Whether optional-vs-null differences count as conflicts.
- Numeric representation equivalence.
- Query parameter inclusion.
- Concurrent in-flight handling (replay returns? 409? 202?).

## 3. D-25 — Scope, retention, durability

### Problem
Key namespace, retention, expiry, and durability guarantees.

### Candidate alternatives

| Dimension | Options |
|---|---|
| Scope | Global / tenant / client / operation / endpoint / composite |
| Storage | In-memory / process-local DB / durable DB / distributed shared |
| Retention | Fixed TTL / configurable / operation-dependent |
| Expiry reuse | Reject / allow with new operation |

### Historical recommendation and approved outcome
The approved model requires durable shared production state, atomic claim/create, namespace-scoped uniqueness, recovery, and documented retention. In-memory state remains reference-only. Response and tombstone retention are separate; the delivery model is at-least-once with appropriate effect coordination, not a universal exactly-once promise. Database technology and numeric durations remain implementation/operational decisions.

### Rejected
- Global key scope (cross-tenant risk).
- Claiming exactly-once execution from in-memory deduplication.
- Letting storage implementation define the API contract.

## 4. Dependency outcome

D-02 → D-24 → D-25 is **confirmed but with a feedback edge**: D-25's
scope/retention requirements (especially multi-instance and tenant isolation)
constrain D-24's identity model. Recommend representing as a partially parallel
model: D-02 and D-25-scope can be analysed in parallel; D-24's equivalence
definition depends on D-02; D-25's durability requirements feed back into D-24.

## 4.5 Refinement — Three digest purposes (D-02)

See implementation baseline §6. Raw-byte identity, canonical JSON identity, and
scientific semantic identity are distinct. JCS (RFC 8785) is the approved
generic JSON canonicalization only; it uses IEEE 754 binary64 numbers and does
not perform Unicode normalization or scientific decimal normalization. Scientific
semantic fingerprints, if needed, must be defined per domain contract, not
silently folded into JSON canonicalization.

## 4.6 Refinement — Idempotency lookup identity vs request fingerprint (D-24)

Idempotency record lookup identity (which previous submission is referenced):
`namespace + key`, where namespace may include tenant, principal, and stable
operation identity.

Request fingerprint (whether a new submission is equivalent): `operation
identity + canonical request content (+ relevant query/headers)`.

These must be modelled separately. The current prototype conflates them in a
single `canonical(body)` comparison. Stable operation identity should be the
GenX operation identifier, not the literal HTTP route.

Header/body conflict: current behaviour gives header precedence silently. The approved rule rejects conflicting values with HTTP 400. The approved replay rule requires fresh authentication and authorization before disclosure.

## 4.7 Refinement — Transaction boundaries and side effects (D-25)

Database transactional atomicity covers only the primary store. External side
effects require separate coordination (outbox, downstream idempotency
propagation, reconciliation). Exactly-once execution cannot be claimed from
duplicate-request detection alone. Retention: separate full-response retention
from minimal tombstone retention to extend conflict detection without storing
responses indefinitely.

## 5. Approval and remaining-review authority

- D-02/D-24/D-25: approved by the BrAPI-GenX project maintainer on 2026-11-03.
- Implementers, security specialists, and operators remain responsible for implementation and evidence; external BrAPI/community endorsement is not implied.

## 6. Historical draft decision text (superseded by approval)

> "BrAPI-GenX will define a versioned canonicalization profile for digest inputs,
> referencing JCS (RFC 8785) for generic JSON while specifying domain-specific
> rules for decimal quantities and units separately. Request idempotency identity
> will be a composite of tenant, principal, operation, endpoint, and canonical
> payload. Idempotency state will be durable and database-backed for any
> production claim; in-memory implementations are reference-only. Exactly-once
> execution is not claimed."
