#!/usr/bin/env python3
"""Mission 121: L-24 verifies one stored job, not only matching responses."""
from __future__ import annotations

import copy
from pathlib import Path
from threading import Lock
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class ConcurrentJobStoredEffectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(probe for probe in doc["probes"] if probe["id"] == "L-24")

    def test_registered_probe_requires_readback(self):
        self.assertEqual(2, len(self.probe["calls"]))
        self.assertEqual(8, self.probe["calls"][0]["concurrent_posts"])
        self.assertEqual("GET", self.probe["calls"][1]["method"])
        self.assertEqual("/jobs", self.probe["calls"][1]["path"])
        self.assertIs(True, self.probe["calls"][1]["assert"]["concurrent_single_stored_job"])

    def exercise(self, change_rows=None, change_page=None, read_status=200,
                 different_response_id=False, add_unrelated=False,
                 mutate_ack=None):
        lock = Lock()
        submitted = []
        calls = []

        def fake_http(_server, method, path, body=None, token=None):
            with lock:
                calls.append((method, path))
                if method == "POST":
                    submitted.append(copy.deepcopy(body))
                    sequence = len(submitted)
                else:
                    sequence = None
            if method == "POST":
                self.assertEqual("/jobs", path)
                self.assertEqual(submitted[0]["idempotencyKey"], body["idempotencyKey"])
                job_id = ("JOB_SECOND" if different_response_id and sequence == 8
                          else "JOB_ONE")
                accepted = {
                    "jobDbId": job_id, "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"],
                    "status": "SUBMITTED"}
                if mutate_ack is not None:
                    accepted = mutate_ack(accepted, sequence)
                return (202 if sequence == 1 else 200), {
                    "result": accepted}
            self.assertEqual(("GET", "/jobs"), (method, path))
            self.assertEqual(8, len(submitted))
            rows = [{
                "jobDbId": "JOB_ONE",
                "jobType": submitted[0]["jobType"],
                "idempotencyKey": submitted[0]["idempotencyKey"],
                "status": "SUBMITTED",
            }]
            if add_unrelated:
                rows.append({"jobDbId": "JOB_UNRELATED",
                             "jobType": "analysis", "idempotencyKey": "unrelated-key",
                             "status": "RUNNING"})
            if change_rows is not None:
                rows = change_rows(copy.deepcopy(rows))
            page = {
                "totalCount": len(rows) if isinstance(rows, list) else 1,
                "pageSize": len(rows) if isinstance(rows, list) else 1,
                "totalPages": 1,
                "currentPage": 0,
            }
            if change_page is not None:
                page = change_page(page)
            return read_status, {"result": {"data": rows},
                                 "metadata": {"pagination": page}}

        result = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe("http://example.test/genx/v1", self.probe,
                                   {"conformance_dir": str(CONF)},
                                   result, None, None)
        return result.failures, calls

    def test_eight_responses_and_one_persisted_job_pass(self):
        failures, calls = self.exercise()
        self.assertEqual(0, failures)
        self.assertEqual(8, len([method for method, _ in calls if method == "POST"]))
        self.assertEqual(1, len([method for method, _ in calls if method == "GET"]))

    def test_single_stored_job_missing_status_fails(self):
        def change(rows):
            del rows[0]["status"]
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_unrelated_stored_job_unknown_status_fails(self):
        def change(rows):
            rows[1]["status"] = "QUEUED"
            return rows
        self.assertEqual(1, self.exercise(
            add_unrelated=True, change_rows=change)[0])

    def test_stored_job_nonstring_status_fails(self):
        for wrong in (None, False, 0, [], {}):
            with self.subTest(wrong=wrong):
                def change(rows):
                    rows[0]["status"] = wrong
                    return rows
                self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_unrelated_existing_job_is_allowed(self):
        self.assertEqual(0, self.exercise(add_unrelated=True)[0])

    def test_matching_responses_with_extra_key_duplicate_fail(self):
        def change(rows):
            rows.append({**rows[0], "jobDbId": "JOB_HIDDEN"})
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_duplicate_copy_of_same_stored_identifier_fails(self):
        self.assertEqual(1, self.exercise(
            change_rows=lambda rows: rows + [copy.deepcopy(rows[0])])[0])

    def test_absent_stored_record_fails(self):
        self.assertEqual(1, self.exercise(change_rows=lambda rows: [])[0])

    def test_unexpected_stored_identifier_fails(self):
        def change(rows):
            rows[0]["jobDbId"] = "JOB_OTHER"
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_wrong_job_type_fails(self):
        def change(rows):
            rows[0]["jobType"] = "different-job-type"
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_missing_original_idempotency_key_fails(self):
        def change(rows):
            rows[0].pop("idempotencyKey")
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_incorrect_stored_key_fails(self):
        def change(rows):
            rows[0]["idempotencyKey"] = "wrong-key"
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_malformed_collection_row_fails(self):
        self.assertEqual(1, self.exercise(change_rows=lambda rows: [None])[0])

    def test_missing_collection_array_fails(self):
        self.assertEqual(1, self.exercise(change_rows=lambda rows: None)[0])

    def test_truncated_collection_with_higher_total_fails(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "totalCount": 2})[0])

    def test_multi_page_collection_is_not_complete_evidence(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "totalPages": 2})[0])

    def test_wrong_current_page_fails(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "currentPage": 1})[0])

    def test_page_size_below_rows_fails(self):
        self.assertEqual(1, self.exercise(
            add_unrelated=True,
            change_page=lambda p: {**p, "pageSize": 1})[0])

    def test_boolean_pagination_value_fails(self):
        self.assertEqual(1, self.exercise(
            change_page=lambda p: {**p, "totalCount": True})[0])

    def test_failed_read_fails(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_disagreeing_concurrent_post_identifier_fails(self):
        failures, calls = self.exercise(different_response_id=True)
        self.assertEqual(1, failures)
        self.assertEqual(0, len([m for m, _ in calls if m == "GET"]))


    def test_one_missing_status_reply_fails_before_collection(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: (
                {key: value for key, value in row.items() if key != "status"}
                if index == 8 else row))
        self.assertEqual(1, failures)
        self.assertEqual(0, sum(method == "GET" for method, _ in calls))

    def test_one_unknown_status_reply_fails_before_collection(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: (
                {**row, "status": "QUEUED"} if index == 8 else row))
        self.assertEqual(1, failures)
        self.assertEqual(0, sum(method == "GET" for method, _ in calls))

    def test_one_nonstring_status_reply_fails_before_collection(self):
        for invalid in (None, False, 0, [], {}):
            with self.subTest(invalid=invalid):
                failures, calls = self.exercise(
                    mutate_ack=lambda row, index: (
                        {**row, "status": invalid} if index == 8 else row))
                self.assertEqual(1, failures)
                self.assertEqual(
                    0, sum(method == "GET" for method, _ in calls))

    def test_mixed_valid_concurrent_lifecycle_statuses_allowed(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: {
                **row, "status": "RUNNING" if index % 2 else "SUBMITTED"})
        self.assertEqual(0, failures)
        self.assertEqual(1, sum(method == "GET" for method, _ in calls))

    def test_one_corrupted_type_reply_fails_before_collection(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: (
                {**row, "jobType": "analysis"} if index == 8 else row))
        self.assertEqual(1, failures)
        self.assertEqual(0, sum(method == "GET" for method, _ in calls))

    def test_one_missing_type_reply_fails_before_collection(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: (
                {key: value for key, value in row.items() if key != "jobType"}
                if index == 8 else row))
        self.assertEqual(1, failures)
        self.assertEqual(0, sum(method == "GET" for method, _ in calls))

    def test_one_corrupted_key_reply_fails_before_collection(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: (
                {**row, "idempotencyKey": "unrelated"} if index == 8 else row))
        self.assertEqual(1, failures)
        self.assertEqual(0, sum(method == "GET" for method, _ in calls))

    def test_one_missing_key_reply_fails_before_collection(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: (
                {key: value for key, value in row.items()
                 if key != "idempotencyKey"}
                if index == 8 else row))
        self.assertEqual(1, failures)
        self.assertEqual(0, sum(method == "GET" for method, _ in calls))

    def test_one_nonobject_reply_fails_before_collection(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: [] if index == 8 else row)
        self.assertEqual(1, failures)
        self.assertEqual(0, sum(method == "GET" for method, _ in calls))

    def test_extra_server_metadata_on_all_responses_allowed(self):
        failures, calls = self.exercise(
            mutate_ack=lambda row, index: {
                **row, "serverAudit": f"accepted-{index}"})
        self.assertEqual(0, failures)
        self.assertEqual(1, sum(method == "GET" for method, _ in calls))


    def test_unrelated_job_without_type_fails(self):
        self.assertEqual(1, self.exercise(
            change_rows=lambda rows: rows + [
                {"jobDbId": "OTHER", "idempotencyKey": "other-key"}])[0])

    def test_duplicate_unrelated_job_id_fails(self):
        def change(rows):
            rows.extend([
                {"jobDbId": "OTHER", "jobType": "analysis",
                 "idempotencyKey": "other-1", "status": "SUBMITTED"},
                {"jobDbId": "OTHER", "jobType": "analysis",
                 "idempotencyKey": "other-2", "status": "SUBMITTED"},
            ])
            return rows
        self.assertEqual(1, self.exercise(change_rows=change)[0])

    def test_unrelated_job_blank_id_fails(self):
        self.assertEqual(1, self.exercise(
            change_rows=lambda rows: rows + [
                {"jobDbId": "", "jobType": "analysis", "status": "SUBMITTED"}])[0])

    def test_unrelated_job_boolean_key_fails(self):
        self.assertEqual(1, self.exercise(
            change_rows=lambda rows: rows + [
                {"jobDbId": "OTHER", "jobType": "analysis",
                 "idempotencyKey": True, "status": "SUBMITTED"}])[0])

    def test_unrelated_job_optional_key_may_be_missing(self):
        self.assertEqual(0, self.exercise(
            change_rows=lambda rows: rows + [
                {"jobDbId": "OTHER", "jobType": "analysis",
                 "status": "SUBMITTED"}])[0])



if __name__ == "__main__":
    unittest.main()
