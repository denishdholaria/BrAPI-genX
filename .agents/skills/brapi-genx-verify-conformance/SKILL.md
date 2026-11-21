---
name: brapi-genx-verify-conformance
description: Reproduce or verify BrAPI-GenX contract, fixture, catalogue, generated compatibility artifact, or conformance workflow results at an exact revision.
---

# Verify BrAPI-GenX conformance

Pin the revision and identify the claim being tested. Use the
[repository instructions](../../../AGENTS.md) for baseline checks and the
[conformance workflow](../../../.github/workflows/genx-static-conformance.yml)
for dependency versions, test commands, and fixture server setup.

## Choose evidence that can falsify the claim

| Claim | Evidence to request or run |
| --- | --- |
| Registry and source agree | Run [the endpoint registry check](../../../Scripts/checkEndpointRegistry.py) and the relevant contract checker. Run [catalogue generation](../../../Scripts/generateEndpointArtifacts.py) with `--check` if the source registry or derived catalogues changed. |
| A fixture exercises an invariant | Use a valid control and a focused mutation. Confirm the altered scenario still reaches the intended check and fails for the expected invariant. For BreedingPipeline, run the [validator regression suite](../../../Scripts/test_breeding_pipeline_contract_fixture_validator.py) in addition to the corpus validator. |
| HTTP behavior is observable | Run the relevant [static and live probes](../../../Scripts/checkGenXConformance.py) against the intended server and record which probes executed. The in-memory server checks the reference behavior within its supported scope. |
| Behavior interoperates independently | Use separately implemented participants and exercise the intended exchange, state transition, or failure cases. For BreedingPipeline publication, use the [CAS behavioral plan](../../../docs/assessment/BRAPI-GENX-BREEDING-PIPELINE-CAS-BEHAVIORAL-TEST-PLAN.md) when validating durability or concurrent writes. |

## Diagnose workflow or generator failures

- Inspect job steps and annotations for the exact tested SHA. A runner failure
  before the test step yields no test verdict. Reproduce locally when
  feasible and record toolchain differences.
- Compare regenerated artifacts with the released OpenAPI source using HTTP
  method and path pairs and the affected resolved schemas. A successful
  build can still omit operations. Compare the same generation command on
  the base and changed revisions before assigning the regression. Keep
  diagnosis outputs in a scratch checkout or directory.
- Use the existing descriptive source audit as a report when it runs in that
  mode. Treat its findings independently of the command's exit status.

Report executed commands, outcomes, skipped checks, and the revision and
server configuration they cover. Claims about persistence, authorization,
and concurrency require evidence from the implementation layers that enforce
those behaviors.
