# BrAPI-GenX — Cluster 1 Implementation Architecture

**Status:** Phase 1B.0 authoritative architecture. Ratified decisions are not
open for revision.
**Baseline:** commit `55f970d92dc3e64d34ea36fd184b3a48ec670f13`.
**Depends on:** `docs/governance/BRAPI-GENX-PROJECT-DECISION-AUTHORITY.md`.

---

## 1. Approved architectural baseline

### 1.1 D-02 — Digest architecture (three purposes)

| Purpose | Use cases | Canonicalization |
|---|---|---|
| **Raw-byte digest** | File/artifact integrity, exact payload verification, byte-level provenance | None — hash exact bytes |
| **Canonical JSON digest** | Provenance binding, mutation detection, interoperable request equivalence | JCS-RFC8785 (RFC 8785) |
| **Scientific semantic fingerprint** | Domain-specific scientific equivalence (optional, per-domain) | Domain contract defines; not in generic layer |

### 1.2 D-24 — Idempotency architecture (two concepts)

**Lookup identity** (which previous submission):
```
tenant_id + authenticated_client_id + effective_principal_id + stable_genx_operation_id + idempotency_key
```

**Request fingerprint** (whether a new submission is equivalent):
```
stable_genx_operation_id + relevant_request_context + canonical_request_payload
```

**Key-source behaviour:**
- Header only → accept
- Header + body identical → accept
- Header + body conflicting → **reject HTTP 400** (no silent precedence)
- Body only → supported for compatibility until deliberate migration

**Replay security:** Fresh authentication + authorization required on every replay.
Possession of idempotency key does not grant access.

### 1.3 D-25 — Durability and recovery

- Durable shared idempotency state (not in-memory).
- Atomic key claiming with composite unique constraint.
- Multi-instance coordination via database.
- Persistence across restarts.
- Transactional coordination where idempotency record and business mutation share a store.
- At-least-once delivery with idempotent effects; no universal exactly-once claim.
- Separate retention: full response vs. identity tombstone.

---

## 2. Digest subsystem architecture

### 2.1 Component boundaries (minimal)

```
┌─────────────────────────────────────────────────────────────┐
│                    Digest Service                           │
├──────────────────┬──────────────────────┬──────────────────┤
│  RawByteDigest   │  CanonicalJsonDigest │ SemanticDigest   │
│  (exact bytes)   │  (JCS-RFC8785)       │ (domain-owned)   │
└────────┬─────────┴──────────┬───────────┴────────┬─────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    hash(bytes)       jcs_canonicalize()    domain_fn()
         │                    │                    │
         ▼                    ▼                    ▼
    SHA-256(bytes)    SHA-256(canonical)    SHA-256(domain_canonical)
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                    DigestResult {
                      algorithm: "sha256",
                      purpose: "raw|canonical_json|semantic",
                      value: "hex",
                      canonicalization_profile?: "jcs-rfc8785:v1"
                    }
```

### 2.2 Raw-byte processing

```python
def raw_byte_digest(data: bytes) -> DigestResult:
    """Hash exact transmitted/stored bytes."""
    return DigestResult(
        algorithm="sha256",
        purpose="raw",
        value=sha256(data).hexdigest(),
    )
```

- Input: exact byte sequence (file content, HTTP body bytes, artifact bytes).
- No parsing, no decoding, no transformation.
- Used for: file integrity, artifact verification, byte-level provenance.

### 2.3 JCS canonical JSON processing

```python
def canonical_json_digest(json_bytes: bytes) -> DigestResult:
    """Parse, validate, JCS-canonicalize, hash."""
    # 1. Parse with duplicate-property detection
    value = parse_strict_json(json_bytes)
    # 2. Validate JCS input constraints (no NaN, no lone surrogates, etc.)
    validate_jcs_input(value)
    # 3. JCS canonicalize
    canonical_bytes = rfc8785.dumps(value)  # returns bytes
    # 4. Hash
    digest = sha256(canonical_bytes).hexdigest()
    return DigestResult(
        algorithm="sha256",
        purpose="canonical_json",
        value=digest,
        canonicalization_profile="jcs-rfc8785:v1",
    )
```

**Critical implementation details:**

1. **Duplicate-property detection** — Must occur *before* standard JSON parsing
   collapses duplicates. Use `object_pairs_hook` (Python) or streaming parser
   (TypeScript/Bun) that reports duplicates as errors.

