#!/usr/bin/env python3
"""Mission 119: L-28 must check actual telemetry page-zero contents."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TelemetryPaginationSliceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-28")

    def test_registered_probe_checks_page_contents(self):
        self.assertEqual(2, len(self.probe["calls"]))
        request = self.probe["calls"][1]
        self.assertEqual("GET", request["method"])
        self.assertIn("page=0&pageSize=2", request["path"])
        self.assertIs(True, request["assert"]["telemetry_page_slice"])

    def exercise(self, mutate_rows=None, mutate_page=None, status=200):
        seen = []
        submitted = []

        def fake_http(_server, method, path, body=None, token=None):
            seen.append((method, path))
            if len(seen) == 1:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(3, len(body))
                submitted.extend(copy.deepcopy(body))
                return 200, {"result": {
                    "appended": 3, "replayed": 0, "conflicts": []}}
            if len(seen) == 2:
                self.assertEqual("GET", method)
                self.assertIn(f"deviceDbId={submitted[0]['deviceDbId']}", path)
                self.assertIn("page=0&pageSize=2", path)
                rows = copy.deepcopy(sorted(
                    submitted, key=lambda point: point["timestamp"])[:2])
                pagination = {"currentPage": 0, "pageSize": 2,
                              "totalCount": 3, "totalPages": 2}
                if mutate_rows is not None:
                    rows = mutate_rows(rows, submitted)
                if mutate_page is not None:
                    pagination = mutate_page(pagination)
                return status, {"result": {"data": rows}, "metadata": {
                    "pagination": pagination}}
            self.fail("unexpected extra live request")

        result = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, result, None, None)
        self.assertEqual(2, len(seen))
        return result.failures

    def test_correct_page_passes(self):
        self.assertEqual(0, self.exercise())

    def test_wrong_second_record_fails_despite_same_count(self):
        self.assertEqual(1, self.exercise(
            mutate_rows=lambda rows, source: [rows[0], copy.deepcopy(source[2])]))

    def test_reversed_page_order_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_rows=lambda rows, _: list(reversed(rows))))

    def test_duplicated_first_row_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_rows=lambda rows, _: [rows[0], copy.deepcopy(rows[0])]))

    def test_mutated_value_fails(self):
        def mutate(rows, _):
            rows[1]["value"] += 10
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=mutate))

    def test_changed_timestamp_fails(self):
        def mutate(rows, _):
            rows[0]["timestamp"] = "2026-09-07T09:00:00Z"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=mutate))

    def test_changed_sensor_fails(self):
        def mutate(rows, _):
            rows[1]["sensorDbId"] = "different-sensor"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=mutate))

    def test_missing_row_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_rows=lambda rows, _: rows[:1]))

    def test_malformed_row_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_rows=lambda rows, _: [rows[0], None]))

    def test_wrong_current_page_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "currentPage": 1}))

    def test_wrong_page_size_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "pageSize": 3}))

    def test_wrong_total_pages_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "totalPages": 1}))

    def test_wrong_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "totalCount": 4}))

    def test_boolean_pagination_value_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "currentPage": False}))

    def test_missing_pagination_key_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {k: v for k, v in p.items()
                                   if k != "totalPages"}))

    def test_failed_read_does_not_pass(self):
        self.assertEqual(1, self.exercise(status=404))


if __name__ == "__main__":
    unittest.main()
