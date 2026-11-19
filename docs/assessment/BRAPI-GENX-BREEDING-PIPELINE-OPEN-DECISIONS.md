# BrAPI-GenX — Breeding Pipeline Open Maintainer Decisions

**Status:** Advisory record of remaining open choices; the CAS ratification is D-BP-14 in the approved decision record.  
**Workstream:** BGX-P1-06  
**Canonical specification:** [RFC-154 — Breeding Pipeline](../../Specification/BrAPI-GenX/RFC-154-BreedingPipeline.md)  
**Ratified decisions:** [D-BP-01 through D-BP-14](./BRAPI-GENX-BREEDING-PIPELINE-DECISIONS-APPROVED.md)

This note separates the approved conceptual model from additional wire-level, authorization, authority-resolution, and measurement semantics that must be settled before RFC-154 can become normative.

## 1. Ratified candidate decision — current published revision concurrency

**Maintainer decision: Option A — optimistic compare-and-set (CAS) approved on 19 November 2026.**

The maintainer approved retaining the candidate profile in RFC-154 §12.7. The ratification is limited to the concurrency model for a single current published revision per stable BreedingPipeline identity. It does not approve publication/withdrawal permissions, actor roles, audit-resource shape, authority onboarding/dereferencing, target-scale resolution, or normative RFC promotion.

The normative intent of the ratified candidate profile is:

- First registration omits the expected-current precondition; creation of the workstream and first revision is atomic. Competing first creators cannot overwrite or silently append to the winner's workstream.
- A new immutable revision under an existing workstream supplies the exact current published version, or explicit JSON `null` when none exists. Omission is not equivalent to null.
- Replay lookup is scoped to the owning pipeline. An identical same-version retry is resolved before checking a now-stale expected pointer; the same version identity with different canonical content conflicts.
- A new draft is appended only after a successful expected-pointer comparison and does not move the current published pointer. It records the declared preparation baseline in `basedOnBreedingPipelineVersionDbId`, not in a `supersedes` or `corrects` revision relationship.
- Publication appends the immutable revision and advances the current pointer in one atomic commit. Withdrawal appends an immutable withdrawal revision and clears the pointer in one atomic commit.
- A publication/withdrawal becomes effective at the successful atomic commit. Competing requests against the same baseline have at most one successful pointer transition; a stale loser receives HTTP 409 Conflict with no partial append or pointer mutation.
- Persistence mechanisms may differ, but must prevent time-of-check/time-of-use races and provide equivalent externally observable semantics. Defined audit/outbox side effects must commit or roll back with the operation.

The current 62-scenario fixture corpus (15 valid, 47 invalid) validates selected logical branches and includes a fixture-only Scale evidence profile. It does not execute remote dereferencing or service behavior. Before normative promotion, run the implementation-independent [BreedingPipeline CAS Behavioral Conformance Plan](./BRAPI-GENX-BREEDING-PIPELINE-CAS-BEHAVIORAL-TEST-PLAN.md) against an independently implemented service. It includes deterministic two-writer race tests, first-creation collision tests, cross-pipeline version-ID collision tests, retries after a lost response, withdrawal races, and transaction-failure injection. These tests distinguish contract fixture validation from actual concurrent service behavior.

RFC-154 §12.7 records the ratification and the strengthened candidate semantics. D-BP-01 through D-BP-13 remain the original conceptual design baseline; D-BP-14 separately ratifies CAS as the candidate current-pointer concurrency model.
## 2. Draft/withdrawal relationship semantics — schema refinement applied

A draft revision records its preparation baseline with `basedOnBreedingPipelineVersionDbId`; this is not a `revisionRelationship` and does not mean that the draft supersedes or corrects the current published revision. RFC-154 §12.4 and the candidate BreedingPipeline schema now express this separation. Candidate fixtures also reject a draft that claims a published supersession and require the baseline when a draft is appended over a published revision.

Withdrawal remains a new immutable revision that uses `revisionRelationship.relationshipType=withdraws` and identifies the exact current published version it withdraws. It does not mutate or delete that historical published revision. Drafts use `basedOnBreedingPipelineVersionDbId` and omit `revisionRelationship`; published successors use `supersedes` or `corrects`.

This refinement does not change the ratified CAS model.
## 3. Publication and withdrawal authorization

The contract must distinguish permission to create a draft from permission to publish or withdraw a strategy used by breeding operations.

