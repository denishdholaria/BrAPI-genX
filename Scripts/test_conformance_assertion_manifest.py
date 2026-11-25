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
            self.mutated("L-23", 1, lambda s: s["assert"].pop("telemetry_samples")))

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
            "telemetry_page_slice GET assertion required",
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

    def test_window_partition_assertion_must_remain_registered(self):
        self.assertIn(
            "telemetry_window_partitions GET assertion required",
            self.mutated("L-26", 1,
                         lambda s: s["assert"].pop("telemetry_window_partitions")))

    def test_window_partition_assertion_cannot_be_false(self):
        self.assertIn(
            "telemetry_window_partitions must be true",
            self.mutated("L-26", 1,
                         lambda s: s["assert"].update(telemetry_window_partitions=False)))

    def test_window_partition_assertion_typo_rejected(self):
        self.assertIn(
            "unknown live assertion",
            self.mutated("L-26", 1,
                         lambda s: s["assert"].update(telemetry_window_partition=True)))

    def test_replay_flag_needs_explicit_same_job_identity_assertion(self):
        self.assertIn("same_jobDbId assertion",
            self.mutated("L-01", 1, lambda s: s.update({"assert": {"status": 202}})))

    def test_replay_identity_assertion_without_flag_rejected(self):
        self.assertIn("same_jobDbId assertion",
            self.mutated("L-01", 1, lambda s: (
                s.pop("replay_capture"),
                s.update(body_fixture="live_submit"),
            )))

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
