#!/usr/bin/env python3
"""Mission 124: ledger replay response must match stored original entry."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class LedgerReplayReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-10")

    def test_registered_replay_reads_back_original(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][1]["assert"]["same_ledger"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["ledger_original_intact"])

    def exercise(self, mutate=None, mutate_page=None, get_status=200,
                 replay_id="ENTRY_001"):
        calls = []
        original = {}
        lot = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual("POST", method)
                lot.append(path.split("/")[2])
                original.update(copy.deepcopy(body))
                return 200, {"result": {
                    **copy.deepcopy(body), "seedLotDbId": lot[0],
                    "entryDbId": "ENTRY_001", "position": 0}}
            if len(calls) == 2:
                self.assertEqual(("POST", f"/seedlots/{lot[0]}/ledger"),
                                 (method, path))
                self.assertEqual(original, body)
                return 200, {"result": {
                    **copy.deepcopy(body), "seedLotDbId": lot[0],
                    "entryDbId": replay_id, "position": 0}}
            if len(calls) == 3:
                self.assertEqual(("GET", f"/seedlots/{lot[0]}/ledger"),
                                 (method, path))
                rows = [{**copy.deepcopy(original),
                         "seedLotDbId": lot[0],
                         "entryDbId": "ENTRY_001", "position": 0}]
                if mutate is not None:
                    rows = mutate(rows)
                page = {"totalCount": 1, "totalPages": 1,
                        "currentPage": 0, "pageSize": 1000}
                if mutate_page is not None:
                    page = mutate_page(page)
                return get_status, {"result": {"data": rows},
                                    "metadata": {"pagination": page}}
            self.fail("unexpected extra request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_correct_replay_and_storage_pass(self):
        self.assertEqual(0, self.exercise()[0])

    def test_extra_server_metadata_allowed(self):
        self.assertEqual(0, self.exercise(
            mutate=lambda rows: [{**rows[0], "serverNote": "retained"}])[0])

    def test_same_replay_id_with_corrupt_stored_quantity_fails(self):
        def change(rows):
            rows[0]["quantity"] = "50.000"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_corrupt_stored_actor_fails(self):
        def change(rows):
            rows[0]["actor"] = "actor:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_corrupt_nested_provenance_fails(self):
        def change(rows):
            rows[0]["provenance"]["actor"] = "actor:wrong"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_missing_original_field_fails(self):
        def change(rows):
            rows[0].pop("idempotencyKey")
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_changed_entry_id_fails(self):
        def change(rows):
            rows[0]["entryDbId"] = "ENTRY_002"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_wrong_seed_lot_id_fails(self):
        def change(rows):
            rows[0]["seedLotDbId"] = "LOT_WRONG"
            return rows
        self.assertEqual(1, self.exercise(mutate=change)[0])

    def test_duplicate_storage_fails(self):
        self.assertEqual(1, self.exercise(
            mutate=lambda rows: rows + [rows[0]])[0])

    def test_missing_stored_entry_fails(self):
        self.assertEqual(1, self.exercise(mutate=lambda rows: [])[0])

    def test_unseen_additional_page_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "totalPages": 2})[0])

    def test_incorrect_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            mutate_page=lambda p: {**p, "totalCount": 2})[0])

    def test_get_unavailable_fails(self):
        self.assertEqual(1, self.exercise(get_status=404)[0])

    def test_wrong_replay_identifier_fails_before_readback(self):
        failures, calls = self.exercise(replay_id="ENTRY_DIFFERENT")
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
