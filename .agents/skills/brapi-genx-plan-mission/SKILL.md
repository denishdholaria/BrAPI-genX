---
name: brapi-genx-plan-mission
description: Turn a BrAPI-GenX architecture question or an IDE agent completion report into the next bounded development mission and a verifiable handoff.
---

# Plan the next BrAPI-GenX mission

Use the [repository instructions](../../../AGENTS.md) and
[project decision authority](../../../docs/governance/BRAPI-GENX-PROJECT-DECISION-AUTHORITY.md).
The principal architect sets technical direction and reviews evidence.
The maintainer decides scientific policy, compatibility changes, and normative
specification changes.

## Decide what is ready to advance

When reviewing a completion report, compare it with the actual diff and
the cited sources at the inspected revision. Identify the claim that
controls the next decision and verify it independently. A passing
registry check establishes structural consistency. Claims about scientific
meaning require source-contract evidence and a worked example.

Choose one slice that resolves the first uncertainty blocking the next
deliverable. Useful outcomes include a source-backed overlap assessment,
an executable exchange fixture, and a narrowly scoped repair. When a prior
finding changes, correct the evidence and check how it affects downstream
recommendations before authorizing implementation.

## Write the prompt

Make the prompt usable in a fresh IDE session. Include the repository,
the base or how to verify it, the scientific question or observable
behavior, the relevant source locations, and acceptance criteria that can
fail. Name the permitted write scope and protected contracts. Specify the
Git and publication actions the maintainer authorized. Use local `main`
for routine work under the repository workflow.

Ask the agent to return the exact revision, changed files, evidence links,
commands and observed results, remaining gaps, and any decision that needs
the maintainer's input. For a scientific decision, give the maintainer the
question, why it matters, the trade-off, and a recommendation. Leave the
subsequent slice conditional on the results.
