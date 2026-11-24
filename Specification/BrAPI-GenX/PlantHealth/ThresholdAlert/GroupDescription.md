# Group ThresholdAlert

**Status:** BrAPI-GenX **STRUCTURAL_DRAFT** candidate under Request for Comments (RFC) 126; not a scientifically validated recommendation, official Breeding Application Programming Interface (BrAPI) version 2.1 contract, or independently verified service.

The `ThresholdAlert` record requires its namespaced identifier and a lifecycle `status` (`active`, `superseded`, `withdrawn`), while `alertType`, `thresholdValue`, `currentValue`, `triggerDate`, `fieldOrPlot`, `supersedes`, and provenance are optional. The draft supports register, list, and retrieve operations; its purported idempotency and immutable-publication semantics have no independent persistent-service evidence.

**Scientific and operational boundaries:** ThresholdValue and currentValue are untyped strings without units, comparable quantity definitions, measurement method, evaluation direction, hysteresis, evaluation time or trigger algorithm. The candidate lifecycle status is not an alert acknowledgment, delivery receipt or control-action record. A threshold example is not proof of a valid pest-management intervention. Requiredness, controlled vocabularies, and reference relationships remain unresolved under decisions D-376 and its associated RFC question list. Any semantic-neighbor links between proposed operations are advisory only, not scientific causality or executable workflow dependencies.

**Sources:** [module overview](./README.md), [candidate record schema](./Schemas/ThresholdAlert.yaml), [registration schema](./Schemas/ThresholdAlertNewRequest.yaml), [candidate operations](./ThresholdAlert_GET_POST.yaml), [RFC source](../../RFCs/RFC-126-ThresholdAlert.md), [maturity register](../../../../docs/governance/BRAPI-GENX-RFC-MATURITY-REGISTER.md).
