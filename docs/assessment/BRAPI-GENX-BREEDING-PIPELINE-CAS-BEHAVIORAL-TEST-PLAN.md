# BrAPI-GenX — BreedingPipeline CAS Behavioral Conformance Plan

**Status:** Candidate acceptance plan; implementation-independent.  
**Decision:** D-BP-14 — optimistic compare-and-set for the current published revision pointer.  
**Canonical contract:** [RFC-154 §12.7](../../Specification/BrAPI-GenX/RFC-154-BreedingPipeline.md).  
**Scope:** Behavioral evidence required before the CAS profile can be used as a normative interoperability guarantee.

This plan defines externally observable behavior. It does not prescribe a database, transaction isolation level, locking strategy, programming language, or server architecture. A conforming implementation may use row locks, serializable transactions, conditional updates, or another mechanism, provided the externally observable results are equivalent.

## 1. Test environment and observability

Run these tests against an independently implemented BreedingPipeline service backed by its actual persistence layer. An in-memory mock or a sequential unit test alone is insufficient evidence for concurrent publication.

The harness must be able to:

- issue authenticated requests from at least two independent clients;
- coordinate concurrent requests with a barrier so both clients act on the same observed baseline;
- read the logical pipeline and its revision summaries after each operation;
- retrieve an exact immutable revision by version ID;
- record response status, structured conflict code, request correlation ID, and resulting resource state;
- repeat tests across separate service processes or replicas where the deployment supports them.

The harness may use a test-only failpoint to verify transaction rollback. Such a failpoint is test infrastructure, not a production API requirement.

For every rejected mutation, capture a before/after state snapshot containing at least:

- `currentBreedingPipelineVersionDbId`;
- the set of immutable revision IDs and their publication states;
- any externally observable lifecycle/audit/outbox event created by the operation.

## 2. Required behavioral scenarios

### CAS-01 — stale expected-current precondition

**Initial state:** pipeline P exists; V3 is the current published revision.

**Request:** append a new published revision V4 with `expectedCurrentBreedingPipelineVersionDbId=V2`.

**Expected result:**

- HTTP 409 Conflict;
- `errorCode=current-version-precondition-failed`;
- no V4 revision is appended;
- current pointer remains V3;
- no publication or lifecycle side effect is emitted.

### CAS-02 — simultaneous publication from one baseline

**Initial state:** pipeline P has current published revision V3.

**Concurrent requests:** Client A submits published V4-A and Client B submits published V4-B. Both use expected-current V3 and both identify V3 as the exact prior revision in their published successor relationship. A barrier ensures both requests are in flight against the same baseline.

**Expected result:**

- exactly one request succeeds;
- exactly one request receives HTTP 409 with `errorCode=current-version-precondition-failed`;
- the winner's immutable revision is present and is the current pointer;
- the losing revision is absent from history;
- no request reports success before its append and pointer transition are durably committed.

The test must be repeated with reversed client ordering and under realistic concurrent load. It must not assume that Client A always wins.

### CAS-03 — identical retry after pointer advancement

**Initial state:** CAS-02 has succeeded with V4-A as current; the successful request body is retained.

**Request:** resend the identical V4-A revision payload and version ID, including the original now-stale expected-current V3 precondition.

**Expected result:**

- the existing immutable V4-A result is replayed;
- the stale expected-current precondition does not turn an identical replay into a conflict;
- no additional revision or lifecycle event is created;
- the current pointer remains V4-A.

### CAS-04 — same version ID with changed immutable content

**Initial state:** version ID V4-A already exists under pipeline P.

**Request:** submit V4-A again with different canonical revision content.

**Expected result:**

- HTTP 409 Conflict;
- `errorCode=version-content-conflict`;
- the original V4-A content remains unchanged;
- no revision or pointer mutation occurs.

### CAS-05 — version-ID collision across logical pipelines

**Initial state:** pipeline P owns version ID V4-A. Pipeline Q is a different logical workstream.

**Request:** submit a revision under Q that reuses the version ID V4-A.

**Expected result:**

- HTTP 409 Conflict;
- `errorCode=pipeline-identity-conflict`;
- no replay of P's revision is returned to the Q request;
- no existence detail or payload from P is disclosed beyond the conflict needed to reject the collision;
- neither pipeline's history or current pointer is mutated.

### CAS-06 — simultaneous first creation of one logical pipeline

**Initial state:** logical pipeline ID P does not exist.

**Concurrent requests:** Client A and Client B both attempt first registration for P, each with a distinct immutable version ID. Neither request supplies the expected-current precondition.

**Expected result:**

- exactly one creation succeeds;
- the losing request receives HTTP 409 with `errorCode=pipeline-identity-conflict`;
- the losing request does not silently append its revision to the newly created pipeline;
- the losing client must re-read P and retry as an append with the observed expected-current value;
- the created logical identity and first revision are atomic.

