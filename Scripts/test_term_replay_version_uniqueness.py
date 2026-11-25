#!/usr/bin/env python3
"""Mission 125: identical variable-term publication must not create a version."""
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


class TermReplayVersionUniquenessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        manifest = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in manifest["probes"] if p["id"] == "L-08")

    def test_registered_replay_requires_collection_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["same_term"])
        self.assertEqual(200, self.probe["calls"][1]["assert"]["status"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["term_replay_single_version"])

    def exercise(self, mutate=None, page_change=None, get_status=200,
                 replay_version=None, replay_status=200, replay_mutate=None):
        calls = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/variable-terms"), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/variable-terms"), (method, path))
                self.assertEqual(original, body)
                returned = copy.deepcopy(body)
                if replay_version is not None:
                    returned["version"] = replay_version
                if replay_mutate is not None:
                    returned = replay_mutate(returned)
                return replay_status, {"result": returned}
            if len(calls) == 3:
                expected = ("/variable-terms?variableDbId=" +
                            quote(original["variableDbId"], safe=":"))
                self.assertEqual(("GET", expected), (method, path))
                rows = [copy.deepcopy(original)]
                if mutate is not None:
                    rows = mutate(rows)
                page = {"totalCount": 1, "totalPages": 1,
                        "currentPage": 0, "pageSize": 1000}
                if page_change is not None:
                    page = page_change(page)
                return get_status, {"result": {"data": rows},
                                    "metadata": {"pagination": page}}
            self.fail("unexpected extra call")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_one_unchanged_version_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_extra_server_managed_field_allowed(self):
        self.assertEqual(0, self.exercise(
            mutate=lambda rows: [{**rows[0], "retrievedBy": "test"}])[0])

    def test_hidden_second_version_fails_despite_same_replay_reply(self):
        def bad(rows):
            rows.append({**rows[0], "version": "2"})
            return rows
        self.assertEqual(1, self.exercise(mutate=bad)[0])

    def test_duplicated_same_version_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_missing_original_version_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda rows: [])[0])

    def test_changed_term_scale_fails(self):
        def bad(rows):
            rows[0]["scaleDbId"] = "other:scale:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate=bad)[0])

    def test_changed_nested_provenance_fails(self):
        def bad(rows):
            rows[0]["provenance"]["actor"] = "actor:unknown"
            return rows
        self.assertEqual(1, self.exercise(mutate=bad)[0])

    def test_wrong_published_version_fails(self):
        def bad(rows):
            rows[0]["version"] = "3"
            return rows
        self.assertEqual(1, self.exercise(mutate=bad)[0])

    def test_wrong_published_term_id_fails(self):
        def bad(rows):
            rows[0]["variableDbId"] = "other:variable:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate=bad)[0])

    def test_missing_original_field_fails(self):
        def bad(rows):
            rows[0].pop("provenance")
            return rows
        self.assertEqual(1, self.exercise(mutate=bad)[0])

    def test_malformed_collection_row_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda rows: [None])[0])

    def test_higher_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda p: {**p, "totalCount": 2})[0])

    def test_incomplete_pagination_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda p: {**p, "totalPages": 2})[0])

    def test_boolean_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda p: {**p, "totalCount": True})[0])

    def test_failed_get_fails(self):
        self.assertEqual(1, self.exercise(get_status=404)[0])

    def test_wrong_replay_version_fails_before_get(self):
        failures, calls = self.exercise(replay_version="999")
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


    def test_replay_accepted_as_new_write_fails(self):
        failures, calls = self.exercise(replay_status=202)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_server_failure_fails(self):
        failures, calls = self.exercise(replay_status=500)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


    def test_replay_variable_name_corruption_fails_before_readback(self):
        def change(row):
            row.__setitem__('variableName', 'wrong name')
            return row
        failures, calls = self.exercise(replay_mutate=change)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_nested_provenance_corruption_fails_before_readback(self):
        def change(row):
            row['provenance'].__setitem__('actor', 'actor:wrong')
            return row
        failures, calls = self.exercise(replay_mutate=change)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_missing_scale_corruption_fails_before_readback(self):
        def change(row):
            row.pop('scaleDbId')
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
