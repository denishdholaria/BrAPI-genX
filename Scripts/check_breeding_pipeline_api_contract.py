#!/usr/bin/env python3
"""Validate the approved-candidate BreedingPipeline OpenAPI and registry boundary.

This is a static source-contract consistency check. It does not prove server
runtime behavior, schema conformance against a production implementation, or
normative/community approval.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: YAML root must be a mapping")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def schema(doc: dict[str, Any], name: str, path: Path, errors: list[str]) -> dict[str, Any]:
    schemas = doc.get("components", {}).get("schemas", {})
    value = schemas.get(name)
    if not isinstance(value, dict):
        errors.append(f"{path}: missing components.schemas.{name}")
        return {}
    return value


def required_fields(value: dict[str, Any]) -> set[str]:
    raw = value.get("required", [])
    return set(raw) if isinstance(raw, list) else set()


def ref_name(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    ref = value.get("$ref")
    if not isinstance(ref, str) or not ref.startswith("#/components/schemas/"):
        return None
    return ref.rsplit("/", 1)[-1]


def list_operation(path: Path, route: str, errors: list[str]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = load_yaml(path)
    operation = document.get("paths", {}).get(route, {}).get("get")
    if not isinstance(operation, dict):
        errors.append(f"{path}: missing GET {route}")
        return document, []
    params = operation.get("parameters", [])
    if not isinstance(params, list):
        errors.append(f"{path}: GET {route} parameters must be a list")
        return document, []
    return document, [p for p in params if isinstance(p, dict)]


def parameter_map(parameters: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        p.get("name"): p
        for p in parameters
        if isinstance(p.get("name"), str)
    }


def require_filter_pair(
    parameters: dict[str, dict[str, Any]],
    dbid_name: str,
    server_name: str,
    errors: list[str],
    resource_type_name: str | None = None,
) -> None:
    for name in (dbid_name, server_name):
        if name not in parameters:
            errors.append(f"List filter contract is missing query parameter '{name}'.")
    if resource_type_name and resource_type_name not in parameters:
        errors.append(f"List filter contract is missing query parameter '{resource_type_name}'.")
    for name in (dbid_name, server_name, resource_type_name):
        if not name or name not in parameters:
            continue
        parameter = parameters[name]
        if parameter.get("in") != "query":
            errors.append(f"List filter parameter '{name}' must be in=query.")
        if parameter.get("required") is not False:
            errors.append(f"List filter parameter '{name}' must be optional when the filter is unused.")
        description = parameter.get("description", "")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"List filter parameter '{name}' needs an explicit authority-pair description.")
    identifier_description = str(parameters.get(dbid_name, {}).get("description", "")).lower()
    server_description = str(parameters.get(server_name, {}).get("description", "")).lower()
    if server_name.lower() not in identifier_description or "paired" not in identifier_description:
        errors.append(f"List identifier parameter '{dbid_name}' must explicitly require pairing with '{server_name}'.")
    if dbid_name.lower() not in server_description:
        errors.append(f"Authority parameter '{server_name}' must explicitly identify the dbId it qualifies.")
    server = parameters.get(server_name)
    if server:
        fmt = server.get("schema", {}).get("format")
        if fmt != "uri":
            errors.append(f"Authority parameter '{server_name}' must declare schema.format=uri.")
    if resource_type_name and resource_type_name in parameters:
        desc = str(parameters[resource_type_name].get("description", "")).lower()
        if "exact" not in desc or "resource type" not in desc:
            errors.append(
                f"Population resource type filter '{resource_type_name}' must state that the exact resource type is supplied."
            )


def run(root: Path) -> list[str]:
    errors: list[str] = []
    bp_dir = root / "Specification" / "BrAPI-GenX" / "BreedingPipeline"
    bp_schema_path = bp_dir / "Schemas" / "BreedingPipeline.yaml"
    request_path = bp_dir / "Schemas" / "BreedingPipelineNewRequest.yaml"
    pop_schema_path = root / "Specification" / "BrAPI-GenX" / "PopulationAdvancement" / "Schemas" / "PopulationAdvancement.yaml"
    pop_request_path = root / "Specification" / "BrAPI-GenX" / "PopulationAdvancement" / "Schemas" / "PopulationAdvancementNewRequest.yaml"
    sel_schema_path = root / "Specification" / "BrAPI-GenX" / "SelectionDecisions" / "Schemas" / "SelectionDecision.yaml"
    sel_request_path = root / "Specification" / "BrAPI-GenX" / "SelectionDecisions" / "Schemas" / "SelectionDecisionNewRequest.yaml"

    try:
        bp_doc = load_yaml(bp_schema_path)
        request_doc = load_yaml(request_path)
        pop_doc = load_yaml(pop_schema_path)
        pop_request_doc = load_yaml(pop_request_path)
        sel_doc = load_yaml(sel_schema_path)
        sel_request_doc = load_yaml(sel_request_path)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        return [f"Cannot load required BreedingPipeline contract YAML: {exc}"]

    # Authority-qualified BrAPI identity.
    brapi_ref = schema(bp_doc, "BrapiResourceReference", bp_schema_path, errors)
    require(
        {"apiGeneration", "resourceType", "server", "dbId"} <= required_fields(brapi_ref),
        "BrapiResourceReference must require apiGeneration, resourceType, server, and dbId.",
        errors,
    )
    generation = brapi_ref.get("properties", {}).get("apiGeneration", {})
    require(
        generation.get("enum") == ["brapi-v2.1"],
        "BrapiResourceReference.apiGeneration must be fixed to the brapi-v2.1 token for this initial contract.",
        errors,
    )
    server = brapi_ref.get("properties", {}).get("server", {})
    require(server.get("format") == "uri", "BrapiResourceReference.server must be a URI.", errors)

    # Stable logical identity and immutable revision must remain distinct.
    pipeline = schema(bp_doc, "BreedingPipeline", bp_schema_path, errors)
    revision = schema(bp_doc, "BreedingPipelineRevision", bp_schema_path, errors)
    require("breedingPipelineDbId" in pipeline.get("properties", {}), "BreedingPipeline must own breedingPipelineDbId.", errors)
    require(
        {"breedingPipelineDbId", "breedingPipelineVersionDbId", "programReference", "publicationState"} <= required_fields(revision),
        "BreedingPipelineRevision must require its stable ID, immutable version ID, Program reference, and publication state.",
        errors,
    )
    require("pipelineStage" not in pipeline.get("properties", {}), "BreedingPipeline must not carry a scalar pipeline-wide stage.", errors)
    require(
        ref_name(revision.get("properties", {}).get("programReference")) == "BrapiResourceReference",
        "BreedingPipelineRevision.programReference must use BrapiResourceReference.",
        errors,
    )
    revision_summary = schema(bp_doc, "BreedingPipelineRevisionSummary", bp_schema_path, errors)
    require(
        {"breedingPipelineVersionDbId", "publicationState"} <= required_fields(revision_summary),
        "BreedingPipelineRevisionSummary must identify an immutable revision and its publication state.",
        errors,
    )
    logical_properties = pipeline.get("properties", {})
    require(
        ref_name(logical_properties.get("currentRevisionSummary")) == "BreedingPipelineRevisionSummary",
        "BreedingPipeline.currentRevisionSummary must use BreedingPipelineRevisionSummary.",
        errors,
    )
    revision_summaries = logical_properties.get("revisionSummaries", {})
    require(
        revision_summaries.get("type") == "array"
        and ref_name(revision_summaries.get("items")) == "BreedingPipelineRevisionSummary",
        "BreedingPipeline.revisionSummaries must be an array of BreedingPipelineRevisionSummary.",
        errors,
    )
    require(
        "includeRevisions=true" in str(revision_summaries.get("description", "")),
        "BreedingPipeline.revisionSummaries must be explicitly conditional on includeRevisions=true.",
        errors,
    )

    # Scheme definition is embedded in the binding, not referenced as a mutable pointer.
    scheme_binding = schema(bp_doc, "BreedingSchemeBinding", bp_schema_path, errors)
    scheme_version = schema(bp_doc, "BreedingSchemeVersion", bp_schema_path, errors)
    require(
        {"breedingSchemeDbId", "breedingSchemeVersionDbId", "schemeVersion"} <= required_fields(scheme_binding),
        "BreedingSchemeBinding must require both scheme IDs and the embedded schemeVersion.",
        errors,
    )
    require(
        ref_name(scheme_binding.get("properties", {}).get("schemeVersion")) == "BreedingSchemeVersion",
        "BreedingSchemeBinding.schemeVersion must reference BreedingSchemeVersion.",
        errors,
    )
    require(
        {"breedingSchemeDbId", "breedingSchemeVersionDbId", "stages"} <= required_fields(scheme_version),
        "BreedingSchemeVersion must require both scheme identities and its stage definitions.",
        errors,
    )
    binding_items = revision.get("properties", {}).get("schemeBindings", {}).get("items", {})
    require(
        ref_name(binding_items) == "BreedingSchemeBinding",
        "BreedingPipelineRevision.schemeBindings must contain BreedingSchemeBinding objects.",
        errors,
    )
    transition = schema(bp_doc, "StageTransition", bp_schema_path, errors)
    require(
        {"transitionId", "fromStageId", "toStageId", "transitionType"} <= required_fields(transition),
        "StageTransition must declare its identity, directed endpoints, and transition type.",
        errors,
    )
    task = schema(bp_doc, "TaskDefinition", bp_schema_path, errors)
    require(
        {"taskId", "activityCategory"} <= required_fields(task),
        "TaskDefinition must require taskId and activityCategory.",
        errors,
    )

    # Quantitative target objectives must be interpretable through the official BrAPI measurement scale.
    target_requirement = schema(bp_doc, "TargetTraitRequirement", bp_schema_path, errors)
    target_properties = target_requirement.get("properties", {})
    require(
        "unit" not in target_properties,
        "TargetTraitRequirement must not duplicate a free-text unit field; units come from the referenced BrAPI ObservationVariable Scale.",
        errors,
    )
    for field in ("traitReference", "desiredDirection", "threshold", "minimum", "maximum", "exactDecimal", "minimumExactDecimal", "maximumExactDecimal"):
        require(field in target_properties, f"TargetTraitRequirement is missing {field}.", errors)
    decimal_pattern = r"^-?[0-9]+(\.[0-9]+)?$"
    for field in ("exactDecimal", "minimumExactDecimal", "maximumExactDecimal"):
        definition = target_properties.get(field, {})
        require(
            definition.get("type") == "string" and definition.get("pattern") == decimal_pattern,
            f"TargetTraitRequirement.{field} must use the base-10 decimal string pattern without exponent notation.",
            errors,
        )
    trait_description = str(target_properties.get("traitReference", {}).get("description", "")).lower()
    require(
        "observationvariable" in trait_description and "numeric" in trait_description,
        "TargetTraitRequirement must state that quantitative targets require ObservationVariable resourceType.",
        errors,
    )
    target_description = str(target_requirement.get("description", "")).lower()
    require(
        "scale" in target_description and "decimal precision" in target_description,
        "TargetTraitRequirement must explain that BrAPI ObservationVariable Scale supplies units and precision.",
        errors,
    )

    # Registration request must wrap the shared immutable revision schema.
    request = schema(request_doc, "BreedingPipelineNewRequest", request_path, errors)
    require(
        {"breedingPipelineDbId", "breedingPipelineVersion"} <= required_fields(request),
        "BreedingPipelineNewRequest must require stable pipeline identity and revision payload.",
        errors,
    )
    require(
        ref_name(request.get("properties", {}).get("breedingPipelineVersion")) == "BreedingPipelineRevision",
        "BreedingPipelineNewRequest.breedingPipelineVersion must reference the canonical BreedingPipelineRevision schema.",
        errors,
    )
    outer_identity_description = str(
        request.get("properties", {}).get("breedingPipelineDbId", {}).get("description", "")
    ).lower()
    require(
        "must exactly match" in outer_identity_description
        and "breedingpipelineversion.breedingpipelinedbid" in outer_identity_description
        and "400 bad request" in outer_identity_description,
        "BreedingPipelineNewRequest must require the outer and immutable revision pipeline identities to match exactly.",
        errors,
    )

    expected_current = request.get("properties", {}).get("expectedCurrentBreedingPipelineVersionDbId", {})
    require(
        expected_current.get("type") == "string" and expected_current.get("nullable") is True,
        "BreedingPipelineNewRequest.expectedCurrentBreedingPipelineVersionDbId must be a nullable string to distinguish no current revision from an omitted precondition.",
        errors,
    )
    require(
        "expectedCurrentBreedingPipelineVersionDbId" not in required_fields(request),
        "expectedCurrentBreedingPipelineVersionDbId must remain conditionally required, not unconditional, so first creation and identical replay can omit it.",
        errors,
    )
    expected_current_description = str(expected_current.get("description", "")).lower()
    require(
        "explicit null" in expected_current_description
        and "existing" in expected_current_description
        and "replay" in expected_current_description,
        "Expected-current-version description must define explicit-null, existing-pipeline, and replay behavior.",
        errors,
    )

    pipeline_operations_path = bp_dir / "BreedingPipeline_GET_POST.yaml"
    try:
        pipeline_operations = load_yaml(pipeline_operations_path)
        post_operation = pipeline_operations.get("paths", {}).get("/breeding-pipelines", {}).get("post", {})
    except (OSError, yaml.YAMLError, ValueError) as exc:
        errors.append(f"Cannot load BreedingPipeline registration operation: {exc}")
        post_operation = {}
        pipeline_operations = {}
    require(
        post_operation.get("responses", {}).get("200", {}).get("$ref")
        == "#/components/responses/BreedingPipelineResponse",
        "BreedingPipeline registration POST must reference the canonical success Response component.",
        errors,
    )
    success_response = pipeline_operations.get("components", {}).get("responses", {}).get("BreedingPipelineResponse", {})
    success_schema_ref = (
        success_response.get("content", {}).get("application/json", {}).get("schema", {}).get("$ref")
    )
    require(
        success_schema_ref == "#/components/schemas/BreedingPipelineRevisionEnvelope",
        "BreedingPipelineResponse must wrap the canonical immutable revision envelope schema.",
        errors,
    )
    success_envelope = schema(pipeline_operations, "BreedingPipelineRevisionEnvelope", pipeline_operations_path, errors)
    require(
        {"metadata", "result"} <= required_fields(success_envelope)
        and ref_name(success_envelope.get("properties", {}).get("result")) == "BreedingPipelineRevision",
        "BreedingPipelineRevisionEnvelope must require metadata and the exact immutable revision result.",
        errors,
    )
    try:
        get_operation_doc = load_yaml(bp_dir / "BreedingPipeline_BreedingPipelineDbId_GET.yaml")
        get_operation = get_operation_doc.get("paths", {}).get("/breeding-pipelines/{breedingPipelineDbId}", {}).get("get", {})
    except (OSError, yaml.YAMLError, ValueError) as exc:
        errors.append(f"Cannot load BreedingPipeline exact-revision retrieval operation: {exc}")
        get_operation = {}
    require(
        get_operation.get("responses", {}).get("200", {}).get("$ref")
        == "#/components/responses/BreedingPipelineResponse",
        "BreedingPipeline single-resource GET must reuse the canonical success Response component.",
        errors,
    )
    require(
        post_operation.get("responses", {}).get("409", {}).get("$ref")
        == "#/components/responses/BreedingPipelineConflictResponse",
        "BreedingPipeline registration POST must document its structured 409 Conflict response.",
        errors,
    )
    conflict_schema = schema(pipeline_operations, "BreedingPipelineConflict", pipeline_operations_path, errors)
    require(
        {"errorCode", "message"} <= required_fields(conflict_schema),
        "BreedingPipelineConflict must require errorCode and message.",
        errors,
    )
    conflict_properties = conflict_schema.get("properties", {})
    require(
        {"version-content-conflict", "current-version-precondition-failed", "revision-relationship-mismatch", "pipeline-identity-conflict"}
        <= set(conflict_properties.get("errorCode", {}).get("enum", [])),
        "BreedingPipelineConflict.errorCode must distinguish revision content, current pointer, relationship, and logical-pipeline identity conflicts.",
        errors,
    )
    current_on_conflict = conflict_properties.get("currentBreedingPipelineVersionDbId", {})
    require(
        current_on_conflict.get("type") == "string" and current_on_conflict.get("nullable") is True,
        "BreedingPipelineConflict.currentBreedingPipelineVersionDbId must be a nullable string.",
        errors,
    )
    current_on_conflict_description = str(current_on_conflict.get("description", "")).lower()
    require(
        "authorized to read" in current_on_conflict_description
        and "omitted" in current_on_conflict_description
        and "null" in current_on_conflict_description,
        "Conflict response must disclose the current pointer only to an authorized reader and distinguish omission from authorized null.",
        errors,
    )
    post_extension = post_operation.get("x-brapi-genx", {})
    idempotency_text = str(post_extension.get("idempotency", "")).lower()
    require(
        "jcs" in idempotency_text
        and "before" in idempotency_text
        and "atomically" in idempotency_text
        and "409" in idempotency_text,
        "BreedingPipeline POST idempotency contract must document canonical replay-before-precondition and atomic 409 conflict behavior.",
        errors,
    )

    # Execution contexts are nested; no event schema may accept unqualified top-level stage IDs.
    pipeline_context = schema(bp_doc, "BreedingPipelineExecutionContext", bp_schema_path, errors)
    scheme_context = schema(bp_doc, "BreedingSchemeExecutionContext", bp_schema_path, errors)
    require(
        {"breedingPipelineDbId", "breedingPipelineVersionDbId"} <= required_fields(pipeline_context),
        "BreedingPipelineExecutionContext must require the stable pipeline ID and exact revision ID.",
        errors,
    )
    require(
        {"breedingSchemeDbId", "breedingSchemeVersionDbId"} <= required_fields(scheme_context),
        "BreedingSchemeExecutionContext must require the scheme ID and exact scheme version ID.",
        errors,
    )
    require(
        {"stageId", "fromStageId", "toStageId"} <= set(scheme_context.get("properties", {})),
        "BreedingSchemeExecutionContext must contain all optional scheme-local stage references.",
        errors,
    )
    for label, doc, path in (
        ("PopulationAdvancement", pop_doc, pop_schema_path),
        ("PopulationAdvancementNewRequest", pop_request_doc, pop_request_path),
        ("SelectionDecision", sel_doc, sel_schema_path),
        ("SelectionDecisionNewRequest", sel_request_doc, sel_request_path),
    ):
        definition = schema(doc, label, path, errors)
        props = definition.get("properties", {})
        require(
            ref_name(props.get("pipelineContext")) == "BreedingPipelineExecutionContext",
            f"{label}.pipelineContext must use BreedingPipelineExecutionContext.",
            errors,
        )
        require(
            ref_name(props.get("schemeContext")) == "BreedingSchemeExecutionContext",
            f"{label}.schemeContext must use BreedingSchemeExecutionContext.",
            errors,
        )
        forbidden = {"stageId", "fromStageId", "toStageId"} & set(props)
        require(
            not forbidden,
            f"{label} must not expose top-level scheme stage fields: {sorted(forbidden)}.",
            errors,
        )

    # Authority scope for list filters.
    pop_ops_path = root / "Specification" / "BrAPI-GenX" / "PopulationAdvancement" / "PopulationAdvancement_GET_POST.yaml"
    sel_ops_path = root / "Specification" / "BrAPI-GenX" / "SelectionDecisions" / "SelectionDecisions_GET_POST.yaml"
    try:
        _, pop_params = list_operation(pop_ops_path, "/population-advancements", errors)
        _, sel_params = list_operation(sel_ops_path, "/selection-decisions", errors)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        errors.append(f"Cannot load execution list endpoints: {exc}")
        pop_params, sel_params = [], []

    pop_map = parameter_map(pop_params)
    sel_map = parameter_map(sel_params)
    require_filter_pair(pop_map, "programDbId", "programServer", errors)
    require_filter_pair(pop_map, "populationDbId", "populationServer", errors, "populationResourceType")
    require_filter_pair(sel_map, "programDbId", "programServer", errors)
    require_filter_pair(sel_map, "studyDbId", "studyServer", errors)
    require_filter_pair(sel_map, "candidateGermplasmDbId", "candidateGermplasmServer", errors)

    # The structured registry must document exactly the new authority-context query parameters.
    registry_path = root / "Specification" / "ENDPOINT-REGISTRY.json"
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"Cannot read endpoint registry: {exc}"]
    expected = {
        "brapi-genx.genx.v1.population-advancements.list": {
            "programDbId", "programServer", "populationDbId", "populationServer",
            "populationResourceType", "status", "page", "pageSize", "authorizationHeader"
        },
        "brapi-genx.genx.v1.selection-decisions.list": {
            "programDbId", "programServer", "studyDbId", "studyServer",
            "candidateGermplasmDbId", "candidateGermplasmServer", "decision",
            "page", "pageSize", "authorizationHeader"
        },
    }
    rows = {
        entry.get("catalogId"): entry
        for entry in registry.get("entries", [])
        if isinstance(entry, dict)
    }
    for catalog_id, wanted in expected.items():
        row = rows.get(catalog_id, {})
        actual = set(row.get("parameters", []))
        if actual != wanted:
            errors.append(
                f"{catalog_id}: registry parameters differ from the authority-qualified filter contract; "
                f"missing={sorted(wanted - actual)}, extra={sorted(actual - wanted)}."
            )

    if errors:
        return errors
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = run(args.root.resolve())
    if errors:
        print("BreedingPipeline API contract checks failed:")
        for error in errors:
            print("- " + error)
        return 1
    print("PASS: embedded scheme versions, immutable identities, nested execution contexts, authority-qualified list filters, and atomic revision registration preconditions.")
    print("NOTE: static contract consistency only; no production runtime conformance or normative status is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
