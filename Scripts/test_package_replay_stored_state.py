#!/usr/bin/env python3
"""Mission 127: package replay must preserve a single stored original package."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class PackageReplayStoredStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-18")

    def test_registered_probe_requires_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["same_package"])
        self.assertEqual(200, self.probe["calls"][1]["assert"]["status"])
        final = self.probe["calls"][2]
        self.assertEqual(("GET", "/fair-packages"), (final["method"], final["path"]))
        self.assertIs(True, final["assert"]["package_replay_single_record"])

    def exercise(self, mutate_rows=None, mutate_page=None, read_status=200,
                 replay_identifier=None, unrelated=False, replay_status=200, replay_mutate=None):
        calls = []
        original = {}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/fair-packages"), (method, path))
                original.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(calls) == 2:
                self.assertEqual(("POST", "/fair-packages"), (method, path))
                self.assertEqual(original, body)
                returned = copy.deepcopy(body)
                if replay_identifier is not None:
                    returned["packageDbId"] = replay_identifier
                if replay_mutate is not None:
                    returned = replay_mutate(returned)
                return replay_status, {"result": returned}
            if len(calls) == 3:
                self.assertEqual(("GET", "/fair-packages"), (method, path))
                rows = [copy.deepcopy(original)]
                if unrelated:
                    rows.append({**copy.deepcopy(original),
                                 "packageDbId": "external:package:unrelated"})
                if mutate_rows is not None:
                    rows = mutate_rows(rows)
                page = {"totalCount": len(rows) if isinstance(rows, list) else 1,
                        "pageSize": 1000, "totalPages": 1, "currentPage": 0}
                if mutate_page is not None:
                    page = mutate_page(page)
                return read_status, {
                    "result": {"data": rows}, "metadata": {"pagination": page}
                }
            self.fail("unexpected extra network request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_original_package_is_retained(self):
        self.assertEqual(0, self.exercise()[0])

    def test_unrelated_packages_are_allowed(self):
        self.assertEqual(0, self.exercise(unrelated=True)[0])

    def test_extra_server_metadata_allowed(self):
        self.assertEqual(0, self.exercise(
            mutate_rows=lambda rows: [{**rows[0], "audited": True}])[0])

    def test_duplicate_package_id_is_rejected(self):
        self.assertEqual(1, self.exercise(
            mutate_rows=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_original_package_missing_is_rejected(self):
        self.assertEqual(1, self.exercise(mutate_rows=lambda rows: [])[0])

    def test_package_identifier_mismatch_is_rejected(self):
        def change(rows):
            rows[0]["packageDbId"] = "external:package:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=change)[0])

    def test_modified_license_is_rejected(self):
        def change(rows):
            rows[0]["license"] = "CC0-1.0"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=change)[0])

    def test_modified_access_rights_are_rejected(self):
        def change(rows):
            rows[0]["accessRights"] = "restricted"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=change)[0])

    def test_modified_nested_reference_digest_is_rejected(self):
        def change(rows):
            rows[0]["payloadRefs"][0]["responseDigest"] = "f" * 64
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=change)[0])

    def test_modified_nested_provenance_is_rejected(self):
        def change(rows):
            rows[0]["provenance"]["actor"] = "actor:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=change)[0])

    def test_missing_original_nested_field_is_rejected(self):
        def change(rows):
            rows[0].pop("payloadRefs")
            return rows
        self.assertEqual(1, self.exercise(mutate_rows=change)[0])

    def test_missing_collection_row_is_rejected(self):
        self.assertEqual(1, self.exercise(mutate_rows=lambda rows: [None])[0])

    def test_missing_collection_array_is_rejected(self):
        self.assertEqual(1, self.exercise(mutate_rows=lambda rows: None)[0])

    def test_incomplete_pagination_is_rejected(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "totalPages": 2})[0])

    def test_hidden_total_count_is_rejected(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "totalCount": 2})[0])

    def test_boolean_pagination_count_is_rejected(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "totalCount": True})[0])

    def test_wrong_page_index_is_rejected(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda page: {**page, "currentPage": 1})[0])

    def test_unavailable_collection_is_rejected(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_wrong_replay_identifier_fails_before_readback(self):
        failures, calls = self.exercise(replay_identifier="external:package:wrong")
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


    def test_replay_license_corruption_fails_before_readback(self):
        def change(row):
            row.__setitem__('license', 'wrong-license')
            return row
        failures, calls = self.exercise(replay_mutate=change)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_replay_payload_digest_corruption_fails_before_readback(self):
        def change(row):
            row['payloadRefs'][0].__setitem__('responseDigest', 'f' * 64)
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
