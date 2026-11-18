# BrAPI-GenX — Phase 1B Open Technical Decisions

**Status:** Phase 1B.0 planning. These decisions remain for maintainer resolution.
**Excludes:** Already ratified Cluster 1 architectural decisions (D-02, D-24, D-25).

---

## 1. Cryptographic hash algorithm

| Aspect | Detail |
|---|---|
| **Question** | Which hash algorithm for all digest purposes? |
| **Alternatives** | SHA-256 (recommended), SHA-512/256, BLAKE3, SHA3-256 |
| **Recommended** | SHA-256 |
| **Why** | Universal support, existing repository usage, adequate security, no migration |
| **Consequences** | 64-char hex digest; algorithm identifier `"sha256"` in all results |
| **Reversibility** | Algorithm agility via `DigestResult.algorithm` field; migration path documented |
| **Blocks Slice 1?** | **Yes** — must be decided before digest primitives implemented |
| **Authority** | Maintainer (technical architecture) |

---

## 2. Digest encoding and algorithm identification

| Aspect | Detail |
|---|---|
| **Question** | How to encode digest output and identify algorithm/profile? |
| **Alternatives** | Lowercase hex + JSON envelope; multihash (CID); binary + base64url |
| **Recommended** | Lowercase hex (64 chars) + `DigestResult` JSON envelope with `algorithm`, `purpose`, `canonicalization_profile` |
| **Why** | Human-readable, standard, matches existing vectors, self-describing |
| **Consequences** | All digest consumers parse JSON envelope; hex string for storage/indexing |
| **Reversibility** | Envelope version field allows future extension |
| **Blocks Slice 1?** | **Yes** — `DigestResult` type defined in Slice 0 |
| **Authority** | Maintainer (technical architecture) |

---

## 3. Algorithm versioning and migration

| Aspect | Detail |
|---|---|
| **Question** | How to handle future algorithm/canonicalization changes? |
| **Alternatives** | Versioned profile IDs; content-addressed migration; dual-write transition |
| **Recommended** | Versioned canonicalization profiles (e.g., `jcs-rfc8785:v1`), `DigestResult` includes profile; migration via re-hashing on read with version check |
| **Why** | Explicit, auditable, supports gradual migration |
| **Consequences** | Storage must retain profile version; verification code handles multiple versions |
| **Reversibility** | New versions additive; old versions verifiable indefinitely |
| **Blocks Slice 1?** | No — can start with `v1`; migration logic in Slice 7+ |
| **Authority** | Maintainer (technical architecture) |

---

## 4. Request-fingerprint envelope structure

| Aspect | Detail |
|---|---|
| **Question** | Exact JSON structure for request fingerprint canonicalization? |
| **Alternatives** | Minimal (op_id + method + payload); extended (all context); per-operation schemas |
| **Recommended** | Common envelope with optional fields: `{"v":1,"op":"...","method":"...","payload":{},"query":{},"headers":{},"cv":"..."}` — JCS-canonicalized as unit |
| **Why** | Extensible, versioned, operation-specific context via optional fields |
| **Consequences** | Fingerprint changes if envelope version changes; cross-language must match exactly |
| **Reversibility** | Version field (`"v"`) allows evolution |
| **Blocks Slice 1?** | No — defined in Slice 5 |
| **Authority** | Maintainer (technical architecture) |

---

## 5. Operation-specific context fields

| Aspect | Detail |
|---|---|
| **Question** | Which query parameters and headers are fingerprint-relevant per operation? |
| **Alternatives** | None (only payload); static registry per operation; dynamic per-request |
| **Recommended** | Static registry in code/config: default empty; explicit opt-in for operations needing query/header context (e.g., `genxListVariableTermVersions` needs `variableDbId`, `status`) |
| **Why** | Predictable, auditable, avoids accidental inclusion of unstable headers |
| **Consequences** | Adding context requires registry update + fingerprint version bump |
| **Reversibility** | Registry is code/config; changes are explicit |
| **Blocks Slice 1?** | No — Slice 5 |
| **Authority** | Maintainer (technical architecture) |

---

## 6. Namespace encoding format

| Aspect | Detail |
|---|---|
| **Question** | Serialized string format for composite idempotency namespace (if needed)? |
| **Alternatives** | Structured DB columns only (preferred); `genx:idemp:v1:{tenant}:{client}:{principal}:{op}:{key}`; UUIDv5 of components |
| **Recommended** | Structured DB composite primary key as primary; if serialized needed, `genx:idemp:v1:{tenant}:{client}:{principal}:{op}:{key}` with `:` delimiter and no `:` in components |
| **Why** | Database enforcement is primary; serialization only for logging/debugging |
| **Consequences** | Component values must not contain delimiter; UUIDs safe |
| **Reversibility** | Version prefix (`v1`) allows format change |
| **Blocks Slice 1?** | No — Slice 4/7 |
| **Authority** | Maintainer (technical architecture) |

---

## 7. Idempotency key constraints

| Aspect | Detail |
|---|---|
| **Question** | Format, length, and character set constraints for client-supplied keys? |
| **Alternatives** | Unconstrained string; UUID only; base64url; client-generated with prefix |
| **Recommended** | 1–255 chars, ASCII printable (no control chars), client-generated; server does not generate keys |
| **Why** | Flexible for clients; length limit prevents abuse; ASCII avoids encoding issues |
| **Consequences** | Validation on receipt; malformed key → 400 |
| **Reversibility** | Constraint relaxation additive; tightening requires migration |
| **Blocks Slice 1?** | No — Slice 6 |
| **Authority** | Maintainer (technical architecture) |

