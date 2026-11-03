# BrAPI-GenX — Cluster 1 Decision Options (D-02 / D-24 / D-25)

**Status:** DRAFT — NOT APPROVED. Decision-engineering analysis only.

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

### Recommendation (draft, not approved)
Evaluate JCS as the *candidate* for general JSON canonicalization, but do not
assume it covers scientific decimals, units, or domain semantics. Consider a
versioned GenX canonicalization profile that references JCS for generic JSON
and defines domain-specific rules (decimal strings, quantities) separately.
Separate digest purposes (request fingerprint vs. provenance binding) explicitly.

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

### Recommendation (draft)
A composite model: idempotency identity = (key namespace) + (method) + (route)
+ (canonical payload) + (tenant/principal). This separates request identity,
operation identity, and payload identity. Header/body key precedence must be
decided explicitly (current prototype: header wins). Conflicting payload → 409.

### Unresolved
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

### Recommendation (draft)
- Scope: composite namespace (tenant + principal + operation + endpoint), not
  global. Global scope risks cross-tenant collision and unauthorized replay.
- Storage: durable, database-backed idempotency state required for any claim
  beyond in-process deduplication. In-memory is a reference implementation
  only.
- Retention: configurable with a documented minimum; separate response-retention
  from identity-retention (tombstone may suffice).
- Durability: at-least-once delivery + idempotent retry, not exactly-once
  execution (external side effects require separate analysis).

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

## 5. Required approval authority

- D-02: technical architecture + interoperability review (+ community if
  normative canonicalization profile adopted).
- D-24: maintainer + implementers + community (normative API contract).
- D-25: maintainer + security + operational (retention/durability obligations).

## 6. DRAFT — NOT APPROVED decision text (for maintainer consideration)

> "BrAPI-GenX will define a versioned canonicalization profile for digest inputs,
> referencing JCS (RFC 8785) for generic JSON while specifying domain-specific
> rules for decimal quantities and units separately. Request idempotency identity
> will be a composite of tenant, principal, operation, endpoint, and canonical
> payload. Idempotency state will be durable and database-backed for any
> production claim; in-memory implementations are reference-only. Exactly-once
> execution is not claimed."