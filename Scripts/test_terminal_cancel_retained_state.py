#!/usr/bin/env python3
"""Mission 135: rejecting a terminal cancellation must preserve terminal state."""
from __future__ import annotations

from pathlib import Path
from unittest import mock
import unittest

import yaml
import checkGenXConformance as checker

ROOT = Path(__file__).resolve().parents[1]
CONF = ROOT / "Specification" / "BrAPI-GenX" / "Conformance"


class TerminalCancelRetainedStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = yaml.safe_load((CONF / "probes.yaml").read_text(encoding="utf-8"))
        cls.probe = next(p for p in doc["probes"] if p["id"] == "L-03")

    def test_registered_probe_requires_readback(self):
        self.assertEqual(3, len(self.probe["calls"]))
        self.assertIs(True, self.probe["calls"][0]["wait_terminal"])
        self.assertIs(True, self.probe["calls"][1]["assert"]["rejected"])
        self.assertIs(True, self.probe["calls"][2]["assert"]["terminal_state_unchanged"])

    def exercise(self, baseline_status="COMPLETED", retrieved_status="COMPLETED",
                 baseline_id="JOB_TERMINAL", retrieved_id="JOB_TERMINAL",
                 delete_status=400, read_status=200, result_type="normal",
                 baseline_mutation=None, readback_mutation=None):
        calls = []
        original = {}

        def terminal_record(job_id, state):
            record = {
                "jobDbId": job_id,
                "status": state,
                "jobType": original["jobType"],
                "idempotencyKey": original["idempotencyKey"],
            }
            if state == "COMPLETED":
                record["result"] = {
                    "data": [{"germplasmDbId": "G-001", "evidence": {
                        "source": "original", "revision": 1}}],
                }
            return record

        def terminal_reply(_server, _job_id, _token,
                           expected_type=None, expected_key=None):
            self.assertEqual(original["jobType"], expected_type)
            self.assertEqual(original["idempotencyKey"], expected_key)
            row = terminal_record(baseline_id, baseline_status)
            if baseline_mutation is not None:
                baseline_mutation(row)
            return {"result": row}

        def fake_http(_server, method, path, body=None, token=None):
            calls.append((method, path))
            if len(calls) == 1:
                self.assertEqual(("POST", "/jobs"), (method, path))
                original.update(body)
                return 202, {"result": {
                    "jobDbId": "JOB_TERMINAL",
                    "jobType": body["jobType"],
                    "idempotencyKey": body["idempotencyKey"], "status": "SUBMITTED"}}
            if len(calls) == 2:
                self.assertEqual(("DELETE", "/jobs/JOB_TERMINAL"), (method, path))
                return delete_status, {}
            if len(calls) == 3:
                self.assertEqual(("GET", "/jobs/JOB_TERMINAL"), (method, path))
                result = terminal_record(retrieved_id, retrieved_status)
                if readback_mutation is not None:
                    readback_mutation(result)
                if result_type == "missing":
                    result = None
                if result_type == "malformed":
                    result = [result]
                return read_status, {"result": result}
            self.fail("unexpected extra network call")

        outcome = checker.Results()
        with (mock.patch.object(checker, "http_call", side_effect=fake_http),
              mock.patch.object(checker, "wait_terminal",
                                side_effect=terminal_reply)):
            checker.run_live_probe(
                "http://example.test/genx/v1", self.probe,
                {"conformance_dir": str(CONF)}, outcome, None, None)
        return outcome.failures, calls

    def test_completed_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise()[0])

    def test_failed_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise(
            baseline_status="FAILED", retrieved_status="FAILED")[0])

    def test_cancelled_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise(
            baseline_status="CANCELLED", retrieved_status="CANCELLED")[0])

    def test_expired_job_unchanged_passes(self):
        self.assertEqual(0, self.exercise(
            baseline_status="EXPIRED", retrieved_status="EXPIRED")[0])

    def test_expired_job_with_null_result_allowed_both_readbacks(self):
        def redact(row):
            row["result"] = None
        self.assertEqual(0, self.exercise(
            baseline_status="EXPIRED", retrieved_status="EXPIRED",
            baseline_mutation=redact, readback_mutation=redact)[0])

    def test_expired_job_with_same_leaked_result_rejected(self):
        # Both snapshots match exactly: unchanged-result checks alone
        # previously accepted this confidential expired result.
        def leak(row):
            row["result"] = {"data": [{"secret": "expired-output"}]}
        self.assertEqual(1, self.exercise(
            baseline_status="EXPIRED", retrieved_status="EXPIRED",
            baseline_mutation=leak, readback_mutation=leak)[0])

    def test_expired_job_with_empty_object_result_rejected(self):
        def leak(row):
            row["result"] = {}
        self.assertEqual(1, self.exercise(
            baseline_status="EXPIRED", retrieved_status="EXPIRED",
            baseline_mutation=leak, readback_mutation=leak)[0])

    def test_expired_job_with_leak_only_before_delete_rejected(self):
        def leak(row):
            row["result"] = {"data": [1]}
        self.assertEqual(1, self.exercise(
            baseline_status="EXPIRED", retrieved_status="EXPIRED",
            baseline_mutation=leak)[0])

    def test_expired_job_with_leak_only_after_delete_rejected(self):
        def leak(row):
            row["result"] = {"data": [1]}
        self.assertEqual(1, self.exercise(
            baseline_status="EXPIRED", retrieved_status="EXPIRED",
            readback_mutation=leak)[0])

    def test_terminal_to_cancelled_mutation_fails(self):
        self.assertEqual(1, self.exercise(retrieved_status="CANCELLED")[0])

    def test_terminal_to_submitted_mutation_fails(self):
        self.assertEqual(1, self.exercise(retrieved_status="SUBMITTED")[0])

    def test_terminal_to_failed_mutation_fails(self):
        self.assertEqual(1, self.exercise(retrieved_status="FAILED")[0])

    def test_wrong_original_job_id_fails(self):
        self.assertEqual(1, self.exercise(baseline_id="JOB_WRONG")[0])

    def test_wrong_retrieved_job_id_fails(self):
        self.assertEqual(1, self.exercise(retrieved_id="JOB_WRONG")[0])

    def test_nonterminal_baseline_rejected(self):
        self.assertEqual(1, self.exercise(
            baseline_status="RUNNING", retrieved_status="RUNNING")[0])

    def test_missing_baseline_status_rejected(self):
        self.assertEqual(1, self.exercise(baseline_status=None)[0])

    def test_missing_retrieved_status_rejected(self):
        self.assertEqual(1, self.exercise(retrieved_status=None)[0])

    def test_missing_get_result_rejected(self):
        self.assertEqual(1, self.exercise(result_type="missing")[0])

    def test_malformed_get_result_rejected(self):
        self.assertEqual(1, self.exercise(result_type="malformed")[0])

    def test_unavailable_readback_rejected(self):
        self.assertEqual(1, self.exercise(read_status=404)[0])

    def test_successful_delete_fails_before_readback(self):
        failures, calls = self.exercise(delete_status=200)
        self.assertEqual(1, failures)
        self.assertEqual(2, len(calls))

    def test_server_failure_is_not_a_terminal_cancel_rejection(self):
        for code in (500, 503):
            with self.subTest(code=code):
                failures, calls = self.exercise(delete_status=code)
                self.assertEqual(1, failures)
                self.assertEqual(2, len(calls))

    def test_conflict_client_status_still_rejected(self):
        self.assertEqual(0, self.exercise(delete_status=409)[0])


    def test_rejected_delete_cannot_change_job_type(self):
        def mutate(row):
            row["jobType"] = "analysis"
        self.assertEqual(1, self.exercise(readback_mutation=mutate)[0])

    def test_rejected_delete_cannot_remove_job_type(self):
        def mutate(row):
            row.pop("jobType")
        self.assertEqual(1, self.exercise(readback_mutation=mutate)[0])

    def test_rejected_delete_cannot_change_idempotency_key(self):
        def mutate(row):
            row["idempotencyKey"] = "fabricated-key"
        self.assertEqual(1, self.exercise(readback_mutation=mutate)[0])

    def test_rejected_delete_cannot_remove_idempotency_key(self):
        def mutate(row):
            row.pop("idempotencyKey")
        self.assertEqual(1, self.exercise(readback_mutation=mutate)[0])

    def test_completed_result_cannot_change_with_same_status(self):
        def mutate(row):
            row["result"]["data"][0]["germplasmDbId"] = "G-REWRITTEN"
        self.assertEqual(1, self.exercise(readback_mutation=mutate)[0])

    def test_nested_completed_result_cannot_change(self):
        def mutate(row):
            row["result"]["data"][0]["evidence"]["revision"] = 2
        self.assertEqual(1, self.exercise(readback_mutation=mutate)[0])

    def test_completed_result_cannot_disappear(self):
        def mutate(row):
            row.pop("result")
        self.assertEqual(1, self.exercise(readback_mutation=mutate)[0])

    def test_completed_result_cannot_appear_after_rejected_delete(self):
        def mutate(row):
            row["result"] = {"data": []}
        self.assertEqual(1, self.exercise(
            baseline_status="FAILED", retrieved_status="FAILED",
            readback_mutation=mutate)[0])

    def test_terminal_baseline_cannot_mismatch_original_type(self):
        def mutate(row):
            row["jobType"] = "analysis"
        self.assertEqual(1, self.exercise(baseline_mutation=mutate)[0])

    def test_terminal_baseline_cannot_mismatch_original_key(self):
        def mutate(row):
            row["idempotencyKey"] = "fabricated-key"
        self.assertEqual(1, self.exercise(baseline_mutation=mutate)[0])

    def test_invalid_optional_progress_before_delete_rejected(self):
        for invalid in (-0.1, 1.1, None, True, "0.5", float("nan")):
            with self.subTest(invalid=invalid):
                def mutate(row):
                    row["progress"] = invalid
                self.assertEqual(1, self.exercise(
                    baseline_mutation=mutate)[0])

    def test_invalid_optional_progress_after_delete_rejected(self):
        for invalid in (-0.1, 1.1, None, False, "0.5", float("inf")):
            with self.subTest(invalid=invalid):
                def mutate(row):
                    row["progress"] = invalid
                self.assertEqual(1, self.exercise(
                    readback_mutation=mutate)[0])

    def test_invalid_optional_timestamp_before_delete_rejected(self):
        for name in ("createdAt", "updatedAt", "expiresAt"):
            with self.subTest(name=name):
                def mutate(row):
                    row[name] = "2026-11-25T12:00:00"
                self.assertEqual(1, self.exercise(
                    baseline_mutation=mutate)[0])

    def test_invalid_optional_timestamp_after_delete_rejected(self):
        for invalid in (None, False, "2026-02-30T12:00:00Z",
                        "2026-11-25T12:00:00"):
            with self.subTest(invalid=invalid):
                def mutate(row):
                    row["updatedAt"] = invalid
                self.assertEqual(1, self.exercise(
                    readback_mutation=mutate)[0])

    def test_valid_optional_fields_before_and_after_delete_allowed(self):
        def before(row):
            row["progress"] = 0.4
            row["createdAt"] = "2026-11-25T12:00:00Z"
            row["updatedAt"] = "2026-11-25T12:00:10+05:30"

        def after(row):
            row["progress"] = 1.0
            row["createdAt"] = "2026-11-25T12:00:00Z"
            row["updatedAt"] = "2026-11-25T12:00:12-0600"

        self.assertEqual(0, self.exercise(
            baseline_mutation=before, readback_mutation=after)[0])

    def test_extra_server_metadata_allowed(self):
        def mutate(row):
            row["observedAt"] = "2026-11-25T10:00:00Z"
        self.assertEqual(0, self.exercise(readback_mutation=mutate)[0])



    def test_terminal_poll_rejects_error_even_with_completed_body(self):
        completed = {"result": {"jobDbId": "JOB_TERMINAL",
                                "status": "COMPLETED"}}
        for status in (404, 503):
            with self.subTest(status=status):
                with mock.patch.object(checker, "http_call",
                                       return_value=(status, completed)) as call:
                    with self.assertRaisesRegex(
                            ValueError, f"terminal job polling GET returned HTTP {status}"):
                        checker.wait_terminal("http://example.test/genx/v1",
                                              "JOB_TERMINAL", None)
                self.assertEqual(1, call.call_count)

    def test_terminal_poll_rejects_redirect_body(self):
        completed = {"result": {"jobDbId": "JOB_TERMINAL",
                                "status": "COMPLETED"}}
        with mock.patch.object(checker, "http_call",
                               return_value=(302, completed)):
            with self.assertRaisesRegex(ValueError, "returned HTTP 302"):
                checker.wait_terminal("http://example.test/genx/v1",
                                      "JOB_TERMINAL", None)

    def test_terminal_poll_accepts_completed_success(self):
        completed = {"result": {"jobDbId": "JOB_TERMINAL",
                                "jobType": "germplasm_search",
                                "status": "COMPLETED"}}
        with mock.patch.object(checker, "http_call",
                               return_value=(200, completed)) as call:
            self.assertEqual(
                completed,
                checker.wait_terminal("http://example.test/genx/v1",
                                      "JOB_TERMINAL", None))
        self.assertEqual(1, call.call_count)



    def test_terminal_poll_rejects_wrong_completed_job_id(self):
        different = {"result": {"jobDbId": "JOB_UNRELATED",
                                "status": "COMPLETED"}}
        with mock.patch.object(checker, "http_call",
                               return_value=(200, different)) as call:
            with self.assertRaisesRegex(
                    ValueError, "did not return requested job JOB_TERMINAL"):
                checker.wait_terminal("http://example.test/genx/v1",
                                      "JOB_TERMINAL", None)
        self.assertEqual(1, call.call_count)

    def test_terminal_poll_rejects_missing_completed_job_id(self):
        missing = {"result": {"status": "COMPLETED"}}
        with mock.patch.object(checker, "http_call",
                               return_value=(200, missing)):
            with self.assertRaisesRegex(ValueError, "did not return requested job"):
                checker.wait_terminal("http://example.test/genx/v1",
                                      "JOB_TERMINAL", None)

    def test_terminal_poll_rejects_malformed_job_object(self):
        malformed = {"result": ["JOB_TERMINAL", "COMPLETED"]}
        with mock.patch.object(checker, "http_call",
                               return_value=(200, malformed)):
            with self.assertRaisesRegex(ValueError, "did not return requested job"):
                checker.wait_terminal("http://example.test/genx/v1",
                                      "JOB_TERMINAL", None)

    def test_terminal_poll_rejects_wrong_nonterminal_job_id(self):
        different = {"result": {"jobDbId": "JOB_OTHER",
                                "status": "RUNNING"}}
        with mock.patch.object(checker, "http_call",
                               return_value=(200, different)) as call:
            with self.assertRaisesRegex(ValueError, "did not return requested job"):
                checker.wait_terminal("http://example.test/genx/v1",
                                      "JOB_TERMINAL", None)
        self.assertEqual(1, call.call_count)



    @staticmethod
    def _poll_job(job, responses=None, expected_type=None, expected_key=None):
        if responses is None:
            responses = [(200, {"result": job})]
        with mock.patch.object(checker, "http_call", side_effect=responses) as call:
            with mock.patch("time.sleep", return_value=None):
                try:
                    value = checker.wait_terminal(
                        "http://example.test/genx/v1", "JOB_TERMINAL", None,
                        expected_type, expected_key
                    )
                except ValueError as exc:
                    return None, str(exc), call.call_count
        return value, None, call.call_count

    def test_terminal_poll_rejects_expired_result_disclosure(self):
        for leaked in ({"data": [42]}, {}, [], "", 0, False):
            with self.subTest(leaked=leaked):
                row = {"jobDbId": "JOB_TERMINAL",
                       "jobType": "germplasm_search", "status": "EXPIRED",
                       "result": leaked}
                value, error, count = self._poll_job(row)
                self.assertIsNone(value)
                self.assertIn("exposed expired result", error)
                self.assertEqual(1, count)

    def test_terminal_poll_accepts_expired_withheld_result(self):
        for marker in ("absent", None):
            with self.subTest(marker=marker):
                row = {"jobDbId": "JOB_TERMINAL",
                       "jobType": "germplasm_search", "status": "EXPIRED"}
                if marker is None:
                    row["result"] = None
                value, error, count = self._poll_job(row)
                self.assertIsNone(error)
                self.assertEqual({"result": row}, value)
                self.assertEqual(1, count)

    def test_terminal_poll_with_valid_nonexpired_result_allowed(self):
        for status in ("COMPLETED", "FAILED", "CANCELLED"):
            with self.subTest(status=status):
                row = {"jobDbId": "JOB_TERMINAL",
                       "jobType": "germplasm_search", "status": status,
                       "result": {"data": [42]}}
                value, error, count = self._poll_job(row)
                self.assertIsNone(error)
                self.assertEqual({"result": row}, value)
                self.assertEqual(1, count)

    def test_terminal_poll_rejects_missing_or_invalid_required_job_type(self):
        for wrong in (None, "", False, 2, []):
            with self.subTest(wrong=wrong):
                row = {"jobDbId": "JOB_TERMINAL", "status": "COMPLETED"}
                if wrong is not None:
                    row["jobType"] = wrong
                value, error, count = self._poll_job(row)
                self.assertIsNone(value)
                self.assertIn("schema-invalid Job", error)
                self.assertEqual(1, count)

    def test_terminal_poll_rejects_missing_or_unknown_lifecycle_status(self):
        for wrong in (None, "QUEUED", False, 5, {}):
            with self.subTest(wrong=wrong):
                row = {"jobDbId": "JOB_TERMINAL",
                       "jobType": "germplasm_search"}
                if wrong is not None:
                    row["status"] = wrong
                value, error, count = self._poll_job(row)
                self.assertIsNone(value)
                self.assertIn("schema-invalid Job", error)
                self.assertEqual(1, count)

    def test_terminal_poll_rejects_malformed_optional_progress(self):
        for wrong in (None, False, "0.5", -0.1, 1.01,
                      float("nan"), float("inf")):
            with self.subTest(wrong=wrong):
                row = {"jobDbId": "JOB_TERMINAL",
                       "jobType": "germplasm_search",
                       "status": "COMPLETED", "progress": wrong}
                value, error, count = self._poll_job(row)
                self.assertIsNone(value)
                self.assertIn("schema-invalid Job", error)
                self.assertEqual(1, count)

    def test_terminal_poll_rejects_bad_optional_date_time(self):
        for field in ("createdAt", "updatedAt", "expiresAt"):
            for wrong in (None, "2026-11-25",
                          "2026-11-25T12:00:00",
                          "2026-02-30T12:00:00Z"):
                with self.subTest(field=field, wrong=wrong):
                    row = {"jobDbId": "JOB_TERMINAL",
                           "jobType": "germplasm_search",
                           "status": "COMPLETED", field: wrong}
                    value, error, count = self._poll_job(row)
                    self.assertIsNone(value)
                    self.assertIn("schema-invalid Job", error)
                    self.assertEqual(1, count)

    def test_terminal_poll_rejects_nonstring_optional_key(self):
        row = {"jobDbId": "JOB_TERMINAL",
               "jobType": "germplasm_search",
               "status": "COMPLETED", "idempotencyKey": True}
        value, error, count = self._poll_job(row)
        self.assertIsNone(value)
        self.assertIn("schema-invalid Job", error)
        self.assertEqual(1, count)

    def test_intermediate_poll_rejects_invalid_status_before_retry(self):
        row = {"jobDbId": "JOB_TERMINAL",
               "jobType": "germplasm_search",
               "status": "QUEUED"}
        value, error, count = self._poll_job(row)
        self.assertIsNone(value)
        self.assertIn("schema-invalid Job", error)
        self.assertEqual(1, count)

    def test_intermediate_poll_rejects_bad_progress_before_retry(self):
        row = {"jobDbId": "JOB_TERMINAL",
               "jobType": "germplasm_search",
               "status": "RUNNING", "progress": -1}
        value, error, count = self._poll_job(row)
        self.assertIsNone(value)
        self.assertIn("schema-invalid Job", error)
        self.assertEqual(1, count)

    def test_intermediate_poll_accepts_valid_running_then_completed(self):
        running = {"jobDbId": "JOB_TERMINAL",
                   "jobType": "germplasm_search", "status": "RUNNING",
                   "progress": 0.25, "createdAt": "2026-11-25T12:00:00Z"}
        done = {"jobDbId": "JOB_TERMINAL",
                "jobType": "germplasm_search", "status": "COMPLETED",
                "progress": 1.0, "updatedAt": "2026-11-25T12:01:00-0600"}
        terminal = (200, {"result": done})
        value, error, count = self._poll_job(
            None, [(200, {"result": running}), terminal]
        )
        self.assertIsNone(error)
        self.assertEqual({"result": done}, value)
        self.assertEqual(2, count)

    def test_terminal_poll_rejects_changed_original_type(self):
        row = {"jobDbId": "JOB_TERMINAL", "jobType": "analysis",
               "status": "COMPLETED", "idempotencyKey": "client-key"}
        value, error, count = self._poll_job(
            row, expected_type="germplasm_search", expected_key="client-key")
        self.assertIsNone(value)
        self.assertIn("changed original type/key", error)
        self.assertEqual(1, count)

    def test_terminal_poll_rejects_missing_or_changed_original_key(self):
        for invalid in (None, "changed-key"):
            with self.subTest(invalid=invalid):
                row = {"jobDbId": "JOB_TERMINAL",
                       "jobType": "germplasm_search", "status": "COMPLETED"}
                if invalid is not None:
                    row["idempotencyKey"] = invalid
                value, error, count = self._poll_job(
                    row, expected_type="germplasm_search",
                    expected_key="client-key")
                self.assertIsNone(value)
                self.assertIn("changed original type/key", error)
                self.assertEqual(1, count)

    def test_intermediate_poll_changed_original_type_or_key_fails_early(self):
        terminal = {"jobDbId": "JOB_TERMINAL",
                    "jobType": "germplasm_search",
                    "idempotencyKey": "client-key", "status": "COMPLETED"}
        for corrupted in (
            {**terminal, "status": "RUNNING", "jobType": "analysis"},
            {**terminal, "status": "RUNNING", "idempotencyKey": "wrong-key"},
            {k: v for k, v in {**terminal, "status": "RUNNING"}.items()
             if k != "idempotencyKey"},
        ):
            with self.subTest(corrupted=corrupted):
                value, error, count = self._poll_job(
                    None,
                    [(200, {"result": corrupted}), (200, {"result": terminal})],
                    expected_type="germplasm_search",
                    expected_key="client-key")
                self.assertIsNone(value)
                self.assertIn("changed original type/key", error)
                self.assertEqual(1, count)

    def test_polling_preserves_original_binding_across_valid_transition(self):
        first = {"jobDbId": "JOB_TERMINAL",
                 "jobType": "germplasm_search",
                 "idempotencyKey": "client-key",
                 "status": "RUNNING"}
        done = {**first, "status": "COMPLETED"}
        value, error, count = self._poll_job(
            None, [(200, {"result": first}), (200, {"result": done})],
            expected_type="germplasm_search", expected_key="client-key")
        self.assertIsNone(error)
        self.assertEqual({"result": done}, value)
        self.assertEqual(2, count)

    def test_terminal_poll_allows_valid_optional_fields(self):
        for progress in (0, 0.6, 1.0):
            with self.subTest(progress=progress):
                row = {"jobDbId": "JOB_TERMINAL",
                       "jobType": "germplasm_search",
                       "status": "COMPLETED", "progress": progress,
                       "createdAt": "2026-11-25T12:00:00Z",
                       "updatedAt": "2026-11-25T12:01:00+05:30",
                       "expiresAt": "2026-11-25T12:02:00-0600",
                       "idempotencyKey": "client-key"}
                value, error, count = self._poll_job(row)
                self.assertIsNone(error)
                self.assertEqual({"result": row}, value)
                self.assertEqual(1, count)


if __name__ == "__main__":
    unittest.main()