2. **JCS input validation** — Reject:
   - Non-finite numbers (`NaN`, `Infinity`, `-Infinity`).
   - Lone Unicode surrogates.
   - Integers outside IEEE 754 safe range (`> 2^53-1` or `< -2^53+1`).

3. **Numeric representation** — JCS uses IEEE 754 binary64 shortest-form
   representation. Scientific decimals requiring exact precision **must be
   represented as strings** in the JSON (e.g., `"0.0000000000000001"` not
   `1e-16`). The generic canonicalizer does not convert.

4. **Unicode** — JCS preserves code points as-is; no normalization (NFC/NFD).
   Composed and decomposed forms produce different canonical output.

### 2.4 Cryptographic algorithm selection

**Recommendation: SHA-256 as initial interoperability baseline.**

| Algorithm | Security | Standardization | Rust/Python/TS support | Digest length | Recommendation |
|---|---|---|---|---|---|
| SHA-256 | Adequate (NIST approved) | FIPS 180-4, RFC 6234 | Universal | 64 hex chars | **Primary** |
| SHA-512/256 | Stronger | FIPS 180-4 | Universal | 64 hex chars | Alternative |
| BLAKE3 | Very fast, modern | RFC (draft) | Good | 64 hex chars | Future consideration |
| SHA3-256 | Different construction | FIPS 202 | Universal | 64 hex chars | Not needed |

**Reasons for SHA-256:**
- Existing repository usage (digest vectors, provenance digests).
- Universal availability in all three target runtimes.
- Adequate security margin for digest identification (not password hashing).
- No migration needed for existing digests.

**Digest representation:**
- Lowercase hexadecimal (64 characters).
- Algorithm identifier in `DigestResult.algorithm`.
- Profile identifier in `DigestResult.canonicalization_profile` where applicable.

### 2.5 Domain-specific semantic fingerprint extension

- **Owned by domain modules**, not the generic digest service.
- Domain contract defines:
  - Input structure (which fields, in what form).
  - Equivalence rules (unit conversion, precision, identifiers).
  - Canonicalization function (separate from JCS).
- Generic digest service provides only `hash(canonical_bytes)` primitive.
- Example (hypothetical):
  ```python
  # In a domain module, not generic service
  def seed_lot_quantity_fingerprint(entry: LotLedgerEntry) -> str:
      canonical = json_dumps({
          "quantity": entry.quantity,  # already decimal string
          "unit": entry.unit,          # normalized unit code
          "operation": entry.type,     # controlled vocabulary
      }, sort_keys=True)
      return sha256(canonical.encode()).hexdigest()
  ```

---

## 3. Stable operation identity and namespace

### 3.1 Operation identity source

The endpoint registry (`Specification/ENDPOINT-REGISTRY.json`) contains 462 GenX
operations with stable `recommendedOperationId` values (e.g., `genxSubmitAsyncJob`,
`genxRegisterBreedingPipeline`). These are the **canonical operation identifiers**.

- Ownership: registry is the single source of truth.
- Uniqueness: enforced by `checkEndpointRegistry.py` (catalogId, operationId).
- Route aliases: an operation may have multiple routes; identity is stable.
- API version changes: new operationId for breaking changes.

### 3.2 Identity resolution interfaces

```python
# Abstract interfaces for implementation
class IdentityResolver:
    def get_tenant_id(self, request: Request) -> TenantId: ...
    def get_client_id(self, request: Request) -> ClientId: ...
    def get_effective_principal(self, request: Request) -> PrincipalId: ...
    def get_operation_id(self, request: Request) -> OperationId: ...
```

**Stable identity components:**
- `TenantId` — organizational/data-isolation boundary (from auth context).
- `ClientId` — authenticated application/service identity (not user-facing name).
- `PrincipalId` — effective user/service identity (for delegated calls, both preserved).
- `OperationId` — `recommendedOperationId` from registry (e.g., `genxSubmitAsyncJob`).

**Do not use:**
- Access tokens, email addresses, display names, usernames.
- Literal HTTP paths (they change; operationId is stable).

### 3.3 Namespace encoding

**Prefer structured composite keys with database-enforced uniqueness:**

```sql
-- Example PostgreSQL schema
CREATE TABLE idempotency_records (
    tenant_id       UUID NOT NULL,
    client_id       UUID NOT NULL,
    principal_id    UUID NOT NULL,
    operation_id    TEXT NOT NULL,  -- genxSubmitAsyncJob
    idempotency_key TEXT NOT NULL,
    request_fingerprint TEXT NOT NULL,
    status          TEXT NOT NULL,  -- claimed|in_progress|completed|...
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    response_ref    TEXT,           -- reference to stored response (optional)
    tombstone       BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (tenant_id, client_id, principal_id, operation_id, idempotency_key)
);
```

