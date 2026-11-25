#!/usr/bin/env python3
"""Fail closed when GenX CI no longer watches shared specification dependencies."""
from __future__ import annotations

import copy
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/genx-static-conformance.yml"
REQUIRED_PATHS = {
    "Specification/**",
    "docs/governance/**",
    "docs/assessment/**",
    "Scripts/**",
    ".github/workflows/genx-static-conformance.yml",
    ".github/workflows/generate-schema.yml",
    "Scripts/checkGenXConformance.py",
    "Scripts/checkGenXEndpointCatalog.py",
    "Scripts/checkEndpointRegistry.py",
    "Scripts/generateEndpointArtifacts.py",
    "Scripts/specification_structure.py",
    "Scripts/test_specification_structure.py",
    "Scripts/test_conformance_workflow_scope.py",
    "Scripts/auditEndpointRegistrySourceConsistency.py",
    "Scripts/test_registry_source_consistency.py",
    "Scripts/check_semantic_neighbor_governance.py",
    "Scripts/test_semantic_neighbor_governance.py",
    "Scripts/audit_genx_readme_routes.py",
    "Scripts/test_genx_readme_routes.py",
}
REQUIRED_COMMANDS = {
    "python Scripts/specification_structure.py",
    "python Scripts/test_specification_structure.py",
    "python Scripts/checkGenXConformance.py",
    "python Scripts/test_conformance_probe_selection.py",
    "python Scripts/test_conformance_assertion_manifest.py",
    "python Scripts/test_conformance_step_manifest.py",
    "python Scripts/test_telemetry_conflict_postcondition.py",
    "python Scripts/test_telemetry_replay_postcondition.py",
    "python Scripts/test_telemetry_window_partition.py",
    "python Scripts/test_telemetry_pagination_slice.py",
    "python Scripts/test_provenance_roundtrip_integrity.py",
    "python Scripts/test_collection_envelope_integrity.py",
    "python Scripts/test_concurrent_job_stored_effect.py",
    "python Scripts/test_variable_term_conflict_postcondition.py",
    "python Scripts/test_ledger_conflict_postcondition.py",
    "python Scripts/test_ledger_replay_postcondition.py",
    "python Scripts/test_term_replay_version_uniqueness.py",
    "python Scripts/test_matrix_replay_stored_state.py",
    "python Scripts/test_package_replay_stored_state.py",
    "python Scripts/test_model_replay_version_integrity.py",
    "python Scripts/test_matrix_conflict_whole_record.py",
    "python Scripts/test_package_conflict_whole_record.py",
    "python Scripts/test_model_conflict_whole_record.py",
    "python Scripts/test_rejected_inference_no_stored_job.py",
    "python Scripts/test_job_replay_single_stored.py",
    "python Scripts/test_job_conflict_collection_unchanged.py",
    "python Scripts/test_terminal_cancel_retained_state.py",
    "python Scripts/test_unknown_jobtype_no_stored_job.py",
    "python Scripts/test_expired_job_result_withheld.py",
    "python Scripts/test_embargo_denial_no_payload.py",
    "python Scripts/test_collection_pagination_arithmetic.py",
    "python Scripts/test_deprecated_inference_result_binding.py",
    "python Scripts/test_inference_result_identity_digest.py",
    "python Scripts/test_telemetry_mean_source_integrity.py",
    "python Scripts/test_deprecated_inference_completion.py",
    "python Scripts/test_model_conflict_postcondition.py",
    "python Scripts/test_publication_conflict_postconditions.py",
    "python Scripts/test_v21_fallback_envelope.py",
    "python Scripts/checkEndpointRegistry.py",
    "python Scripts/auditEndpointRegistrySourceConsistency.py --strict",
    "python Scripts/test_registry_source_consistency.py",
    "python Scripts/check_semantic_neighbor_governance.py",
    "python Scripts/check_semantic_neighbor_governance.py --comparison-ref",
    "python Scripts/test_semantic_neighbor_governance.py",
    "python Scripts/generateEndpointArtifacts.py --check",
    "python Scripts/audit_genx_readme_routes.py --module Geospatial/VegetationIndex --strict --require-coverage",
    "python Scripts/test_genx_readme_routes.py",
    "python Scripts/test_generation_workflow_permissions.py",
    "python Scripts/check_rfc_governance.py",
    "python Scripts/test_rfc_governance.py",
    "python Scripts/report_genx_evidence_coverage.py --check",
    "python Scripts/test_genx_evidence_coverage.py",
}


