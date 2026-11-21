#!/usr/bin/env python3
"""Validate approved-candidate BreedingPipeline/BreedingScheme contract fixtures.

This validator checks implementation-independent invariants for the candidate
OpenAPI model. It is not production conformance and cannot promote RFC maturity.
Registration replay checks use the repository's JCS (RFC 8785) canonicalizer.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from brapi_genx.canonicalization import JCSError, jcs_canonicalize


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
            has_range_bounds = bool(
                ({"minimum", "maximum"} & present_numeric)
                or ({"minimumExactDecimal", "maximumExactDecimal"} & present_exact)
            )
            if "threshold" in present_numeric and has_range_bounds:
                add(
                    errors,
                    "BM-TARGET-02",
                    "threshold is a scalar target and cannot be combined with numeric or exact-decimal range bounds.",
                )

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



def validate_conflict_atomicity(request: dict[str, Any], errors: list[str]) -> None:
    """Require rejected-registration fixtures to preserve history and pointer."""
    before = request.get("stateBefore")
    after = request.get("stateAfter")
    if not isinstance(before, dict) or not isinstance(after, dict):
        add(
            errors,
            "BM-REG-04",
            "A conflict-behavior fixture must include stateBefore and stateAfter snapshots.",
        )
    elif before != after:
        add(
            errors,
            "BM-REG-04",
            "A rejected registration must not append revision history or mutate the current published pointer.",
        )


def validate_registration(registration: Any) -> list[str]:
    """Validate replay, append, publish, withdrawal, and current-pointer CAS semantics."""
    errors: list[str] = []
    request = as_object(registration)
    existing_raw = request.get("existingRevision")
    incoming = as_object(request.get("incomingRevision"))

    request_pipeline_id = request.get("breedingPipelineDbId")
    incoming_pipeline_id = incoming.get("breedingPipelineDbId")
    incoming_version_id = incoming.get("breedingPipelineVersionDbId")
    if not nonempty_string(request_pipeline_id):
        add(
            errors,
            "BM-REG-01",
            "Registration request must include its outer breedingPipelineDbId.",
        )
        return errors
    if request_pipeline_id != incoming_pipeline_id:
        add(
            errors,
            "BM-REG-01",
            "Outer breedingPipelineDbId must exactly match breedingPipelineVersion.breedingPipelineDbId.",
        )
        return errors
    if not nonempty_string(incoming_pipeline_id) or not nonempty_string(incoming_version_id):
        add(
            errors,
            "BM-REG-01",
            "Registration fixtures require a stable pipeline ID and immutable incoming version ID.",
        )
        return errors

    # First registration creates the logical workstream; there is no current
    # published version against which a precondition can be evaluated. The
    # logical-identity uniqueness race is represented separately by fixtures.
    if existing_raw is None:
        if "expectedCurrentBreedingPipelineVersionDbId" in request:
            add(
                errors,
                "BM-REG-02",
                "A first registration must omit the expected-current-version precondition.",
            )
        if request.get("logicalPipelineAlreadyExists") is True:
            add(
                errors,
                "BM-REG-02",
                "A concurrent first-create collision must not overwrite an existing logical pipeline; re-read and append under the expected-current precondition.",
            )
            actual_outcome = "conflict"
        else:
            actual_outcome = "create"
        expected_outcome = request.get("expectedOutcome")
        if nonempty_string(expected_outcome) and expected_outcome != actual_outcome:
            add(errors, "BM-REG-01", f"Registration fixture declares {expected_outcome!r}, expected {actual_outcome!r}.")
        return errors

    existing = as_object(existing_raw)
    existing_pipeline_id = existing.get("breedingPipelineDbId")
    existing_version_id = existing.get("breedingPipelineVersionDbId")
    if not nonempty_string(existing_pipeline_id) or not nonempty_string(existing_version_id):
        add(
            errors,
            "BM-REG-01",
            "An existing revision must contain stable pipeline and immutable version identifiers.",
        )
        return errors

    try:
        existing_canonical = jcs_canonicalize(
            json.dumps(existing, ensure_ascii=False, allow_nan=False).encode("utf-8")
        )
        incoming_canonical = jcs_canonicalize(
            json.dumps(incoming, ensure_ascii=False, allow_nan=False).encode("utf-8")
        )
    except (JCSError, TypeError, ValueError, UnicodeError) as exc:
        add(errors, "BM-REG-01", f"Registration payload is not valid JCS JSON: {exc}.")
        return errors

    # Idempotent replay/conflict detection precedes the current-pointer
    # precondition. A retry after a successful publish must replay even though
    # the supplied expected pointer is now stale.
    if existing_version_id == incoming_version_id:
        if existing_pipeline_id != incoming_pipeline_id or existing_canonical != incoming_canonical:
            actual_outcome = "conflict"
            add(
                errors,
                "BM-REG-01",
                "Reusing a breedingPipelineVersionDbId with a different canonical payload must conflict; immutable content must never be overwritten.",
            )
        else:
            actual_outcome = "replay"
        expected_outcome = request.get("expectedOutcome")
        if nonempty_string(expected_outcome) and expected_outcome != actual_outcome:
            add(errors, "BM-REG-01", f"Registration fixture declares {expected_outcome!r}, expected {actual_outcome!r}.")
        return errors

    # A different version under the same logical workstream is an append.
    # The caller must state the current published pointer (including explicit
    # null when the workstream has no published revision) and the server must
    # compare it atomically before any state-changing publication operation.
    if existing_pipeline_id == incoming_pipeline_id:
        if "currentBreedingPipelineVersionDbId" not in request:
            add(
                errors,
                "BM-REG-02",
                "Append fixture must expose the server's current published revision snapshot.",
            )
            return errors
        if "expectedCurrentBreedingPipelineVersionDbId" not in request:
            if request.get("expectedOutcome") == "conflict":
                validate_conflict_atomicity(request, errors)
                return errors
            add(
                errors,
                "BM-REG-02",
                "Appending a new version to an existing pipeline requires expectedCurrentBreedingPipelineVersionDbId.",
            )
            return errors

        current_pointer = request.get("currentBreedingPipelineVersionDbId")
        expected_pointer = request.get("expectedCurrentBreedingPipelineVersionDbId")
        if expected_pointer != current_pointer:
            if request.get("expectedOutcome") == "conflict":
                validate_conflict_atomicity(request, errors)
                return errors
            add(
                errors,
                "BM-REG-02",
                "The expected current published version is stale; the server must reject the append without changing the pipeline.",
            )
            return errors

        state = incoming.get("publicationState")
        if state not in {"draft", "published", "withdrawn"}:
            add(
                errors,
                "BM-REG-03",
                "Incoming revision publicationState must be draft, published, or withdrawn.",
            )
        relationship_raw = incoming.get("revisionRelationship")
        relationship = as_object(relationship_raw)
        relationship_type = relationship.get("relationshipType")
        prior = relationship.get("priorBreedingPipelineVersionDbId")
        based_on_present = "basedOnBreedingPipelineVersionDbId" in incoming
        based_on = incoming.get("basedOnBreedingPipelineVersionDbId")
        if state == "draft":
            if based_on_present and not nonempty_string(based_on):
                add(
                    errors,
                    "BM-REG-03",
                    "A supplied basedOnBreedingPipelineVersionDbId must be a non-empty string; JSON null is not equivalent to omission.",
                )
            if relationship_raw is not None:
                add(
                    errors,
                    "BM-REG-03",
                    "A draft revision must omit revisionRelationship and use basedOnBreedingPipelineVersionDbId for its preparation baseline.",
                )
            if based_on is not None and based_on != current_pointer:
                add(
                    errors,
                    "BM-REG-03",
                    "A draft baseline reference must identify the current published pointer observed by the request.",
                )
            if based_on is None and current_pointer is not None:
                add(
                    errors,
                    "BM-REG-03",
                    "A draft appended over a published baseline must identify it with basedOnBreedingPipelineVersionDbId.",
                )
        elif based_on_present:
            add(
                errors,
                "BM-REG-03",
                "basedOnBreedingPipelineVersionDbId is reserved for drafts and must be absent from published or withdrawn revisions, including as JSON null.",
            )
        if state == "published":
            if current_pointer is None:
                if relationship_raw is not None:
                    add(
                        errors,
                        "BM-REG-03",
                        "A first publication with no current published pointer must not claim a prior-revision relationship.",
                    )
            elif relationship_type not in {"supersedes", "corrects"} or prior != current_pointer:
                add(
                    errors,
                    "BM-REG-03",
                    "A published successor must use supersedes/corrects and identify the exact current published revision.",
                )
            actual_outcome = "publish"
        elif state == "withdrawn":
            if current_pointer is None or relationship_type != "withdraws" or prior != current_pointer:
                add(
                    errors,
                    "BM-REG-03",
                    "A withdrawal revision must use relationshipType=withdraws and identify the exact current published version it withdraws.",
                )
            actual_outcome = "withdraw"
        elif state == "draft":
            # Drafts are immutable history records but do not move the current
            # published pointer. Multiple drafts may branch from one baseline.
            actual_outcome = "append"
        else:
            actual_outcome = "reject"
    else:
        # Version identifiers are unique only within their owning logical
        # pipeline; do not replay or disclose a different pipeline's revision.
        actual_outcome = "conflict"
        add(
            errors,
            "BM-REG-01",
            "A version identifier collision across different pipeline identities must conflict and must not replay another pipeline's revision.",
        )

    expected_outcome = request.get("expectedOutcome")
    if nonempty_string(expected_outcome) and expected_outcome != actual_outcome:
        add(
            errors,
            "BM-REG-01",
            f"Registration fixture declares outcome {expected_outcome!r}, but identifiers and publication state imply {actual_outcome!r}.",
        )

    return errors


def validate_authority_filter_request(value: Any) -> list[str]:
    """Validate fail-closed authority-paired filters used by execution list operations."""
    errors: list[str] = []
    filters = as_object(value)

    pairs = (
        ("programDbId", "programServer"),
        ("studyDbId", "studyServer"),
        ("candidateGermplasmDbId", "candidateGermplasmServer"),
    )
    for identifier_name, server_name in pairs:
        identifier_present = identifier_name in filters and filters.get(identifier_name) is not None
        server_present = server_name in filters and filters.get(server_name) is not None
        if identifier_present != server_present:
            add(
                errors,
                "BM-FILTER-01",
                f"{identifier_name} and {server_name} must be supplied together; an unqualified BrAPI identifier must not be resolved by guessing its server.",
            )
        if identifier_present and not nonempty_string(filters.get(identifier_name)):
            add(errors, "BM-FILTER-01", f"{identifier_name} must be a non-empty string when supplied.")
        if server_present:
            server = filters.get(server_name)
            if not nonempty_string(server):
                add(errors, "BM-FILTER-01", f"{server_name} must be a non-empty absolute HTTP(S) URI.")
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
                        raise ValueError("not an absolute authority URI")
                except ValueError:
                    add(errors, "BM-FILTER-01", f"{server_name} must be an absolute HTTP(S) URI without credentials, query, or fragment.")

    population_id = "populationDbId"
    population_server = "populationServer"
    population_type = "populationResourceType"
    population_presence = [
        name in filters and filters.get(name) is not None
        for name in (population_id, population_server, population_type)
    ]
    if any(population_presence) and not all(population_presence):
        add(
            errors,
            "BM-FILTER-02",
            "populationDbId, populationServer, and populationResourceType must be supplied together; the server must not infer a resource type.",
        )
    if population_presence[0] and not nonempty_string(filters.get(population_id)):
        add(errors, "BM-FILTER-02", "populationDbId must be a non-empty string when supplied.")
    if population_presence[2] and not nonempty_string(filters.get(population_type)):
        add(errors, "BM-FILTER-02", "populationResourceType must be the exact non-empty BrAPI resource type when supplied.")
    if population_presence[1]:
        server = filters.get(population_server)
        if not nonempty_string(server):
            add(errors, "BM-FILTER-02", "populationServer must be a non-empty absolute HTTP(S) URI.")
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
                    raise ValueError("not an absolute authority URI")
            except ValueError:
                add(errors, "BM-FILTER-02", "populationServer must be an absolute HTTP(S) URI without credentials, query, or fragment.")

    # The authority tuple is (resourceType, server, dbId), not dbId alone.
    seen_references: set[tuple[str, str, str]] = set()
    for index, raw_reference in enumerate(as_list(filters.get("authorityReferences"))):
        reference = as_object(raw_reference)
        validate_brapi_reference(
            reference,
            f"authorityReferences[{index}]",
            errors,
        )
        resource_type = reference.get("resourceType")
        server = reference.get("server")
        db_id = reference.get("dbId")
        if all(nonempty_string(item) for item in (resource_type, server, db_id)):
            key = (resource_type, server, db_id)
            if key in seen_references:
                add(errors, "BM-FILTER-03", "Duplicate authority-qualified reference tuple.")
            seen_references.add(key)

    return errors


def _target_decimals(trait: dict[str, Any]) -> list[tuple[str, Decimal, int]]:
    """Return validated target values as (field, decimal, fractional_digits)."""
    values: list[tuple[str, Decimal, int]] = []
    for key in ("threshold", "minimum", "maximum"):
        if key in trait and isinstance(trait[key], (int, float)) and not isinstance(trait[key], bool):
            rendered = str(trait[key])
            try:
                number = Decimal(rendered)
            except InvalidOperation:
                continue
            if number.is_finite():
                fractional_digits = max(0, -number.as_tuple().exponent)
                values.append((key, number, fractional_digits))
    for key in ("exactDecimal", "minimumExactDecimal", "maximumExactDecimal"):
        value = trait.get(key)
        if isinstance(value, str) and DECIMAL_RE.fullmatch(value):
            number = Decimal(value)
            fractional_digits = len(value.partition(".")[2]) if "." in value else 0
            values.append((key, number, fractional_digits))
    return values


def _parse_aware_timestamp(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp only when it includes an explicit UTC offset."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def scale_evidence_records(fixture: dict[str, Any]) -> list[Any]:
    """Read both the original single record and the multi-target fixture form."""
    raw = fixture.get("scaleEvidence")
    if raw is None:
        return []
    return raw if isinstance(raw, list) else [raw]


def validate_scale_evidence(fixture: dict[str, Any], errors: list[str]) -> None:
    """Validate fixture-supplied per-target evidence without network dereferencing."""
    revision = as_object(fixture.get("pipelineRevision"))
    state = revision.get("publicationState")
    validation_state = fixture.get("scaleValidationState")
    records = scale_evidence_records(fixture)

    if validation_state is not None and validation_state not in ("verified", "unverified"):
        add(errors, "BM-SCALE-04", "scaleValidationState must be verified or unverified in this candidate fixture profile.")
        return
    if validation_state == "verified" and not records:
        add(errors, "BM-SCALE-04", "Verified target validation requires separate Scale evidence.")
        return
    if validation_state == "unverified":
        if state == "published":
            add(errors, "BM-SCALE-04", "Published quantitative targets require verified ObservationVariable Scale evidence.")
        elif state != "draft":
            add(errors, "BM-SCALE-04", "Only a draft may remain unverified in this candidate profile.")
        if records:
            add(errors, "BM-SCALE-04", "An unverified fixture must not present Scale evidence as verified.")
        return
    if not records:
        return

    covered_targets: set[tuple[str, int]] = set()
    for record in records:
        binding = validate_scale_evidence_record(revision, as_object(record), errors)
        if binding is None:
            continue
        if binding in covered_targets:
            add(errors, "BM-SCALE-05", f"Target {binding!r} has multiple evidence records.")
        covered_targets.add(binding)

    if state == "published":
        for raw_context in as_list(revision.get("targetContexts")):
            context = as_object(raw_context)
            context_id = context.get("targetContextId")
            if not nonempty_string(context_id):
                continue
            for index, trait in enumerate(as_list(context.get("traitRequirements"))):
                binding = (context_id, index)
                if _target_decimals(as_object(trait)) and binding not in covered_targets:
                    add(
                        errors, "BM-SCALE-05",
                        f"Published quantitative target {binding!r} requires its own bound Scale evidence record.",
                    )


def validate_scale_evidence_record(
    revision: dict[str, Any], evidence: dict[str, Any], errors: list[str],
) -> tuple[str, int] | None:
    """Validate an evidence record and return its exact target binding."""
    evidence_id = evidence.get("evidenceRecordId")
    pipeline_context = as_object(evidence.get("pipelineContext"))
    target_binding = as_object(evidence.get("targetBinding"))
    expected_pipeline = (revision.get("breedingPipelineDbId"), revision.get("breedingPipelineVersionDbId"))
    supplied_pipeline = (pipeline_context.get("breedingPipelineDbId"), pipeline_context.get("breedingPipelineVersionDbId"))
    target_context_id = target_binding.get("targetContextId")
    target_index = target_binding.get("traitRequirementIndex")
    if not nonempty_string(evidence_id) or supplied_pipeline != expected_pipeline:
        add(errors, "BM-SCALE-05", "Evidence identity and pipelineContext must identify the exact immutable pipeline revision.")
        return None
    if (
        not nonempty_string(target_context_id)
        or not isinstance(target_index, int)
        or isinstance(target_index, bool)
        or target_index < 0
    ):
        add(errors, "BM-SCALE-05", "Evidence targetBinding requires a targetContextId and non-negative integer traitRequirementIndex.")
        return None

    matching_contexts = [
        as_object(context)
        for context in as_list(revision.get("targetContexts"))
        if as_object(context).get("targetContextId") == target_context_id
    ]
    if len(matching_contexts) != 1:
        add(errors, "BM-SCALE-05", "Evidence targetBinding must identify exactly one target context in the immutable revision.")
        return None
    requirements = as_list(matching_contexts[0].get("traitRequirements"))
    if target_index >= len(requirements):
        add(errors, "BM-SCALE-05", "Evidence traitRequirementIndex is outside the selected target context.")
        return None
    target = as_object(requirements[target_index])
    target_reference = as_object(target.get("traitReference"))
    evidence_reference = as_object(evidence.get("observationVariableReference"))
    identity_keys = ("apiGeneration", "resourceType", "server", "dbId")
    if any(target_reference.get(key) != evidence_reference.get(key) for key in identity_keys):
        add(errors, "BM-SCALE-05", "Evidence ObservationVariable reference must exactly match the selected target authority-qualified traitReference.")
        return None
    if (
        evidence_reference.get("apiGeneration") != "brapi-v2.1"
        or evidence_reference.get("resourceType") != "ObservationVariable"
        or not nonempty_string(evidence_reference.get("server"))
        or not nonempty_string(evidence_reference.get("dbId"))
    ):
        add(errors, "BM-SCALE-05", "Evidence must reference an authority-qualified BrAPI v2.1 ObservationVariable.")
        return None

    retrieved = _parse_aware_timestamp(evidence.get("sourceRetrievedAt"))
    validated = _parse_aware_timestamp(evidence.get("validatedAt"))
    profile = as_object(evidence.get("validationProfile"))
    if (
        retrieved is None
        or validated is None
        or retrieved > validated
        or not nonempty_string(profile.get("profileId"))
        or not nonempty_string(profile.get("profileVersion"))
        or evidence.get("validationResult") != "passed"
    ):
        add(errors, "BM-SCALE-07", "A passed evidence record requires ordered timezone-aware timestamps and a versioned validation profile.")

    values = _target_decimals(target)
    if not values:
        add(errors, "BM-SCALE-01", "Evidence target binding must select a quantitative target requirement.")
        return None
    validate_scale_projection(as_object(evidence.get("scaleProjection")), values, errors)
    return target_context_id, target_index


def validate_scale_projection(
    projection: dict[str, Any], values: list[tuple[str, Decimal, int]], errors: list[str],
) -> None:
    data_type = projection.get("dataType")
    decimal_places = projection.get("decimalPlaces")
    if not projection:
        add(errors, "BM-SCALE-01", "Evidence requires a non-empty Scale projection.")
        return
    raw_valid_values = projection.get("validValues")
    if raw_valid_values is not None and not isinstance(raw_valid_values, dict):
        add(errors, "BM-SCALE-01", "Scale validValues must be an object or null.")
    valid_values = as_object(raw_valid_values)
    if decimal_places is not None and (
        not isinstance(decimal_places, int)
        or isinstance(decimal_places, bool)
        or decimal_places < 0
    ):
        add(errors, "BM-SCALE-02", "Scale evidence decimalPlaces must be a non-negative integer or null.")
        decimal_places = None

    category_values: set[Decimal] | None = None
    raw_categories = valid_values.get("categories")
    if raw_categories is not None:
        if not isinstance(raw_categories, list) or not raw_categories:
            add(errors, "BM-SCALE-03", "A category-governed Numerical Scale must provide a non-empty categories array.")
            category_values = set()
        else:
            category_values = set()
            for category_index, raw_category in enumerate(raw_categories):
                category_value = as_object(raw_category).get("value")
                if not isinstance(category_value, str) or not DECIMAL_RE.fullmatch(category_value):
                    add(errors, "BM-SCALE-03", f"Numerical Scale category[{category_index}].value must be an exact decimal string.")
                else:
                    category_values.add(Decimal(category_value))

    bound_values: dict[str, Decimal] = {}
    for bound_name in ("minimumValue", "maximumValue"):
        if bound_name in valid_values:
            raw_bound = valid_values[bound_name]
            if not isinstance(raw_bound, str) or not DECIMAL_RE.fullmatch(raw_bound):
                add(errors, "BM-SCALE-01", f"Scale validValues.{bound_name} must be a decimal string.")
            else:
                bound_values[bound_name] = Decimal(raw_bound)
    if (
        "minimumValue" in bound_values
        and "maximumValue" in bound_values
        and bound_values["minimumValue"] > bound_values["maximumValue"]
    ):
        add(errors, "BM-SCALE-01", "Scale minimumValue must not exceed maximumValue.")

    if data_type != "Numerical":
        add(errors, "BM-SCALE-03", "Quantitative target requires dataType Numerical.")
    for field, number, fractional_digits in values:
        if "minimumValue" in bound_values and number < bound_values["minimumValue"]:
            add(errors, "BM-SCALE-01", f"Target {field} is below Scale validValues.minimumValue.")
        if "maximumValue" in bound_values and number > bound_values["maximumValue"]:
            add(errors, "BM-SCALE-01", f"Target {field} is above Scale validValues.maximumValue.")
        if category_values is not None and number not in category_values:
            add(errors, "BM-SCALE-03", f"Target {field} does not match a permitted Numerical Scale category value.")
        if decimal_places is not None and fractional_digits > decimal_places:
            add(errors, "BM-SCALE-02", f"Target {field} requires more fractional precision than Scale decimalPlaces.")


def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    """Validate one positive or negative candidate scenario."""
    errors: list[str] = []
    revision = as_object(fixture.get("pipelineRevision")) if fixture.get("pipelineRevision") is not None else None
    definitions: dict[tuple[str, str], dict[str, Any]] = {}

    if revision is not None:
        revision_errors, definitions = validate_pipeline_revision(revision)
        errors.extend(revision_errors)
        validate_scale_evidence(fixture, errors)

    if fixture.get("event") is not None:
        errors.extend(validate_execution_event(fixture.get("event"), revision, definitions))

    if fixture.get("registration") is not None:
        errors.extend(validate_registration(fixture.get("registration")))

    if fixture.get("authorityFilterRequest") is not None:
        errors.extend(validate_authority_filter_request(fixture.get("authorityFilterRequest")))

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

    evidence_before = as_object(fixture.get("evidenceBefore"))
    evidence_after = as_object(fixture.get("evidenceAfter"))
    if evidence_before and evidence_after:
        before_evidence_id = evidence_before.get("evidenceRecordId")
        after_evidence_id = evidence_after.get("evidenceRecordId")
        if before_evidence_id and before_evidence_id == after_evidence_id and evidence_before != evidence_after:
            add(errors, "BM-SCALE-06", "An immutable evidenceRecordId must not identify different evidence content.")

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

    # Evidence record identifiers are immutable across the corpus, not just
    # within one fixture's before/after pair. Identical repeated snapshots are
    # allowed; reusing an identifier for different content is rejected.
    corpus_evidence_errors: dict[str, list[str]] = {}
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for scenario_id, fixture in by_id.items():
        snapshots = [
            *scale_evidence_records(fixture),
            fixture.get("evidenceBefore"),
            fixture.get("evidenceAfter"),
        ]
        for snapshot in snapshots:
            evidence = as_object(snapshot)
            evidence_id = evidence.get("evidenceRecordId")
            if not nonempty_string(evidence_id):
                continue
            previous = evidence_by_id.get(evidence_id)
            if previous is None:
                evidence_by_id[evidence_id] = evidence
            elif previous != evidence:
                corpus_evidence_errors.setdefault(scenario_id, []).append(
                    "BM-SCALE-06: An evidenceRecordId must not identify different evidence content across fixtures."
                )

    valid_count = 0
    invalid_count = 0
    for scenario_id, fixture in by_id.items():
        expectation = fixture.get("expectation")
        if expectation not in {"valid", "invalid"}:
            errors.append(f"{scenario_id}: expectation must be valid or invalid")
            continue
        scenario_errors = validate_fixture(fixture)
        detected_invariants = {error.split(":", 1)[0] for error in scenario_errors}
        for corpus_error in corpus_evidence_errors.get(scenario_id, []):
            invariant = corpus_error.split(":", 1)[0]
            if invariant not in detected_invariants:
                scenario_errors.append(corpus_error)
                detected_invariants.add(invariant)
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

    # Requiring each scenario ID alone allowed a row to keep its name while
    # silently dropping the input needed to exercise its invariant.
    required_payloads = {
        ("executionEvents", "pipelineRevision"): (
            "valid-embedded-schemes-multiple-targets",
            "invalid-authority-server-uri-with-userinfo",
            "invalid-authority-server-uri-with-query",
            "invalid-authority-server-uri-with-fragment",
            "invalid-authority-server-uri-relative",
        ),
        ("event",): (
            "valid-event-without-registered-strategy",
            "invalid-stage-without-scheme-version-context",
        ),
        ("pipelineRevision",): (
            "invalid-embedded-scheme-version-identity-mismatch",
            "invalid-duplicate-stage-identifiers",
            "invalid-dangling-transition-endpoint",
            "invalid-duplicate-transition-identifier",
            "invalid-duplicate-task-identifier",
            "invalid-pipeline-version-does-not-match-logical-identity",
            "invalid-target-context-duplicate-identifiers",
            "invalid-exact-decimal-mixed-with-binary-numeric",
            "invalid-authority-qualified-program-reference",
            "valid-exact-decimal-observation-variable-range",
            "invalid-quantitative-target-references-trait-only",
            "invalid-incomplete-exact-decimal-range",
            "invalid-scalar-threshold-combined-with-range",
        ),
        ("event", "pipelineRevision"): (
            "invalid-event-scheme-version-not-bound-by-pipeline-revision",
        ),
        ("after", "before"): (
            "invalid-mutated-published-scheme-version",
        ),
        ("authorityFilterRequest",): (
            "valid-authority-qualified-filters-distinct-authorities",
            "invalid-authority-filter-without-server",
            "invalid-population-filter-without-resource-type",
            "invalid-duplicate-authority-reference-tuple",
        ),
        ("registration",): (
            "valid-identical-registration-replay",
            "valid-new-revision-appends-same-workstream",
            "invalid-same-version-different-payload-registration",
            "valid-first-registration-with-no-current-pointer",
            "valid-published-revision-advances-current-with-matching-precondition",
            "valid-draft-revision-preserves-current-pointer",
            "invalid-append-missing-current-pointer-precondition",
            "invalid-append-stale-current-pointer-precondition",
            "invalid-published-revision-does-not-reference-current-version",
            "valid-withdrawal-references-current-version",
            "invalid-withdrawal-does-not-reference-current-version",
            "invalid-draft-claims-published-supersession",
            "invalid-cross-pipeline-revision-id-replay",
            "invalid-first-create-over-existing-logical-identity",
            "invalid-request-and-revision-pipeline-identities-disagree",
            "invalid-withdrawal-uses-supersedes-relationship",
            "invalid-published-revision-uses-withdraws-relationship",
            "invalid-published-revision-contains-draft-baseline",
            "invalid-published-revision-has-null-draft-baseline",
            "invalid-unknown-publication-state",
            "valid-stale-publication-conflict-preserves-state",
            "invalid-stale-publication-conflict-mutates-state",
        ),
        ("pipelineRevision", "scaleEvidence", "scaleValidationState"): (
            "valid-target-scale-evidence-within-bounds",
            "invalid-target-exceeds-scale-maximum",
            "invalid-target-precision-exceeds-scale",
            "invalid-quantitative-target-nonnumerical-scale",
            "invalid-target-scale-evidence-wrong-pipeline-revision",
            "invalid-target-scale-evidence-wrong-target-context",
            "invalid-target-scale-evidence-wrong-target-index",
            "invalid-target-scale-evidence-wrong-observation-variable",
            "invalid-target-scale-evidence-missing-provenance-metadata",
            "valid-target-scale-evidence-null-precision-and-unit",
            "valid-target-scale-evidence-nonzero-trait-index",
            "valid-target-scale-evidence-matches-numerical-category",
            "invalid-target-scale-evidence-not-in-numerical-categories",
            "invalid-target-scale-evidence-empty-numerical-categories",
            "invalid-target-scale-evidence-malformed-numerical-category",
            "invalid-target-scale-evidence-reversed-scale-bounds",
            "invalid-target-scale-evidence-timestamp-without-timezone",
            "invalid-target-scale-evidence-retrieval-after-validation",
            "invalid-evidence-identity-reused-with-different-content",
        ),
        ("pipelineRevision", "scaleValidationState"): (
            "valid-draft-unresolved-scale-reference",
            "invalid-published-unverified-scale-reference",
        ),
        ("evidenceAfter", "evidenceBefore", "pipelineRevision", "scaleEvidence", "scaleValidationState"): (
            "invalid-target-scale-evidence-mutates-same-id",
        ),
    }
    payload_types = {
        "executionEvents": list,
        "scaleEvidence": (dict, list),
        "scaleValidationState": str,
    }
    missing = []
    for fields, scenario_ids in required_payloads.items():
        for scenario_id in scenario_ids:
            if scenario_id not in by_id:
                missing.append(scenario_id)
                continue
            fixture = by_id[scenario_id]
            for field in fields:
                payload = fixture.get(field)
                if not isinstance(payload, payload_types.get(field, dict)) or not payload:
                    errors.append(f"{scenario_id}: missing or malformed required fixture payload {field}.")
    if missing:
        errors.append("missing required contract scenarios: " + ", ".join(sorted(missing)))

    return errors


def _unique_json_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject ambiguous duplicate object members in the fixture JSON."""
    result: dict[str, Any] = {}
    for name, value in pairs:
        if name in result:
            raise ValueError(f"duplicate JSON object key: {name!r}")
        result[name] = value
    return result


def _reject_nonfinite_json_constant(value: str) -> None:
    """Reject NaN/Infinity, which Python's decoder otherwise permits."""
    raise ValueError(f"non-standard JSON numeric constant: {value}")


def load_fixture_corpus(path: Path) -> Any:
    """Read only standards-compliant, unambiguous JSON fixture documents."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(
            handle,
            object_pairs_hook=_unique_json_object_pairs,
            parse_constant=_reject_nonfinite_json_constant,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=DEFAULT_FIXTURE_PATH)
    args = parser.parse_args()

    try:
        corpus = load_fixture_corpus(args.file)
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
    except ValueError as exc:
        print(f"ERROR: invalid fixture JSON in {args.file}: {exc}", file=sys.stderr)
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
