#!/usr/bin/env python3
"""Mission 118: L-26 must verify the contents of each telemetry minute bucket."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TelemetryWindowPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-26")

    def test_registered_probe_checks_actual_partition_contents(self):
        self.assertEqual(2, len(self.probe["calls"]))
        request = self.probe["calls"][1]
        self.assertEqual("GET", request["method"])
        self.assertIn("windowSeconds=60", request["path"])
        self.assertEqual(3, request["assert"]["data_length"])
        self.assertIs(True, request["assert"]["telemetry_window_partitions"])

    def exercise(self, corrupt=None, status=200):
        seen = []
        submitted = []

        def fake_http(_server, method, path, body=None, token=None):
            seen.append((method, path))
            if len(seen) == 1:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(3, len(body))
                submitted.extend(copy.deepcopy(body))
                return 200, {"result": {"appended": 3, "replayed": 0, "conflicts": []}}
            if len(seen) == 2:
                self.assertEqual("GET", method)
                self.assertIn(f"deviceDbId={submitted[0]['deviceDbId']}", path)
                self.assertIn("sensorDbId=air-temp-01", path)
                self.assertIn("windowSeconds=60", path)
                buckets = [
                    {"windowStart": point["timestamp"], "aggregation": "mean",
                     "value": point["value"], "sampleCount": 1}
                    for point in submitted
                ]
                if corrupt is not None:
                    buckets = corrupt(buckets)
                return status, {"result": {"data": buckets}}
            self.fail("unexpected extra live request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        self.assertEqual(2, len(seen))
        return outcome.failures

    def test_correct_one_sample_per_minute_passes(self):
        self.assertEqual(0, self.exercise())

    def test_wrong_sample_count_fails_despite_three_rows(self):
        def corrupt(rows):
            rows[0]["sampleCount"] = 2
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_redistributed_samples_fail_despite_three_rows(self):
        def corrupt(rows):
            rows[0]["sampleCount"] = 3
            rows[1]["sampleCount"] = 0
            rows[2]["sampleCount"] = 0
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_boolean_sample_count_fails(self):
        def corrupt(rows):
            rows[1]["sampleCount"] = True
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_wrong_mean_value_fails_despite_correct_counts(self):
        def corrupt(rows):
            rows[1]["value"] += 10
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_swapped_bucket_values_fail(self):
        def corrupt(rows):
            rows[0]["value"], rows[2]["value"] = rows[2]["value"], rows[0]["value"]
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_wrong_window_start_fails(self):
        def corrupt(rows):
            rows[1]["windowStart"] = "2026-09-07T08:01:30Z"
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_duplicate_window_start_fails(self):
        def corrupt(rows):
            rows[2]["windowStart"] = rows[1]["windowStart"]
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_unordered_but_correct_buckets_pass(self):
        self.assertEqual(0, self.exercise(lambda rows: list(reversed(rows))))

    def test_wrong_aggregation_fails(self):
        def corrupt(rows):
            rows[1]["aggregation"] = "max"
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_missing_sample_count_fails(self):
        def corrupt(rows):
            rows[0].pop("sampleCount")
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_missing_bucket_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: rows[:2]))

    def test_malformed_bucket_fails(self):
        def corrupt(rows):
            rows[1] = None
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_nonfinite_value_fails(self):
        def corrupt(rows):
            rows[0]["value"] = float("nan")
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_unsuccessful_read_fails(self):
        self.assertEqual(1, self.exercise(status=404))


if __name__ == "__main__":
    unittest.main()
