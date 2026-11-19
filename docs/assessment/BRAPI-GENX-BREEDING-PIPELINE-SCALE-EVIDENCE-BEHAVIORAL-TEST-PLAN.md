# BreedingPipeline Target-Scale Evidence — Behavioral Acceptance Plan

**Status:** Independent-service acceptance plan for a candidate profile. Not ratified. No production implementation or conformance is claimed by this plan.

**Related:** RFC-154 §12.8; Target-Scale Validation Evidence Candidate Design; D-BP-14; D-02; D-22.

## 1. Purpose and test boundary

These scenarios test the behavior of a real BreedingPipeline service, including its BrAPI authority-resolution boundary, persistence, immutable revision history, evidence retention, and current-pointer mutation. They are not satisfied by static JSON fixtures or a pure validation helper.

The selected authority, client authentication, tenant context, and persistence configuration must be recorded by each implementation running the plan. Do not invent a universal permission-scope token. Publication/withdrawal authorization remains subject to D-22 and RFC-154 §12.10.

## 2. Candidate scenarios

### SCALE-EV-01 — draft may remain unverified

**Initial state:** a valid draft references an authority-qualified ObservationVariable that has not yet been resolved.

**Action:** register the draft.

**Expected result:** the draft may be stored as a draft; no successful Scale-validation evidence is attached; the current published pointer is unchanged. The response must not imply that the target has been scientifically or quantitatively validated.

### SCALE-EV-02 — publication requires exact ObservationVariable resolution

**Initial state:** a draft has a quantitative target referencing a BrAPI Trait, a wrong resource type, or an ObservationVariable under another authority with the same dbId.

**Action:** publish the draft.

**Expected result:** publication fails closed. The server must not substitute a Trait, infer a local server, or resolve an equal dbId at another authority. No revision append, evidence record, or current-pointer mutation is committed.

### SCALE-EV-03 — source unavailable or not found

**Initial state:** the declared authority returns not-found, times out, is unreachable, or returns an invalid response.

**Action:** publish the draft.

**Expected result:** publication is rejected with a documented retriable or non-retriable error classification. The draft remains available; the current published revision and history are unchanged; no successful evidence record is persisted.

### SCALE-EV-04 — Numerical Scale and valid-value bounds

**Initial state:** the exact ObservationVariable resolves to a Numerical Scale with configured minimumValue and maximumValue.

**Action:** publish targets at each bound and just outside each bound.

**Expected result:** the candidate profile accepts the inclusive endpoints and rejects values outside the configured interval. Bounds are parsed as decimal strings. Deprecated min/max must not override the v2.1 minimumValue/maximumValue fields.

### SCALE-EV-05 — non-numerical Scale

**Initial state:** the ObservationVariable Scale has Code, Date, Duration, Nominal, Ordinal, Text, or another non-Numerical data type.

**Action:** publish a numeric threshold or range.

**Expected result:** publication is rejected. No coercion into Numerical occurs and no Scale-validation evidence with a passed result is persisted.

### SCALE-EV-06 — category-governed values

**Initial state:** the Scale's validValues.categories defines allowed categories.

**Action:** publish a target using an allowed value and another target using a value absent from the category set.

**Expected result:** values are checked against the allowed category values, not treated as unrestricted continuous numeric values. The service documents its exact string/decimal matching semantics.

### SCALE-EV-07 — decimal precision and exact representation

**Initial state:** the Scale declares decimalPlaces.

**Action:** publish targets with precision within and beyond the limit, including exact-decimal strings with trailing zeroes.

**Expected result:** the selected profile applies the approved precision rule without rounding or truncation. Until the maintainer chooses the JSON-number rule, the implementation must not claim that parsed JSON numbers preserve the original lexical number of decimal places.

### SCALE-EV-08 — null or absent precision and units

**Initial state:** the Scale has null/absent decimalPlaces, and/or null/absent units.

**Action:** publish an otherwise valid quantitative target.

