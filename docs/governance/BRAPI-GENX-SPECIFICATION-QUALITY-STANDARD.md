# BrAPI-GenX Specification Quality Standard

**Status:** mandatory gate for future RFCs and resource specifications (Phase 0).
**Location:** `docs/governance/BRAPI-GENX-SPECIFICATION-QUALITY-STANDARD.md`

This standard is the principal gate for future RFCs and resource specifications.
It is written so that a small AI model can apply it without inventing missing
information: where evidence is insufficient, the RFC must document the ambiguity
and identify the required decision or external authority rather than guess.

## 1. Problem and scientific justification (E1)

Every RFC must describe:

- The real-world scientific, breeding, or interoperability problem.
- Intended users and organisations.
- Processes in which the information is used.
- Why the information needs standardised exchange.
- What existing official BrAPI contracts already cover.
- Why those contracts are insufficient, where applicable.
- What GenX adds.
- What is deliberately excluded.

A statement such as "BrAPI has no place to store X" is **not sufficient**
justification. The RFC must explain what X represents and why exchanging it
requires a distinct contract.

## 2. Domain modelling (E2)

Every RFC must identify:

- Core entities.
- Their relationships.
- Authoritative ownership.
- Identity boundaries.
- Cardinality.
- Lifecycle.
- Temporal semantics.
- Provenance requirements.
- Dependencies.
- Related scientific concepts.
- Explicit non-ownership boundaries.

Do not create an entity merely because it appears in an endpoint name.

## 3. Data model quality (E3)

For every property, define as appropriate: name, meaning, data type, required/
optional, nullability, cardinality, units, precision, permitted values,
constraints, example, relationship to controlled vocabularies, versioning
implications, unknown-value representation.

Scientific numeric values require particular attention. For measurements,
distinguish among: physical quantity, numeric value, measurement unit, precision,
uncertainty, measurement method, calibration context, observation time, and
recording time.

Do not represent structured scientific concepts as unrestricted strings when their
meaning must be interpreted consistently by independent systems.

## 4. Terminology and ontology governance (E4)

Where scientific terminology is involved, define: vocabulary authority,
persistent identifier, term definition, version, synonyms, deprecated terms,
replacement terms, mapping relationships, source authority, and local extension
policy.

Use established ontologies and vocabularies where appropriate. Do not invent
ontology identifiers.

## 5. Units and quantities (E5)

Numeric contracts must establish: integer/decimal/float choice, permitted
precision, units, conversion rules, missing-value behaviour, zero vs unknown
distinctions, range constraints, and rounding behaviour.

Do not assume decimal strings are interchangeable with scientific floating-point
measurements. Different domains require different numeric semantics.

## 6. Identifier design (E6)

Define: who creates identifiers, namespace authority, global uniqueness, cross-
system references, resolution, unknown-identifier behaviour, survival across
version changes, and historical reference validity.

Use a coherent identity policy throughout the specification.

## 7. Lifecycle and state transitions (E7)

For resources with lifecycles, document: initial state, permitted transitions,
terminal states, supersession, withdrawal, correction, deletion policy,
historical access, and concurrency considerations.

An enum alone is not a lifecycle specification.

## 8. Endpoint contract quality (E8)

For every operation, define: HTTP method, route, stable operation identifier,
purpose, request schema, response schema, status codes, error semantics,
pagination, filtering, sorting (where supported), authorization requirements,
idempotency requirements, side effects, retry semantics, and compatibility
expectations.

Ensure list/retrieve/create/update/delete operations are justified by the actual
resource lifecycle. Do not blindly generate the same GET/POST/GET pattern for
every domain object.

## 9. Security and authority (E9)

Explicitly distinguish: authentication, authorization, tenant isolation,
resource ownership, data access, scopes, actor identity, auditability, restricted
information, and public vs private metadata.

Do not claim security enforcement merely because an OpenAPI document declares a
bearer-token header.

## 10. External standard reuse (E10)

For each relevant concept, evaluate established standards before designing a
custom mechanism. Potential areas: genomic data formats, geospatial standards,
remote-sensing metadata, scientific provenance, persistent identifiers,
controlled vocabularies, dataset packaging, sensor data, measurement units, data
integrity and canonicalisation.

Record: standard name, version, authority, maturity, applicability, adopted
portion, deliberately excluded portion, and compatibility considerations.

Do not cite an external standard simply to make a proposal look mature.

## 11. Validation and testability (E11)

Every RFC must have objective acceptance criteria and falsifiable tests. Required
evidence should include applicable combinations of: schema validation, positive
fixtures, negative fixtures, boundary-value tests, identifier tests,
relationship tests, lifecycle tests, mutation tests, compatibility tests,
cross-implementation tests, behavioural tests, and security tests.

Each test must trace to a requirement or invariant. Do not count the existence of
a test file as evidence that the test passed.

## 12. Independent implementability (E12)

Explain how an organisation that has never seen Bijmantra could implement the
resource. Remove dependencies on internal Bijmantra modules, private database
structures, Bijmantra-specific assumptions, internal service names, and
unpublished implementation behaviour.

The specification must describe observable interoperable behaviour, not merely
the behaviour of one application.

## 13. Phase 0 review checklist

A reviewer applying this standard should record, per RFC: problem-statement
quality, domain-model completeness, schema completeness, operation completeness,
terminology quality, lifecycle completeness, security requirements, existing
tests, implementation evidence, unresolved decisions, assigned maturity status,
principal deficiencies, and recommended next action. See RFC maturity register.