#!/usr/bin/env python3
"""Reject false agreement when two reference servers return the same wrong status."""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import sys
import unittest
from unittest import mock

import genx_differential_check as differential


class ExpectedStatusDifferentialTests(unittest.TestCase):
    # The nine requests in the RFC-001/RFC-004 subset, in checker order.
    EXPECTED = (200, 202, 200, 409, 400, 200, 200, 200, 202)

    def run_mocked(self, statuses):
        self.assertEqual(18, len(statuses))
        responses = iter(statuses)

        def call(_server, _method, path, body=None):
            status = next(responses)
            document = {
                "metadata": {"pagination": {}, "status": [], "datafiles": []},
                "result": {"capabilities": []} if path == "/serverinfo" else {},
            }
            return status, document

        capture = io.StringIO()
        with mock.patch.object(differential, "http_call", side_effect=call), \
                mock.patch.object(sys, "argv", [
                    "genx_differential_check.py",
                    "--a", "http://left/genx/v1",
                    "--b", "http://right/genx/v1",
                ]), redirect_stdout(capture):
            result = differential.main()
        self.assertEqual([], list(responses), "differential skipped calls")
        return result, capture.getvalue()

    def test_expected_statuses_with_equal_payloads_pass(self):
        statuses = [status for expected in self.EXPECTED
                    for status in (expected, expected)]
        result, output = self.run_mocked(statuses)
        self.assertEqual(0, result, output)
        self.assertIn("differential: 9/9 steps agree", output)

    def test_two_equal_but_incorrect_conflict_responses_fail(self):
        statuses = [status for expected in self.EXPECTED
                    for status in (expected, expected)]
        statuses[6:8] = [200, 200]  # Conflict step must return 409.
        result, output = self.run_mocked(statuses)
        self.assertEqual(1, result)
        self.assertIn("expected HTTP 409, got 200 vs 200", output)

    def test_one_sided_wrong_replay_response_fails(self):
        statuses = [status for expected in self.EXPECTED
                    for status in (expected, expected)]
        statuses[5] = 500  # Third request, second implementation.
        result, output = self.run_mocked(statuses)
        self.assertEqual(1, result)
        self.assertIn("expected HTTP 200, got 200 vs 500", output)

    def test_matching_internal_errors_do_not_count_as_agreement(self):
        result, output = self.run_mocked([500] * 18)
        self.assertEqual(1, result)
        self.assertIn("differential: 0/9 steps agree", output)


if __name__ == "__main__":
    unittest.main()