**Expected result:** the service does not invent a precision or unit. The evidence projection preserves the source's null-versus-absent field state. Any product requirement that needs a unit must fail or require a stronger profile rather than infer a conversion.

### SCALE-EV-09 — target/evidence binding

**Initial state:** a pipeline revision has multiple target contexts and multiple trait requirements, including repeated ObservationVariable dbId values across distinct authority references.

**Action:** publish the revision and retrieve its evidence.

**Expected result:** every evidence record binds to exactly one (pipelineDbId, pipelineVersionDbId, targetContextId, traitRequirementIndex) tuple and the exact four-part ObservationVariable reference. Evidence from a different revision, target context, index, or authority must not be accepted.

### SCALE-EV-10 — immutable Scale projection

**Initial state:** a published pipeline revision has a passed evidence record with a captured Scale projection.

**Action:** the remote authority changes dataType, decimalPlaces, units, or validValues; retrieve the old revision and evidence.

**Expected result:** the old revision and evidence remain byte-for-byte/content-identical. A new published revision performs a new resolution and creates a new evidence identity. No old evidence is refreshed or silently overwritten.

### SCALE-EV-11 — publication transaction failure

**Initial state:** the server has resolved and validated the Scale and prepared a new revision and evidence record. The expected-current pointer matches.

**Action:** inject a failure after evidence persistence is staged but before the publication transaction commits.

**Expected result:** revision append, evidence persistence, current-pointer change, and required audit/outbox record all roll back together. No success is returned before durable commit.

### SCALE-EV-12 — concurrent publication

**Initial state:** two writers submit different new published revisions against the same expected-current pointer; both have independently resolved and validated their target evidence.

**Action:** execute both publications concurrently.

**Expected result:** D-BP-14 semantics hold. At most one publication advances the pointer. The losing transaction commits neither a published revision nor orphaned passed evidence. It receives the documented stale-precondition conflict and must re-read before retrying with a new version/evidence identity.

### SCALE-EV-13 — identical replay after pointer movement

**Initial state:** a published revision and its immutable Scale evidence already exist. The current pointer has since advanced.

**Action:** replay the identical registration for the earlier version ID.

**Expected result:** the original result and already-bound evidence are returned only after fresh authorization under D-24. No second evidence record is created, no new Scale resolution is needed for the immutable replay, and the current pointer is not moved backward.

### SCALE-EV-14 — authority fetch protections

**Initial state:** a caller supplies an untrusted or unregistered authority URI, a redirect to a disallowed destination, or a host resolving to a private/link-local destination.

**Action:** request publication-time dereferencing.

**Expected result:** the implementation applies its explicitly approved trust/egress profile and fails closed when the destination is not authorized. It must not expose credentials or permit an unrestricted server-side request forgery path. Exact allow-list, redirect, DNS, proxy, and HTTPS rules require maintainer approval before this scenario can be normative.

### SCALE-EV-15 — fingerprint reproducibility

**Initial state:** two independent implementations receive the same exact authority reference and Scale projection, including identical null/omitted-field state.

**Action:** calculate the candidate Scale-projection fingerprint after a cryptographic algorithm has been separately selected.

**Expected result:** both implementations produce identical JCS-RFC8785 preimage bytes and identical digest output for the selected algorithm. Mutating the authority reference, Scale fields, or null/omitted state changes the preimage. This scenario cannot pass as an interoperable digest test until the hash algorithm and envelope are approved.

## 3. Evidence to retain per run

- implementation name/version and commit;
- persistence engine/isolation configuration;
- authority fixture/server identity and controlled response payloads;
- trusted-authority policy and network egress configuration;
- exact request/response payloads with credentials removed;
- pipeline revision/evidence IDs before and after;
- current-pointer state before and after;
- transaction fault-injection point and commit/rollback trace;
- expected and observed outcomes for every scenario.

## 4. Explicit non-claims

Passing this plan demonstrates only the tested service/configuration behavior. It does not prove scientific suitability of the breeding target, authority trust outside the tested allow-list, official BrAPI endorsement, D-22 authorization approval, or conformance of every BrAPI-GenX operation.
