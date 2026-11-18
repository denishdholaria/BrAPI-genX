#!/usr/bin/env python3
"""Validate approved-candidate BreedingPipeline/BreedingScheme contract fixtures.

This validator checks implementation-independent invariants for the candidate
OpenAPI model. It is not production conformance and cannot promote RFC maturity.
It uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import json
import re
from decimal import Decimal
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


DEFAULT_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "assessment"
    / "BRAPI-GENX-BREEDING-PIPELINE-CONTRACT-FIXTURES.json"
)
ALLOWED_PUBLICATION_STATES = {"draft", "published", "withdrawn"}
ALLOWED_TRANSITION_TYPES = {"advance", "branch", "recurrent", "other"}
ALLOWED_TASK_CATEGORIES = {
    "crossing",
    "generation-advancement",
    "multiplication",
    "evaluation",
    "selection",
}
ALLOWED_DIRECTIONS = {"increase", "decrease", "maintain", "target-range"}
DECIMAL_RE = re.compile(r"^-?[0-9]+(\.[0-9]+)?$")


def as_object(value: Any) -> dict[str, Any]:
    """Return a mapping or an empty mapping for safe validation."""
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    """Return a list or an empty list for safe validation."""
    return value if isinstance(value, list) else []


def nonempty_string(value: Any) -> bool:
    """Return whether value is a non-blank string."""
    return isinstance(value, str) and bool(value.strip())


def add(errors: list[str], invariant: str, message: str) -> None:
    """Add a stable invariant code and a useful diagnostic."""
    errors.append(f"{invariant}: {message}")


def validate_brapi_reference(
    value: Any,
    label: str,
    errors: list[str],
    expected_resource_type: str | None = None,
) -> None:
    """Validate the authority-qualified BrAPI reference envelope."""
    reference = as_object(value)
    valid = True
    if reference.get("apiGeneration") != "brapi-v2.1":
        add(errors, "BM-20", f"{label} apiGeneration must be brapi-v2.1.")
        valid = False
    if not nonempty_string(reference.get("resourceType")):
        add(errors, "BM-20", f"{label} requires a non-empty resourceType.")
        valid = False
    if expected_resource_type and reference.get("resourceType") != expected_resource_type:
        add(errors, "BM-20", f"{label} resourceType must be {expected_resource_type}.")
        valid = False
    if not nonempty_string(reference.get("dbId")):
        add(errors, "BM-20", f"{label} requires a non-empty dbId.")
        valid = False

    server = reference.get("server")
    if not nonempty_string(server):
        add(errors, "BM-20", f"{label} requires an authoritative server URI.")
        valid = False
    else:
        try:
            parsed = urlsplit(server)
            if (
                parsed.scheme not in {"https", "http"}
                or not parsed.netloc
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError("not an absolute server URI")
        except ValueError:
            add(errors, "BM-20", f"{label} server must be an absolute HTTP(S) URI without credentials, query, or fragment.")
            valid = False

    # Do not require a particular path or trailing-slash normalization here.
    # RFC-154 keeps canonical server URI resolution as an explicit gate.
    _ = valid


def _validate_tasks(
    task_rows: Any,
    seen_task_ids: set[str],
    label: str,
    errors: list[str],
) -> None:
    for index, raw_task in enumerate(as_list(task_rows)):
        task = as_object(raw_task)
        task_id = task.get("taskId")
        if not nonempty_string(task_id):
            add(errors, "BM-TASK-01", f"{label}[{index}] requires a non-empty taskId.")
        elif task_id in seen_task_ids:
            add(errors, "BM-TASK-01", "Duplicate taskId across one BreedingSchemeVersion.")
        else:
            seen_task_ids.add(task_id)

        if task.get("activityCategory") not in ALLOWED_TASK_CATEGORIES:
            add(errors, "BM-TASK-02", f"{label}[{index}] has an unsupported activityCategory.")


def validate_scheme_binding(
    raw_binding: Any,
    index: int,
    errors: list[str],
) -> tuple[str | None, str | None, dict[str, Any] | None]:
    """Validate one binding and its embedded immutable scheme version."""
    binding = as_object(raw_binding)
    scheme_id = binding.get("breedingSchemeDbId")
    version_id = binding.get("breedingSchemeVersionDbId")
    scheme = as_object(binding.get("schemeVersion"))

    if not nonempty_string(scheme_id) or not nonempty_string(version_id):
        add(errors, "BM-BIND-01", f"schemeBindings[{index}] requires both logical and version identifiers.")
        return None, None, None

    if (
        scheme.get("breedingSchemeDbId") != scheme_id
        or scheme.get("breedingSchemeVersionDbId") != version_id
    ):
        add(errors, "BM-BIND-01", "Scheme binding identifiers do not match the embedded schemeVersion identity.")

    if scheme.get("publicationState") is not None and scheme.get("publicationState") not in ALLOWED_PUBLICATION_STATES:
        add(errors, "BM-03", f"schemeBindings[{index}] has an unsupported publicationState.")

    stages = as_list(scheme.get("stages"))
    if not stages:
        add(errors, "BM-05", f"schemeBindings[{index}] embedded schemeVersion must contain at least one stage.")

    stage_ids: list[str] = []
    for stage_index, raw_stage in enumerate(stages):
        stage = as_object(raw_stage)
        stage_id = stage.get("stageId")
        if not nonempty_string(stage_id):
            add(errors, "BM-05", f"schemeBindings[{index}].stages[{stage_index}] requires a non-empty stageId.")
        else:
            stage_ids.append(stage_id)

    stage_set = set(stage_ids)
    if len(stage_ids) != len(stage_set):
        add(errors, "BM-05", "Duplicate stageId within one BreedingSchemeVersion.")

    seen_task_ids: set[str] = set()
    for stage_index, raw_stage in enumerate(stages):
        _validate_tasks(
            as_object(raw_stage).get("tasks"),
            seen_task_ids,
            f"schemeBindings[{index}].stages[{stage_index}].tasks",
            errors,
        )

    transitions = as_list(scheme.get("transitions"))
    transition_ids: set[str] = set()
    for transition_index, raw_transition in enumerate(transitions):
        transition = as_object(raw_transition)
        transition_id = transition.get("transitionId")
        if not nonempty_string(transition_id):
            add(errors, "BM-15", f"schemeBindings[{index}].transitions[{transition_index}] requires a transitionId.")
        elif transition_id in transition_ids:
            add(errors, "BM-15", "Duplicate transitionId within one BreedingSchemeVersion.")
        else:
            transition_ids.add(transition_id)

        from_stage = transition.get("fromStageId")
        to_stage = transition.get("toStageId")
        if (
            not nonempty_string(from_stage)
            or not nonempty_string(to_stage)
            or from_stage not in stage_set
            or to_stage not in stage_set
        ):
            add(errors, "BM-10", "Transition endpoint does not resolve to a stage in the same scheme version.")

        if transition.get("transitionType") not in ALLOWED_TRANSITION_TYPES:
            add(errors, "BM-15", f"schemeBindings[{index}].transitions[{transition_index}] requires a governed transitionType.")

        _validate_tasks(
            transition.get("tasks"),
            seen_task_ids,
            f"schemeBindings[{index}].transitions[{transition_index}].tasks",
            errors,
        )

    return scheme_id, version_id, scheme


def validate_target_contexts(revision: dict[str, Any], errors: list[str]) -> None:
    seen_context_ids: set[str] = set()
    for context_index, raw_context in enumerate(as_list(revision.get("targetContexts"))):
        context = as_object(raw_context)
        context_id = context.get("targetContextId")
        if not nonempty_string(context_id):
            add(errors, "BM-TARGET-01", f"targetContexts[{context_index}] requires targetContextId.")
        elif context_id in seen_context_ids:
            add(errors, "BM-TARGET-01", "Duplicate targetContextId within one pipeline revision.")
        else:
            seen_context_ids.add(context_id)

        traits = as_list(context.get("traitRequirements"))
        for trait_index, raw_trait in enumerate(traits):
            trait = as_object(raw_trait)
            label = f"targetContexts[{context_index}].traitRequirements[{trait_index}]"
            reference = as_object(trait.get("traitReference"))
            validate_brapi_reference(
                trait.get("traitReference"),
                f"{label}.traitReference",
                errors,
            )
            resource_type = reference.get("resourceType")
            if resource_type not in {"Trait", "ObservationVariable"}:
                add(errors, "BM-TARGET-03", f"{label}.traitReference resourceType must be Trait or ObservationVariable.")

            direction = trait.get("desiredDirection")
            if direction not in ALLOWED_DIRECTIONS:
                add(errors, "BM-TARGET-03", f"{label} has an unsupported desiredDirection.")

            numeric_keys = ("threshold", "minimum", "maximum")
            exact_keys = ("exactDecimal", "minimumExactDecimal", "maximumExactDecimal")
            present_numeric = {key for key in numeric_keys if key in trait}
            present_exact = {key for key in exact_keys if key in trait}
            quantitative = bool(present_numeric or present_exact)

            for key in present_numeric:
                value = trait.get(key)
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    add(errors, "BM-TARGET-02", f"{label}.{key} must be a JSON number.")

            for key in present_exact:
                value = trait.get(key)
                if not isinstance(value, str) or not DECIMAL_RE.fullmatch(value):
                    add(errors, "BM-TARGET-02", f"{label}.{key} must be a base-10 decimal string without exponent notation.")

            if "exactDecimal" in present_exact and (present_numeric or {"minimumExactDecimal", "maximumExactDecimal"} & present_exact):
                add(errors, "BM-TARGET-02", "exactDecimal is a scalar target and cannot be combined with numeric or range bounds.")
            if {"minimum", "maximum"} & present_numeric:
                if not {"minimum", "maximum"} <= present_numeric:
                    add(errors, "BM-TARGET-02", f"{label} numeric ranges require both minimum and maximum.")
                elif (
                    isinstance(trait.get("minimum"), (int, float))
                    and not isinstance(trait.get("minimum"), bool)
                    and isinstance(trait.get("maximum"), (int, float))
                    and not isinstance(trait.get("maximum"), bool)
                    and trait["minimum"] > trait["maximum"]
                ):
                    add(errors, "BM-TARGET-02", f"{label} minimum must not exceed maximum.")
            if {"minimumExactDecimal", "maximumExactDecimal"} & present_exact:
                if not {"minimumExactDecimal", "maximumExactDecimal"} <= present_exact:
                    add(errors, "BM-TARGET-02", f"{label} exact-decimal ranges require both minimumExactDecimal and maximumExactDecimal.")
                elif all(
                    isinstance(trait.get(key), str) and DECIMAL_RE.fullmatch(trait[key])
                    for key in ("minimumExactDecimal", "maximumExactDecimal")
                ) and Decimal(trait["minimumExactDecimal"]) > Decimal(trait["maximumExactDecimal"]):
                    add(errors, "BM-TARGET-02", f"{label} minimumExactDecimal must not exceed maximumExactDecimal.")

            has_numeric_range = {"minimum", "maximum"} <= present_numeric
            has_exact_range = {"minimumExactDecimal", "maximumExactDecimal"} <= present_exact
            has_any_range = bool({"minimum", "maximum", "minimumExactDecimal", "maximumExactDecimal"} & (present_numeric | present_exact))
            if present_numeric & {"minimum", "maximum"} and present_exact & {"minimumExactDecimal", "maximumExactDecimal"}:
                add(errors, "BM-TARGET-02", "A target range must use either JSON numeric bounds or exact-decimal bounds, not both.")
            if direction == "target-range" and not (has_numeric_range or has_exact_range):
                add(errors, "BM-TARGET-02", f"{label} target-range requires a complete minimum/maximum pair.")
            if direction != "target-range" and has_any_range:
                add(errors, "BM-TARGET-02", f"{label} range bounds require desiredDirection target-range.")

            if quantitative and resource_type != "ObservationVariable":
                add(errors, "BM-TARGET-04", "Quantitative target references must use resourceType ObservationVariable so the BrAPI Scale is explicit.")

def validate_pipeline_revision(revision: Any) -> tuple[list[str], dict[tuple[str, str], dict[str, Any]]]:
    """Validate pipeline revision identity, authority, targets, and embedded schemes."""
    errors: list[str] = []
    pipeline = as_object(revision)
    logical_id = pipeline.get("breedingPipelineDbId")
    version_id = pipeline.get("breedingPipelineVersionDbId")

    if not nonempty_string(logical_id) or not nonempty_string(version_id) or logical_id == version_id:
        add(errors, "BM-04", "Pipeline logical and revision identifiers must be different non-empty identifiers.")

    validate_brapi_reference(
        pipeline.get("programReference"),
        "programReference",
        errors,
        expected_resource_type="Program",
    )

    if pipeline.get("publicationState") not in ALLOWED_PUBLICATION_STATES:
        add(errors, "BM-03", "Pipeline revision requires a governed publicationState.")

    validate_target_contexts(pipeline, errors)

    bindings = as_list(pipeline.get("schemeBindings"))
    seen_bindings: set[tuple[str, str]] = set()
    definitions: dict[tuple[str, str], dict[str, Any]] = {}
    for index, raw_binding in enumerate(bindings):
        scheme_id, scheme_version_id, definition = validate_scheme_binding(raw_binding, index, errors)
        if scheme_id and scheme_version_id:
            key = (scheme_id, scheme_version_id)
            if key in seen_bindings:
                add(errors, "BM-BIND-02", "Duplicate scheme logical/version binding in one pipeline revision.")
            seen_bindings.add(key)
            if definition is not None:
                definitions[key] = definition

    return errors, definitions


def validate_execution_event(
    event: Any,
    pipeline_revision: dict[str, Any] | None,
    definitions: dict[tuple[str, str], dict[str, Any]] | None = None,
) -> list[str]:
    """Validate optional exact pipeline and scheme contexts on an execution event."""
    errors: list[str] = []
    execution = as_object(event)
    pipeline_context = execution.get("pipelineContext")
    scheme_context = execution.get("schemeContext")

    # Stage fields outside the scheme context are never valid: their namespace
    # and exact owning version would be ambiguous.
    if any(key in execution for key in ("stageId", "fromStageId", "toStageId")):
        add(errors, "BM-11", "Stage identifiers must be nested inside schemeContext.")

    if pipeline_context is not None:
        pipeline_ref = as_object(pipeline_context)
        if (
            not nonempty_string(pipeline_ref.get("breedingPipelineDbId"))
            or not nonempty_string(pipeline_ref.get("breedingPipelineVersionDbId"))
        ):
            add(errors, "BM-07", "pipelineContext requires both logical and exact revision identifiers.")
        elif pipeline_revision is not None:
            if (
                pipeline_ref.get("breedingPipelineDbId") != pipeline_revision.get("breedingPipelineDbId")
                or pipeline_ref.get("breedingPipelineVersionDbId") != pipeline_revision.get("breedingPipelineVersionDbId")
            ):
                add(errors, "BM-07", "Execution event pipelineContext does not identify the supplied pipeline revision.")

    if scheme_context is not None:
        scheme_ref = as_object(scheme_context)
        scheme_id = scheme_ref.get("breedingSchemeDbId")
        scheme_version_id = scheme_ref.get("breedingSchemeVersionDbId")
        stage_fields = ("stageId", "fromStageId", "toStageId")
        has_stage = any(nonempty_string(scheme_ref.get(key)) for key in stage_fields)

        if not nonempty_string(scheme_id) or not nonempty_string(scheme_version_id):
            add(errors, "BM-11", "schemeContext with stage references must include breedingSchemeDbId and breedingSchemeVersionDbId.")
        elif pipeline_revision is not None and pipeline_context is not None:
            key = (scheme_id, scheme_version_id)
            bound = (definitions or {}).get(key)
            if bound is None:
                add(errors, "BM-12", "Execution event scheme version is not bound by the referenced pipeline revision.")
            elif has_stage:
                known_stages = {
                    as_object(stage).get("stageId")
                    for stage in as_list(bound.get("stages"))
                    if nonempty_string(as_object(stage).get("stageId"))
                }
                for stage_key in stage_fields:
                    value = scheme_ref.get(stage_key)
                    if value is not None and (not nonempty_string(value) or value not in known_stages):
                        add(errors, "BM-10", f"schemeContext.{stage_key} does not resolve in the referenced scheme version.")
    elif any(key in execution for key in ("stageId", "fromStageId", "toStageId")):
        add(errors, "BM-11", "Stage identifiers require an exact schemeContext.")

    return errors


def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    """Validate one positive or negative candidate scenario."""
    errors: list[str] = []
    revision = as_object(fixture.get("pipelineRevision")) if fixture.get("pipelineRevision") is not None else None
    definitions: dict[tuple[str, str], dict[str, Any]] = {}

    if revision is not None:
        revision_errors, definitions = validate_pipeline_revision(revision)
        errors.extend(revision_errors)

    if fixture.get("event") is not None:
        errors.extend(validate_execution_event(fixture.get("event"), revision, definitions))

    for index, event in enumerate(as_list(fixture.get("executionEvents"))):
        event_errors = validate_execution_event(event, revision, definitions)
        errors.extend(f"executionEvents[{index}] {item}" for item in event_errors)

    if fixture.get("before") is not None and fixture.get("after") is not None:
        before = as_object(fixture.get("before"))
        after = as_object(fixture.get("after"))
        before_id = before.get("breedingSchemeVersionDbId")
        after_id = after.get("breedingSchemeVersionDbId")
        if (
            before.get("publicationState") == "published"
            and after.get("publicationState") == "published"
            and before_id
            and before_id == after_id
            and before != after
        ):
            add(errors, "BM-03", "Published scheme content changed without a new breedingSchemeVersionDbId.")

    return errors


def validate_corpus(corpus: Any) -> list[str]:
    """Return all corpus validation errors; an empty list means success."""
    errors: list[str] = []
    if not isinstance(corpus, dict):
        return ["top-level JSON value must be an object"]
    if corpus.get("contractStatus") != "approved-candidate-only":
        errors.append("contractStatus must be 'approved-candidate-only'")
    if corpus.get("normative") is not False:
        errors.append("normative must be false")
    if corpus.get("schemaStatus") != "candidate-openapi-contract-fixtures":
        errors.append("schemaStatus must be 'candidate-openapi-contract-fixtures'")

    fixtures = as_list(corpus.get("fixtures"))
    if not fixtures:
        return errors + ["fixtures must be a non-empty array"]

    by_id: dict[str, dict[str, Any]] = {}
    for index, raw_fixture in enumerate(fixtures):
        fixture = as_object(raw_fixture)
        scenario_id = fixture.get("scenarioId")
        if not nonempty_string(scenario_id):
            errors.append(f"fixtures[{index}] has no non-empty scenarioId")
            continue
        if scenario_id in by_id:
            errors.append(f"duplicate scenarioId: {scenario_id}")
            continue
        by_id[scenario_id] = fixture

    valid_count = 0
    invalid_count = 0
    for scenario_id, fixture in by_id.items():
        expectation = fixture.get("expectation")
        if expectation not in {"valid", "invalid"}:
            errors.append(f"{scenario_id}: expectation must be valid or invalid")
            continue
        scenario_errors = validate_fixture(fixture)
        expected_invariants = set(as_list(fixture.get("invariantIds")))
        error_invariants = {error.split(":", 1)[0] for error in scenario_errors}

        if expectation == "valid":
            valid_count += 1
            if scenario_errors:
                errors.extend(f"{scenario_id}: {item}" for item in scenario_errors)
        else:
            invalid_count += 1
            expected_failure = fixture.get("expectedFailure")
            if not nonempty_string(expected_failure):
                errors.append(f"{scenario_id}: invalid scenario needs expectedFailure")
            if not expected_invariants:
                errors.append(f"{scenario_id}: invalid scenario needs invariantIds")
            missing = sorted(expected_invariants - error_invariants)
            if missing:
                errors.append(
                    f"{scenario_id}: expected invariant(s) not detected: {', '.join(missing)}"
                )
            unexpected = [
                item for item in scenario_errors
                if item.split(":", 1)[0] not in expected_invariants
            ]
            if unexpected:
                errors.extend(f"{scenario_id}: unrelated failure: {item}" for item in unexpected)

    if not valid_count or not invalid_count:
        errors.append("corpus must include at least one valid and one invalid scenario")

    required = {
        "valid-embedded-schemes-multiple-targets",
        "valid-event-without-registered-strategy",
        "invalid-embedded-scheme-version-identity-mismatch",
        "invalid-duplicate-stage-identifiers",
        "invalid-dangling-transition-endpoint",
        "invalid-duplicate-transition-identifier",
        "invalid-duplicate-task-identifier",
        "invalid-stage-without-scheme-version-context",
        "invalid-event-scheme-version-not-bound-by-pipeline-revision",
        "invalid-pipeline-version-does-not-match-logical-identity",
        "invalid-target-context-duplicate-identifiers",
        "invalid-exact-decimal-mixed-with-binary-numeric",
        "invalid-authority-qualified-program-reference",
        "invalid-mutated-published-scheme-version",
        "valid-exact-decimal-observation-variable-range",
        "invalid-quantitative-target-references-trait-only",
        "invalid-incomplete-exact-decimal-range",
    }
    missing = sorted(required - set(by_id))
    if missing:
        errors.append("missing required contract scenarios: " + ", ".join(missing))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=DEFAULT_FIXTURE_PATH)
    args = parser.parse_args()

    try:
        with args.file.open("r", encoding="utf-8") as handle:
            corpus = json.load(handle)
    except OSError as exc:
        print(f"ERROR: cannot read {args.file}: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(
            f"ERROR: invalid JSON in {args.file} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}",
            file=sys.stderr,
        )
        return 2

    failures = validate_corpus(corpus)
    fixture_count = len(as_list(as_object(corpus).get("fixtures")))
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"FAILED: {len(failures)} error(s) across {fixture_count} contract fixture(s).")
        return 1

    valid_count = sum(
        1 for item in as_list(as_object(corpus).get("fixtures"))
        if as_object(item).get("expectation") == "valid"
    )
    invalid_count = fixture_count - valid_count
    print(
        "PASS: approved-candidate contract fixtures "
        f"({fixture_count} scenarios: {valid_count} valid, {invalid_count} invalid)."
    )
    print("PASS: embedded scheme identity, stage/transition/task, target, authority, and event-context invariants.")
    print("NOTE: no production conformance or normative contract is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
