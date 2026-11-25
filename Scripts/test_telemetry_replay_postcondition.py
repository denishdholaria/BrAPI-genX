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

    def exercise(self, change=None, read_status=200, replay_counts=None):
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
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(submitted, body)
                counts = replay_counts or {"appended": 0, "replayed": 3}
                return 200, {"result": {**counts, "conflicts": []}}
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
        if replay_counts is None:
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

    def test_malformed_row_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: [rows[0], None, rows[2]]))

    def test_missing_data_array_fails(self):
        self.assertEqual(1, self.exercise(lambda rows: None))

    def test_unavailable_read_fails(self):
        self.assertEqual(1, self.exercise(read_status=404))

    def test_false_replay_counters_fail(self):
        self.assertEqual(1, self.exercise(replay_counts={"appended": 1, "replayed": 2}))


if __name__ == "__main__":
    unittest.main()