**Recommendation:**
- Permit draft registration under the ordinary pipeline write authority.
- Require an explicit publish permission for the transition to `published`.
- Require an explicit withdrawal permission for the transition to `withdrawn`.
- Enforce authorization against the owning BrAPI Program and the pipeline authority/tenant context.
- Record actor, time, reason, and the exact prior/current version in an auditable lifecycle event or equivalent immutable provenance.
- Do not infer publication permission from possession of a general write token.

Do not hard-code scope token names until the repository's authorization model and deployment profile are selected. The decision is whether publish/withdraw are separate governed actions, not the spelling of a token.

**Candidate profile:** RFC-154 §12.10 now records a more complete implementation-independent security profile. It distinguishes authenticated client from effective principal, binds authorization to the owning Program and pipeline authority, requires fresh authorization before replay disclosure, prevents stale-pointer disclosure to callers without read access, and requires successful lifecycle audit evidence to commit atomically with publication/withdrawal.

**Recommendation:** separate draft/write, publish, and withdraw actions; retain distinct authenticated-client, effective-principal, and tenant context; record immutable publish/withdraw audit events; and revalidate authorization at the mutation commit boundary or document a versioned authorization decision with explicit revocation semantics.

**Open choice:** approve or revise this action separation, revocation timing, delegation model, required reason/justification, and audit evidence shape. Exact scope-token names and provider/claim mapping remain governed by D-22 and are intentionally not invented here. This proposal is not ratified.

## 4. BrAPI server authority canonicalization and dereferencing

The reference envelope is approved in shape: BrAPI (Breeding Application Programming Interface) generation, exact resource type, authoritative server URI (Uniform Resource Identifier), and server-issued dbId. The canonical server identity and network dereferencing policy remain open.

**Candidate normalization baseline:** RFC 3986 §§6.2.2–6.2.3. Current fixture checks only reject non-absolute HTTP(S) references and user information, query, or fragment components; they do not implement the full normalization rules below.

- Require an absolute HTTP or HTTPS base URI with an authority.
- Reject user information, query, and fragment components.
- Lowercase scheme and DNS host.
- Normalize percent-encoding hex case, decode unreserved characters only, remove dot segments, and remove the default port.
- Normalize an empty HTTP(S) path to `/`.
- Preserve path case, reserved percent-encoded octets, and non-empty trailing slash; the configured BrAPI base path is part of the server identity.
- Do not replace the declared authority with a redirect target during canonicalization.

**Security recommendation:** URI normalization does not itself authorize a network fetch. Runtime dereferencing should be restricted to explicitly configured/trusted authorities, with outbound-request controls and redirect restrictions. Do not let an arbitrary request URI become an unrestricted server-side fetch target.

**Open choices:** whether production authorities must be HTTPS-only; how private/test HTTP authorities are registered; the internationalized DNS name profile; DNS rebinding and proxy rules; redirect policy; and whether authority onboarding is an administrator-managed trust registry or a tenant-controlled registry.

## 5. Quantitative target validation against BrAPI Scale

The official BrAPI v2.1 schema defines an ObservationVariable as a unique combination of Trait, Method, and Scale. Its Scale defines `dataType`, `decimalPlaces`, `units`, and `validValues`; the v2.1 `minimumValue` and `maximumValue` fields are strings, while older `min` and `max` fields are deprecated.

