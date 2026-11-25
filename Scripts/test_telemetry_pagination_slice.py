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
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertEqual(
            {"appended": 3, "replayed": 0},
            self.probe["calls"][0]["assert"]["telemetry_counts"])
        self.assertIs(
            True, self.probe["calls"][0]["assert"]["telemetry_no_conflicts"])
        first, last = self.probe["calls"][1:]
        self.assertEqual("GET", first["method"])
        self.assertEqual("GET", last["method"])
        self.assertIn("page=0&pageSize=2", first["path"])
        self.assertIn("page=1&pageSize=2", last["path"])
        self.assertIs(True, first["assert"]["telemetry_page_slice"])
        self.assertIs(True, last["assert"]["telemetry_page_slice"])

    def exercise(self, mutate_rows=None, mutate_page=None, status=200,
                 mutate_tail_rows=None, mutate_tail_page=None, tail_status=200,
                 initial_mutate=None, initial_status=200):
        seen = []
        submitted = []

        def fake_http(_server, method, path, body=None, token=None):
            seen.append((method, path))
            if len(seen) == 1:
                self.assertEqual(("POST", "/telemetry"), (method, path))
                self.assertEqual(3, len(body))
                submitted.extend(copy.deepcopy(body))
                outcome = {"appended": 3, "replayed": 0, "conflicts": []}
                if initial_mutate is not None:
                    outcome = initial_mutate(outcome)
                return initial_status, {"result": outcome}
            if len(seen) in (2, 3):
                index = len(seen) - 2
                self.assertEqual("GET", method)
                self.assertIn(f"deviceDbId={submitted[0]['deviceDbId']}", path)
                self.assertIn(f"page={index}&pageSize=2", path)
                rows = copy.deepcopy(sorted(
                    submitted, key=lambda point: point["timestamp"])[index * 2:(index + 1) * 2])
                pagination = {"currentPage": index, "pageSize": 2,
                              "totalCount": 3, "totalPages": 2}
                if index == 0:
                    if mutate_rows is not None:
                        rows = mutate_rows(rows, submitted)
                    if mutate_page is not None:
                        pagination = mutate_page(pagination)
                    response_status = status
                else:
                    if mutate_tail_rows is not None:
                        rows = mutate_tail_rows(rows, submitted)
                    if mutate_tail_page is not None:
                        pagination = mutate_tail_page(pagination)
                    response_status = tail_status
                return response_status, {"result": {"data": rows}, "metadata": {
                    "pagination": pagination}}
            self.fail("unexpected extra live request")

        result = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, result, None, None)
        # A failing first page exits before requesting the second page.
        if initial_mutate is None and initial_status == 200:
            self.assertIn(len(seen), (2, 3))
        else:
            self.assertIn(len(seen), (1, 2, 3))
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


    def test_missing_tail_record_fails(self):
        self.assertEqual(1, self.exercise(mutate_tail_rows=lambda rows, _: []))

    def test_duplicated_first_page_row_in_tail_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_rows=lambda rows, source: [copy.deepcopy(source[0])]))

    def test_second_page_substitutes_middle_record_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_rows=lambda rows, source: [copy.deepcopy(source[1])]))

    def test_corrupted_tail_value_fails(self):
        def corrupt(rows, _):
            rows[0]["value"] += 1.0
            return rows
        self.assertEqual(1, self.exercise(mutate_tail_rows=corrupt))

    def test_tail_sensor_changed_fails(self):
        def corrupt(rows, _):
            rows[0]["sensorDbId"] = "unrelated-sensor"
            return rows
        self.assertEqual(1, self.exercise(mutate_tail_rows=corrupt))

    def test_tail_timestamp_changed_fails(self):
        def corrupt(rows, _):
            rows[0]["timestamp"] = "2026-09-07T08:01:30Z"
            return rows
        self.assertEqual(1, self.exercise(mutate_tail_rows=corrupt))

    def test_tail_unit_removed_fails(self):
        def corrupt(rows, _):
            rows[0].pop("unit")
            return rows
        self.assertEqual(1, self.exercise(mutate_tail_rows=corrupt))

    def test_tail_quality_changed_fails(self):
        def corrupt(rows, _):
            rows[0]["quality"] = "bad"
            return rows
        self.assertEqual(1, self.exercise(mutate_tail_rows=corrupt))

    def test_first_page_nested_provenance_mutated_fails(self):
        def corrupt(rows, _):
            rows[0]["provenance"]["algorithmVersion"] = "fabricated"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=corrupt))

    def test_first_page_unit_changed_fails(self):
        def corrupt(rows, _):
            rows[0]["unit"] = "kelvin"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=corrupt))

    def test_wrong_tail_page_index_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_page=lambda p: {**p, "currentPage": 0}))

    def test_wrong_tail_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_page=lambda p: {**p, "totalCount": 2}))

    def test_wrong_tail_total_pages_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_page=lambda p: {**p, "totalPages": 1}))

    def test_wrong_tail_page_size_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_page=lambda p: {**p, "pageSize": 1}))

    def test_boolean_tail_pagination_value_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_page=lambda p: {**p, "currentPage": True}))

    def test_missing_tail_pagination_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_page=lambda p: {k: v for k, v in p.items()
                                        if k != "totalCount"}))

    def test_non_successful_tail_read_fails(self):
        self.assertEqual(1, self.exercise(tail_status=404))

    def test_extra_tail_record_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_tail_rows=lambda rows, source: rows + [copy.deepcopy(source[0])]))



    def test_initial_post_incorrect_append_count_fails(self):
        self.assertEqual(1, self.exercise(
            initial_mutate=lambda result: {**result, "appended": 2}))

    def test_initial_post_boolean_replayed_count_fails(self):
        self.assertEqual(1, self.exercise(
            initial_mutate=lambda result: {**result, "replayed": False}))

    def test_initial_post_fabricated_conflict_fails(self):
        self.assertEqual(1, self.exercise(
            initial_mutate=lambda result: {**result, "conflicts": ["fabricated"]}))

    def test_initial_post_missing_conflict_array_fails(self):
        self.assertEqual(1, self.exercise(
            initial_mutate=lambda result: {
                key: value for key, value in result.items()
                if key != "conflicts"}))

    def test_initial_post_non_success_status_fails(self):
        self.assertEqual(1, self.exercise(initial_status=409))



if __name__ == "__main__":
    unittest.main()
