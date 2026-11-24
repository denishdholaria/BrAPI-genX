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

    def test_partial_removal_from_same_operation_is_permitted(self):
        baseline = copy.deepcopy(BASELINE)
        baseline["registryOnlyNeighbors"][0]["neighbors"] = ["genx.first", "genx.second", "genx.third"]
        current = copy.deepcopy(baseline)
        current["registryOnlyNeighbors"][0]["neighbors"] = ["genx.first", "genx.third"]
        self.assertEqual([], regression_errors(baseline, current))

    def test_reordering_historical_neighbors_is_not_new_drift(self):
        baseline = copy.deepcopy(BASELINE)
        baseline["registryOnlyNeighbors"][0]["neighbors"] = ["genx.first", "genx.second"]
        current = copy.deepcopy(baseline)
        current["registryOnlyNeighbors"][0]["neighbors"].reverse()
        self.assertEqual([], regression_errors(baseline, current))

    def test_replacing_one_existing_neighbor_fails(self):
        baseline = copy.deepcopy(BASELINE)
        baseline["registryOnlyNeighbors"][0]["neighbors"] = ["genx.first", "genx.second"]
        current = copy.deepcopy(baseline)
        current["registryOnlyNeighbors"][0]["neighbors"] = ["genx.first", "genx.third"]
        self.assertTrue(any('genx.third' in x for x in regression_errors(baseline, current)))

    def test_moving_neighbor_to_another_source_is_new_drift(self):
        current = copy.deepcopy(BASELINE)
        current["registryOnlyNeighbors"][0]["catalogId"] = "genx.another"
        self.assertTrue(any('genx.another' in x for x in regression_errors(BASELINE, current)))

    def test_duplicate_edge_cannot_bypass_regression(self):
        current = copy.deepcopy(BASELINE)
        current["registryOnlyNeighbors"][0]["neighbors"].append("genx.legacy")
        self.assertTrue(any('registryOnlyNeighbors' in x for x in regression_errors(BASELINE, current)))

    def test_invalid_edge_record_fails_closed(self):
        current = copy.deepcopy(BASELINE)
        current["registryOnlyNeighbors"][0]["neighbors"] = [None]
        with self.assertRaisesRegex(ValueError, 'invalid neighbor'):
            regression_errors(BASELINE, current)

    def test_invalid_edge_list_fails_closed(self):
        current = copy.deepcopy(BASELINE)
        current["registryOnlyNeighbors"][0]["neighbors"] = 'genx.legacy'
        with self.assertRaisesRegex(ValueError, 'neighbor list'):
            regression_errors(BASELINE, current)


if __name__ == "__main__":
    unittest.main()
