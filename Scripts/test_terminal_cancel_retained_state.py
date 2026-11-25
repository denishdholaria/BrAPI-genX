#!/usr/bin/env python3
"""Mission 135: rejecting a terminal cancellation must preserve terminal state."""
from __future__ import annotations

from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TerminalCancelRetainedStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-03")

    def test_registered_probe_requires_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][0]["wait_terminal"])
        self.assertIs(True, self.probe["calls"][1]["assert"]["rejected"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["terminal_state_unchanged"])

    def exercise(self, baseline_status="COMPLETED", retrieved_status="COMPLETED",
                 baseline_id="JOB_TERMINAL", retrieved_id="JOB_TERMINAL",
                 delete_status=400, read_status=200, result_type="normal"):
        calls = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                return 202, {"result": {"jobDbId": "JOB_TERMINAL"}}
            if len(calls) == 2:
                self.assertEqual(("DELETE", "/jobs/JOB_TERMINAL"), (method, path))
                return delete_status, {}
            if len(calls) == 3:
                self.assertEqual(("GET", "/jobs/JOB_TERMINAL"), (method, path))
                result = {"jobDbId": retrieved_id, "status": retrieved_status}
                if result_type == "missing":
                    result = None
                if result_type == "malformed":
                    result = [result]
                return read_status, {"result": result}
            self.fail("unexpected extra network call")

        outcome = checker.Results()
        with (mock.patch.object(checker, "http_call", side_effect=fake_http),
              mock.patch.object(checker, "wait_terminal",
                                return_value={"result": {
                                    "jobDbId": baseline_id, "status": baseline_status}})):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_completed_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_failed_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise(
            baseline_status="FAILED", retrieved_status="FAILED")[0])

    def test_cancelled_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise(
            baseline_status="CANCELLED", retrieved_status="CANCELLED")[0])

    def test_expired_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise(
            baseline_status="EXPIRED", retrieved_status="EXPIRED")[0])

    def test_terminal_to_cancelled_mutation_fails(self):
        self.assertEqual(1, self.exercise(retrieved_status="CANCELLED")[0])

    def test_terminal_to_submitted_mutation_fails(self):
        self.assertEqual(1, self.exercise(retrieved_status="SUBMITTED")[0])

    def test_terminal_to_failed_mutation_fails(self):
        self.assertEqual(1, self.exercise(retrieved_status="FAILED")[0])

    def test_wrong_original_job_id_fails(self):
        self.assertEqual(1, self.exercise(baseline_id="JOB_WRONG")[0])

    def test_wrong_retrieved_job_id_fails(self):
        self.assertEqual(1, self.exercise(retrieved_id="JOB_WRONG")[0])

    def test_nonterminal_baseline_rejected(self):
        self.assertEqual(1, self.exercise(
            baseline_status="RUNNING", retrieved_status="RUNNING")[0])

    def test_missing_baseline_status_rejected(self):
        self.assertEqual(1, self.exercise(baseline_status=None)[0])

    def test_missing_retrieved_status_rejected(self):
        self.assertEqual(1, self.exercise(retrieved_status=None)[0])

    def test_missing_get_result_rejected(self):
        self.assertEqual(1, self.exercise(result_type="missing")[0])

    def test_malformed_get_result_rejected(self):
        self.assertEqual(1, self.exercise(result_type="malformed")[0])

    def test_unavailable_readback_rejected(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_successful_delete_fails_before_readback(self):
        failures, calls = self.exercise(delete_status=200)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
