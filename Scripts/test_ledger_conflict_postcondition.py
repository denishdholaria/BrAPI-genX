#!/usr/bin/env python3
"""Mission 123: L-11 conflict rejection must preserve original ledger content."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class LedgerConflictReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-11")

    def test_registered_probe_requires_original_entry_after_conflict(self):
        self.assertEqual(3, len(self.probe["calls"]))
        read = self.probe["calls"][-1]
        self.assertEqual("GET", read["method"])
        self.assertIs(True, read["assert"]["ledger_original_intact"])
        self.assertEqual(1, read["assert"]["ledger_count"])

    def exercise(self, alter=None, page_change=None, status=200,
                 conflicting_status=409):
        calls = []
        original = {}
        lot = []

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual("POST", method)
                self.assertTrue(path.startswith("/seedlots/"))
                lot.append(path.split("/")[2])
                original.update(copy.deepcopy(body))
                record = {**copy.deepcopy(body),
                          "entryDbId": "LEDGER_001",
                          "seedLotDbId": lot[0],
                          "position": 0}
                return 200, {"result": record}
            if len(calls) == 2:
                self.assertEqual(("POST", f"/seedlots/{lot[0]}/ledger"),
                                 (method, path))
                self.assertEqual(original["idempotencyKey"], body["idempotencyKey"])
                self.assertNotEqual(original["quantity"], body["quantity"])
                return conflicting_status, {"result": {}}
            if len(calls) == 3:
                self.assertEqual(("GET", f"/seedlots/{lot[0]}/ledger"),
                                 (method, path))
                record = {**copy.deepcopy(original),
                          "entryDbId": "LEDGER_001",
                          "seedLotDbId": lot[0],
                          "position": 0}
                rows = [record]
                if alter is not None:
                    rows = alter(rows)
                page = {"totalCount": 1, "totalPages": 1,
                        "currentPage": 0, "pageSize": 1000}
                if page_change is not None:
                    page = page_change(page)
                return status, {"metadata": {"pagination": page},
                                "result": {"data": rows}}
            self.fail("unexpected extra request")

        outcomes = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcomes, None, None)
        return outcomes.failures, calls

    def test_original_entry_survives(self):
        self.assertEqual(0, self.exercise()[0])

    def test_extra_server_managed_property_allowed(self):
        self.assertEqual(0, self.exercise(
            alter=lambda rows: [{**rows[0], "auditTimestamp": "2026-11-25"}])[0])

    def test_mutated_quantity_fails_even_with_one_row(self):
        def bad(rows):
            rows[0]["quantity"] = "99.000"
            return rows
        self.assertEqual(1, self.exercise(alter=bad)[0])

    def test_actor_mutation_fails(self):
        def bad(rows):
            rows[0]["actor"] = "actor:unexpected"
            return rows
        self.assertEqual(1, self.exercise(alter=bad)[0])

    def test_provenance_digest_mutation_fails(self):
        def bad(rows):
            rows[0]["provenance"]["inputsDigest"] = "f" * 64
            return rows
        self.assertEqual(1, self.exercise(alter=bad)[0])

    def test_wrong_entry_identifier_fails(self):
        def bad(rows):
            rows[0]["entryDbId"] = "LEDGER_WRONG"
            return rows
        self.assertEqual(1, self.exercise(alter=bad)[0])

    def test_wrong_lot_identifier_fails(self):
        def bad(rows):
            rows[0]["seedLotDbId"] = "LOT_WRONG"
            return rows
        self.assertEqual(1, self.exercise(alter=bad)[0])

    def test_missing_original_field_fails(self):
        def bad(rows):
            rows[0].pop("idempotencyKey")
            return rows
        self.assertEqual(1, self.exercise(alter=bad)[0])

    def test_extra_entry_fails_even_if_first_original_is_intact(self):
        self.assertEqual(1, self.exercise(alter=lambda rows: rows + [rows[0]])[0])

    def test_deleted_record_fails(self):
        self.assertEqual(1, self.exercise(alter=lambda rows: [])[0])

    def test_malformed_record_fails(self):
        self.assertEqual(1, self.exercise(alter=lambda rows: [None])[0])

    def test_incorrect_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda p: {**p, "totalCount": 2})[0])

    def test_unseen_second_page_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda p: {**p, "totalPages": 2})[0])

    def test_boolean_pagination_count_fails(self):
        self.assertEqual(1, self.exercise(
            page_change=lambda p: {**p, "totalCount": True})[0])

    def test_non_successful_read_fails(self):
        self.assertEqual(1, self.exercise(status=404)[0])

    def test_conflict_not_rejected_fails_before_readback(self):
        fail, calls = self.exercise(conflicting_status=200)
        self.assertEqual(1, fail)
        self.assertEqual(2, len(calls))


if __name__ == "__main__":
    unittest.main()
