#!/usr/bin/env python3
"""Export the BrAPI-GenX endpoint registry into a SQLite database.

NVIDIA Auto Ontology (https://github.com/NVIDIA/auto-ontology) ingests
relational sources (PostgreSQL, MySQL, SQLite, ...). This script turns the
machine-readable BrAPI-GenX endpoint registry into a SQLite catalog that an
Auto Ontology instance can connect to (connection string:
``sqlite:////absolute/path/to/brapi_genx_catalog.db``).

The export is read-only with respect to the registry: it never modifies
``Specification/ENDPOINT-REGISTRY.json``. Re-running overwrites the target DB.

Usage:
    python3 Scripts/exportEndpointRegistryToSqlite.py [--output PATH]
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "Specification" / "ENDPOINT-REGISTRY.json"


def build(db_path: Path) -> None:
    with REGISTRY.open(encoding="utf-8") as f:
        reg = json.load(f)

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE domain_classes (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )
    for code, name in (reg.get("proposedDomainClasses") or {}).items():
        cur.execute("INSERT INTO domain_classes (code, name) VALUES (?, ?)", (code, name))

    cur.execute(
        """
        CREATE TABLE cross_cutting_capabilities (
            code TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )
    for code, name in (reg.get("crossCuttingCapabilities") or {}).items():
        cur.execute(
            "INSERT INTO cross_cutting_capabilities (code, name) VALUES (?, ?)",
            (code, name),
        )

    cur.execute(
        """
        CREATE TABLE operations (
            catalog_id TEXT PRIMARY KEY,
            api_generation TEXT NOT NULL,
            base_path TEXT,
            method TEXT NOT NULL,
            path TEXT NOT NULL,
            operation_name TEXT,
            brapi_module TEXT,
            brapi_tag TEXT,
            primary_domain TEXT,
            classification_basis TEXT,
            classification_review_status TEXT,
            classification_confidence TEXT,
            purpose TEXT,
            source_description TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE operation_capabilities (
            catalog_id TEXT NOT NULL,
            capability_code TEXT NOT NULL,
            FOREIGN KEY (catalog_id) REFERENCES operations (catalog_id)
        )
        """
    )

    for entry in reg.get("entries", []):
        cls = entry.get("classification") or {}
        cur.execute(
            """
            INSERT INTO operations (
                catalog_id, api_generation, base_path, method, path,
                operation_name, brapi_module, brapi_tag, primary_domain,
                classification_basis, classification_review_status,
                classification_confidence, purpose, source_description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.get("catalogId"),
                entry.get("apiGeneration"),
                entry.get("basePath"),
                entry.get("method"),
                entry.get("path"),
                entry.get("operationName"),
                entry.get("brapiModule"),
                entry.get("brapiTag"),
                cls.get("primaryDomain"),
                cls.get("basis"),
                cls.get("reviewStatus"),
                cls.get("confidence"),
                entry.get("purpose"),
                entry.get("sourceDescription"),
            ),
        )
        for cap in cls.get("crossCuttingCapabilities") or []:
            cur.execute(
                "INSERT INTO operation_capabilities (catalog_id, capability_code) VALUES (?, ?)",
                (entry.get("catalogId"), cap),
            )

    cur.execute(
        """
        CREATE TABLE semantic_relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            predicate TEXT,
            object TEXT,
            raw_json TEXT NOT NULL
        )
        """
    )
    for rel in reg.get("semanticRelationships") or []:
        # Store both a best-effort triple extraction and the raw payload.
        subject = rel.get("subject") or rel.get("source") or rel.get("from")
        predicate = rel.get("predicate") or rel.get("relationship") or rel.get("type")
        obj = rel.get("object") or rel.get("target") or rel.get("to")
        cur.execute(
            "INSERT INTO semantic_relationships (subject, predicate, object, raw_json) "
            "VALUES (?, ?, ?, ?)",
            (subject, predicate, obj, json.dumps(rel, sort_keys=True)),
        )

    conn.commit()
    conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(ROOT / "brapi_genx_catalog.db"),
        help="Output SQLite database path (default: ./brapi_genx_catalog.db)",
    )
    args = parser.parse_args()
    out = Path(args.output).resolve()
    build(out)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