If a serialized namespace string is needed:
```
genx:idemp:v1:{tenant_id}:{client_id}:{principal_id}:{operation_id}:{key}
```
- Version prefix (`v1`) for future migration.
- Explicit field boundaries (no ambiguous concatenation).

---

## 4. Request fingerprint architecture

### 4.1 Common envelope

```python
@dataclass
class RequestFingerprintInput:
    operation_id: str                    # stable GenX operation ID
    http_method: str                     # GET, POST, etc.
    canonical_payload: bytes             # JCS-canonicalized request body
    relevant_query_params: dict[str, str]  # operation-specific
    relevant_headers: dict[str, str]       # operation-specific
    contract_version: str                # API/contract version
    # Excluded: auth tokens, trace IDs, connection info, timestamps, proxy headers
```

### 4.2 Operation-specific context definitions

Each GenX operation defines which query parameters and headers materially affect
its behaviour. Examples:

| Operation | Relevant query params | Relevant headers |
|---|---|---|
| `genxSubmitAsyncJob` | none | `Content-Type` |
| `genxListVariableTermVersions` | `variableDbId`, `ontologyDbId`, `status`, `page`, `pageSize` | `Accept` |
| `genxRegisterModelVersion` | none | `Content-Type` |
| `genxAppendSeedLotLedgerEntry` | none (path param `seedLotDbId` in operation_id context) | `Content-Type` |
| `genxAppendTelemetryBatch` | none | `Content-Type` |

### 4.3 Fingerprint calculation

```python
def compute_request_fingerprint(input: RequestFingerprintInput) -> str:
    envelope = {
        "operation_id": input.operation_id,
        "http_method": input.http_method,
        "payload": json.loads(input.canonical_payload.decode()),
        "query": input.relevant_query_params,
        "headers": input.relevant_headers,
        "contract_version": input.contract_version,
    }
    canonical_bytes = rfc8785.dumps(envelope)
    return sha256(canonical_bytes).hexdigest()
```

### 4.4 Equivalence rules

| Scenario | Fingerprint | Equivalent? |
|---|---|---|
| Same key, identical request | Same | **Yes** (replay) |
| Same key, different property order | Same (JCS normalizes) | **Yes** |
| Same key, omitted vs explicit `null` | Different (JCS preserves) | **No** (conflict) |
| Same key, different numeric repr | Same (JCS normalizes numbers) | **Yes** |
| Same key, different array order | Different (JCS preserves array order) | **No** |
| Same key, different query param | Different | **No** |
| Same key, different HTTP method | Different | **No** |
| Same key, different tenant | Different namespace | N/A (separate namespace) |

---

## 5. Persistent idempotency state model

### 5.1 Record schema

```python
@dataclass
class IdempotencyRecord:
    # Composite primary key
    tenant_id: UUID
    client_id: UUID
    principal_id: UUID
    operation_id: str          # e.g., genxSubmitAsyncJob
    idempotency_key: str       # client-supplied

    # Request identity
    request_fingerprint: str   # SHA-256 hex

    # State machine
    status: IdempotencyStatus  # claimed | in_progress | completed | retryable_failure | terminal_failure | indeterminate | tombstoned
    created_at: datetime
    updated_at: datetime
    expires_at: datetime       # TTL for tombstone/response

    # Completion data
    completed_at: Optional[datetime] = None
    response_ref: Optional[str] = None    # reference to stored response
    failure_info: Optional[FailureInfo] = None

    # Recovery
    retry_count: int = 0
    last_attempt_at: Optional[datetime] = None
```

### 5.2 State machine

