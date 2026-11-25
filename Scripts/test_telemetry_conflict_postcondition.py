#!/usr/bin/env python3
"""L-22 must reread unchanged telemetry values after reporting a conflict."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TelemetryConflictPostconditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-22")

    def test_registered_probe_rereads_retained_values(self):
        self.assertEqual(3, len(self.probe["calls"]))
        last = self.probe["calls"][2]
        self.assertEqual("GET", last["method"])
        self.assertEqual(
            "/telemetry?deviceDbId={telemetry_device}&sensorDbId=air-temp-01&aggregation=none",
            last["path"])
        self.assertIs(True, last["assert"]["telemetry_original_intact"])

    def exercise(self, change=None, read_status=200):
        seen = []
        submitted = []

        def fake_http(_server, method, path, body=None, token=None):
            seen.append((method, path))
            if len(seen) == 1:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                submitted.extend(copy.deepcopy(body))
                return 200, {"result": {
                    "appended": 3, "replayed": 0, "conflicts": []}}
            if len(seen) == 2:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(1, len(body))
                self.assertNotEqual(submitted[2]["value"], body[0]["value"])
                return 200, {"result": {
                    "appended": 0, "replayed": 0,
                    "conflicts": ["conflicting-value"]}}
            if len(seen) == 3:
                self.assertEqual("GET", method)
                self.assertIn(f"deviceDbId={submitted[0]['deviceDbId']}", path)
                self.assertIn("sensorDbId=air-temp-01", path)
                rows = copy.deepcopy(submitted)
                if change is not None:
                    rows = change(rows)
                return read_status, {"result": {"data": rows}}
            self.fail("unexpected extra live request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe("http://example.test/genx/v1", self.probe,
                                   {"conformance_dir": str(CONF)},
                                   outcome, None, None)
        self.assertEqual(3, len(seen))
        return outcome

    def test_unchanged_readings_pass(self):
        self.assertEqual(0, self.exercise().failures)

    def test_value_mutation_despite_conflict_response_fails(self):
        def corrupt(rows):
            rows[2]["value"] += 10
            return rows
        self.assertEqual(1, self.exercise(corrupt).failures)

    def test_missing_record_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: rows[:2]).failures)

    def test_duplicated_record_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: rows + [rows[0]]).failures)

    def test_reassigned_timestamp_fails(self):
        def mutate(rows):
            rows[2]["timestamp"] = "2026-09-07T09:01:00Z"
            return rows
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_wrong_sensor_fails(self):
        def mutate(rows):
            rows[2]["sensorDbId"] = "different-sensor"
            return rows
        self.assertEqual(1, self.exercise(mutate).failures)

    def test_changed_unit_after_conflict_fails(self):
        def change(rows):
            rows[1]["unit"] = "degree_fahrenheit"
            return rows
        self.assertEqual(1, self.exercise(change).failures)

    def test_changed_quality_after_conflict_fails(self):
        def change(rows):
            rows[2]["quality"] = "good"
            return rows
        self.assertEqual(1, self.exercise(change).failures)

    def test_changed_provenance_after_conflict_fails(self):
        def change(rows):
            rows[0]["provenance"]["algorithm"] = "malicious-algorithm"
            return rows
        self.assertEqual(1, self.exercise(change).failures)

    def test_missing_original_unit_after_conflict_fails(self):
        def change(rows):
            rows[1].pop("unit")
            return rows
        self.assertEqual(1, self.exercise(change).failures)

    def test_added_server_metadata_is_allowed(self):
        def change(rows):
            rows[1]["auditSeen"] = True
            return rows
        self.assertEqual(0, self.exercise(change).failures)

    def test_missing_data_shape_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: None).failures)

    def test_unavailable_telemetry_read_fails(self):
        self.assertEqual(1, self.exercise(read_status=404).failures)


if __name__ == "__main__":
    unittest.main()
