#!/usr/bin/env python3
"""L-25 collection arithmetic, full Job scan and filtered expired confidentiality."""
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
        self.assertEqual(7, len(self.probe["calls"]))
        self.assertEqual(
            ["jobs", "models"],
            [step["assert"]["collection_contains_created"]
             for step in self.probe["calls"][2:4]],
        )
        self.assertIs(True, self.probe["calls"][4]["assert"][
            "filtered_expired_jobs_withheld"])
        self.assertIs(True, self.probe["calls"][5]["assert"][
            "filtered_expired_job_type_withheld"])
        self.assertIs(True, self.probe["calls"][6]["assert"][
            "filtered_job_type_integrity"])

    def exercise(self, modify=None, include_unrelated=False, status=200,
                 job_pages=None, filtered_pages=None, combined_pages=None,
                 type_only_pages=None):
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
            if method == "GET" and path.startswith("/jobs?status=EXPIRED&page="):
                index = int(path.split("page=", 1)[1].split("&", 1)[0])
                if index > 0:
                    return copy.deepcopy(
                        (filtered_pages or {}).get(index, (404, {})))
                value = first_page([{
                    "jobDbId": "JOB_EXPIRED", "jobType": "analysis",
                    "status": "EXPIRED", "result": None}])
                value["metadata"]["pagination"]["pageSize"] = 2
                if modify:
                    value = modify("filtered_jobs", value)
                return status, value
            if (method == "GET"
                    and path.startswith(
                        "/jobs?jobType=germplasm_search&status=EXPIRED&page=")):
                index = int(path.split("page=", 1)[1].split("&", 1)[0])
                if index > 0:
                    return copy.deepcopy(
                        (combined_pages or {}).get(index, (404, {})))
                value = first_page([{
                    "jobDbId": "JOB_EXPIRED_MATCH",
                    "jobType": "germplasm_search", "status": "EXPIRED",
                    "result": None}])
                value["metadata"]["pagination"]["pageSize"] = 2
                if modify:
                    value = modify("combined_jobs", value)
                return status, value
            if (method == "GET"
                    and path.startswith("/jobs?jobType=germplasm_search&page=")):
                index = int(path.split("page=", 1)[1].split("&", 1)[0])
                if index > 0:
                    return copy.deepcopy(
                        (type_only_pages or {}).get(index, (404, {})))
                value = first_page([
                    {"jobDbId": "TYPE_EXPIRED", "jobType": "germplasm_search",
                     "status": "EXPIRED", "result": None},
                    {"jobDbId": "TYPE_COMPLETED", "jobType": "germplasm_search",
                     "status": "COMPLETED", "result": {"value": 5}}])
                if modify:
                    value = modify("type_only_jobs", value)
                return status, value
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
            ("GET", "/jobs?status=EXPIRED&page=0&pageSize=2"),
            ("GET", "/jobs?jobType=germplasm_search&status=EXPIRED&page=0&pageSize=2"),
            ("GET", "/jobs?jobType=germplasm_search&page=0&pageSize=2"),
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
        # An otherwise well-formed later page must not repeat the created
        # submission's key under another Job identifier.
        pagination = {"totalCount": 3, "pageSize": 1, "totalPages": 3}
        seen = {"JOB_PAGE"}
        pages = {
            1: self.job_page(1, {
                "jobDbId": "OTHER_1", "jobType": "analysis", "status": "RUNNING",
                "idempotencyKey": "submitted-key"}),
            2: self.job_page(2, {
                "jobDbId": "OTHER_2", "jobType": "analysis", "status": "RUNNING"}),
        }
        def read(_server, method, path, body=None, token=None):
            return pages[int(path.split("page=", 1)[1].split("&")[0])]
        with mock.patch.object(checker, "http_call", side_effect=read):
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

    def test_filtered_expired_result_leaks_are_rejected(self):
        for leaked in ({"secret": [42]}, {}, [], False, 0):
            with self.subTest(leaked=leaked):
                def change(kind, payload):
                    if kind == "filtered_jobs":
                        payload["result"]["data"][0]["result"] = leaked
                    return payload
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_filtered_wrong_status_and_malformed_rows_rejected(self):
        for row in (
                {"jobDbId": "JOB_EXPIRED", "jobType": "analysis",
                 "status": "COMPLETED", "result": None},
                {"jobDbId": "JOB_EXPIRED", "jobType": "analysis"},
                {"jobDbId": "", "jobType": "analysis", "status": "EXPIRED"},
                {"jobDbId": "JOB_EXPIRED", "jobType": "",
                 "status": "EXPIRED"},
                {"jobDbId": "JOB_EXPIRED", "jobType": "analysis",
                 "status": "EXPIRED", "progress": None},
                None):
            with self.subTest(row=row):
                def change(kind, payload):
                    if kind == "filtered_jobs":
                        payload["result"]["data"] = [row]
                    return payload
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_empty_filtered_collection_is_valid_shape_only(self):
        for total_pages in (0, 1):
            with self.subTest(total_pages=total_pages):
                def change(kind, payload):
                    if kind == "filtered_jobs":
                        payload["result"]["data"] = []
                        payload["metadata"]["pagination"].update(
                            totalCount=0, totalPages=total_pages)
                    return payload
                self.assertEqual(0, self.exercise(modify=change)[0])

    def test_filtered_expired_absent_result_and_null_are_allowed(self):
        def change(kind, payload):
            if kind == "filtered_jobs":
                payload["result"]["data"][0].pop("result")
            return payload
        self.assertEqual(0, self.exercise(modify=change)[0])

    def filtered_three_rows(self, mutate=None):
        def change(kind, payload):
            if kind == "filtered_jobs":
                payload["result"]["data"] = [
                    {"jobDbId": "EXPIRED_1", "jobType": "analysis",
                     "status": "EXPIRED", "result": None},
                    {"jobDbId": "EXPIRED_2", "jobType": "analysis",
                     "status": "EXPIRED"}]
                payload["metadata"]["pagination"].update(
                    totalCount=3, pageSize=2, totalPages=2, currentPage=0)
            return payload
        tail = (200, {
            "result": {"data": [{"jobDbId": "EXPIRED_3",
                                  "jobType": "analysis",
                                  "status": "EXPIRED", "result": None}]},
            "metadata": {"pagination": {"totalCount": 3, "pageSize": 2,
                                       "totalPages": 2, "currentPage": 1}},
        })
        pages = {1: tail}
        if mutate:
            mutate(pages)
        return self.exercise(modify=change, filtered_pages=pages)

    def test_filtered_tail_page_is_retrieved_and_accepted(self):
        failures, requests = self.filtered_three_rows()
        self.assertEqual(0, failures)
        self.assertIn(
            ("GET", "/jobs?status=EXPIRED&page=1&pageSize=2"), requests)

    def test_filtered_tail_leak_fails_even_with_clean_first_page(self):
        for leaked in ({"data": ["secret"]}, [], {}, False, 0):
            with self.subTest(leaked=leaked):
                def change(pages):
                    pages[1][1]["result"]["data"][0]["result"] = leaked
                self.assertEqual(1, self.filtered_three_rows(change)[0])

    def test_filtered_tail_wrong_status_or_duplicate_id_fails(self):
        for changes in (
                {"status": "COMPLETED"}, {"jobDbId": "EXPIRED_1"},
                {"jobType": ""}, {"progress": "0.5"}):
            with self.subTest(changes=changes):
                def change(pages):
                    pages[1][1]["result"]["data"][0].update(changes)
                self.assertEqual(1, self.filtered_three_rows(change)[0])

    def test_filtered_tail_missing_or_malformed_page_fails(self):
        self.assertEqual(1, self.filtered_three_rows(lambda p: p.clear())[0])
        for change in (
                lambda p: p[1][1]["metadata"]["pagination"].update(
                    totalPages=3),
                lambda p: p[1][1]["metadata"]["pagination"].update(
                    currentPage=0),
                lambda p: p[1][1]["result"].update(data=[]),
                lambda p: p.__setitem__(1, (500, {})),
                lambda p: p.__setitem__(1, (200, []))):
            self.assertEqual(1, self.filtered_three_rows(change)[0])

    def test_filtered_first_page_bad_counts_and_truncation_fail(self):
        for bad in ("pageSize", "totalPages", "totalCount", "currentPage"):
            with self.subTest(field=bad):
                def change(kind, payload):
                    if kind == "filtered_jobs":
                        payload["metadata"]["pagination"][bad] = (
                            4 if bad == "totalCount" else
                            1 if bad == "currentPage" else 0)
                    return payload
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_combined_filters_matching_expired_job_passes(self):
        failures, calls = self.exercise()
        self.assertEqual(0, failures)
        self.assertEqual(
            ("GET", "/jobs?jobType=germplasm_search&status=EXPIRED&page=0&pageSize=2"),
            calls[-1])

    def test_combined_filters_reject_wrong_type_even_if_expired(self):
        def change(kind, payload):
            if kind == "combined_jobs":
                payload["result"]["data"][0]["jobType"] = "analysis"
            return payload
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_combined_filters_reject_wrong_status_even_if_type_matches(self):
        def change(kind, payload):
            if kind == "combined_jobs":
                payload["result"]["data"][0]["status"] = "RUNNING"
            return payload
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_combined_filters_reject_expired_result_leak(self):
        for leaked in ({"secret": 1}, {}, [], False, 0):
            with self.subTest(leaked=leaked):
                def change(kind, payload):
                    if kind == "combined_jobs":
                        payload["result"]["data"][0]["result"] = leaked
                    return payload
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_combined_filters_accept_absent_result_and_empty_list(self):
        def omitted(kind, payload):
            if kind == "combined_jobs":
                payload["result"]["data"][0].pop("result")
            return payload
        self.assertEqual(0, self.exercise(modify=omitted)[0])
        for empty_pages in (0, 1):
            with self.subTest(empty_pages=empty_pages):
                def empty(kind, payload):
                    if kind == "combined_jobs":
                        payload["result"]["data"] = []
                        payload["metadata"]["pagination"].update(
                            totalCount=0, totalPages=empty_pages)
                    return payload
                self.assertEqual(0, self.exercise(modify=empty)[0])

    def combined_three_rows(self, change_page=None, change_first=None):
        def first(kind, payload):
            if kind == "combined_jobs":
                payload["result"]["data"] = [
                    {"jobDbId": "COMBINED_1", "jobType": "germplasm_search",
                     "status": "EXPIRED", "result": None},
                    {"jobDbId": "COMBINED_2", "jobType": "germplasm_search",
                     "status": "EXPIRED"}]
                payload["metadata"]["pagination"].update(
                    totalCount=3, pageSize=2, totalPages=2, currentPage=0)
                if change_first:
                    change_first(payload)
            return payload
        pages = {1: (
            200, {
                "result": {"data": [{
                    "jobDbId": "COMBINED_3", "jobType": "germplasm_search",
                    "status": "EXPIRED", "result": None}]},
                "metadata": {"pagination": {
                    "totalCount": 3, "pageSize": 2,
                    "totalPages": 2, "currentPage": 1}},
            }
        )}
        if change_page:
            change_page(pages)
        return self.exercise(modify=first, combined_pages=pages)

    def test_combined_filters_fetch_every_page_with_both_parameters(self):
        failures, calls = self.combined_three_rows()
        self.assertEqual(0, failures)
        self.assertEqual(
            ("GET", "/jobs?jobType=germplasm_search&status=EXPIRED&page=1&pageSize=2"),
            calls[-1])

    def test_combined_filters_tail_wrong_type_and_status_fail(self):
        for changes in (
                {"jobType": "analysis"}, {"status": "RUNNING"},
                {"jobDbId": "COMBINED_1"}, {"progress": None},
                {"result": {"secret": 1}}, {"result": {}},
                {"result": []}, {"result": 0}):
            with self.subTest(changes=changes):
                def change(pages):
                    pages[1][1]["result"]["data"][0].update(changes)
                self.assertEqual(1, self.combined_three_rows(change)[0])

    def test_combined_filters_tail_absent_result_allowed(self):
        def change(pages):
            pages[1][1]["result"]["data"][0].pop("result")
        self.assertEqual(0, self.combined_three_rows(change)[0])

    def test_combined_filters_fail_closed_on_missing_or_bad_pages(self):
        self.assertEqual(1, self.combined_three_rows(
            change_page=lambda pages: pages.clear())[0])
        for change in (
                lambda pages: pages[1][1]["metadata"]["pagination"].update(
                    totalCount=4),
                lambda pages: pages[1][1]["metadata"]["pagination"].update(
                    pageSize=1),
                lambda pages: pages[1][1]["metadata"]["pagination"].update(
                    totalPages=3),
                lambda pages: pages[1][1]["metadata"]["pagination"].update(
                    currentPage=0),
                lambda pages: pages[1][1]["result"].update(data=[]),
                lambda pages: pages.__setitem__(1, (500, {})),
                lambda pages: pages.__setitem__(1, (200, []))):
            self.assertEqual(1, self.combined_three_rows(
                change_page=change)[0])

    def test_combined_filters_first_page_malformed_counts_fail(self):
        for key, value in (
                ("totalCount", 4), ("pageSize", 0),
                ("totalPages", 3), ("currentPage", 1)):
            with self.subTest(key=key):
                def change(payload):
                    payload["metadata"]["pagination"][key] = value
                self.assertEqual(1, self.combined_three_rows(
                    change_first=change)[0])

    def test_type_only_filter_allows_mixed_lifecycle_with_completed_result(self):
        failures, calls = self.exercise()
        self.assertEqual(0, failures)
        self.assertEqual(
            ("GET", "/jobs?jobType=germplasm_search&page=0&pageSize=2"),
            calls[-1])

    def test_type_only_filter_wrong_job_type_fails(self):
        def change(kind, payload):
            if kind == "type_only_jobs":
                payload["result"]["data"][1]["jobType"] = "analysis"
            return payload
        self.assertEqual(1, self.exercise(modify=change)[0])

    def test_type_only_filter_rejects_any_expired_result_leak(self):
        for leaked in ({"secret": 17}, {}, [], False, 0):
            with self.subTest(leaked=leaked):
                def change(kind, payload):
                    if kind == "type_only_jobs":
                        payload["result"]["data"][0]["result"] = leaked
                    return payload
                self.assertEqual(1, self.exercise(modify=change)[0])

    def test_type_only_filter_missing_expired_result_allowed(self):
        def change(kind, payload):
            if kind == "type_only_jobs":
                payload["result"]["data"][0].pop("result")
            return payload
        self.assertEqual(0, self.exercise(modify=change)[0])

    def test_type_only_filter_empty_pages_valid(self):
        for pages in (0, 1):
            with self.subTest(pages=pages):
                def change(kind, payload):
                    if kind == "type_only_jobs":
                        payload["result"]["data"] = []
                        payload["metadata"]["pagination"].update(
                            totalCount=0, pageSize=2, totalPages=pages)
                    return payload
                self.assertEqual(0, self.exercise(modify=change)[0])

    def test_type_only_filter_invalid_optional_job_fields_rejected(self):
        for change_fields in (
                {"status": "UNKNOWN"}, {"status": None},
                {"progress": None}, {"createdAt": "2026-11-26"},
                {"idempotencyKey": False}, {"jobDbId": ""},
                {"jobType": ""}):
            with self.subTest(change_fields=change_fields):
                def change(kind, payload):
                    if kind == "type_only_jobs":
                        payload["result"]["data"][1].update(change_fields)
                    return payload
                self.assertEqual(1, self.exercise(modify=change)[0])

    def type_only_multi_page(self, change_tail=None, change_first=None):
        """Three type-only pages with distinct valid lifecycle statuses."""
        def first(kind, payload):
            if kind == "type_only_jobs":
                payload["metadata"]["pagination"].update(
                    totalCount=5, pageSize=2, totalPages=3, currentPage=0)
                if change_first:
                    change_first(payload)
            return payload
        def page(index, rows):
            return (200, {
                "result": {"data": rows},
                "metadata": {"pagination": {
                    "totalCount": 5, "pageSize": 2,
                    "totalPages": 3, "currentPage": index}}})
        pages = {
            1: page(1, [
                {"jobDbId": "TYPE_RUNNING", "jobType": "germplasm_search",
                 "status": "RUNNING", "result": {"partial": True}},
                {"jobDbId": "TYPE_FAILED", "jobType": "germplasm_search",
                 "status": "FAILED", "result": {"error": "validation"}}]),
            2: page(2, [
                {"jobDbId": "TYPE_TAIL_EXPIRED", "jobType": "germplasm_search",
                 "status": "EXPIRED"}]),
        }
        if change_tail:
            change_tail(pages)
        return self.exercise(modify=first, type_only_pages=pages)

    def test_type_only_reads_all_pages_and_keeps_filter(self):
        failures, calls = self.type_only_multi_page()
        self.assertEqual(0, failures)
        self.assertEqual([
            ("GET", "/jobs?jobType=germplasm_search&page=1&pageSize=2"),
            ("GET", "/jobs?jobType=germplasm_search&page=2&pageSize=2"),
        ], calls[-2:])

    def test_type_only_tail_expired_result_leaks_fail(self):
        for leaked in ({"hidden": 1}, {}, [], False, 0):
            with self.subTest(leaked=leaked):
                def change(pages):
                    pages[2][1]["result"]["data"][0]["result"] = leaked
                self.assertEqual(1, self.type_only_multi_page(change_tail=change)[0])

    def test_type_only_tail_expired_null_result_passes(self):
        def change(pages):
            pages[2][1]["result"]["data"][0]["result"] = None
        self.assertEqual(0, self.type_only_multi_page(change_tail=change)[0])

    def test_type_only_tail_wrong_type_and_duplicate_identity_fail(self):
        for update in (
                {"jobType": "analysis"}, {"jobDbId": "TYPE_EXPIRED"},
                {"status": "QUEUED"}, {"progress": 2.0},
                {"idempotencyKey": False}):
            with self.subTest(update=update):
                def change(pages):
                    pages[1][1]["result"]["data"][0].update(update)
                self.assertEqual(1, self.type_only_multi_page(change_tail=change)[0])

    def test_type_only_missing_and_corrupt_later_page_fail(self):
        for edit in (
                lambda pages: pages.pop(1),
                lambda pages: pages.pop(2),
                lambda pages: pages[2][1]["result"].update(data=[]),
                lambda pages: pages[1][1]["metadata"]["pagination"].update(
                    totalCount=6),
                lambda pages: pages[2][1]["metadata"]["pagination"].update(
                    currentPage=0),
                lambda pages: pages[1][1]["metadata"]["pagination"].update(
                    pageSize=1),
                lambda pages: pages[2][1]["metadata"]["pagination"].update(
                    totalPages=2),
                lambda pages: pages.__setitem__(2, (500, {})),
                lambda pages: pages.__setitem__(1, (200, []))):
            self.assertEqual(1, self.type_only_multi_page(change_tail=edit)[0])

    def test_type_only_first_page_pagination_corruption_rejected(self):
        for field, value in (
                ("totalCount", 4), ("pageSize", 0),
                ("totalPages", 2), ("currentPage", 1)):
            with self.subTest(field=field):
                def change(payload):
                    payload["metadata"]["pagination"][field] = value
                self.assertEqual(1, self.type_only_multi_page(
                    change_first=change)[0])

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