def scope_errors(document: dict) -> list[str]:
    errors: list[str] = []
    # PyYAML's YAML 1.1 resolver interprets 'on:' as the boolean True.
    triggers = document.get("on", document.get(True))
    if not isinstance(triggers, dict):
        return ["Missing pull_request/push workflow trigger mapping"]
    for event in ("pull_request", "push"):
        options = triggers.get(event)
        paths = set((options or {}).get("paths") or [])
        for dep in sorted(REQUIRED_PATHS - paths):
            errors.append(f"{event} trigger missing dependency: {dep}")
    jobs = document.get("jobs") or {}
    job = jobs.get("static-conformance") or {}
    commands = "\n".join(str(s.get("run", "")) for s in job.get("steps", [])
                        if isinstance(s, dict) and "failure()" not in str(s.get("if", "")))
    for command in sorted(REQUIRED_COMMANDS):
        if command not in commands:
            errors.append(f"static-conformance job missing command: {command}")
    differential = jobs.get("independent-runtime-differential")
    if not isinstance(differential, dict):
        errors.append("missing independent-runtime-differential job")
    else:
        steps = differential.get("steps") or []
        commands = "\n".join(str(step.get("run", "")) for step in steps
                             if isinstance(step, dict)
                             and "failure()" not in str(step.get("if", "")))
        for required in (
            "python Scripts/genx_test_server.py --port 18080",
            "bun Scripts/genx_test_server_ts.ts --port 18082",
            "bun Scripts/genx_test_server_ts.ts --port 18083 --delay 0.4 --profile v21",
            "python Scripts/checkGenXConformance.py --server http://127.0.0.1:18083/genx/v1 --only L-06",
            "python Scripts/genx_differential_check.py --a http://127.0.0.1:18080/genx/v1 --b http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED",
            "python Scripts/test_genx_differential_check.py",
            "python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED --only L-12",
            "python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED --only L-13",
            "python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED --only L-15",
            "python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED --only L-14",
            "python Scripts/checkGenXConformance.py --server http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED --only L-24",
        ):
            if required not in commands:
                errors.append(f"independent-runtime-differential missing command: {required}")
        if not any(isinstance(step, dict)
                   and step.get("uses") == "oven-sh/setup-bun@v2"
                   for step in steps):
            errors.append("independent-runtime-differential missing Bun setup")
    return errors


class WorkflowScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))

    def test_complete_scope_and_required_commands(self):
        self.assertEqual([], scope_errors(self.workflow))

    def test_missing_shared_specification_dependency_is_detected(self):
        damaged = copy.deepcopy(self.workflow)
        triggers = damaged.get("on", damaged.get(True))
        triggers["pull_request"]["paths"].remove("Specification/**")
        self.assertTrue(any("pull_request trigger missing dependency: Specification/**" in x
                            for x in scope_errors(damaged)))

    def test_missing_validator_execution_is_detected(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        step = next(s for s in steps if s.get("run") == "python Scripts/specification_structure.py")
        step["run"] = "echo skipped"
        self.assertTrue(any("job missing command: python Scripts/specification_structure.py" in x
                            for x in scope_errors(damaged)))


    def test_readme_route_gate_cannot_hide_in_failure_only_diagnostics(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        required = ("python Scripts/audit_genx_readme_routes.py "
                    "--module Geospatial/VegetationIndex --strict --require-coverage")
        step = next(s for s in steps if s.get("run") == required)
        step["run"] = "echo route-audit-skipped"
        self.assertTrue(any(
            "job missing command: " + required in error
            for error in scope_errors(damaged)
        ))


    def test_readme_coverage_flag_is_enforced_by_workflow(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        expected = ("python Scripts/audit_genx_readme_routes.py "
                    "--module Geospatial/VegetationIndex --strict --require-coverage")
        step = next(s for s in steps if s.get("run") == expected)
        step["run"] = expected.replace(" --require-coverage", "")
        self.assertTrue(any(
            "job missing command: " + expected in error
            for error in scope_errors(damaged)
        ))



    def test_governance_assessment_and_script_changes_trigger_both_events(self):
        # A relevant file edit must not bypass the entire CI workflow.
        for event in ("pull_request", "push"):
            for dependency in ("docs/governance/**", "docs/assessment/**",
                               "Scripts/**"):
                with self.subTest(event=event, dependency=dependency):
                    damaged = copy.deepcopy(self.workflow)
                    triggers = damaged.get("on", damaged.get(True))
                    triggers[event]["paths"].remove(dependency)
                    self.assertIn(
                        f"{event} trigger missing dependency: {dependency}",
                        scope_errors(damaged),
                    )

    def test_maturity_and_evidence_commands_cannot_be_skipped(self):
        commands = (
            "python Scripts/check_rfc_governance.py",
            "python Scripts/test_rfc_governance.py",
            "python Scripts/report_genx_evidence_coverage.py --check",
            "python Scripts/test_genx_evidence_coverage.py",
        )
        for required in commands:
            with self.subTest(command=required):
                damaged = copy.deepcopy(self.workflow)
                steps = damaged["jobs"]["static-conformance"]["steps"]
                step = next(s for s in steps if s.get("run") == required)
                step["run"] = "echo validation-skipped"
                self.assertIn(
                    f"static-conformance job missing command: {required}",
                    scope_errors(damaged),
                )


    def test_missing_independent_differential_job_fails_closed(self):
        damaged = copy.deepcopy(self.workflow)
        damaged["jobs"].pop("independent-runtime-differential")
        self.assertIn("missing independent-runtime-differential job",
                      scope_errors(damaged))

    def test_differential_execution_cannot_be_removed(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
        step = next(step for step in steps
                    if str(step.get("run", "")).startswith(
                        "python Scripts/genx_differential_check.py --a"))
        step["run"] = "echo differential-skip"
        self.assertTrue(any("missing command: python Scripts/genx_differential_check.py" in x
                            for x in scope_errors(damaged)))

    def test_differential_required_server_cannot_be_removed(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
        step = next(step for step in steps
                    if "bun Scripts/genx_test_server_ts.ts --port 18082"
                    in str(step.get("run", "")))
        step["run"] = step["run"].replace(
            "bun Scripts/genx_test_server_ts.ts --port 18082",
            "echo TypeScript-server-disabled")
        self.assertTrue(any("missing command: bun Scripts/genx_test_server_ts.ts" in x
                            for x in scope_errors(damaged)))

    def test_differential_only_in_diagnostics_cannot_pass(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
        step = next(step for step in steps
                    if str(step.get("run", "")).startswith(
                        "python Scripts/genx_differential_check.py --a"))
        step["if"] = "failure()"
        self.assertTrue(any("missing command: python Scripts/genx_differential_check.py" in x
                            for x in scope_errors(damaged)))

    def test_differential_bun_setup_required(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
        steps[:] = [step for step in steps
                    if step.get("uses") != "oven-sh/setup-bun@v2"]
        self.assertIn("independent-runtime-differential missing Bun setup",
                      scope_errors(damaged))


    def test_differential_http_status_mutations_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
        step = next(item for item in steps
                    if item.get("run") == "python Scripts/test_genx_differential_check.py")
        step["run"] = "echo status-tests-skipped"
        self.assertTrue(any(
            "missing command: python Scripts/test_genx_differential_check.py" in error
            for error in scope_errors(damaged)
        ))


    def test_typescript_live_probes_are_not_diagnostic_only(self):
        for probe in ("L-14", "L-24"):
            with self.subTest(probe=probe):
                damaged = copy.deepcopy(self.workflow)
                steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
                command = ("python Scripts/checkGenXConformance.py --server "
                           "http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED "
                           f"--only {probe}")
                step = next(s for s in steps if s.get("run") == command)
                step["if"] = "failure()"
                self.assertTrue(any(
                    "independent-runtime-differential missing command: " + command in error
                    for error in scope_errors(damaged)
                ))

    def test_typescript_live_probes_cannot_be_silently_removed(self):
        for probe in ("L-14", "L-24"):
            with self.subTest(probe=probe):
                damaged = copy.deepcopy(self.workflow)
                steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
                command = ("python Scripts/checkGenXConformance.py --server "
                           "http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED "
                           f"--only {probe}")
                step = next(s for s in steps if s.get("run") == command)
                step["run"] = "echo probe-skipped"
                self.assertTrue(any(
                    "independent-runtime-differential missing command: " + command in error
                    for error in scope_errors(damaged)
                ))


    def test_selected_probe_fail_closed_regression_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        step = next(s for s in steps
                    if s.get("run") == "python Scripts/test_conformance_probe_selection.py")
        step["run"] = "echo selected-probe-check-skipped"
        self.assertIn(
            "static-conformance job missing command: python Scripts/test_conformance_probe_selection.py",
            scope_errors(damaged),
        )


    def test_typescript_model_integrity_probes_cannot_be_skipped(self):
        for probe_id in ("L-12", "L-13", "L-15"):
            with self.subTest(probe=probe_id):
                command = (
                    "python Scripts/checkGenXConformance.py --server "
                    "http://127.0.0.1:18082/genx/v1 --expired-job JOB_EXPIRED "
                    f"--only {probe_id}"
                )
                for defect in ("removed", "diagnostic_only"):
                    with self.subTest(defect=defect):
                        damaged = copy.deepcopy(self.workflow)
                        steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
                        step = next(s for s in steps if s.get("run") == command)
                        if defect == "removed":
                            step["run"] = "echo model-integrity-check-skipped"
                        else:
                            step["if"] = "failure()"
                        self.assertIn(
                            "independent-runtime-differential missing command: " + command,
                            scope_errors(damaged),
                        )


    def test_model_conflict_postcondition_test_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        test = next(s for s in steps if s.get("run")
                    == "python Scripts/test_model_conflict_postcondition.py")
        test["run"] = "echo model-conflict-postcondition-skipped"
        self.assertIn(
            "static-conformance job missing command: python Scripts/test_model_conflict_postcondition.py",
            scope_errors(damaged),
        )


    def test_publication_postcondition_regressions_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        step = next(s for s in steps
                    if s.get("run") == "python Scripts/test_publication_conflict_postconditions.py")
        step["run"] = "echo publication-integrity-check-skipped"
        self.assertIn(
            "static-conformance job missing command: python Scripts/test_publication_conflict_postconditions.py",
            scope_errors(damaged),
        )


    def test_typescript_v21_fallback_probe_required_and_active(self):
        command = ("python Scripts/checkGenXConformance.py --server "
                   "http://127.0.0.1:18083/genx/v1 --only L-06")
        for defect in ("removed", "failure-only"):
            with self.subTest(defect=defect):
                damaged = copy.deepcopy(self.workflow)
                steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
                step = next(s for s in steps if s.get("run") == command)
                if defect == "removed":
                    step["run"] = "echo skip-fallback-probe"
                else:
                    step["if"] = "failure()"
                self.assertIn(
                    "independent-runtime-differential missing command: " + command,
                    scope_errors(damaged),
                )

    def test_typescript_v21_server_startup_required(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["independent-runtime-differential"]["steps"]
        command = "bun Scripts/genx_test_server_ts.ts --port 18083 --delay 0.4 --profile v21"
        step = next(s for s in steps if command in str(s.get("run", "")))
        step["run"] = step["run"].replace(command, "echo skip-v21-server")
        self.assertTrue(any(
            "independent-runtime-differential missing command: " + command in error
            for error in scope_errors(damaged)
        ))


    def test_v21_fallback_shape_regression_required(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        step = next(s for s in steps
                    if s.get("run") == "python Scripts/test_v21_fallback_envelope.py")
        step["run"] = "echo v21-fallback-check-skipped"
        self.assertIn(
            "static-conformance job missing command: python Scripts/test_v21_fallback_envelope.py",
            scope_errors(damaged),
        )


    def test_live_assertion_manifest_guard_cannot_be_removed(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        command = "python Scripts/test_conformance_assertion_manifest.py"
        step = next(s for s in steps if s.get("run") == command)
        step["run"] = "echo ignore-bad-assertions"
        self.assertIn(
            "static-conformance job missing command: " + command,
            scope_errors(damaged),
        )


    def test_live_step_manifest_validation_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        command = "python Scripts/test_conformance_step_manifest.py"
        step = next(s for s in steps if s.get("run") == command)
        step["run"] = "echo ignore-unrecognized-body-fixtures"
        self.assertIn(
            "static-conformance job missing command: " + command,
            scope_errors(damaged),
        )


    def test_telemetry_postconflict_regressions_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        command = "python Scripts/test_telemetry_conflict_postcondition.py"
        step = next(s for s in steps if s.get("run") == command)
        step["run"] = "echo skip-telemetry-postconflict"
        self.assertIn(
            "static-conformance job missing command: " + command,
            scope_errors(damaged),
        )


    def test_provenance_roundtrip_regressions_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        command = "python Scripts/test_provenance_roundtrip_integrity.py"
        step = next(s for s in steps if s.get("run") == command)
        step["run"] = "echo skip-structural-provenance"
        self.assertIn(
            "static-conformance job missing command: " + command,
            scope_errors(damaged),
        )


    def test_collection_envelope_regression_gate_cannot_be_removed(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        command = "python Scripts/test_collection_envelope_integrity.py"
        step = next(s for s in steps if s.get("run") == command)
        step["run"] = "echo skip-paginated-collections"
        self.assertIn(
            "static-conformance job missing command: " + command,
            scope_errors(damaged),
        )


    def test_deprecated_inference_completion_regressions_cannot_be_skipped(self):
        damaged = copy.deepcopy(self.workflow)
        steps = damaged["jobs"]["static-conformance"]["steps"]
        command = "python Scripts/test_deprecated_inference_completion.py"
        step = next(s for s in steps if s.get("run") == command)
        step["run"] = "echo skip-deprecated-inference"
        self.assertIn(
            "static-conformance job missing command: " + command,
            scope_errors(damaged),
        )

if __name__ == "__main__":
    unittest.main()