```
                    ┌─────────────────────┐
                    │      CLAIMED        │
                    │  (record created,   │
                    │   operation not     │
                    │   started)          │
                    └──────────┬──────────┘
                               │ start execution
                               ▼
                    ┌─────────────────────┐
                    │   IN_PROGRESS       │
                    │ (operation running) │
                    └──────────┬──────────┘
                ┌───────────────┴───────────────┐
                │                               │
         success/fail                     crash/restart
                │                               │
                ▼                               ▼
       ┌───────────────┐              ┌──────────────────┐
       │   COMPLETED   │              │ INDETERMINATE    │
       │ (result stored)│              │ (recovery needed)│
       └───────┬───────┘              └────────┬─────────┘
               │                               │
         response                    reconciliation
        retained or                    (check actual
       tombstoned only                 state, update)
               │                               │
               ▼                               ▼
       ┌───────────────┐              ┌──────────────────┐
       │  TOMBSTONED   │              │  COMPLETED or    │
       │ (identity only)│              │  RETRYABLE_FAIL  │
       └───────────────┘              └────────┬─────────┘
                                                  │
                                           retry / give up
                                                  │
                                           ┌──────┴──────┐
                                           ▼             ▼
                                    ┌──────────┐ ┌───────────────┐
                                    │COMPLETED │ │TERMINAL_FAIL  │
                                    └──────────┘ └───────────────┘
```

**Key transitions:**
- `CLAIMED` → `IN_PROGRESS` (atomic with mutation start).
- `IN_PROGRESS` → `COMPLETED` (on success, with result).
- `IN_PROGRESS` → `RETRYABLE_FAILURE` (on known retryable error).
- `IN_PROGRESS` → `TERMINAL_FAILURE` (on non-retryable error).
- `IN_PROGRESS` → `INDETERMINATE` (on crash/power loss before commit).
- `INDETERMINATE` → `COMPLETED` / `RETRYABLE_FAILURE` (via reconciliation).
- `COMPLETED` → `TOMBSTONED` (after response retention expires).
- `TOMBSTONED` prevents re-execution during remaining TTL.

### 5.3 Concurrency handling

- **Atomic claim:** `INSERT ... ON CONFLICT DO NOTHING` (or equivalent) on
  composite primary key.
- **Race: same key, same fingerprint** → first wins (created), others see
  existing record → replay.
- **Race: same key, different fingerprint** → conflict (unique constraint
  violation on fingerprint column if added, or application-level check).
- **Multi-instance:** Database unique constraint + transaction isolation
  (SERIALIZABLE or explicit locking) coordinates across instances.
- **In-process lock** is a development convenience only; production uses
  database coordination.

---

## 6. Transaction boundaries and external side effects

### 6.1 Primary transactional sequence

```
1. Request received
2. Authentication + identity resolution
3. BEGIN TRANSACTION
4.   Idempotency claim (atomic insert)
5.   Request fingerprint comparison
6.   Business mutation (domain logic)
7.   Outcome persistence (result + idempotency record update)
8. COMMIT TRANSACTION
9. Response delivered
```

**Crash windows:**

| Window | State | Recovery |
|---|---|---|
| Before 4 | No record | Retry = new operation |
| 4-6 | Claimed, not executed | Reconciliation checks actual state |
| 6-7 | Mutation partial | Transaction rollback undoes both |
| 7-8 | Committed, not delivered | Retry finds COMPLETED record → replay |
| After 9 | Delivered | Normal replay path |

### 6.2 External side-effect patterns (use only where needed)

| Pattern | When to use | Complexity |
|---|---|---|
| **Transactional outbox** | Message broker, event log in same DB | Low |
| **Downstream idempotency** | External service accepts idempotency key | Medium |
| **Durable workflow state** | Multi-step async with external dependencies | High |
| **Event deduplication** | Event broker with at-least-once | Medium |
| **Reconciliation** | Uncertain state after crash | Medium |
| **Compensation** | Irreversible external action needs rollback | High |

**Default for GenX:** Start with **transactional outbox** for async job
completion events. Add other patterns only when a concrete workflow requires
them.

### 6.3 Delivery guarantees matrix

| Layer | Guarantee | Mechanism |
|---|---|---|
| HTTP transport | At-most-once (client may retry) | — |
| Idempotency layer | Duplicate detection | Composite unique key |
| Primary DB transaction | Atomic mutation + record | ACID |
| Async worker | At-least-once | Outbox + retry |
| External side effects | At-least-once + idempotent | Downstream key / reconciliation |

**No universal exactly-once execution.** The contract guarantees:
- A successfully completed operation will not be re-executed.
- A client retry will not create a duplicate mutation.
- An in-flight operation may be recovered via reconciliation.

---

## 7. Replay authentication and authorization

### 7.1 Required sequence (every replay)

```
1. Authenticate current request (token, credentials)
2. Resolve tenant_id, client_id, principal_id
3. Resolve operation_id from request
4. Look up idempotency record under composite key
5. IF record not found → normal processing (not a replay)
6. IF record.status == COMPLETED:
     a. Check current principal authorization for this operation + result
     b. IF authorized → return stored response (200 with replay status)
     c. IF NOT authorized → 403/404 (do not reveal record existence)
7. IF record.status == IN_PROGRESS:
     a. Return current status (202 or 200 with progress)
8. IF record.status in {RETRYABLE_FAILURE, INDETERMINATE}:
     a. Allow retry (re-execute or reconcile)
```

