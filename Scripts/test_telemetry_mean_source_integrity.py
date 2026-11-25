#!/usr/bin/env python3
"""Mission 142: aggregated telemetry means must match stored source readings."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TelemetryMeanSourceIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-23")

    def test_registered_source_get_precedes_mean(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["telemetry_original_intact"])
        self.assertEqual(21.7, self.probe["calls"][2]["assert"]["telemetry_mean"])
        self.assertEqual(3, self.probe["calls"][2]["assert"]["telemetry_samples"])

    def exercise(self, source_change=None, mean_change=None, read_status=200,
                 source_status=200):
        calls = []
        original = []

        def response(rows):
            return {
                "result": {"data": rows},
                "metadata": {"pagination": {
                    "totalCount": len(rows), "pageSize": 1000,
                    "totalPages": 1, "currentPage": 0,
                }},
            }

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                original.extend(copy.deepcopy(body))
                return 200, {"result": {"appended": 3, "replayed": 0}}
            if len(calls) == 2:
                self.assertEqual("GET", method)
                self.assertIn("aggregation=none", path)
                rows = copy.deepcopy(original)
                if source_change is not None:
                    rows = source_change(rows)
                return source_status, response(rows)
            if len(calls) == 3:
                self.assertEqual("GET", method)
                self.assertIn("aggregation=mean", path)
                rows = [{
                    "windowStart": original[0]["timestamp"],
                    "aggregation": "mean", "value": 21.7,
                    "sampleCount": 3,
                }]
                data = response(rows)
                if mean_change is not None:
                    data = mean_change(data)
                return read_status, data
            self.fail("unexpected extra HTTP request")

        results = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, results, None, None)
        return results.failures, calls

    def test_original_mean_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_wrong_raw_source_value_fails(self):
        def change(rows):
            rows[0]["value"] = 21.7
            return rows
        self.assertEqual(1, self.exercise(source_change=change)[0])

    def test_duplicate_raw_source_identity_fails(self):
        self.assertEqual(1, self.exercise(
            source_change=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_missing_raw_source_sample_fails(self):
        self.assertEqual(1, self.exercise(
            source_change=lambda rows: rows[:2])[0])

    def test_wrong_raw_source_timestamp_fails(self):
        def change(rows):
            rows[0]["timestamp"] = "2026-09-07T08:10:00Z"
            return rows
        self.assertEqual(1, self.exercise(source_change=change)[0])

    def test_source_read_failure_fails(self):
        self.assertEqual(1, self.exercise(source_status=404)[0])

    def test_aggregate_read_failure_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_wrong_mean_fails(self):
        def change(data):
            data["result"]["data"][0]["value"] = 22.0
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_wrong_bucket_aggregation_type_fails(self):
        def change(data):
            data["result"]["data"][0]["aggregation"] = "min"
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_wrong_anchor_timestamp_fails(self):
        def change(data):
            data["result"]["data"][0]["windowStart"] = "2026-09-07T08:05:00Z"
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_wrong_sample_count_fails(self):
        def change(data):
            data["result"]["data"][0]["sampleCount"] = 2
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_boolean_sample_count_fails(self):
        def change(data):
            data["result"]["data"][0]["sampleCount"] = True
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_boolean_aggregate_value_fails(self):
        def change(data):
            data["result"]["data"][0]["value"] = True
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_missing_aggregate_bucket_fails(self):
        def change(data):
            data["result"]["data"] = []
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_extra_aggregate_bucket_fails(self):
        def change(data):
            data["result"]["data"].append(copy.deepcopy(data["result"]["data"][0]))
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_wrong_pagination_total_fails(self):
        def change(data):
            data["metadata"]["pagination"]["totalCount"] = 2
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_wrong_page_index_fails(self):
        def change(data):
            data["metadata"]["pagination"]["currentPage"] = 1
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])

    def test_missing_pagination_fails(self):
        def change(data):
            data["metadata"].pop("pagination")
            return data
        self.assertEqual(1, self.exercise(mean_change=change)[0])


if __name__ == "__main__":
    unittest.main()
