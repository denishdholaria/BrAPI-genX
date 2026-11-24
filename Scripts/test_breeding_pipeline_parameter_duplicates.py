#!/usr/bin/env python3
"""Regression tests for duplicate RFC-154 list-filter parameter identities."""
from __future__ import annotations

import unittest

from check_breeding_pipeline_api_contract import require_unique_parameter_names


class UniqueParametersTests(unittest.TestCase):
    def validate(self, parameters):
        errors = []
        require_unique_parameter_names(parameters, 'Test GET', errors)
        return errors

    def test_unique_query_parameters_pass(self):
        self.assertEqual([], self.validate([
            {'in': 'query', 'name': 'programDbId'},
            {'in': 'query', 'name': 'programServer'},
            {'$ref': '#/components/parameters/pageSize'},
        ]))

    def test_duplicate_authority_filter_fails(self):
        errors = self.validate([
            {'in': 'query', 'name': 'programServer'},
            {'in': 'query', 'name': 'programServer'},
        ])
        self.assertTrue(any('duplicate parameter identity' in error for error in errors), errors)

    def test_duplicate_identifier_filter_fails(self):
        errors = self.validate([
            {'in': 'query', 'name': 'populationDbId'},
            {'in': 'query', 'name': 'populationDbId'},
        ])
        self.assertTrue(any('populationDbId' in error for error in errors), errors)

    def test_duplicate_parameter_reference_fails(self):
        errors = self.validate([
            {'$ref': '#/components/parameters/page'},
            {'$ref': '#/components/parameters/page'},
        ])
        self.assertTrue(any('duplicate parameter identity' in error for error in errors), errors)

    def test_same_name_in_distinct_locations_not_collapsed(self):
        self.assertEqual([], self.validate([
            {'in': 'path', 'name': 'studyDbId'},
            {'in': 'query', 'name': 'studyDbId'},
        ]))

    def test_empty_non_resolved_reference_not_marked_duplicate(self):
        self.assertEqual([], self.validate([{'$ref': ''}, {'$ref': ''}]))


if __name__ == '__main__':
    unittest.main()
