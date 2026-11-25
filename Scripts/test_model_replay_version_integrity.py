#!/usr/bin/env python3
"""Mission 128: model replay must retain exactly one original published version."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest
from urllib.parse import quote

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class ModelReplayVersionIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-12")

    def test_registered_probe_checks_filtered_collection(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["same_model"])
        self.assertEqual(200, self.probe["calls"][1]["assert"]["status"])
        last = self.probe["calls"][2]
        self.assertEqual(("GET", "/models?modelDbId={modelDbId}"),
                         (last["method"], last["path"]))
        self.assertIs(True, last["assert"]["model_replay_single_version"])

    def exercise(self, mutate=None, page_change=None, read_status=200,
                 replay_version=None, replay_status=200, replay_mutate=None):
        calls = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/models"), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/models"), (method, path))
                self.assertEqual(original, body)
                replay = copy.deepcopy(body)
                if replay_version is not None:
                    replay["modelVersion"] = replay_version
                if replay_mutate is not None:
                    replay = replay_mutate(replay)
                return replay_status, {"result": replay}
            if len(calls) == 3:
                expected_path = ("/models?modelDbId=" +
                                 quote(original["modelDbId"], safe=":"))
                self.assertEqual(("GET", expected_path), (method, path))
                rows = [copy.deepcopy(original)]
                if mutate:
                    rows = mutate(rows)
                page = {"totalCount": len(rows) if isinstance(rows, list) else 1,
                        "pageSize": 1000, "totalPages": 1, "currentPage": 0}
                if page_change:
                    page = page_change(page)
                return read_status, {"result": {"data": rows},
                                     "metadata": {"pagination": page}}
            self.fail("unexpected additional call")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_one_original_version_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_additional_server_metadata_is_allowed(self):
        self.assertEqual(0, self.exercise(
            mutate=lambda rows: [{**rows[0], "reviewStatus": "retained"}])[0])

    def test_additional_version_with_identical_response_fails(self):
        def change(rows):
            rows.append({**copy.deepcopy(rows[0]), "modelVersion": "8"})
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_duplicate_version_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_missing_stored_model_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda rows: [])[0])

    def test_wrong_stored_model_identifier_fails(self):
        def change(rows):
            rows[0]["modelDbId"] = "other:model:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_model_version_fails(self):
        def change(rows):
            rows[0]["modelVersion"] = "9"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_artifact_digest_fails(self):
        def change(rows):
            rows[0]["artifactDigest"] = "f" * 64
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_training_digest_fails(self):
        def change(rows):
            rows[0]["trainingDataDigest"] = "f" * 64
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_metrics_fails(self):
        def change(rows):
            rows[0]["metrics"]["rmse"] = 9.99
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_nested_provenance_fails(self):
        def change(rows):
            rows[0]["provenance"]["actor"] = "actor:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_missing_original_field_fails(self):
        def change(rows):
            rows[0].pop("framework")
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_malformed_row_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda rows: [None])[0])

    def test_non_successful_get_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_more_than_one_reported_page_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda page: {**page, "totalPages": 2})[0])

    def test_inconsistent_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda page: {**page, "totalCount": 2})[0])

    def test_boolean_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda page: {**page, "totalCount": True})[0])

    def test_bad_current_page_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda page: {**page, "currentPage": 1})[0])

    def test_wrong_replay_version_fails_before_readback(self):
        failed, calls = self.exercise(replay_version="8")
        self.assertEqual(1, failed)
        self.assertEqual(2, len(calls))


    def test_replay_accepted_as_new_write_fails(self):
        failures, calls = self.exercise(replay_status=202)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_server_failure_fails(self):
        failures, calls = self.exercise(replay_status=500)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


    def test_replay_artifact_digest_corruption_fails_before_readback(self):
        def change(row):
            row.__setitem__('artifactDigest', 'f' * 64)
            return row
        failures, calls = self.exercise(replay_mutate=change)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_nested_metric_corruption_fails_before_readback(self):
        def change(row):
            row['metrics'].__setitem__('rmse', 9.8)
            return row
        failures, calls = self.exercise(replay_mutate=change)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_missing_provenance_corruption_fails_before_readback(self):
        def change(row):
            row.pop('provenance')
            return row
        failures, calls = self.exercise(replay_mutate=change)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_allows_additional_server_metadata(self):
        failures, calls = self.exercise(
            replay_mutate=lambda row: {**row, "serverAuditMarker": "verified"})
        self.assertEqual(0, failures)
        self.assertEqual(3, len(calls))



if __name__ == "__main__":
    unittest.main()
