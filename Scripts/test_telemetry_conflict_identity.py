#!/usr/bin/env python3
"""Mission 144: conflicting telemetry reply must identify the actual rejected key."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TelemetryConflictIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in registry["probes"] if p["id"] == "L-22")

    def test_registered_procedure_retains_conflict_assertion(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertEqual(1, self.probe["calls"][1]["assert"]["telemetry_conflicts"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["telemetry_original_intact"])

    def exercise(self, modify_conflicts=None, mutate_counts=None,
                 post_status=200, alter_original=None):
        calls = []
        submitted = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                submitted.extend(copy.deepcopy(body))
                return 200, {"result": {"appended": 3, "replayed": 0,
                                        "conflicts": []}}
            if len(calls) == 2:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(1, len(body))
                expected = "/".join((body[0]["deviceDbId"],
                                     body[0]["sensorDbId"], body[0]["timestamp"]))
                result = {"appended": 0, "replayed": 0,
                          "conflicts": [expected]}
                if modify_conflicts is not None:
                    result["conflicts"] = modify_conflicts(expected)
                if mutate_counts:
                    result.update(mutate_counts)
                return post_status, {"result": result}
            if len(calls) == 3:
                self.assertEqual("GET", method)
                rows = copy.deepcopy(submitted)
                if alter_original:
                    rows = alter_original(rows)
                return 200, {"result": {"data": rows}}
            self.fail("unexpected extra request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_actual_conflicting_key_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_arbitrary_conflict_string_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: ["conflicting-value"])[0])

    def test_wrong_device_conflict_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: [expected.replace(
                "test-station-", "other-station-")])[0])

    def test_wrong_sensor_conflict_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: [expected.replace(
                "air-temp-01", "soil-temp-01")])[0])

    def test_wrong_timestamp_conflict_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: [expected.replace(
                "08:02:00Z", "08:01:00Z")])[0])

    def test_duplicate_conflict_key_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: [expected, expected])[0])

    def test_no_conflict_key_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: [])[0])

    def test_non_string_conflict_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: [{"key": expected}])[0])

    def test_null_conflict_array_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: None)[0])

    def test_null_conflict_entry_fails(self):
        self.assertEqual(1, self.exercise(
            modify_conflicts=lambda expected: [None])[0])

    def test_incorrect_appended_counter_fails(self):
        self.assertEqual(1, self.exercise(mutate_counts={"appended": 1})[0])

    def test_incorrect_replayed_counter_fails(self):
        self.assertEqual(1, self.exercise(mutate_counts={"replayed": 1})[0])

    def test_non_successful_conflict_response_fails(self):
        self.assertEqual(1, self.exercise(post_status=400)[0])

    def test_original_source_unchanged_must_be_readable(self):
        def change(rows):
            rows[2]["value"] += 1
            return rows
        self.assertEqual(1, self.exercise(alter_original=change)[0])

    def test_original_provenance_must_be_readable(self):
        def change(rows):
            rows[0]["provenance"]["actor"] = "actor:tampered"
            return rows
        self.assertEqual(1, self.exercise(alter_original=change)[0])


    def test_boolean_false_appended_conflict_counter_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_counts={"appended": False})[0])

    def test_boolean_false_replayed_conflict_counter_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_counts={"replayed": False})[0])

    def test_fractional_zero_conflict_counter_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_counts={"appended": 0.0})[0])

    def test_null_conflict_counter_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_counts={"replayed": None})[0])

    def test_string_conflict_counter_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_counts={"appended": "0"})[0])

    def test_negative_conflict_counter_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_counts={"replayed": -1})[0])


if __name__ == "__main__":
    unittest.main()
