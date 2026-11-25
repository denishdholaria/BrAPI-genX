#!/usr/bin/env python3
"""Mission 137: expired job status must not leak the result payload."""
from __future__ import annotations

from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class ExpiredJobResultWithheldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-05")

    def test_registered_probe_verifies_result_absent(self):
        self.assertEqual(1, len(self.probe["calls"]))
        self.assertEqual("/jobs/{expiredJobDbId}", self.probe["calls"][0]["path"])
        self.assertIs(True, self.probe["calls"][0]["assert"]["expired_result_withheld"])

    def exercise(self, job_status="EXPIRED", job_id="JOB_EXPIRED",
                 result_marker="absent", http_status=200, payload_shape="normal"):
        observed = []

        def fake_http(_server, method, path, body=None, token=None):
            observed.append((method, path))
            self.assertEqual(("GET", "/jobs/JOB_EXPIRED"), (method, path))
            job = {"jobDbId": job_id, "status": job_status}
            if result_marker != "absent":
                job["result"] = result_marker
            if payload_shape == "null":
                job = None
            if payload_shape == "list":
                job = [job]
            return http_status, {"result": job}

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, "JOB_EXPIRED")
        return outcome.failures, observed

    def test_expired_job_without_result_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_expired_job_with_null_result_passes(self):
        self.assertEqual(0, self.exercise(result_marker=None)[0])

    def test_expired_job_with_result_data_fails(self):
        self.assertEqual(1, self.exercise(result_marker={"data": [42]})[0])

    def test_expired_job_with_empty_result_object_fails(self):
        self.assertEqual(1, self.exercise(result_marker={})[0])

    def test_expired_job_with_empty_result_list_fails(self):
        self.assertEqual(1, self.exercise(result_marker=[])[0])

    def test_expired_job_with_scalar_result_fails(self):
        self.assertEqual(1, self.exercise(result_marker="secret") [0])

    def test_completed_job_response_fails(self):
        self.assertEqual(1, self.exercise(job_status="COMPLETED")[0])

    def test_missing_status_fails(self):
        self.assertEqual(1, self.exercise(job_status=None)[0])

    def test_wrong_expired_job_identity_fails(self):
        self.assertEqual(1, self.exercise(job_id="JOB_OTHER")[0])

    def test_missing_expired_job_identity_fails(self):
        self.assertEqual(1, self.exercise(job_id=None)[0])

    def test_unavailable_expired_job_fails(self):
        self.assertEqual(1, self.exercise(http_status=404)[0])

    def test_null_response_record_fails(self):
        self.assertEqual(1, self.exercise(payload_shape="null")[0])

    def test_malformed_response_record_fails(self):
        self.assertEqual(1, self.exercise(payload_shape="list")[0])


if __name__ == "__main__":
    unittest.main()