---

## 8. State-machine transitions (details)

| Aspect | Detail |
|---|---|
| **Question** | Exact transitions, terminal states, and retry semantics? |
| **Alternatives** | Simple (claimed→completed); full (claimed→in_progress→completed|failed|indeterminate→reconciled) |
| **Recommended** | Full state machine per architecture doc: `CLAIMED → IN_PROGRESS → {COMPLETED, RETRYABLE_FAILURE, TERMINAL_FAILURE, INDETERMINATE}` with reconciliation to `COMPLETED/RETRYABLE_FAILURE`, then `TOMBSTONED` after retention |
| **Why** | Covers crash recovery, async workers, retryable vs terminal failures |
| **Consequences** | More states = more implementation; but necessary for durability claims |
| **Reversibility** | States are internal; clients see only HTTP responses |
| **Blocks Slice 1?** | No — Slice 6 |
| **Authority** | Maintainer (technical architecture) |

---

## 9. Minimum retention duration

| Aspect | Detail |
|---|---|
| **Question** | Numeric `response_ttl` and `tombstone_ttl` defaults? |
| **Alternatives** | 1 day / 7 days; 7 days / 30 days (recommended); 30 days / 90 days; configurable only |
| **Recommended** | `response_ttl = 7 days`, `tombstone_ttl = 30 days` (configurable override) |
| **Why** | 7 days covers typical async job + client retry; 30 days covers audit/recovery |
| **Consequences** | Storage growth proportional to operation volume × 30 days |
| **Reversibility** | Configurable; can be changed per deployment |
| **Blocks Slice 1?** | No — Slice 9 |
| **Authority** | Maintainer (operational policy) |

---

## 10. Expired-response behaviour

| Aspect | Detail |
|---|---|
| **Question** | What happens when client replays after response TTL but before tombstone TTL? |
| **Alternatives** | Re-execute operation; return 404; return 200 with "response expired" status |
| **Recommended** | Return 200 with status `{"message": "Response expired; operation completed", "messageType": "INFO"}` — operation not re-executed, tombstone prevents mutation |
| **Why** | Honest about completion; prevents duplicate mutation; client knows result unavailable |
| **Consequences** | Client must handle "result not available" case |
| **Reversibility** | Response format change is backward-compatible (new status message) |
| **Blocks Slice 1?** | No — Slice 9 |
| **Authority** | Maintainer (technical architecture) |

---

## 11. Minimum replay-security interfaces

| Aspect | Detail |
|---|---|
| **Question** | What auth integration points are required for replay authorization? |
| **Alternatives** | Full auth framework; minimal `IdentityResolver` + `authorize_replay(principal, record)` callback |
| **Recommended** | Minimal callback interface: `can_replay(principal: Principal, record: IdempotencyRecord) -> bool` implemented by application layer |
| **Why** | Decouples idempotency from auth scheme; works with OIDC, API keys, mTLS |
| **Consequences** | Application must implement; not provided by library |
| **Reversibility** | Interface is stable; implementation change doesn't affect contract |
| **Blocks Slice 1?** | No — Slice 8 |
| **Authority** | Maintainer (security architecture) |

---

## 12. Persistence strategy

| Aspect | Detail |
|---|---|
| **Question** | Database backend for durable idempotency state? |
| **Alternatives** | PostgreSQL (recommended); SQLite (dev); Redis + Lua (atomic); custom |
| **Recommended** | PostgreSQL with advisory locks or `INSERT ON CONFLICT` for atomic claim; schema as defined in architecture doc |
| **Why** | ACID, composite PK enforcement, mature tooling, AuMatiKaya alignment |
| **Consequences** | Adds PostgreSQL dependency for production; dev can use SQLite |
| **Reversibility** | Abstract `IdempotencyStore` interface allows backend swap |
| **Blocks Slice 1?** | No — Slice 7 (Slice 6 uses in-memory) |
| **Authority** | Maintainer (technical architecture) |

---

## 13. Summary: decisions blocking first slice

| Decision | Blocks Slice 1? | Required before |
|---|---|---|
| 1. Cryptographic hash algorithm | **YES** | Slice 2 (digest primitives) |
| 2. Digest encoding/identification | **YES** | Slice 0 (DigestResult type) |
| 4. Request-fingerprint envelope | No | Slice 5 |
| 12. Persistence strategy | No | Slice 7 |

**Recommendation:** Maintainer confirms SHA-256 + lowercase hex + `DigestResult`
envelope → Slices 0–3 can proceed immediately.

---

## 14. Decisions requiring security/operational authority

| Decision | Authority |
|---|---|
| 9. Minimum retention duration | Maintainer (operational policy) |
| 10. Expired-response behaviour | Maintainer (technical architecture) |
| 11. Replay-security interfaces | Maintainer (security architecture) |

---

## 15. Decisions that are reversible implementation details

| Decision | Reversibility |
|---|---|
| 3. Algorithm versioning/migration | Additive (new versions) |
| 5. Operation-specific context fields | Registry update |
| 6. Namespace encoding format | Version prefix |
| 7. Idempotency key constraints | Relaxation additive |
| 8. State-machine transitions | Internal only |
| 12. Persistence strategy | Interface abstraction |

---

*All ratified Cluster 1 architectural decisions (D-02, D-24, D-25) are excluded from
this list. This document tracks only the remaining technical choices needed for
implementation.*