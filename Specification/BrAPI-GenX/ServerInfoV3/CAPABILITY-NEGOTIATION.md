# ServerInfoV3 capability negotiation audit

**Status:** experimental design review for BrAPI GenX; non-normative. This document does not change BrAPI V2.1 and does not ratify deferred decisions.

## Findings

The current ServerInfoV3 draft advertises a capability `name`, a set of `versions`, a set of `methods`, and optional `scopes`, but does not name the routes that a client should associate with the capability. That gap is material because the capabilities are not all route families. `provenanceEnvelope` is an embedded data contract with no standalone route, yet the example advertises `GET` and `POST`. Without an explicit boundary, a client or an agent could incorrectly invent a `/provenanceEnvelope` route.

A second ambiguity concerns versions. The contract currently shows both `brapiVersions` (for example, `2.1`, `3.0-draft`) and per-capability `versions` (for example, `1.0`) without stating whether they can be compared or ordered. The safe interim behavior is exact token matching only; a draft token must not be treated as a released version by inferred semver ordering.

A fourth concrete gap is the advertised set of job types. `JobNewRequest.jobType` says the requested type must be a type the server advertises, but the old ServerInfoV3 capability only named the `jobs` methods. It did not enumerate whether that server accepts `germplasm_search`, `analysis`, `inference`, or other types. The prototype accepts exactly the first three and rejects `export`, so a client previously had no explicit discovery field to rely on. This branch adds experimental optional `jobs.jobTypes[]` and verifies that the advertisement matches the runtime's accepted-token list. Requiredness, compatibility when the list is absent, and job-type version/deprecation semantics remain open as D-23.

A third ambiguity is security-related: `ServerCapability.scopes` is described as scopes “required to use” a capability, while `ServerAuthProfile.scopes` is described as scopes “issued or required”. These do not mean the same thing. The current reference server advertises an auth profile named `none` while not implementing authentication at all; the schema text gives a meaning to `oidc` and then says absence of `oidc` means V2.1 bearer semantics, without defining what `none` means. Clients must not treat these descriptive strings as proof of enforcement.

## Proposed additive operation mapping

The machine-readable [capability registry](./capability-registry.json) lists every current GenX capability and its operation surfaces. The experimental optional `operations[]` property in `ServerCapability` mirrors that information using:

- `route`: full route template, including `/brapi/v3`;
- `method`: HTTP method;
- `operationId`: stable operation identity already catalogued in [ENDPOINT-IDENTITY.md](../ENDPOINT-IDENTITY.md).

The `methods` property is defined here as the set union of methods from the operation list; array ordering is not semantically significant in this proposal. It is not an endpoint locator and does not imply that every method works on every route under that capability. A client must use the exact route/method mapping and a known contract; it must not probe for undocumented routes. If an older server omits `operations`, the client must not infer route mappings from `methods` alone.

The mapping for `provenanceEnvelope` deliberately lists only the enclosing Job submission and retrieval operations where the example contract can travel. It explicitly does **not** invent a standalone provenance route. The current reference profile does not promise that every job result contains a provenance envelope.

This mapping is an implementation/audit proposal. Whether `operations` becomes part of ServerInfoV3, whether its operation identifiers are stable wire values, and whether a capability must have one or more operations are review decisions (D-21).

## Conservative client behavior to review

1. Fetch the server-info resource at the versioned base path being used. Parse the ordinary BrAPI response envelope.
2. Treat capability names and all version strings as exact, case-sensitive tokens. Require an explicit supported version token; do not sort or compare version strings as if their ordering were defined.
3. Ignore unknown capability names so that a newer server can advertise capabilities a client does not understand. Do not ignore duplicate names or contradictory duplicate entries; treat the document as malformed for that capability.
4. When `operations[]` is present, validate the route/method/operation identity against a known GenX contract before use. Do not discover capabilities by sending requests to routes not advertised by the negotiated contract.
5. When a V2.1-only response contains only `calls[]`, accept it as the V2.1 negotiation result. Use its `service`, `versions`, and `methods` under the existing V2.1 rules. Do not infer GenX availability or send GenX operations merely because a path might exist.
6. Do not derive authorization guarantees from advertised scopes or auth profile names until D-22 is resolved. Deployment policy and actual runtime enforcement remain separate concerns.

Items 2–6 are conservative proposal guidance for review, not newly ratified normative language.

## Static guardrail added in this branch

The checker verifies, for the example registry, that:

- advertised capability names are unique and correspond exactly to registered names;
- capability versions and methods are non-empty, unique string tokens, with supported method spellings;
- `methods` equals the union of the operation methods;
- every advertised operation maps to a unique operation in the checked-in GenX specification, with exact path, method, and operationId;
- capability operation references are unique and complete;
- auth profile names are unique and any scopes are well-formed arrays;
- unknown capabilities in a client-facing document can be ignored by clients, but the example server must not emit an unregistered capability.

Mutation tests must prove these checks fail closed when an advertised route is stale, a method is false, a version is duplicated, a capability name is duplicated, a scope list is malformed, or a required capability disappears.

## Proposed exact-token job type advertisement

When the `jobs` capability includes `jobTypes[]`, each string is an exact, case-sensitive token accepted by that server; it is not a synonym list and it does not imply support for other similarly named or unadvertised job types. In this prototype the list is `germplasm_search`, `analysis`, and `inference`. The list must match the actual job submission validator, not just the documentation example.

The schema keeps `jobTypes[]` optional for compatibility with older draft documents. Conservative client behavior is: when it is present, submit only an exact advertised token; when absent, do not assume any particular job type is supported and use only a type established through a separate versioned contract. Whether a future GenX release must include the list, and how job type names are versioned or deprecated, requires D-23 review.

## Decision boundary

D-21 covers whether the additive operation mapping, exact version-token matching, and method-summary semantics should be accepted. D-22 covers scope/auth-profile semantics, including empty/missing scopes, the `none` profile, and the distinction between scopes required to invoke an operation versus scopes issued by an identity provider. D-23 covers the `jobs.jobTypes[]` field, its requiredness when negotiating GenX, exact-token/namespace semantics, and future job-type versioning/deprecation.

This branch records evidence and a proposed mechanism; it does not change authentication behavior, publish a normative security model, alter any V2.1 contract, or wire GenX into V2.1 generation.
