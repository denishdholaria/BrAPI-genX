#!/usr/bin/env python3
"""Concurrency guards and non-normative diagnostics for GenX job idempotency."""

import importlib.util
import json
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "Scripts" / "genx_test_server.py"
SPEC = importlib.util.spec_from_file_location("genx_test_server_under_test", SERVER_PATH)
SERVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SERVER)

Store = SERVER.Store
canonical = SERVER.canonical


class JobIdempotencyTests(unittest.TestCase):
    def setUp(self):
        self.store = Store(delay=0)

    def test_same_key_same_canonical_body_replays_one_job(self):
        body = canonical({"jobType": "analysis", "parameters": {"x": 1}})
        first, first_status = self.store.submit_idempotent("analysis", {"x": 1}, "key-1", body)
        replay, replay_status = self.store.submit_idempotent("analysis", {"x": 1}, "key-1", body)
        self.assertEqual(first_status, "created")
        self.assertEqual(replay_status, "replay")
        self.assertEqual(first["jobDbId"], replay["jobDbId"])
        self.assertEqual(self.store.counter, 1)

    def test_same_key_different_body_conflicts_without_new_job(self):
        first_body = canonical({"jobType": "analysis", "parameters": {"x": 1}})
        different_body = canonical({"jobType": "analysis", "parameters": {"x": 2}})
        _, first_status = self.store.submit_idempotent("analysis", {"x": 1}, "key-1", first_body)
        job, second_status = self.store.submit_idempotent("analysis", {"x": 2}, "key-1", different_body)
        self.assertEqual(first_status, "created")
        self.assertIsNone(job)
        self.assertEqual(second_status, "conflict")
        self.assertEqual(self.store.counter, 1)

    def test_concurrent_same_key_creates_exactly_one_job(self):
        callers = 48
        barrier = threading.Barrier(callers)
        body = canonical({"jobType": "analysis", "parameters": {"x": 7}})
        results = []
        errors = []
        lock = threading.Lock()

        def submit():
            try:
                barrier.wait(timeout=5)
                result = self.store.submit_idempotent("analysis", {"x": 7}, "shared-key", body)
                with lock:
                    results.append(result)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=submit) for _ in range(callers)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

        self.assertFalse(errors, repr(errors))
        self.assertTrue(all(not thread.is_alive() for thread in threads), "thread did not finish")
        self.assertEqual(len(results), callers)
        self.assertEqual(sum(status == "created" for _, status in results), 1)
        self.assertEqual(sum(status == "replay" for _, status in results), callers - 1)
        self.assertEqual(len({job["jobDbId"] for job, _ in results}), 1)
        self.assertEqual(self.store.counter, 1)

    def test_concurrent_different_keys_create_distinct_jobs(self):
        callers = 24
        barrier = threading.Barrier(callers)
        body = canonical({"jobType": "analysis", "parameters": {"x": 9}})
        results = []
        errors = []
        lock = threading.Lock()

        def submit(index):
            try:
                barrier.wait(timeout=5)
                result = self.store.submit_idempotent("analysis", {"x": 9}, f"key-{index}", body)
                with lock:
                    results.append(result)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=submit, args=(index,)) for index in range(callers)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

        self.assertFalse(errors, repr(errors))
        self.assertTrue(all(not thread.is_alive() for thread in threads), "thread did not finish")
        self.assertEqual(sum(status == "created" for _, status in results), callers)
        self.assertEqual(len({job["jobDbId"] for job, _ in results}), callers)
        self.assertEqual(self.store.counter, callers)

    def test_concurrent_same_key_different_bodies_has_one_winner(self):
        callers_per_body = 12
        callers = callers_per_body * 2
        barrier = threading.Barrier(callers)
        body_a = canonical({"jobType": "analysis", "parameters": {"x": "A"}})
        body_b = canonical({"jobType": "analysis", "parameters": {"x": "B"}})
        results = []
        errors = []
        lock = threading.Lock()

        def submit(label, body):
            try:
                barrier.wait(timeout=5)
                result = self.store.submit_idempotent("analysis", {"x": label}, "shared-key", body)
                with lock:
                    results.append((label, result))
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = []
        for _ in range(callers_per_body):
            threads.append(threading.Thread(target=submit, args=("A", body_a)))
            threads.append(threading.Thread(target=submit, args=("B", body_b)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=10)

        self.assertFalse(errors, repr(errors))
        self.assertTrue(all(not thread.is_alive() for thread in threads), "thread did not finish")
        created = [(label, result) for label, result in results if result[1] == "created"]
        self.assertEqual(len(created), 1)
        winner = created[0][0]
        losers = [(label, result) for label, result in results if label != winner]
        self.assertEqual(len(losers), callers_per_body)
        self.assertTrue(all(result[1] == "conflict" for _, result in losers))
        winner_results = [(label, result) for label, result in results if label == winner]
        self.assertEqual(sum(result[1] == "replay" for _, result in winner_results), callers_per_body - 1)
        self.assertEqual(self.store.counter, 1)

    def test_legacy_prototype_compares_parsed_canonical_body_not_raw_request_bytes(self):
        # Diagnostic only, not a standard requirement: current handler parses
        # JSON and then hashes/computes equality on this Python serialization.
        raw_a = '{"jobType":"analysis","parameters":{"a":1,"b":2}}'
        raw_b = '{ "parameters" : {"b":2, "a":1}, "jobType":"analysis" }'
        parsed_a = json.loads(raw_a)
        parsed_b = json.loads(raw_b)
        self.assertNotEqual(raw_a.encode("utf-8"), raw_b.encode("utf-8"))
        self.assertEqual(canonical(parsed_a), canonical(parsed_b))
        _, first_status = self.store.submit_idempotent(
            "analysis", parsed_a["parameters"], "body-key", canonical(parsed_a)
        )
        _, next_status = self.store.submit_idempotent(
            "analysis", parsed_b["parameters"], "body-key", canonical(parsed_b)
        )
        self.assertEqual(first_status, "created")
        self.assertEqual(next_status, "replay")
        self.assertEqual(self.store.counter, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
