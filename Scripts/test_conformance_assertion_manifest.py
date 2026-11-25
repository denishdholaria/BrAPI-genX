#!/usr/bin/env python3
"""Negative tests for silently ignored live conformance assertions."""
from __future__ import annotations

import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml
from checkGenXConformance import validate_probe_manifest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "Specification" / "BrAPI-GenX" / "Conformance" / "probes.yaml"
SCRIPT = ROOT / "Scripts" / "checkGenXConformance.py"


class LiveAssertionManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))

    def mutated(self, probe_id, call_index, change):
        probes = copy.deepcopy(self.source["probes"])
        step = next(p for p in probes if p["id"] == probe_id)["calls"][call_index]
        change(step)
        with self.assertRaises(ValueError) as caught:
            validate_probe_manifest(probes)
        return str(caught.exception)

    def test_checked_in_manifest_accepted(self):
        self.assertIsNone(validate_probe_manifest(self.source["probes"]))

    def test_unknown_assertion_does_not_pass_silently(self):
        message = self.mutated(
            "L-13", 1,
            lambda s: s["assert"].update(stauts=409),
        )
        self.assertIn("unknown live assertion(s): stauts", message)

    def test_typo_replacing_only_assertion_detected(self):
        message = self.mutated(
            "L-13", 1,
            lambda s: s.update({"assert": {"statsu": 409}}),
        )
        self.assertIn("statsu", message)

    def test_empty_assertion_mapping_rejected(self):
        self.assertIn("nonempty mapping",
            self.mutated("L-13", 1, lambda s: s.update({"assert": {}})))

    def test_scalar_assertion_rejected(self):
        self.assertIn("nonempty mapping",
            self.mutated("L-13", 1, lambda s: s.update({"assert": "status: 409"})))

    def test_false_boolean_check_rejected(self):
        self.assertIn("must be true",
            self.mutated("L-06", 0, lambda s: s["assert"].update(negotiable=False)))

    def test_string_boolean_check_rejected(self):
        self.assertIn("must be true",
            self.mutated("L-06", 0, lambda s: s["assert"].update(negotiable="true")))

    def test_status_boolean_rejected(self):
        self.assertIn("HTTP status integer",
            self.mutated("L-13", 1, lambda s: s["assert"].update(status=True)))

    def test_invalid_http_status_rejected(self):
        self.assertIn("HTTP status integer",
            self.mutated("L-13", 1, lambda s: s["assert"].update(status=700)))

    def test_bad_count_rejected(self):
        self.assertIn("nonnegative integer",
            self.mutated("L-28", 1, lambda s: s["assert"].update(data_length=-1)))

    def test_bad_body_mapping_rejected(self):
        self.assertIn("nonempty path mapping",
            self.mutated("L-05", 0, lambda s: s["assert"].update(body=[])))

    def test_telemetry_counts_missing_replayed_rejected(self):
        self.assertIn("appended and replayed",
            self.mutated("L-21", 0, lambda s: s["assert"].update(
                telemetry_counts={"appended": 3})))

    def test_telemetry_mean_without_samples_rejected(self):
        self.assertIn("must be paired",
            self.mutated("L-23", 2, lambda s: s["assert"].pop("telemetry_samples")))

    def test_provenance_roundtrip_assertion_required(self):
        self.assertIn(
            "original observation and provenance round-trip required",
            self.mutated("L-07", 1,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_provenance_roundtrip_get_identity_required(self):
        self.assertIn(
            "original observation and provenance round-trip required",
            self.mutated("L-07", 1,
                         lambda s: s.update(path="/jobs/JOB_UNRELATED")))

    def test_provenance_roundtrip_post_fixture_required(self):
        self.assertIn(
            "original observation and provenance round-trip required",
            self.mutated("L-07", 0,
                         lambda s: s.update(body_fixture="live_submit")))

    def test_provenance_roundtrip_job_capture_required(self):
        self.assertIn(
            "wait_terminal requires capture_job",
            self.mutated("L-07", 0,
                         lambda s: s.pop("capture_job")))

    def test_provenance_roundtrip_terminal_wait_required(self):
        self.assertIn(
            "original observation and provenance round-trip required",
            self.mutated("L-07", 0,
                         lambda s: s.pop("wait_terminal")))

    def test_provenance_roundtrip_false_flag_rejected(self):
        self.assertIn(
            "must be true",
            self.mutated("L-07", 1,
                         lambda s: s["assert"].update(provenance_intact=False)))

    def test_clean_telemetry_first_append_no_conflict_required(self):
        self.assertIn(
            "clean append and replay conflict arrays required",
            self.mutated("L-21", 0,
                         lambda s: s["assert"].pop("telemetry_no_conflicts")))

    def test_clean_telemetry_replay_no_conflict_required(self):
        self.assertIn(
            "clean append and replay conflict arrays required",
            self.mutated("L-21", 1,
                         lambda s: s["assert"].pop("telemetry_no_conflicts")))

    def test_clean_telemetry_replay_assertion_cannot_be_false(self):
        self.assertIn(
            "telemetry_no_conflicts must be true",
            self.mutated("L-21", 1,
                         lambda s: s["assert"].update(telemetry_no_conflicts=False)))

    def test_clean_telemetry_replay_must_use_original_batch(self):
        self.assertIn(
            "clean append and replay conflict arrays required",
            self.mutated("L-21", 1,
                         lambda s: s.update(body_fixture="live_telemetry_conflict")))

    def test_clean_telemetry_initial_counts_cannot_change(self):
        self.assertIn(
            "clean append and replay conflict arrays required",
            self.mutated("L-21", 0,
                         lambda s: s["assert"].update(
                             telemetry_counts={"appended": 2, "replayed": 1})))

    def test_telemetry_replay_readback_cannot_be_removed(self):
        self.assertIn(
            "telemetry_original_intact GET assertion required",
            self.mutated("L-21", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_telemetry_replay_readback_cannot_be_disabled(self):
        self.assertIn(
            "telemetry_original_intact must be true",
            self.mutated("L-21", 2,
                         lambda s: s["assert"].update(telemetry_original_intact=False)))

    def test_telemetry_page_slice_assertion_must_remain_registered(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 1,
                         lambda s: s["assert"].pop("telemetry_page_slice")))

    def test_telemetry_page_slice_assertion_cannot_be_false(self):
        self.assertIn(
            "telemetry_page_slice must be true",
            self.mutated("L-28", 1,
                         lambda s: s["assert"].update(telemetry_page_slice=False)))

    def test_telemetry_page_slice_assertion_typo_rejected(self):
        self.assertIn(
            "unknown live assertion",
            self.mutated("L-28", 1,
                         lambda s: s["assert"].update(telemetry_page_slices=True)))

    def test_telemetry_tail_page_cannot_be_removed(self):
        probes = copy.deepcopy(self.source["probes"])
        probe = next(p for p in probes if p["id"] == "L-28")
        probe["calls"].pop(2)
        with self.assertRaisesRegex(ValueError,
                "two-page telemetry slice and source integrity required"):
            validate_probe_manifest(probes)

    def test_telemetry_tail_path_must_request_page_one(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 2,
                         lambda s: s.update(
                             path="/telemetry?deviceDbId={telemetry_device}&page=0&pageSize=2")))

    def test_telemetry_tail_assertion_cannot_be_removed(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 2,
                         lambda s: s["assert"].pop("telemetry_page_slice")))

    def test_telemetry_tail_count_cannot_be_weakened(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 2,
                         lambda s: s["assert"].update(data_length=2)))

    def test_telemetry_initial_source_capture_required(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 0,
                         lambda s: s.pop("capture_telemetry")))

    def test_telemetry_first_page_query_cannot_be_changed(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 1,
                         lambda s: s.update(
                             path="/telemetry?deviceDbId={telemetry_device}&page=1&pageSize=2")))

    def test_window_partition_assertion_must_remain_registered(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 2,
                         lambda s: s["assert"].pop("telemetry_window_partitions")))

    def test_window_partition_assertion_cannot_be_false(self):
        self.assertIn(
            "telemetry_window_partitions must be true",
            self.mutated("L-26", 2,
                         lambda s: s["assert"].update(telemetry_window_partitions=False)))

    def test_window_partition_assertion_typo_rejected(self):
        self.assertIn(
            "unknown live assertion",
            self.mutated("L-26", 2,
                         lambda s: s["assert"].update(telemetry_window_partition=True)))

    def test_window_original_readback_cannot_be_removed(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 1,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_window_original_source_path_cannot_change(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 1,
                         lambda s: s.update(path="/telemetry")))

    def test_window_original_capture_is_required(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 0, lambda s: s.pop("capture_telemetry")))

    def test_window_original_must_precede_mean_get(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 1,
                         lambda s: s.update(path="/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&aggregation=mean&windowSeconds=60")))

    def test_window_mean_query_must_remain_registered(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 2,
                         lambda s: s.update(
                             path="/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&aggregation=none")))

    def test_L_08_publication_replay_202_rejected(self):
        self.assertIn(
            "term_replay_single_version GET after replay required",
            self.mutated("L-08", 1,
                         lambda call: call["assert"].update(status=202)))

    def test_L_08_publication_replay_status_mandatory(self):
        self.assertIn(
            "term_replay_single_version GET after replay required",
            self.mutated("L-08", 1,
                         lambda call: call["assert"].pop("status")))

    def test_L_10_publication_replay_202_rejected(self):
        self.assertIn(
            "ledger_original_intact GET after replay required",
            self.mutated("L-10", 1,
                         lambda call: call["assert"].update(status=202)))

    def test_L_10_publication_replay_status_mandatory(self):
        self.assertIn(
            "ledger_original_intact GET after replay required",
            self.mutated("L-10", 1,
                         lambda call: call["assert"].pop("status")))

    def test_L_12_publication_replay_202_rejected(self):
        self.assertIn(
            "model_replay_single_version GET after replay required",
            self.mutated("L-12", 1,
                         lambda call: call["assert"].update(status=202)))

    def test_L_12_publication_replay_status_mandatory(self):
        self.assertIn(
            "model_replay_single_version GET after replay required",
            self.mutated("L-12", 1,
                         lambda call: call["assert"].pop("status")))

    def test_L_16_publication_replay_202_rejected(self):
        self.assertIn(
            "matrix_replay_single_record GET after replay required",
            self.mutated("L-16", 1,
                         lambda call: call["assert"].update(status=202)))

    def test_L_16_publication_replay_status_mandatory(self):
        self.assertIn(
            "matrix_replay_single_record GET after replay required",
            self.mutated("L-16", 1,
                         lambda call: call["assert"].pop("status")))

    def test_L_18_publication_replay_202_rejected(self):
        self.assertIn(
            "package_replay_single_record GET after replay required",
            self.mutated("L-18", 1,
                         lambda call: call["assert"].update(status=202)))

    def test_L_18_publication_replay_status_mandatory(self):
        self.assertIn(
            "package_replay_single_record GET after replay required",
            self.mutated("L-18", 1,
                         lambda call: call["assert"].pop("status")))

    def test_replay_flag_needs_explicit_same_job_identity_assertion(self):
        self.assertIn("same_jobDbId assertion",
            self.mutated("L-01", 1, lambda s: s.update({"assert": {"status": 202}})))

    def test_replay_identity_assertion_without_flag_rejected(self):
        self.assertIn("same_jobDbId assertion",
            self.mutated("L-01", 1, lambda s: (
                s.pop("replay_capture"),
                s.update(body_fixture="live_submit"),
            )))

    def test_telemetry_conflict_original_append_counts_required(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 0, lambda step: step.update(
                {"assert": {"telemetry_no_conflicts": True}})))

    def test_telemetry_conflict_original_clean_state_required(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 0, lambda step: step["assert"].pop(
                "telemetry_no_conflicts")))

    def test_telemetry_conflict_original_counts_exact(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 0, lambda step: step["assert"].update(
                telemetry_counts={"appended": 2, "replayed": 1})))

    def test_telemetry_conflict_original_batch_required(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 0, lambda step: step.update(
                body_fixture="live_telemetry_conflict")))

    def test_L_23_initial_append_counters_mandatory(self):
        self.assertIn(
            "source telemetry GET and mean recomputation required",
            self.mutated("L-23", 0,
                         lambda step: step["assert"].pop("telemetry_counts")))

    def test_L_23_initial_clean_conflicts_mandatory(self):
        self.assertIn(
            "source telemetry GET and mean recomputation required",
            self.mutated("L-23", 0,
                         lambda step: step["assert"].pop("telemetry_no_conflicts")))

    def test_L_23_initial_incorrect_count_rejected(self):
        self.assertIn(
            "source telemetry GET and mean recomputation required",
            self.mutated("L-23", 0,
                         lambda step: step["assert"].update(
                             telemetry_counts={"appended": 2, "replayed": 1})))


    def test_L_26_initial_append_counters_mandatory(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 0,
                         lambda step: step["assert"].pop("telemetry_counts")))

    def test_L_26_initial_clean_conflicts_mandatory(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 0,
                         lambda step: step["assert"].pop("telemetry_no_conflicts")))

    def test_L_26_initial_incorrect_count_rejected(self):
        self.assertIn(
            "original telemetry source before window aggregation required",
            self.mutated("L-26", 0,
                         lambda step: step["assert"].update(
                             telemetry_counts={"appended": 2, "replayed": 1})))


    def test_L_28_initial_append_counters_mandatory(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 0,
                         lambda step: step["assert"].pop("telemetry_counts")))

    def test_L_28_initial_clean_conflicts_mandatory(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 0,
                         lambda step: step["assert"].pop("telemetry_no_conflicts")))

    def test_L_28_initial_incorrect_count_rejected(self):
        self.assertIn(
            "two-page telemetry slice and source integrity required",
            self.mutated("L-28", 0,
                         lambda step: step["assert"].update(
                             telemetry_counts={"appended": 2, "replayed": 1})))

    def test_telemetry_conflict_identity_assertion_cannot_be_removed(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 1,
                         lambda s: s.update({"assert": {
                             "telemetry_counts": {"appended": 0, "replayed": 0}}})))

    def test_telemetry_conflict_must_use_conflict_fixture(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 1,
                         lambda s: s.update(body_fixture="live_telemetry_batch")))

    def test_telemetry_conflict_readback_required(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_telemetry_conflict_must_capture_original(self):
        self.assertIn(
            "rejected telemetry natural key and retained source required",
            self.mutated("L-22", 0, lambda s: s.pop("capture_telemetry")))

    def test_telemetry_mean_source_readback_cannot_be_removed(self):
        self.assertIn(
            "source telemetry GET and mean recomputation required",
            self.mutated("L-23", 1,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_telemetry_mean_source_query_cannot_change(self):
        self.assertIn(
            "source telemetry GET and mean recomputation required",
            self.mutated("L-23", 1,
                         lambda s: s.update(path="/telemetry")))

    def test_telemetry_mean_calculation_cannot_be_removed(self):
        self.assertIn(
            "source telemetry GET and mean recomputation required",
            self.mutated("L-23", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_telemetry_mean_source_capture_required(self):
        self.assertIn(
            "source telemetry GET and mean recomputation required",
            self.mutated("L-23", 0, lambda s: s.pop("capture_telemetry")))

    def test_inference_complete_result_assertion_cannot_be_removed(self):
        self.assertIn(
            "bound inference result and completion GET required",
            self.mutated("L-14", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_inference_original_model_capture_is_required(self):
        self.assertIn(
            "bound inference result and completion GET required",
            self.mutated("L-14", 0, lambda s: s.pop("capture_model")))

    def test_inference_terminal_wait_is_required(self):
        self.assertIn(
            "bound inference result and completion GET required",
            self.mutated("L-14", 1, lambda s: s.pop("wait_terminal")))

    def test_inference_get_must_use_captured_job_identity(self):
        self.assertIn(
            "bound inference result and completion GET required",
            self.mutated("L-14", 2, lambda s: s.update(path="/jobs/JOB_OTHER")))

    def test_deprecated_completion_assertion_cannot_be_removed(self):
        self.assertIn(
            "bound deprecated inference completion and warning required",
            self.mutated("L-27", 2,
                         lambda s: s.update({"assert": {
                             "status": 202, "status_message": "WARNING"}})))

    def test_deprecated_warning_cannot_be_removed(self):
        self.assertIn(
            "bound deprecated inference completion and warning required",
            self.mutated("L-27", 2,
                         lambda s: s["assert"].pop("status_message")))

    def test_deprecated_model_original_capture_required(self):
        self.assertIn(
            "bound deprecated inference completion and warning required",
            self.mutated("L-27", 0,
                         lambda s: s.pop("capture_model_deprecated")))

    def test_deprecated_inference_fixture_required(self):
        self.assertIn(
            "bound deprecated inference completion and warning required",
            self.mutated("L-27", 2,
                         lambda s: s.update(body_fixture="live_inference_submit")))

    def test_deprecated_model_stored_readback_cannot_be_removed(self):
        self.assertIn(
            "deprecated_model_persisted GET before inference required",
            self.mutated("L-27", 1,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_deprecated_model_stored_readback_cannot_be_disabled(self):
        self.assertIn(
            "deprecated_model_persisted must be true",
            self.mutated("L-27", 1,
                         lambda s: s["assert"].update(
                             deprecated_model_persisted=False)))

    def test_deprecated_model_stored_readback_requires_versioned_path(self):
        self.assertIn(
            "deprecated_model_persisted GET before inference required",
            self.mutated("L-27", 1,
                         lambda s: s.update(path="/models/OTHER")))

    def test_collection_job_readback_cannot_be_removed(self):
        self.assertIn(
            "paged job and model collection evidence required",
            self.mutated("L-25", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_collection_model_readback_cannot_be_removed(self):
        self.assertIn(
            "paged job and model collection evidence required",
            self.mutated("L-25", 3,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_collection_model_must_be_created(self):
        self.assertIn(
            "paged job and model collection evidence required",
            self.mutated("L-25", 1,
                         lambda s: s.update(body_fixture="live_model_conflict")))

    def test_collection_job_must_be_created(self):
        self.assertIn(
            "paged job and model collection evidence required",
            self.mutated("L-25", 0,
                         lambda s: s.pop("capture_job")))

    def test_collection_must_not_swap_endpoints(self):
        self.assertIn(
            "paged job and model collection evidence required",
            self.mutated("L-25", 2, lambda s: s.update(path="/models")))

    def test_embargo_denial_postcondition_cannot_be_removed(self):
        self.assertIn(
            "embargo_denial_no_payload on rejected package GET required",
            self.mutated("L-20", 1,
                         lambda s: s.update({"assert": {"status": 403}})))

    def test_embargo_denial_postcondition_cannot_be_disabled(self):
        self.assertIn(
            "embargo_denial_no_payload must be true",
            self.mutated("L-20", 1,
                         lambda s: s["assert"].update(embargo_denial_no_payload=False)))

    def test_embargo_denial_requires_package_get(self):
        self.assertIn(
            "embargo_denial_no_payload requires embargoed package GET",
            self.mutated("L-20", 1, lambda s: s.update(path="/fair-packages")))

    def test_embargo_denial_requires_embargoed_submission(self):
        self.assertIn(
            "embargo_denial_no_payload on rejected package GET required",
            self.mutated("L-20", 0,
                         lambda s: s.update(body_fixture="live_package_submit")))

    def test_embargo_denial_requires_403(self):
        self.assertIn(
            "embargo_denial_no_payload on rejected package GET required",
            self.mutated("L-20", 1,
                         lambda s: s["assert"].update(status=200)))

    def test_expired_job_result_withheld_cannot_be_removed(self):
        self.assertIn(
            "expired_result_withheld on known-expired job required",
            self.mutated("L-05", 0,
                         lambda s: s.update({"assert": {"body": {
                             "result.status": "EXPIRED"}}})))

    def test_expired_job_result_withheld_cannot_be_disabled(self):
        self.assertIn(
            "expired_result_withheld must be true",
            self.mutated("L-05", 0,
                         lambda s: s["assert"].update(expired_result_withheld=False)))

    def test_expired_job_requires_expired_job_get(self):
        self.assertIn(
            "expired_result_withheld requires known-expired job GET",
            self.mutated("L-05", 0,
                         lambda s: s.update(path="/jobs/JOB_OTHER")))

    def test_expired_job_must_report_expired_status(self):
        self.assertIn(
            "expired_result_withheld on known-expired job required",
            self.mutated("L-05", 0,
                         lambda s: s["assert"]["body"].update(
                             {"result.status": "COMPLETED"})))

    def test_unknown_job_type_readback_is_required(self):
        self.assertIn(
            "unknown_job_type_not_stored GET after rejection required",
            self.mutated("L-04", 1,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_unknown_job_type_readback_cannot_be_disabled(self):
        self.assertIn(
            "unknown_job_type_not_stored must be true",
            self.mutated("L-04", 1,
                         lambda s: s["assert"].update(unknown_job_type_not_stored=False)))

    def test_unknown_job_type_readback_must_get_collection(self):
        self.assertIn(
            "unknown_job_type_not_stored requires GET /jobs",
            self.mutated("L-04", 1,
                         lambda s: s.update(path="/jobs/OTHER")))

    def test_unknown_job_type_request_must_be_preserved(self):
        self.assertIn(
            "unknown_job_type_not_stored GET after rejection required",
            self.mutated("L-04", 0,
                         lambda s: s.update(body_fixture="live_submit")))

    def test_unknown_job_type_rejection_status_must_remain_400(self):
        self.assertIn(
            "unknown_job_type_not_stored GET after rejection required",
            self.mutated("L-04", 0,
                         lambda s: s["assert"].update(status=202)))

    def test_terminal_cancel_readback_is_required(self):
        self.assertIn(
            "terminal_state_unchanged GET after rejected cancellation required",
            self.mutated("L-03", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_terminal_cancel_readback_cannot_be_disabled(self):
        self.assertIn(
            "terminal_state_unchanged must be true",
            self.mutated("L-03", 2,
                         lambda s: s["assert"].update(terminal_state_unchanged=False)))

    def test_terminal_cancel_requires_captured_job_get(self):
        self.assertIn(
            "terminal_state_unchanged requires captured job GET",
            self.mutated("L-03", 2, lambda s: s.update(path="/jobs")))

    def test_terminal_cancel_requires_terminal_wait(self):
        self.assertIn(
            "terminal_state_unchanged GET after rejected cancellation required",
            self.mutated("L-03", 0, lambda s: s.pop("wait_terminal")))

    def test_terminal_cancel_requires_rejected_delete(self):
        self.assertIn(
            "terminal_state_unchanged GET after rejected cancellation required",
            self.mutated("L-03", 1,
                         lambda s: s.update({"assert": {"status": 400}})))

    def test_job_conflict_initial_collection_is_required(self):
        self.assertIn(
            "complete job collection before and after conflict required",
            self.mutated("L-02", 1,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_job_conflict_final_collection_is_required(self):
        self.assertIn(
            "complete job collection before and after conflict required",
            self.mutated("L-02", 3,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_job_conflict_capture_cannot_be_disabled(self):
        self.assertIn(
            "capture_job_collection must be true",
            self.mutated("L-02", 1,
                         lambda s: s["assert"].update(capture_job_collection=False)))

    def test_job_conflict_readback_cannot_be_disabled(self):
        self.assertIn(
            "job_conflict_collection_unchanged must be true",
            self.mutated("L-02", 3,
                         lambda s: s["assert"].update(job_conflict_collection_unchanged=False)))

    def test_job_conflict_requires_complete_collection_route(self):
        self.assertIn(
            "job conflict collection assertions require GET /jobs",
            self.mutated("L-02", 3,
                         lambda s: s.update(path="/jobs/OTHER")))

    def test_job_conflict_requires_rejected_write(self):
        self.assertIn(
            "complete job collection before and after conflict required",
            self.mutated("L-02", 2,
                         lambda s: s.update({"assert": {"status": 409}})))

    def test_job_replay_stored_readback_cannot_be_removed(self):
        self.assertIn(
            "job_replay_single_stored GET after replay required",
            self.mutated("L-01", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_job_replay_stored_readback_cannot_be_disabled(self):
        self.assertIn(
            "job_replay_single_stored must be true",
            self.mutated("L-01", 2,
                         lambda s: s["assert"].update(job_replay_single_stored=False)))

    def test_job_replay_stored_readback_requires_collection(self):
        self.assertIn(
            "job_replay_single_stored requires GET /jobs",
            self.mutated("L-01", 2,
                         lambda s: s.update(path="/jobs/JOB-OTHER")))

    def test_job_replay_must_replay_original_capture(self):
        self.assertIn(
            "job_replay_single_stored GET after replay required",
            self.mutated("L-01", 1,
                         lambda s: (
                             s.pop("replay_capture"),
                             s.update({"assert": {"status": 200},
                                       "body_fixture": "live_submit"}),
                         )))

    def test_job_replay_stored_readback_must_capture_initial_job(self):
        self.assertIn(
            "job_replay_single_stored GET after replay required",
            self.mutated("L-01", 0, lambda s: s.pop("capture_job")))

    def test_rejected_inference_stored_job_readback_cannot_be_removed(self):
        self.assertIn(
            "rejected_inference_not_stored GET after both rejections required",
            self.mutated("L-15", 4,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_rejected_inference_readback_cannot_be_disabled(self):
        self.assertIn(
            "rejected_inference_not_stored must be true",
            self.mutated("L-15", 4,
                         lambda s: s["assert"].update(
                             rejected_inference_not_stored=False)))

    def test_rejected_inference_readback_requires_job_collection(self):
        self.assertIn(
            "rejected_inference_not_stored requires GET /jobs",
            self.mutated("L-15", 4,
                         lambda s: s.update(path="/jobs/OTHER")))

    def test_rejected_inference_requires_original_unknown_submission(self):
        self.assertIn(
            "rejected_inference_not_stored GET after both rejections required",
            self.mutated("L-15", 0,
                         lambda s: s.update(body_fixture="live_inference_submit")))

    def test_rejected_inference_requires_revoked_submission(self):
        self.assertIn(
            "rejected_inference_not_stored GET after both rejections required",
            self.mutated("L-15", 3,
                         lambda s: s.update(body_fixture="live_inference_unknown")))

    def test_revoked_model_readback_cannot_be_removed(self):
        self.assertIn(
            "revoked_model_persisted GET before rejected inference required",
            self.mutated("L-15", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_revoked_model_readback_cannot_be_disabled(self):
        self.assertIn(
            "revoked_model_persisted must be true",
            self.mutated("L-15", 2,
                         lambda s: s["assert"].update(
                             revoked_model_persisted=False)))

    def test_revoked_model_readback_requires_versioned_path(self):
        self.assertIn(
            "revoked_model_persisted GET before rejected inference required",
            self.mutated("L-15", 2,
                         lambda s: s.update(path="/models/OTHER")))

    def test_model_conflict_readback_cannot_be_removed(self):
        self.assertIn(
            "full model original readback after conflict required",
            self.mutated("L-13", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_model_conflict_requires_conflicting_request(self):
        self.assertIn(
            "full model original readback after conflict required",
            self.mutated("L-13", 1,
                         lambda s: s.update(body_fixture="live_model_submit")))

    def test_model_conflict_requires_original_capture(self):
        self.assertIn(
            "full model original readback after conflict required",
            self.mutated("L-13", 0,
                         lambda s: s.pop("capture_model")))

    def test_model_conflict_readback_cannot_be_disabled(self):
        self.assertIn(
            "unchanged_model_digest must be true",
            self.mutated("L-13", 2,
                         lambda s: s["assert"].update(unchanged_model_digest=False)))

    def test_model_conflict_cannot_accept_200_response(self):
        self.assertIn(
            "full model original readback after conflict required",
            self.mutated("L-13", 1,
                         lambda s: s["assert"].update(status=200)))

    def test_package_conflict_readback_cannot_be_removed(self):
        self.assertIn(
            "full package original readback after conflict required",
            self.mutated("L-19", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_package_conflict_requires_conflicting_request(self):
        self.assertIn(
            "full package original readback after conflict required",
            self.mutated("L-19", 1,
                         lambda s: s.update(body_fixture="live_package_submit")))

    def test_package_conflict_readback_cannot_be_disabled(self):
        self.assertIn(
            "unchanged_package_license must be true",
            self.mutated("L-19", 2,
                         lambda s: s["assert"].update(unchanged_package_license=False)))

    def test_matrix_conflict_readback_cannot_be_removed(self):
        self.assertIn(
            "full matrix original readback after conflict required",
            self.mutated("L-17", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_matrix_conflict_requires_original_request(self):
        self.assertIn(
            "full matrix original readback after conflict required",
            self.mutated("L-17", 1, lambda s: s.update(
                body_fixture="live_matrix_submit")))

    def test_matrix_conflict_readback_cannot_be_disabled(self):
        self.assertIn(
            "unchanged_matrix_digest must be true",
            self.mutated("L-17", 2,
                         lambda s: s["assert"].update(unchanged_matrix_digest=False)))

    def test_model_replay_readback_cannot_be_removed(self):
        self.assertIn(
            "model_replay_single_version GET after replay required",
            self.mutated("L-12", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_model_replay_readback_cannot_be_disabled(self):
        self.assertIn(
            "model_replay_single_version must be true",
            self.mutated("L-12", 2,
                         lambda s: s["assert"].update(model_replay_single_version=False)))

    def test_model_replay_requires_filtered_collection(self):
        self.assertIn(
            "requires filtered model collection GET",
            self.mutated("L-12", 2,
                         lambda s: s.update(path="/models")))

    def test_model_replay_must_use_identical_submission(self):
        self.assertIn(
            "model_replay_single_version GET after replay required",
            self.mutated("L-12", 1,
                         lambda s: s.update(body_fixture="live_model_conflict")))

    def test_package_replay_readback_cannot_be_removed(self):
        self.assertIn(
            "package_replay_single_record GET after replay required",
            self.mutated("L-18", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_package_replay_readback_cannot_be_disabled(self):
        self.assertIn(
            "package_replay_single_record must be true",
            self.mutated("L-18", 2,
                         lambda s: s["assert"].update(package_replay_single_record=False)))

    def test_package_replay_readback_requires_collection_get(self):
        self.assertIn(
            "package_replay_single_record requires GET /fair-packages",
            self.mutated("L-18", 2,
                         lambda s: s.update(path="/fair-packages/OTHER")))

    def test_package_replay_must_use_identical_submission(self):
        self.assertIn(
            "package_replay_single_record GET after replay required",
            self.mutated("L-18", 1,
                         lambda s: s.update(body_fixture="live_package_conflict")))

    def test_matrix_replay_readback_cannot_be_removed(self):
        self.assertIn(
            "matrix_replay_single_record GET after replay required",
            self.mutated("L-16", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_matrix_replay_readback_cannot_be_disabled(self):
        self.assertIn(
            "matrix_replay_single_record must be true",
            self.mutated("L-16", 2,
                         lambda s: s["assert"].update(matrix_replay_single_record=False)))

    def test_matrix_replay_readback_requires_collection_get(self):
        self.assertIn(
            "matrix_replay_single_record requires GET /variantmatrices",
            self.mutated("L-16", 2,
                         lambda s: s.update(path="/variantmatrices/OTHER")))

    def test_matrix_replay_must_use_identical_submission(self):
        self.assertIn(
            "matrix_replay_single_record GET after replay required",
            self.mutated("L-16", 1,
                         lambda s: s.update(body_fixture="live_matrix_conflict")))

    def test_term_replay_readback_cannot_be_removed(self):
        self.assertIn(
            "term_replay_single_version GET after replay required",
            self.mutated("L-08", 2, lambda s: s.update(
                {"assert": {"status": 200}})))

    def test_term_replay_readback_cannot_be_disabled(self):
        self.assertIn(
            "term_replay_single_version must be true",
            self.mutated("L-08", 2, lambda s: s["assert"].update(
                term_replay_single_version=False)))

    def test_term_replay_requires_filtered_get(self):
        self.assertIn(
            "requires filtered term collection GET",
            self.mutated("L-08", 2, lambda s: s.update(path="/variable-terms")))

    def test_ledger_replay_readback_cannot_be_removed(self):
        self.assertIn(
            "ledger_original_intact GET after replay required",
            self.mutated("L-10", 2, lambda s: s.update(
                {"assert": {"ledger_count": 1}})))

    def test_ledger_replay_readback_cannot_be_disabled(self):
        self.assertIn(
            "ledger_original_intact must be true",
            self.mutated("L-10", 2, lambda s: s["assert"].update(
                ledger_original_intact=False)))

    def test_ledger_replay_requires_same_identity_reply(self):
        self.assertIn(
            "ledger_original_intact GET after replay required",
            self.mutated("L-10", 1,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_ledger_conflict_readback_cannot_be_removed(self):
        self.assertIn(
            "ledger_original_intact GET after conflict required",
            self.mutated("L-11", 2, lambda s: s.update(
                {"assert": {"ledger_count": 1}})))

    def test_ledger_conflict_readback_cannot_be_disabled(self):
        self.assertIn(
            "ledger_original_intact must be true",
            self.mutated("L-11", 2, lambda s: s["assert"].update(
                ledger_original_intact=False)))

    def test_ledger_conflict_readback_requires_lot_get(self):
        self.assertIn(
            "requires GET on captured seed lot",
            self.mutated("L-11", 2, lambda s: s.update(path="/seedlots/OTHER/ledger")))

    def test_variable_term_conflict_readback_cannot_be_removed(self):
        self.assertIn(
            "unchanged_term_record GET after conflict required",
            self.mutated("L-09", 2,
                         lambda s: s.update({"assert": {"status": 200}})))

    def test_variable_term_conflict_readback_cannot_be_disabled(self):
        self.assertIn(
            "unchanged_term_record must be true",
            self.mutated("L-09", 2,
                         lambda s: s["assert"].update(unchanged_term_record=False)))

    def test_variable_term_conflict_requires_versioned_get(self):
        self.assertIn(
            "requires versioned term GET",
            self.mutated("L-09", 2,
                         lambda s: s.update(path="/variable-terms")))

    def test_concurrent_stored_job_readback_must_remain(self):
        self.assertIn(
            "concurrent_single_stored_job GET assertion required",
            self.mutated("L-24", 1, lambda s: s.update(
                {"assert": {"status": 200}})))

    def test_concurrent_readback_must_be_get_jobs(self):
        self.assertIn(
            "requires GET /jobs",
            self.mutated("L-24", 1,
                         lambda s: s.update(path="/jobs/unrelated")))

    def test_concurrent_readback_boolean_cannot_be_false(self):
        self.assertIn(
            "concurrent_single_stored_job must be true",
            self.mutated("L-24", 1,
                         lambda s: s["assert"].update(
                             concurrent_single_stored_job=False)))

    def test_concurrent_count_must_remain_eight(self):
        self.assertIn(
            "eight concurrent submissions required",
            self.mutated("L-24", 0, lambda s: s.update(
                concurrent_posts=7)))

    def test_concurrent_submissions_require_single_effect(self):
        self.assertIn("single_effect assertion",
            self.mutated("L-24", 0, lambda s: s.update({"assert": {"status": 202}})))

    def test_concurrent_count_must_be_integer(self):
        self.assertIn("concurrent_posts must be >= 2",
            self.mutated("L-24", 0, lambda s: s.update(concurrent_posts=True)))

    def test_cli_rejects_mutated_manifest_before_contacting_server(self):
        bad = copy.deepcopy(self.source)
        next(p for p in bad["probes"] if p["id"] == "L-13")["calls"][1]["assert"] = {
            "stauts": 409,
        }
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / "Specification" / "BrAPI-GenX" / "Conformance"
            dest.mkdir(parents=True)
            (dest / "probes.yaml").write_text(
                yaml.safe_dump(bad, sort_keys=False), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", folder,
                 "--only", "L-13", "--server", "http://127.0.0.1:1/genx/v1"],
                cwd=ROOT, capture_output=True, text=True, timeout=30,
                check=False,
            )
        self.assertNotEqual(0, proc.returncode)
        self.assertIn("unknown live assertion(s): stauts", proc.stderr)


if __name__ == "__main__":
    unittest.main()