### CAS-07 — first publication when no published revision exists

**Initial state:** pipeline P exists but has no current published revision (for example, it contains only drafts).

**Request:** publish a new immutable revision with explicit `expectedCurrentBreedingPipelineVersionDbId=null`.

**Expected result:**

- publication succeeds;
- the new revision is appended;
- the current pointer advances from null to the new version ID;
- omission of the expected-current field is not treated as equivalent to explicit null.

### CAS-08 — draft append preserves the published pointer

**Initial state:** pipeline P has current published revision V3.

**Request:** append draft V4-D with expected-current V3 and `basedOnBreedingPipelineVersionDbId=V3`.

**Expected result:**

- draft append succeeds;
- V4-D is present with publication state draft;
- the current published pointer remains V3;
- the draft does not use a `supersedes` or `corrects` relationship to claim replacement of V3.

### CAS-09 — multiple drafts may share one current baseline

**Initial state:** pipeline P has current published revision V3.

**Concurrent requests:** append two distinct drafts, both based on V3, each with expected-current V3.

**Expected result:**

- both drafts may be appended;
- neither draft moves the current published pointer;
- both drafts record V3 as their preparation baseline;
- a later publication from that baseline still must win the current-pointer comparison at commit time.

### CAS-10 — incorrect published successor relationship

**Initial state:** pipeline P has current published revision V3.

**Request:** publish V4 with expected-current V3 but name a different historical version as the prior revision in `revisionRelationship`.

**Expected result:**

- HTTP 409 Conflict;
- `errorCode=revision-relationship-mismatch`;
- no V4 append or pointer movement occurs.

### CAS-11 — withdrawal clears, but never deletes, the current revision

**Initial state:** pipeline P has current published revision V3.

**Request:** append a new immutable withdrawn revision V4-W with expected-current V3 and a relationship identifying exactly V3.

**Expected result:**

- withdrawal succeeds atomically;
- V4-W is appended as a new immutable revision;
- the current published pointer becomes null;
- V3 remains retrievable as historical content and is not mutated or deleted.

### CAS-12 — competing publication and withdrawal

**Initial state:** pipeline P has current published revision V3.

**Concurrent requests:** one client publishes V4-P and another withdraws V4-W, both against expected-current V3.

**Expected result:**

- at most one pointer-changing operation succeeds;
- the loser receives HTTP 409 with `errorCode=current-version-precondition-failed`;
- the final pointer and immutable history match the single successful operation;
- no partial append from the losing operation remains.

### CAS-13 — failure between append and pointer transition

**Initial state:** pipeline P has current published revision V3.

**Test action:** use a test-only failpoint to cause a transaction failure after the revision append has been attempted but before the current-pointer transition and required side effects complete.

**Expected result:**

- the operation fails;
- the new revision is not visible;
- the current pointer remains V3;
- required audit/outbox events for the failed operation are not visible;
- retrying the same request can complete once the injected failure is removed.

This is a transaction-level integration test. It cannot be proven by a JSON fixture alone.

### CAS-14 — durable success and retry after simulated lost response

**Initial state:** pipeline P has current published revision V3.

**Test action:** allow publication of V4 to commit, then simulate loss of the HTTP response before the client receives it. The client retries the identical request with the same version ID and original expected-current V3.

**Expected result:**

- retry returns the already committed V4 result;
- no duplicate revision, pointer transition, or duplicate lifecycle event is created;
- current pointer remains V4.

## 3. Cross-implementation acceptance criteria

A service implementation passes this profile only when:

1. all applicable scenarios above pass against its real persistence layer;
2. simultaneous publication tests demonstrate one winner and one stale loser, not merely sequential stale-write rejection;
3. conflict responses use the specified structured error codes;
4. every rejected mutation preserves revision history, current pointer, and defined side effects;
5. identical replay is idempotent after pointer advancement and after a simulated lost response;
6. the same behavior is demonstrated across multiple service processes or replicas where applicable;
7. no test relies on a particular database implementation or lock primitive.

Record implementation name, version, test harness version, storage configuration, concurrency configuration, scenario results, and any deployment limitations with the conformance evidence.

## 4. Explicit non-claims

Passing this plan demonstrates the tested CAS behavior for the tested implementation and configuration. It does not prove:

- scientific correctness of a breeding strategy;
- authorization policy for publication or withdrawal (which remains a separate governance decision);
- trusted-authority onboarding or secure remote dereferencing;
- target-scale validation against remote BrAPI ObservationVariable resources;
- conformance of every endpoint or resource in BrAPI-GenX.

The 39 candidate contract fixtures in `BRAPI-GENX-BREEDING-PIPELINE-CONTRACT-FIXTURES.json` cover model-level invariants. They are complementary to, not substitutes for, these behavioral service tests.