Source contracts:
- [ObservationVariable](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/BrAPI-Phenotyping/ObservationVariables/Schemas/ObservationVariable.yaml)
- [VariableBaseClass](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/Components/Schemas/VariableBaseClass.yaml)
- [ScaleBaseClass](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/Components/Schemas/ScaleBaseClass.yaml)
- [TraitDataType](https://github.com/plantbreeding/BrAPI/blob/brapi-V2.1/Specification/BrAPI-Schema/BrAPI-Common/TraitDataType.json)

**Recommended semantic rules:**
- A direction-only objective may cite a Trait or ObservationVariable.
- A quantitative threshold or range must cite an authority-qualified ObservationVariable whose resolved Scale has `dataType: Numerical`.
- Units come from the BrAPI Scale; GenX must not accept a conflicting free-text unit.
- Enforce configured minimumValue/maximumValue bounds.
- When decimalPlaces is explicitly defined, reject a target requiring more precision rather than silently rounding or truncating it.
- Do not guess precision when decimalPlaces is null or absent.
- A categorical Scale must not be coerced into a numeric measurement.

**Candidate lifecycle recommendation — not ratified:** draft authoring may retain an unresolved quantitative ObservationVariable reference, but it must be treated as unverified. Publication requires successful resolution to the exact authority-qualified ObservationVariable and validation against a Numerical Scale, including configured bounds and explicitly defined precision. This profile blocks publication on unresolved or non-numerical references.

A published revision needs durable evidence of the Scale definition used at validation time. Prefer a separate immutable provenance/audit artifact containing the authoritative reference, a content digest, and the relevant Scale fields; do not copy the Scale into the ObservationVariable reference or add a free-text unit to the target. The exact evidence schema, digest algorithm, storage location, retention/freshness rules, revalidation policy, and response to remote Scale changes remain open. The fixture corpus scaleEvidence object is test-harness input only, not a proposed API payload.

**Open choice — dereferencing point and trust:** choose synchronous resolution at registration versus deferral until publication; determine the trusted authority registry, outbound-request restrictions, redirect and DNS rebinding policy, and HTTPS/HTTP deployment profile. Static fixtures do not establish remote-server trust or accessibility.

**Open choice — exact precision and bounds:** confirm whether decimalPlaces is a maximum number of fractional digits (including whether trailing zeroes count), whether minimumValue and maximumValue are inclusive, and how missing/null precision is treated. The candidate check currently interprets configured bounds inclusively and rejects lexical decimal precision above an explicit decimalPlaces; those interpretations remain pending maintainer approval. No silent unit conversion or implicit rounding is proposed.

**Candidate evidence-record model:** one immutable evidence record per quantitative target, bound to the exact pipeline/revision, target-context identifier, zero-based trait-requirement index, and full authority-qualified ObservationVariable reference. It captures the relevant Scale projection and retrieval/validation timestamps. The evidence preimage is the exact ObservationVariable reference plus the captured Scale projection. JCS-RFC8785 is the accepted canonical JSON method, but D-02 does not select the cryptographic hash algorithm; SHA-256 must not be presented as a universal approved algorithm. The exact evidence resource identity, revision link, endpoint/storage location, correction relation, and retention are still open. The detailed candidate is in [Target-Scale Validation Evidence Design](./BRAPI-GENX-BREEDING-PIPELINE-TARGET-SCALE-EVIDENCE-DESIGN.md).

The candidate publication transaction must persist the evidence record, immutable revision, current pointer, and any required audit/outbox record atomically. A remote Scale change after publication does not mutate historical evidence; a new published revision must obtain new evidence under this profile. Independent service tests are listed in [Scale Evidence Behavioral Acceptance Plan](./BRAPI-GENX-BREEDING-PIPELINE-SCALE-EVIDENCE-BEHAVIORAL-TEST-PLAN.md).

## 6. Required evidence before normative promotion

1. Implement and behaviorally validate the ratified current-pointer concurrency model using the [CAS Behavioral Conformance Plan](./BRAPI-GENX-BREEDING-PIPELINE-CAS-BEHAVIORAL-TEST-PLAN.md), including simultaneous publication, first-creation collisions, idempotent retries, withdrawal races, and failure atomicity.
2. Approved publish/withdraw actor permissions and lifecycle audit behavior.
3. Approved authority URI normalization, trusted-server onboarding, and dereferencing policy.
4. Approved target-scale resolution timing, evidence identity/link/storage, snapshot fingerprint algorithm, precision semantics, and immutable scale-evidence profile.
5. Positive and negative contract fixtures for the approved choices.
6. Behavior-level tests against a real implementation, including simultaneous publication attempts, replay after pointer movement, authority collisions, unavailable authority servers, wrong resource types, scale bounds, and precision.

## 7. Status boundary

- D-BP-01 through D-BP-13 remain the original approved conceptual design decisions; D-BP-14 separately ratifies the candidate CAS concurrency profile.
- This note does not ratify the remaining open authorization, authority-trust/dereferencing, and target-scale measurement choices. CAS is separately ratified as D-BP-14.
- RFC-014 remains historical; RFC-154 remains an approved candidate design.
- The candidate fixtures and static checkers prove only the invariants they test. They do not prove production database atomicity, remote authority availability, authorization enforcement, or interoperability with an independently implemented server.
- No official BrAPI v2.1 source contract is modified by this workstream.
