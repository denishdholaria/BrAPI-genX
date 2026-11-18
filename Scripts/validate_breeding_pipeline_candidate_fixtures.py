#!/usr/bin/env python3
"""Validate the advisory BreedingPipeline/BreedingScheme design fixture corpus.

This is a standalone design-evidence checker. It is intentionally not part of
production conformance and does not validate an accepted BrAPI-GenX contract.
It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "assessment"
    / "BRAPI-GENX-BREEDING-PIPELINE-CANDIDATE-FIXTURES.json"
)

REQUIRED_SCENARIOS = {
    "valid-recurrent-overlapping-cohorts",
    "valid-scheme-revision-history",
    "valid-brapi-execution-crosswalk",
    "invalid-dangling-stage-transition",
    "invalid-execution-stage-without-scheme-version",
    "invalid-pipeline-scheme-version-mismatch",
    "invalid-published-scheme-mutated-in-place",
    "invalid-duplicate-parentage-authority",
    "invalid-pipeline-wide-current-stage",
}

BRAPI_RESOURCE_TYPES = {
    "Program",
    "CrossingProject",
    "PlannedCross",
    "Cross",
    "Study",
}
GENX_RESOURCE_TYPES = {"SelectionDecision", "PopulationAdvancement"}


def as_object(value: Any) -> dict[str, Any]:
    """Return a mapping or an empty mapping for safe validation."""
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    """Return a list or an empty list for safe validation."""
    return value if isinstance(value, list) else []


def stage_ids(stage_rows: Any) -> list[str]:
    """Extract non-empty stage identifiers from stage definitions."""
    result: list[str] = []
    for stage in as_list(stage_rows):
        stage_id = as_object(stage).get("stageId")
        if isinstance(stage_id, str) and stage_id:
            result.append(stage_id)
    return result


def validate_corpus(corpus: Any) -> list[str]:
    """Return all corpus validation errors; an empty list means success."""
    errors: list[str] = []

    if not isinstance(corpus, dict):
        return ["top-level JSON value must be an object"]

    if corpus.get("designStatus") != "candidate-only":
        errors.append("designStatus must be 'candidate-only'")
    if corpus.get("normative") is not False:
        errors.append("normative must be false")
    if corpus.get("schemaStatus") != "not-an-openapi-contract":
        errors.append("schemaStatus must be 'not-an-openapi-contract'")

    fixtures = as_list(corpus.get("fixtures"))
    if not fixtures:
        errors.append("fixtures must be a non-empty array")

    by_id: dict[str, dict[str, Any]] = {}
    for index, raw_fixture in enumerate(fixtures):
        fixture = as_object(raw_fixture)
        scenario_id = fixture.get("scenarioId")
        if not isinstance(scenario_id, str) or not scenario_id:
            errors.append(f"fixtures[{index}] has no non-empty scenarioId")
            continue
        if scenario_id in by_id:
            errors.append(f"duplicate scenarioId: {scenario_id}")
            continue
        by_id[scenario_id] = fixture

        expectation = fixture.get("expectation")
        if expectation not in {"valid", "invalid"}:
            errors.append(f"{scenario_id}: expectation must be valid or invalid")
        if expectation == "invalid" and not fixture.get("expectedFailure"):
            errors.append(f"{scenario_id}: invalid scenario needs expectedFailure")

    missing = sorted(REQUIRED_SCENARIOS - set(by_id))
    if missing:
        errors.append("missing required scenarios: " + ", ".join(missing))

    valid_count = sum(
        1 for item in by_id.values() if item.get("expectation") == "valid"
    )
    invalid_count = sum(
        1 for item in by_id.values() if item.get("expectation") == "invalid"
    )
    if valid_count < 1 or invalid_count < 1:
        errors.append("corpus must include at least one valid and one invalid scenario")

    # Positive scenario: recurrent process and concurrently active cohorts.
    fixture = by_id.get("valid-recurrent-overlapping-cohorts", {})
    pipeline = as_object(fixture.get("pipeline"))
    scheme = as_object(fixture.get("schemeVersion"))
    scheme_version_id = scheme.get("schemeVersionId")
    bindings = [
        as_object(item).get("schemeVersionId")
        for item in as_list(pipeline.get("schemeBindings"))
    ]
    if not scheme_version_id or scheme_version_id not in bindings:
        errors.append(
            "valid-recurrent-overlapping-cohorts: pipeline must bind the exact scheme version"
        )

    program_ref = as_object(pipeline.get("programReference"))
    for field in ("apiGeneration", "resourceType", "server", "dbId"):
        if not isinstance(program_ref.get(field), str) or not program_ref.get(field):
            errors.append(
                "valid-recurrent-overlapping-cohorts: Program reference "
                f"requires non-empty {field}"
            )
    if program_ref.get("resourceType") != "Program":
        errors.append(
            "valid-recurrent-overlapping-cohorts: programReference resourceType must be Program"
        )

    defined_stages = stage_ids(scheme.get("stages"))
    defined_stage_set = set(defined_stages)
    if not defined_stages:
        errors.append("valid-recurrent-overlapping-cohorts: at least one stage is required")
    if len(defined_stages) != len(defined_stage_set):
        errors.append("valid-recurrent-overlapping-cohorts: stageId values must be unique")

    transitions = as_list(scheme.get("transitions"))
    if not transitions:
        errors.append("valid-recurrent-overlapping-cohorts: transitions must be non-empty")
    for transition_index, raw_transition in enumerate(transitions):
        transition = as_object(raw_transition)
        if (
            transition.get("fromStageId") not in defined_stage_set
            or transition.get("toStageId") not in defined_stage_set
        ):
            errors.append(
                "valid-recurrent-overlapping-cohorts: "
                f"transition[{transition_index}] has a dangling stage reference"
            )
    if not any(
        as_object(item).get("transitionType") == "recurrent"
        for item in transitions
    ):
        errors.append(
            "valid-recurrent-overlapping-cohorts: at least one recurrent transition is required"
        )

    cohorts = as_list(fixture.get("cohortExecutions"))
    if len(cohorts) < 2:
        errors.append("valid-recurrent-overlapping-cohorts: at least two cohorts are required")
    cohort_stages: set[str] = set()
    for index, raw_cohort in enumerate(cohorts):
        cohort = as_object(raw_cohort)
        if cohort.get("schemeVersionId") != scheme_version_id:
            errors.append(
                f"valid-recurrent-overlapping-cohorts: cohort[{index}] uses a different scheme version"
            )
        if cohort.get("stageId") not in defined_stage_set:
            errors.append(
                f"valid-recurrent-overlapping-cohorts: cohort[{index}] has an unknown stage"
            )
        if isinstance(cohort.get("stageId"), str):
            cohort_stages.add(cohort["stageId"])
    if len(cohort_stages) < 2:
        errors.append(
            "valid-recurrent-overlapping-cohorts: cohorts must occupy at least two distinct stages"
        )

    # Positive scenario: historical events keep their exact revision binding.
    fixture = by_id.get("valid-scheme-revision-history", {})
    pipeline = as_object(fixture.get("pipeline"))
    event = as_object(fixture.get("executionEvent"))
    revisions = [
        as_object(item) for item in as_list(pipeline.get("revisions"))
    ]
    matching_revision = next(
        (
            item
            for item in revisions
            if item.get("pipelineRevisionId") == event.get("pipelineRevisionId")
        ),
        None,
    )
    revision_bindings = {
        as_object(item).get("schemeVersionId")
        for item in as_list(as_object(matching_revision).get("schemeBindings"))
    }
    if not matching_revision or event.get("schemeVersionId") not in revision_bindings:
        errors.append(
            "valid-scheme-revision-history: event must resolve to the exact scheme "
            "version bound by its pipeline revision"
        )

    # Positive scenario: BrAPI and GenX execution resources retain their owners.
    fixture = by_id.get("valid-brapi-execution-crosswalk", {})
    references = as_list(fixture.get("executionReferences"))
    if not references:
        errors.append("valid-brapi-execution-crosswalk: executionReferences must be non-empty")
    for index, raw_reference in enumerate(references):
        reference = as_object(raw_reference)
        owner = reference.get("owner")
        resource_type = reference.get("resourceType")
        if owner == "BrAPI":
            if resource_type not in BRAPI_RESOURCE_TYPES:
                errors.append(
                    f"valid-brapi-execution-crosswalk: reference[{index}] has an "
                    "unrecognized BrAPI resourceType"
                )
            for field in ("server", "dbId"):
                if not isinstance(reference.get(field), str) or not reference.get(field):
                    errors.append(
                        f"valid-brapi-execution-crosswalk: BrAPI reference[{index}] "
                        f"requires {field}"
                    )
        elif owner == "GenX":
            if resource_type not in GENX_RESOURCE_TYPES:
                errors.append(
                    f"valid-brapi-execution-crosswalk: reference[{index}] has an "
                    "unrecognized GenX resourceType"
                )
            if not isinstance(reference.get("dbId"), str) or not reference.get("dbId"):
                errors.append(
                    f"valid-brapi-execution-crosswalk: GenX reference[{index}] requires dbId"
                )
        else:
            errors.append(
                f"valid-brapi-execution-crosswalk: reference[{index}] owner must be BrAPI or GenX"
            )

    # Negative scenario: a transition must not point outside its scheme version.
    fixture = by_id.get("invalid-dangling-stage-transition", {})
    scheme = as_object(fixture.get("schemeVersion"))
    stages = set(stage_ids(scheme.get("stages")))
    dangling = any(
        as_object(item).get("fromStageId") not in stages
        or as_object(item).get("toStageId") not in stages
        for item in as_list(scheme.get("transitions"))
    )
    if not dangling:
        errors.append(
            "invalid-dangling-stage-transition: scenario does not contain a dangling stage reference"
        )

    # Negative scenario: scheme-local stage IDs require an exact scheme version.
    fixture = by_id.get("invalid-execution-stage-without-scheme-version", {})
    event = as_object(fixture.get("executionEvent"))
    has_stage = bool(event.get("fromStageId") or event.get("toStageId") or event.get("stageId"))
    if event.get("schemeVersionId") or not has_stage:
        errors.append(
            "invalid-execution-stage-without-scheme-version: scenario must have stage "
            "reference(s) and no schemeVersionId"
        )

    # Negative scenario: an event must reference a version bound by its pipeline revision.
    fixture = by_id.get("invalid-pipeline-scheme-version-mismatch", {})
    revision = as_object(fixture.get("pipelineRevision"))
    event = as_object(fixture.get("executionEvent"))
    bindings = {
        as_object(item).get("schemeVersionId")
        for item in as_list(revision.get("schemeBindings"))
    }
    if (
        event.get("pipelineRevisionId") != revision.get("pipelineRevisionId")
        or not event.get("schemeVersionId")
        or event.get("schemeVersionId") in bindings
    ):
        errors.append(
            "invalid-pipeline-scheme-version-mismatch: event must cite a scheme version "
            "not bound by the referenced revision"
        )

    # Negative scenario: published content changed without a new version ID.
    fixture = by_id.get("invalid-published-scheme-mutated-in-place", {})
    before = as_object(fixture.get("before"))
    after = as_object(fixture.get("after"))
    if (
        not before.get("schemeVersionId")
        or before.get("schemeVersionId") != after.get("schemeVersionId")
        or before.get("publicationState") != "published"
        or after.get("publicationState") != "published"
        or before.get("stages") == after.get("stages")
    ):
        errors.append(
            "invalid-published-scheme-mutated-in-place: scenario must change published "
            "content while retaining the same schemeVersionId"
        )

    # Negative scenario: two authorities assert conflicting parentage.
    fixture = by_id.get("invalid-duplicate-parentage-authority", {})
    pedigree = as_object(fixture.get("brapiPedigree"))
    progeny_record = as_object(fixture.get("genxProgenyRecord"))
    if (
        not pedigree.get("germplasmDbId")
        or pedigree.get("germplasmDbId") != progeny_record.get("progenyDbId")
        or pedigree.get("parentDbIds") == progeny_record.get("parentDbIds")
        or progeny_record.get("claimsParentageAuthority") is not True
    ):
        errors.append(
            "invalid-duplicate-parentage-authority: scenario must show conflicting "
            "parentage authorities for the same Germplasm"
        )

    # Negative scenario: a pipeline-wide stage cannot represent concurrent cohorts.
    fixture = by_id.get("invalid-pipeline-wide-current-stage", {})
    pipeline = as_object(fixture.get("pipeline"))
    concurrent_states = as_list(fixture.get("concurrentCohortStates"))
    concurrent_stages = {
        as_object(item).get("stageId") for item in concurrent_states
    }
    if (
        not pipeline.get("currentStage")
        or len(concurrent_stages) < 2
        or None in concurrent_stages
    ):
        errors.append(
            "invalid-pipeline-wide-current-stage: scenario must conflict with at least "
            "two different cohort stage values"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the advisory BreedingPipeline/BreedingScheme candidate "
            "fixture corpus. This does not run production conformance."
        )
    )
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FIXTURE_PATH,
        help="Path to the candidate fixture JSON file.",
    )
    args = parser.parse_args()

    try:
        with args.file.open("r", encoding="utf-8") as fixture_file:
            corpus = json.load(fixture_file)
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

    errors = validate_corpus(corpus)
    fixture_count = len(as_list(as_object(corpus).get("fixtures")))
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(
            f"FAILED: {len(errors)} validation error(s) across "
            f"{fixture_count} candidate fixture(s)."
        )
        return 1

    valid_count = sum(
        1
        for item in as_list(as_object(corpus).get("fixtures"))
        if as_object(item).get("expectation") == "valid"
    )
    invalid_count = fixture_count - valid_count
    print(
        "PASS: candidate-only fixture corpus "
        f"({fixture_count} scenarios: {valid_count} valid, {invalid_count} invalid)."
    )
    print("PASS: required identity, transition, versioning, and ownership checks.")
    print("NOTE: no production conformance or normative contract is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