### 7.2 Authorization separation

- **Operation authorization:** Can this principal invoke this operation?
- **Result authorization:** Can this principal see this specific result?
- Both must be checked on replay. A principal may be authorized to submit a
  job but not to view another tenant's result (even with the idempotency key).

### 7.3 Information leakage prevention

- Do not distinguish "record exists but unauthorized" from "record does not
  exist" → both return 404.
- Do not expose idempotency keys in error messages.

---

## 8. Retention architecture

### 8.1 Two retention periods

| Retention type | Purpose | Duration | After expiry |
|---|---|---|---|
| **Full response** | Direct replay with original result | `response_ttl` (configurable) | Discard response body; keep tombstone |
| **Identity tombstone** | Prevent re-execution of completed mutation | `tombstone_ttl` ≥ `response_ttl` | Delete record; key reusable |

### 8.2 Recommended initial durations (maintainer decision required)

| Parameter | Suggested value | Rationale |
|---|---|---|
| `response_ttl` | 7 days | Covers typical async job + client retry window |
| `tombstone_ttl` | 30 days | Covers extended recovery, audit, regulatory |

**Expiry behaviour:**
- Background job deletes records where `expires_at < now()`.
- `TOMBSTONED` records deleted after `tombstone_ttl`.
- Key reuse after tombstone expiry → new operation (safe).

---

## 9. BijMantra integration boundaries

GenX must remain independently implementable while supporting future reuse by
AuMatiKaya and other BijMantra components.

### 9.1 Shared capability interfaces (language-neutral)

| Capability | Interface | Notes |
|---|---|---|
| Raw-byte digest | `digest(bytes) -> hex` | Pure function |
| Canonical JSON digest | `canonical_digest(json_bytes) -> DigestResult` | Includes JCS |
| Operation identity | `get_operation_id(request) -> str` | From registry |
| Identity resolution | `resolve_identities(request) -> IdentityContext` | Tenant, client, principal |
| Request fingerprint | `fingerprint(input) -> str` | Uses JCS |
| Idempotency state | CRUD + atomic claim on composite key | DB-backed |
| Replay authorization | `authorize_replay(principal, record) -> bool` | Domain-specific |

### 9.2 Do not couple to

- Specific Rust crate / Python framework.
- Specific database (PostgreSQL, SQLite, etc.).
- Specific identity provider (OIDC, API key, mTLS).
- Internal BijMantra database structures.
- AuMatiKaya module ownership boundaries.

---

## 10. Architecture diagrams

### 10.1 Digest flow

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────┐
│  Input JSON  │────▶│  JCS Canonicalize │────▶│  SHA-256    │
│   (bytes)    │     │  (rfc8785.dumps)  │     │  (hex)      │
└──────────────┘     └────────┬─────────┘     └──────┬──────┘
                             │                      │
                    ┌────────┴────────┐     ┌───────┴───────┐
                    │ Validate Input  │     │ DigestResult  │
                    │ - dup keys      │     │ {algo, purpose,│
                    │ - no NaN        │     │  value,       │
                    │ - no surrogates │     │  profile}     │
                    │ - safe ints     │     └───────────────┘
                    └─────────────────┘
```

### 10.2 Idempotency flow (submit)

```
Client Request
      │
      ▼
┌─────────────────┐
│ Authenticate    │──▶ tenant_id, client_id, principal_id
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Resolve Op ID   │──▶ genxSubmitAsyncJob (from registry)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Key     │──▶ header > body; conflict → 400
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Canonicalize    │──▶ JCS canonical payload
│ Request Body    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Fingerprint     │──▶ SHA-256(op_id + method + payload + query + headers)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Atomic Claim    │──▶ INSERT ON CONFLICT (composite PK)
│ (DB transaction)│
└────────┬────────┘
    ┌────┴────┐
    │         │
 EXISTING   NEW
    │         │
    ▼         ▼
 Compare   Execute
Fingerprint Mutation
    │         │
    ▼         ▼
 REPLAY    COMPLETE
 (200)     (202)
```

---

*This architecture implements the ratified Cluster 1 decisions. Implementation
proceeds in bounded slices per the roadmap document.*