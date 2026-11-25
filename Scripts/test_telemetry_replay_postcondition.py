#!/usr/bin/env python3
"""Mission 120: correct telemetry replay counters must imply retained records."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TelemetryReplayPostconditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-21")

    def test_registered_probe_rereads_replayed_records(self):
        self.assertEqual(3, len(self.probe["calls"]))
        final = self.probe["calls"][2]
        self.assertEqual("GET", final["method"])
        self.assertIn("sensorDbId=air-temp-01", final["path"])
        self.assertIs(True, final["assert"]["telemetry_original_intact"])

    def exercise(self, change=None, read_status=200, replay_counts=None,
                 first_counts=None, first_status=200, replay_status=200):
        seen = []
        submitted = []

        def fake_http(_server, method, path, body=None, token=None):
            seen.append((method, path))
            if len(seen) == 1:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(3, len(body))
                submitted.extend(copy.deepcopy(body))
                counts = {"appended": 3, "replayed": 0}
                if first_counts is not None:
                    counts = first_counts
                return first_status, {"result": {**counts, "conflicts": []}}
            if len(seen) == 2:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(submitted, body)
                counts = replay_counts or {"appended": 0, "replayed": 3}
                return replay_status, {"result": {**counts, "conflicts": []}}
            if len(seen) == 3:
                self.assertEqual("GET", method)
                self.assertIn(f"deviceDbId={submitted[0]['deviceDbId']}", path)
                self.assertIn("sensorDbId=air-temp-01", path)
                rows = copy.deepcopy(submitted)
                if change is not None:
                    rows = change(rows)
                return read_status, {"result": {"data": rows}}
            self.fail("unexpected extra live request")

        result = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, result, None, None)
        if (replay_counts is None and first_counts is None
                and first_status == 200 and replay_status == 200):
            self.assertEqual(3, len(seen))
        return result.failures

    def test_replay_with_unchanged_storage_passes(self):
        self.assertEqual(0, self.exercise())

    def test_hidden_duplicate_after_correct_replay_counts_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: rows + [rows[0]]))

    def test_changed_value_after_replay_fails(self):
        def corrupt(rows):
            rows[1]["value"] += 10
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_missing_stored_record_after_replay_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: rows[:2]))

    def test_swapped_timestamps_after_replay_fails(self):
        def corrupt(rows):
            rows[0]["timestamp"], rows[1]["timestamp"] = (
                rows[1]["timestamp"], rows[0]["timestamp"])
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_wrong_sensor_fails(self):
        def corrupt(rows):
            rows[2]["sensorDbId"] = "other-sensor"
            return rows
        self.assertEqual(1, self.exercise(corrupt))

    def test_changed_unit_after_replay_fails(self):
        def change(rows):
            rows[0]["unit"] = "degree_fahrenheit"
            return rows
        self.assertEqual(1, self.exercise(change))

    def test_changed_quality_after_replay_fails(self):
        def change(rows):
            rows[2]["quality"] = "good"
            return rows
        self.assertEqual(1, self.exercise(change))

    def test_changed_nested_provenance_after_replay_fails(self):
        def change(rows):
            rows[0]["provenance"]["actor"] = "actor:wrong"
            return rows
        self.assertEqual(1, self.exercise(change))

    def test_missing_original_provenance_after_replay_fails(self):
        def change(rows):
            rows[0].pop("provenance")
            return rows
        self.assertEqual(1, self.exercise(change))

    def test_extra_server_managed_field_is_allowed(self):
        def change(rows):
            rows[0]["auditSeen"] = True
            return rows
        self.assertEqual(0, self.exercise(change))

    def test_malformed_row_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: [rows[0], None, rows[2]]))

    def test_missing_data_array_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: None))

    def test_unavailable_read_fails(self):
        self.assertEqual(1, self.exercise(read_status=404))

    def test_false_replay_counters_fail(self):
        self.assertEqual(1, self.exercise(replay_counts={"appended": 1, "replayed": 2}))


    def test_boolean_zero_replay_counter_fails(self):
        self.assertEqual(1, self.exercise(
            replay_counts={"appended": False, "replayed": 3}))

    def test_boolean_initial_replayed_counter_fails(self):
        self.assertEqual(1, self.exercise(
            first_counts={"appended": 3, "replayed": False}))

    def test_fractional_zero_replay_counter_fails(self):
        self.assertEqual(1, self.exercise(
            replay_counts={"appended": 0.0, "replayed": 3}))

    def test_fractional_three_replayed_counter_fails(self):
        self.assertEqual(1, self.exercise(
            replay_counts={"appended": 0, "replayed": 3.0}))

    def test_missing_replayed_counter_fails(self):
        self.assertEqual(1, self.exercise(
            replay_counts={"appended": 0}))

    def test_null_appended_counter_fails(self):
        self.assertEqual(1, self.exercise(
            replay_counts={"appended": None, "replayed": 3}))

    def test_string_appended_counter_fails(self):
        self.assertEqual(1, self.exercise(
            replay_counts={"appended": "0", "replayed": 3}))

    def test_negative_replayed_counter_fails(self):
        self.assertEqual(1, self.exercise(
            replay_counts={"appended": 0, "replayed": -3}))

    def test_replay_non_success_with_correct_counts_fails(self):
        self.assertEqual(1, self.exercise(replay_status=500))

    def test_first_post_non_success_with_correct_counts_fails(self):
        self.assertEqual(1, self.exercise(first_status=500))


if __name__ == "__main__":
    unittest.main()
