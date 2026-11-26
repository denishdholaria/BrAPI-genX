#!/usr/bin/env python3
"""Mission 139: L-25 pagination counts must match returned first-page rows."""
from __future__ import annotations

import copy
from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class CollectionPaginationArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        document = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in document["probes"] if p["id"] == "L-25")

    def test_registered_collections_are_both_required(self):
        self.assertEqual(4, len(self.probe["calls"]))
        self.assertEqual(
            ["jobs", "models"],
            [step["assert"]["collection_contains_created"]
             for step in self.probe["calls"][-2:]],
        )

    def exercise(self, modify=None, include_unrelated=False, status=200,
                 job_pages=None):
        requests = []
        submitted_model = {}
        job_body = {}

        def first_page(rows):
            page_size = max(len(rows), 1)
            return {
                "metadata": {"pagination": {
                    "totalCount": len(rows), "pageSize": page_size,
                    "totalPages": 1, "currentPage": 0,
                }},
                "result": {"data": rows},
            }

        def fake_http(_server, method, path, body=None, token=None):
            requests.append((method, path))
            if len(requests) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                job_body.update(copy.deepcopy(body))
                return 202, {"result": {
                    "jobDbId": "JOB_PAGE", "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"], "status": "SUBMITTED"}}
            if len(requests) == 2:
                self.assertEqual(("POST", "/models"), (method, path))
                submitted_model.update(copy.deepcopy(body))
                return 200, {"result": copy.deepcopy(body)}
            if len(requests) == 3:
                self.assertEqual(("GET", "/jobs"), (method, path))
                rows = [{"jobDbId": "JOB_PAGE", "jobType": job_body["jobType"],
                         "idempotencyKey": job_body["idempotencyKey"],
                         "status": "SUBMITTED"}]
                if include_unrelated:
                    rows.append({"jobDbId": "OTHER", "jobType": "analysis",
                                 "status": "RUNNING"})
                value = first_page(rows)
                if modify:
                    value = modify("jobs", value)
                return status, value
            if method == "GET" and path.startswith("/jobs?page="):
                index = int(path.split("page=", 1)[1].split("&", 1)[0])
                if job_pages is None:
                    return 404, {}
                return copy.deepcopy(job_pages.get(index, (404, {})))
            if method == "GET" and path == "/models":
                rows = [copy.deepcopy(submitted_model)]
                if include_unrelated:
                    rows.append({**copy.deepcopy(submitted_model),
                                 "modelDbId": "other:model:unrelated"})
                value = first_page(rows)
                if modify:
                    value = modify("models", value)
                return status, value
            self.fail("unexpected extra request")

        outcome = checker.Results()
        with mock.patch.object(checker, "http_call", side_effect=fake_http):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None
            )
        return outcome.failures, requests

    @staticmethod
    def mutate_page(kind, target, field, value):
        if kind == "jobs":
            target["metadata"]["pagination"][field] = value
        return target

    def test_exact_single_page_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_unrelated_records_do_not_fail(self):
        self.assertEqual(0, self.exercise(include_unrelated=True)[0])

    def test_inflated_total_count_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", 50))[0])

    def test_inflated_page_size_with_missing_rows_fails(self):
        # One returned row and totalCount=3 with pageSize=100 means a
        # nominally complete first page is underfilled.
        def change(kind, data):
            if kind == "jobs":
                data["metadata"]["pagination"].update(totalCount=3, pageSize=100)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_incorrect_total_pages_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalPages", 2))[0])

    def test_wrong_current_page_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["metadata"]["pagination"].update(
                    totalCount=2, pageSize=1, totalPages=2, currentPage=1
                )
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_invalid_page_zero_count_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", 0))[0])

    def test_zero_page_size_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "pageSize", 0))[0])

    def test_negative_count_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", -1))[0])

    def test_bool_total_fails(self):
        self.assertEqual(1, self.exercise(
            modify=lambda k, p: self.mutate_page(k, p, "totalCount", True))[0])

    def test_missing_pagination_field_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["metadata"]["pagination"].pop("pageSize")
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_malformed_page_rows_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"].append(None)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_extra_rows_beyond_page_size_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"].append({"jobDbId": "MORE"})
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_model_collection_inconsistent_totals_fails(self):
        def change(kind, data):
            if kind == "models":
                data["metadata"]["pagination"]["totalCount"] = 9
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_missing_created_model_fails(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"][0]["modelDbId"] = "other:model:missing"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_missing_created_job_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0]["jobDbId"] = "OTHER"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_failed_collection_get_fails(self):
        self.assertEqual(1, self.exercise(status=500)[0])


    @staticmethod
    def refresh_first_page(target):
        """Ensure malformed identity cases still have valid pagination arithmetic."""
        rows = target["result"]["data"]
        target["metadata"]["pagination"].update(
            totalCount=len(rows), pageSize=max(len(rows), 1),
            totalPages=1, currentPage=0)
        return target

    def test_created_job_invalid_timestamp_fails(self):
        for field in ("createdAt", "updatedAt", "expiresAt"):
            with self.subTest(field=field):
                def change(kind, data):
                    if kind == "jobs":
                        data["result"]["data"][0][field] = "2026-11-25T12:00:00"
                    return data
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_unrelated_visible_job_invalid_timestamp_fails(self):
        def change(kind, data):
            return self.append_unrelated_job(kind, data, {
                "jobDbId": "OTHER", "jobType": "analysis",
                "expiresAt": "2026-02-30T12:00:00Z"})
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_visible_job_timestamps_with_valid_offsets_pass(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0]["createdAt"] = (
                    "2026-11-25T12:00:00Z")
                return self.append_unrelated_job(kind, data, {
                    "jobDbId": "OTHER", "jobType": "analysis",
                    "updatedAt": "2026-11-25T12:00:00-0600"})
            return data
        self.assertEqual(0, self.exercise(modify=change)[0])

    def test_created_expired_job_result_leak_rejected(self):
        for leaked in ({"data": [42]}, {}, [], False, 0):
            with self.subTest(leaked=leaked):
                def change(kind, data):
                    if kind == "jobs":
                        row = data["result"]["data"][0]
                        row["status"] = "EXPIRED"
                        row["result"] = leaked
                    return data
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_unrelated_visible_expired_job_result_leak_rejected(self):
        def change(kind, data):
            return self.append_unrelated_job(kind, data, {
                "jobDbId": "OTHER", "jobType": "analysis",
                "status": "EXPIRED", "result": {"data": ["secret"]}})
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_visible_expired_job_with_null_or_absent_result_allowed(self):
        for marker in ("absent", None):
            with self.subTest(marker=marker):
                def change(kind, data):
                    if kind == "jobs":
                        row = data["result"]["data"][0]
                        row["status"] = "EXPIRED"
                        if marker is None:
                            row["result"] = None
                    return data
                self.assertEqual(0, self.exercise(modify=change)[0])

    def test_created_job_optional_progress_rejects_invalid_values(self):
        for progress in (-0.01, 1.01, None, False, "0.8", float("inf")):
            with self.subTest(progress=progress):
                def change(kind, data):
                    if kind == "jobs":
                        data["result"]["data"][0]["progress"] = progress
                    return data
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_unrelated_visible_job_optional_progress_rejects_invalid(self):
        def change(kind, data):
            return self.append_unrelated_job(kind, data, {
                "jobDbId": "OTHER", "jobType": "analysis",
                "progress": float("nan")})
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_valid_visible_job_progress_endpoints_allowed(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0]["progress"] = 0
                return self.append_unrelated_job(kind, data, {
                    "jobDbId": "OTHER", "jobType": "analysis",
                    "progress": 1.0})
            return data
        self.assertEqual(0, self.exercise(modify=change)[0])

    def test_created_job_missing_status_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0].pop("status")
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_created_job_unknown_status_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0]["status"] = "QUEUED"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_unrelated_job_missing_status_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data = self.append_unrelated_job(kind, data, {
                    "jobDbId": "OTHER", "jobType": "analysis"})
                data["result"]["data"][-1].pop("status")
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_unrelated_job_invalid_status_fails(self):
        for wrong in ("QUEUED", None, False, 0, [], {}):
            with self.subTest(wrong=wrong):
                def change(kind, data):
                    return self.append_unrelated_job(kind, data, {
                        "jobDbId": "OTHER", "jobType": "analysis",
                        "status": wrong})
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_valid_mixed_first_page_job_states_pass(self):
        self.assertEqual(0, self.exercise(include_unrelated=True)[0])

    def test_created_job_type_changed_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0]["jobType"] = "unrelated-job-type"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_created_job_idempotency_key_changed_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0]["idempotencyKey"] = "different-key"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_created_job_idempotency_key_omitted_fails(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"][0].pop("idempotencyKey")
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_duplicate_job_identifier_fails_with_consistent_pagination(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"].append(
                    copy.deepcopy(data["result"]["data"][0]))
                self.refresh_first_page(data)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_duplicate_job_key_on_distinct_identifier_fails(self):
        def change(kind, data):
            if kind == "jobs":
                other = copy.deepcopy(data["result"]["data"][0])
                other["jobDbId"] = "JOB_DIFFERENT"
                data["result"]["data"].append(other)
                self.refresh_first_page(data)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    @classmethod
    def append_unrelated_job(cls, kind, payload, job):
        if kind == "jobs":
            payload["result"]["data"].append({"status": "SUBMITTED", **job})
            cls.refresh_first_page(payload)
        return payload

    def test_duplicate_unrelated_job_identifiers_fail(self):
        def change(kind, data):
            if kind == "jobs":
                data["result"]["data"].extend([
                    {"jobDbId": "UNRELATED", "jobType": "analysis",
                     "idempotencyKey": "other-key-1", "status": "SUBMITTED"},
                    {"jobDbId": "UNRELATED", "jobType": "analysis",
                     "idempotencyKey": "other-key-2", "status": "RUNNING"},
                ])
                self.refresh_first_page(data)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_missing_unrelated_job_identifier_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_job(k, p, {"jobType": "analysis"}))[0])

    def test_blank_unrelated_job_identifier_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_job(k, p, {
                "jobDbId": "", "jobType": "analysis"}))[0])

    def test_missing_unrelated_job_type_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_job(k, p, {"jobDbId": "UNRELATED"}))[0])

    def test_blank_unrelated_job_type_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_job(k, p, {
                "jobDbId": "UNRELATED", "jobType": ""}))[0])

    def test_nonstring_unrelated_job_key_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_job(k, p, {
                "jobDbId": "UNRELATED", "jobType": "analysis",
                "idempotencyKey": False}))[0])

    def test_unrelated_job_without_optional_key_allowed(self):
        self.assertEqual(0, self.exercise(modify=lambda k, p:
            self.append_unrelated_job(k, p, {
                "jobDbId": "UNRELATED", "jobType": "analysis"}))[0])

    def test_distinct_unrelated_job_with_key_allowed(self):
        self.assertEqual(0, self.exercise(modify=lambda k, p:
            self.append_unrelated_job(k, p, {
                "jobDbId": "UNRELATED", "jobType": "analysis",
                "idempotencyKey": "other-key"}))[0])

    def paged_jobs(self, change_page=None, missing_page=None):
        """Exercise real L-25 dispatch against three advertised Job pages."""
        def first(kind, payload):
            if kind == "jobs":
                payload["metadata"]["pagination"].update(
                    totalCount=3, pageSize=1, totalPages=3, currentPage=0)
            return payload

        pages = {
            1: self.job_page(1, {
                "jobDbId": "HISTORY_EXPIRED", "jobType": "analysis",
                "status": "EXPIRED", "result": None}),
            2: self.job_page(2, {
                "jobDbId": "HISTORY_RUNNING", "jobType": "analysis",
                "status": "RUNNING", "idempotencyKey": "unrelated-key"}),
        }
        if change_page:
            change_page(pages)
        if missing_page is not None:
            pages.pop(missing_page)
        return self.exercise(modify=first, job_pages=pages)

    @staticmethod
    def job_page(index, row):
        return 200, {
            "result": {"data": [row]},
            "metadata": {"pagination": {
                "totalCount": 3, "pageSize": 1, "totalPages": 3,
                "currentPage": index,
            }},
        }

    def test_multi_page_jobs_reconstructs_all_pages_and_withholds_expired(self):
        failures, requests = self.paged_jobs()
        self.assertEqual(0, failures)
        self.assertEqual([
            ("POST", "/jobs"), ("POST", "/models"), ("GET", "/jobs"),
            ("GET", "/jobs?page=1&pageSize=1"),
            ("GET", "/jobs?page=2&pageSize=1"), ("GET", "/models"),
        ], requests)

    def test_unread_job_tail_is_not_accepted(self):
        for missing in (1, 2):
            with self.subTest(missing=missing):
                self.assertEqual(1, self.paged_jobs(missing_page=missing)[0])

    def test_expired_result_leak_on_any_later_job_page_fails(self):
        for page_index in (1, 2):
            for leaked in ({"secret": [42]}, {}, [], False, 0):
                with self.subTest(page=page_index, leaked=leaked):
                    def change(pages):
                        row = pages[page_index][1]["result"]["data"][0]
                        row["status"] = "EXPIRED"
                        row["result"] = leaked
                    self.assertEqual(1, self.paged_jobs(change_page=change)[0])

    def test_expired_tail_result_absent_is_allowed(self):
        def change(pages):
            pages[1][1]["result"]["data"][0].pop("result")
            pages[2][1]["result"]["data"][0]["status"] = "EXPIRED"
            pages[2][1]["result"]["data"][0]["result"] = None
        self.assertEqual(0, self.paged_jobs(change_page=change)[0])

    def test_duplicate_job_identity_across_pages_fails(self):
        def change(pages):
            pages[2][1]["result"]["data"][0]["jobDbId"] = "HISTORY_EXPIRED"
        self.assertEqual(1, self.paged_jobs(change_page=change)[0])

    def test_original_key_repeated_on_tail_page_fails(self):
        # Even if an implementation reuses an original submission's key
        # under another job ID, L-25 cannot report a single created effect.
        def change(pages):
            pages[2][1]["result"]["data"][0]["idempotencyKey"] = (
                "unused-placeholder")
        # Replace with submitted original key from the first-page test fixture
        # through a local wrapper around the HTTP transport.
        original_http = checker.http_call
        def with_duplicate_key(server, method, path, body=None, token=None):
            return original_http(server, method, path, body=body, token=token)
        # The helper itself verifies duplicate original keys when available;
        # verify it independently with an explicit original key here.
        pagination = {"totalCount": 3, "pageSize": 1, "totalPages": 3}
        seen = {"JOB_PAGE"}
        pages = {1: self.job_page(1, {
            "jobDbId": "OTHER_1", "jobType": "analysis", "status": "RUNNING",
            "idempotencyKey": "submitted-key"}), 2: self.job_page(2, {
            "jobDbId": "OTHER_2", "jobType": "analysis", "status": "RUNNING"})}
        with mock.patch.object(checker, "http_call", side_effect=lambda _, m, p,
                               body=None, token=None: pages[int(
                                   p.split("page=", 1)[1].split("&")[0])]):
            self.assertIsNotNone(checker.job_collection_tail_problem(
                "http://example.test", None, pagination, seen,
                "JOB_PAGE", "submitted-key"))

    def test_later_page_pagination_and_transport_errors_fail(self):
        for field, bad in (
                ("totalCount", 4), ("pageSize", 2), ("totalPages", 2),
                ("currentPage", 0), ("currentPage", True)):
            with self.subTest(field=field, bad=bad):
                def change(pages):
                    pages[2][1]["metadata"]["pagination"][field] = bad
                self.assertEqual(1, self.paged_jobs(change_page=change)[0])
        for bad in ([], {}, None):
            with self.subTest(bad=bad):
                self.assertEqual(1, self.paged_jobs(
                    change_page=lambda pages:
                    pages.__setitem__(2, (200, bad)))[0])
        self.assertEqual(1, self.paged_jobs(change_page=lambda pages:
            pages.__setitem__(2, (500, {})))[0])

    def test_later_page_malformed_job_or_missing_rows_fail(self):
        for row in ({}, {"jobDbId": "ANOTHER", "jobType": "analysis"},
                    {"jobDbId": "ANOTHER", "jobType": "analysis",
                     "status": "QUEUED"}, None):
            with self.subTest(row=row):
                def change(pages):
                    pages[2][1]["result"]["data"] = [row]
                self.assertEqual(1, self.paged_jobs(change_page=change)[0])
        self.assertEqual(1, self.paged_jobs(change_page=lambda pages:
            pages[2][1]["result"].update(data=[]))[0])

    def test_duplicate_model_version_fails_with_consistent_pagination(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"].append(
                    copy.deepcopy(data["result"]["data"][0]))
                self.refresh_first_page(data)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    @classmethod
    def append_unrelated_model(cls, kind, payload, model):
        if kind == "models":
            payload["result"]["data"].append(model)
            cls.refresh_first_page(payload)
        return payload

    def test_duplicate_unrelated_model_version_fails(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"].extend([
                    {"modelDbId": "other:model:duplicate", "modelVersion": "5"},
                    {"modelDbId": "other:model:duplicate", "modelVersion": "5"},
                ])
                self.refresh_first_page(data)
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_unrelated_model_missing_identifier_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_model(k, p, {"modelVersion": "5"}))[0])

    def test_unrelated_model_blank_identifier_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_model(k, p, {
                "modelDbId": "", "modelVersion": "5"}))[0])

    def test_unrelated_model_missing_version_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_model(k, p, {
                "modelDbId": "other:model:missing"}))[0])

    def test_unrelated_model_blank_version_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_model(k, p, {
                "modelDbId": "other:model:blank", "modelVersion": ""}))[0])

    def test_unrelated_model_nonstring_version_fails(self):
        self.assertEqual(1, self.exercise(modify=lambda k, p:
            self.append_unrelated_model(k, p, {
                "modelDbId": "other:model:invalid", "modelVersion": False}))[0])

    def test_unrelated_model_distinct_identifier_same_version_allowed(self):
        def change(kind, data):
            if kind == "models":
                original_version = data["result"]["data"][0]["modelVersion"]
                return self.append_unrelated_model(kind, data, {
                    "modelDbId": "other:model:valid",
                    "modelVersion": original_version})
            return data
        self.assertEqual(0, self.exercise(modify=change)[0])

    def test_valid_model_first_page_with_more_pages_allowed(self):
        def change(kind, data):
            if kind == "models":
                data["metadata"]["pagination"].update(
                    totalCount=4, pageSize=1, totalPages=4, currentPage=0)
            return data
        self.assertEqual(0, self.exercise(modify=change)[0])

    def test_changed_model_artifact_digest_fails(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"][0]["artifactDigest"] = "0" * 64
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_changed_model_nested_metrics_fails(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"][0]["metrics"]["rmse"] = 2.3
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_changed_model_nested_provenance_fails(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"][0]["provenance"]["actor"] = "actor:other"
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_missing_model_original_field_fails(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"][0].pop("trainingDataDigest")
            return data
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_extra_server_managed_model_field_allowed(self):
        def change(kind, data):
            if kind == "models":
                data["result"]["data"][0]["serverReviewedAt"] = "2026-11-25"
            return data
        self.assertEqual(0, self.exercise(modify=change)[0])

    def test_unrelated_model_version_is_allowed(self):
        def change(kind, data):
            if kind == "models":
                other = copy.deepcopy(data["result"]["data"][0])
                other["modelVersion"] = "8"
                data["result"]["data"].append(other)
                self.refresh_first_page(data)
            return data
        self.assertEqual(0, self.exercise(modify=change)[0])


if __name__ == "__main__":
    unittest.main()
