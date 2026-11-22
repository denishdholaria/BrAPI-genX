#!/usr/bin/env python3
"""Mutation tests for registry/source descriptive-drift non-regression gates."""
from __future__ import annotations

import copy
import unittest

from check_registry_drift_regression import regression_errors


BASELINE = {
    "errors": [],
    "mismatches": [
        {"catalogId": "genx.example", "field": "sourceDescription",
         "source": "authoritative source", "registry": "historical description"}
    ],
    "registryOnlyNeighbors": [
        {"catalogId": "genx.other", "module": "Other", "neighbors": ["genx.legacy"]}
    ],
}


class RegistryDriftRegressionTests(unittest.TestCase):
    def test_identical_baseline_passes(self):
        self.assertEqual([], regression_errors(BASELINE, copy.deepcopy(BASELINE)))

    def test_removing_historical_discrepancies_is_permitted(self):
        current = copy.deepcopy(BASELINE)
        current["mismatches"].clear()
        current["registryOnlyNeighbors"].clear()
        self.assertEqual([], regression_errors(BASELINE, current))

    def test_new_source_registry_divergence_fails(self):
        current = copy.deepcopy(BASELINE)
        current["mismatches"].append({
            "catalogId": "genx.second", "field": "operationName",
            "source": "source", "registry": "inaccurate"})
        self.assertTrue(any("New or changed mismatches" in error
                            for error in regression_errors(BASELINE, current)))

    def test_changed_existing_divergence_fails(self):
        current = copy.deepcopy(BASELINE)
        current["mismatches"][0]["registry"] = "newly divergent text"
        self.assertTrue(regression_errors(BASELINE, current))

    def test_new_unreviewed_neighbor_fails(self):
        current = copy.deepcopy(BASELINE)
        current["registryOnlyNeighbors"][0]["neighbors"].append("genx.unreviewed")
        self.assertTrue(any("registryOnlyNeighbors" in error
                            for error in regression_errors(BASELINE, current)))

    def test_source_error_fails_even_if_baseline_contains_it(self):
        baseline = copy.deepcopy(BASELINE)
        baseline["errors"] = ["missing source operation"]
        current = copy.deepcopy(baseline)
        self.assertTrue(any("Source audit error" in error
                            for error in regression_errors(baseline, current)))


if __name__ == "__main__":
    unittest.main()
