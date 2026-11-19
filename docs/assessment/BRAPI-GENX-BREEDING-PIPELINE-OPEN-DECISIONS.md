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

The current fixtures validate selected logical branches only. Before normative promotion, run the implementation-independent [BreedingPipeline CAS Behavioral Conformance Plan](./BRAPI-GENX-BREEDING-PIPELINE-CAS-BEHAVIORAL-TEST-PLAN.md) against an independently implemented service. It includes deterministic two-writer race tests, first-creation collision tests, cross-pipeline version-ID collision tests, retries after a lost response, withdrawal races, and transaction-failure injection. These tests distinguish contract fixture validation from actual concurrent service behavior.

RFC-154 §12.7 records the ratification and the strengthened candidate semantics. D-BP-01 through D-BP-13 remain the original conceptual design baseline; D-BP-14 separately ratifies CAS as the candidate current-pointer concurrency model.
## 2. Draft/withdrawal relationship semantics — schema refinement applied

A draft revision records its preparation baseline with `basedOnBreedingPipelineVersionDbId`; this is not a `revisionRelationship` and does not mean that the draft supersedes or corrects the current published revision. RFC-154 §12.4 and the candidate BreedingPipeline schema now express this separation. Candidate fixtures also reject a draft that claims a published supersession and require the baseline when a draft is appended over a published revision.

Withdrawal remains a new immutable revision that identifies the exact current published version it withdraws. It does not mutate or delete that historical published revision.

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

**Candidate normalization baseline:** RFC 3986 §§6.2.2–6.2.3.

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

**Open choice — dereferencing point:** either synchronously resolve the ObservationVariable at registration, or permit unresolved draft references but require successful resolution and validation before publication. The recommended lifecycle is draft may remain unverified, but publication must resolve and validate the reference. A published pipeline revision should preserve enough Scale evidence (authoritative reference plus an immutable snapshot of the relevant dataType, decimalPlaces, units, and validValues) to explain the target semantics even if the remote BrAPI record later changes.

**Open choice — exact precision and bounds:** confirm the meaning of decimalPlaces as a maximum reported precision for targets, whether min/max bounds are inclusive, and how scale changes are handled. No silent unit conversion or implicit rounding should occur.

## 6. Required evidence before normative promotion

1. Implement and behaviorally validate the ratified current-pointer concurrency model using the [CAS Behavioral Conformance Plan](./BRAPI-GENX-BREEDING-PIPELINE-CAS-BEHAVIORAL-TEST-PLAN.md), including simultaneous publication, first-creation collisions, idempotent retries, withdrawal races, and failure atomicity.
2. Approved publish/withdraw actor permissions and lifecycle audit behavior.
3. Approved authority URI normalization, trusted-server onboarding, and dereferencing policy.
4. Approved target-scale resolution timing and immutable scale-evidence profile.
5. Positive and negative contract fixtures for the approved choices.
6. Behavior-level tests against a real implementation, including simultaneous publication attempts, replay after pointer movement, authority collisions, unavailable authority servers, wrong resource types, scale bounds, and precision.

## 7. Status boundary

- D-BP-01 through D-BP-13 remain the original approved conceptual design decisions; D-BP-14 separately ratifies the candidate CAS concurrency profile.
- This note does not ratify the remaining open authorization, authority-trust/dereferencing, and target-scale measurement choices. CAS is separately ratified as D-BP-14.
- RFC-014 remains historical; RFC-154 remains an approved candidate design.
- The candidate fixtures and static checkers prove only the invariants they test. They do not prove production database atomicity, remote authority availability, authorization enforcement, or interoperability with an independently implemented server.
- No official BrAPI v2.1 source contract is modified by this workstream.
