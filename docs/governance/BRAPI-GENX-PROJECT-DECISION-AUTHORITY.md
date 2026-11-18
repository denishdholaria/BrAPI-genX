# BrAPI-GenX — Project Decision Authority

**Status:** authoritative governance document for Phase 1B and beyond.
**Ratified:** commit `55f970d92dc3e64d34ea36fd184b3a48ec670f13`.

## 1. Project operating model

BrAPI-GenX is developed under a deliberately small decision-making structure with three
defined participants.

| Participant | Responsibility | Authority |
|---|---|---|
| **Project maintainer** | Sole project owner. Final decision authority on architecture, priorities, scientific/domain modelling, normative GenX specifications, security policy, technical trade-offs, and implementation milestones. | Decides. |
| **ChatGPT** | Architecture adviser and technical reviewer. Provides architectural reasoning, technical recommendations, scientific/interoperability analysis, critical examination of IDE-agent proposals, review of implementation decisions, identification of risks and contradictions. | Advises and reviews; does not decide. |
| **IDE agents** | Delegated investigators, designers, implementers, and verification agents. Inspect the actual repository, follow approved decisions, execute bounded engineering tasks, produce test evidence, document implementation choices, report unresolved technical questions. | Implements and verifies; does not silently alter approved architecture. |

The maintainer controls the project. ChatGPT advises the maintainer. IDE agents execute
delegated work. This structure is not democratic; it is a clear delegation model.

## 2. No mandatory external community participation

The maintainer has explicitly established that BrAPI-GenX is being developed primarily
for their own scientific and software requirements and as a foundation supporting the
broader BijMantra ecosystem.

There is no expectation of meaningful technical assistance from the plant-breeding
community or the BrAPI community. Therefore:

- Do not wait for community responses before proceeding.
- Do not require community approval for implementation decisions.
- Do not make implementation dependent on external participation.
- Do not invent formal committees, working groups, or approval processes.
- Do not treat unavailable domain experts as automatic project blockers.

Published scientific standards, official specifications, technical documentation, and
existing implementations remain valuable **research sources**. Use them as evidence,
not as permission requirements.

BrAPI-GenX must remain honest about its independent status and must never claim
official BrAPI endorsement without evidence.

## 3. Internal decision policy

For unresolved technical matters that arise during implementation:

1. Investigate actual requirements from the approved architecture.
2. Examine existing implementation for reusable patterns.
3. Identify reasonable alternatives with trade-offs.
4. Recommend one preferred solution.
5. Explain consequences and reversibility.
6. Identify whether the decision is reversible in practice.
7. Present important unresolved decisions to the maintainer through ChatGPT review.

Do not leave decisions indefinitely pending. Make sensible, reversible implementation
choices within an approved scope. Escalate decisions involving:

- Normative contract changes.
- Security guarantee changes.
- Significant compatibility changes.
- Irreversible migrations.

## 4. Ratified architectural decisions (Cluster 1)

The following decisions have been explicitly approved by the maintainer and are not
open for re-litigation during implementation:

- **D-02** — Digest architecture with three purposes: raw-byte, canonical JSON (JCS-RFC8785), and optional domain-specific semantic fingerprint.
- **D-24** — Idempotency architecture with separate lookup identity (`namespace + key`) and request fingerprint (`operation_id + context + canonical_payload`); header/body conflict rejected with 400; replay requires fresh authorization.
- **D-25** — Durability architecture: durable shared state, atomic key claiming, composite unique constraints, multi-instance coordination, at-least-once delivery model, separate response/tombstone retention.

These decisions were ratified in commit `55f970d9`. Their substantive meaning must be
preserved in implementation.

## 5. Relationship to official BrAPI and Ambika

- **Official BrAPI** (latest stable v2.1) remains a separate, community-governed
  specification. BrAPI-GenX is independently governed and additive. No GenX decision
  changes official BrAPI contracts.
- **Ambika** (ideal module catalog, 402 modules) is a read-only domain architecture
  input. GenX does not automatically create API endpoints from Ambika modules.

## 6. Documentation precedence

When documents conflict, apply this order:

1. Explicit current maintainer instruction.
2. This governance document.
3. Approved architectural decisions (Cluster 1 ratification).
4. Phase 1B implementation architecture document.
5. Current code, tests, and runtime evidence.
6. Historical assessments and planning documents.

Historical documents are preserved as evidence; they do not override ratified
decisions.

---

*This document defines the operating rules for Phase 1B and subsequent phases. It
does not require external ratification.*