# BrAPI-GenX and NVIDIA Auto Ontology: Integration Guide

**Status:** proposed / non-normative working note  
**Date:** 2026-11-26  
**Scope:** how NVIDIA Auto Ontology (https://github.com/NVIDIA/auto-ontology) can
serve as the semantic/knowledge layer for BrAPI-GenX's agricultural knowledge
fabric, and how to connect it to BrAPI-GenX artifacts.

## 1. What each project is

- **BrAPI-GenX** is an independently governed specification and conformance
  project. It extends BrAPI v2.1 toward an agricultural knowledge fabric while
  preserving identity, authority, context, and provenance of original records.
  Its machine-readable catalog is `Specification/ENDPOINT-REGISTRY.json`
  (663 operations: 201 BrAPI v2.1 + 462 proposed GenX).
- **NVIDIA Auto Ontology** is a Python framework that builds a semantic,
  graph-based reasoning layer over relational data: terms (concepts), column
  attributes (mappings), relationships (joins), SQL attributes (measures), and
  certification. It exposes context to agents via MCP, REST, and CLI, and
  imports/exports models as Apache Ossie YAML or its own YAML.

Auto Ontology is a *runtime semantic layer*, not a specification. BrAPI-GenX is a
*specification and conformance* project. They are complementary: BrAPI-GenX defines
the contract; Auto Ontology can give agents a governed, queryable meaning layer over
implementations of that contract.

## 2. Candidate integration points

1. **Catalog ingestion.** Export `ENDPOINT-REGISTRY.json` to a relational
   source Auto Ontology can ingest, so an agent can ask "which GenX operations
   touch germplasm?" or "which operations are cross-cutting capability C2?".
   Provided by `Scripts/exportEndpointRegistryToSqlite.py`.
2. **Semantic governance alignment.** BrAPI-GenX's governed semantic-neighbor
   relationships (`semanticRelationships` in the registry) map to Auto
   Ontology's relationship elements. A future export could publish them as
   Ossie YAML terms/relationships.
3. **Agent access.** An Auto Ontology MCP server pointed at a BrAPI-GenX
   implementation's database gives agents trusted business meaning for breeding
   data, with SQL and join paths returned per answer.
4. **Conformance evidence.** Auto Ontology's `check_answerable`/`ask_question`
   can be used as an independent agent-facing check that a BrAPI-GenX
   implementation's data is semantically reachable.

## 3. Quickstart: connect Auto Ontology to the BrAPI-GenX catalog

1. Clone Auto Ontology and bring it up (Docker Compose or Helm). See
   https://github.com/NVIDIA/auto-ontology and its `skills/nvidia-ontology-setup`.

   ```sh
   git clone https://github.com/NVIDIA/auto-ontology.git
   cd auto-ontology
   cp .env.example .env   # set DEFAULT_MODELS_API_KEY (nvapi-...) etc.
   ```

2. Export the BrAPI-GenX catalog to SQLite:

   ```sh
   cd /path/to/brapi-genx
   python3 Scripts/exportEndpointRegistryToSqlite.py --output /tmp/brapi_genx_catalog.db
   ```

3. Add the SQLite file as a connection in Auto Ontology (Settings -> Connections,
   or `CONNECTION_STRINGS=sqlite:////tmp/brapi_genx_catalog.db`), then ingest
   and compile. The `operations`, `domain_classes`, `cross_cutting_capabilities`,
   `operation_capabilities`, and `semantic_relationships` tables become terms.

4. Query via MCP/REST/CLI, e.g. "List GenX operations classified as primary
   domain D1 (Germplasm) with confidence high."

## 4. Boundaries and non-claims

- This guide does not change any BrAPI-GenX specification, RFC maturity, or
  conformance result. Auto Ontology is an external runtime; adopting it is not
  a BrAPI-GenX normative decision.
- The SQLite export is a derived artifact (gitignored `*.db`); regenerate with
  the script. The script is the source of truth for the export shape.
- Auto Ontology requires model endpoints (NVIDIA NIM or OpenAI-compatible) and,
  for the full stack, Docker. Neither is bundled with BrAPI-GenX.
- No production readiness is claimed for either project's reference runtime.

## 5. Open questions

- Should BrAPI-GenX publish an Ossie YAML semantic model for a core subset
  (Germplasm, Study, ObservationVariable, Observation) so Auto Ontology can
  import it directly? (Requires maintainer decision; not done here.)
- Which BrAPI-GenX implementation database (if any) should be the first
  Auto Ontology ingestion target? (Likely a reference server with durable
  storage; current reference servers are in-memory.)
