#!/usr/bin/env python3
"""Generate BrAPI-GenX endpoint documentation from the canonical JSON registry."""
from __future__ import annotations
import argparse, difflib, json, sys
from posixpath import relpath
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "Specification" / "ENDPOINT-REGISTRY.json"
CATALOGUE = ROOT / "Specification" / "ENDPOINT-CATALOG.md"
CROSSWALK = ROOT / "Specification" / "BIJMANTRA-CROSSWALK.md"
GENX_CATALOGUE = ROOT / "Specification" / "BrAPI-GenX" / "GENX-ENDPOINT-CATALOG.md"
BT = chr(96)
MODULES = ["BrAPI-Core", "BrAPI-Germplasm", "BrAPI-Genotyping", "BrAPI-Phenotyping"]
DOMAINS = {
 "D1":"Germplasm and Biological Resources",
 "D2":"Breeding Programs and Experimental Design",
 "D3":"Genotyping and Molecular Genomics",
 "D4":"Phenotyping and Plant Observations",
 "D5":"Environment, Agroecology and Field Context",
 "D6":"Crop Production and Material Operations",
 "D7":"Scientific Analysis, Models and Derived Evidence",
}
CAPS = {
 "C1":"Identity, versioning and capability discovery",
 "C2":"Provenance, evidence and uncertainty",
 "C3":"Asynchronous execution and idempotency",
 "C4":"Scientific terminology governance",
 "C5":"Data exchange, publication and access",
 "C6":"Artifact integrity and external references",
 "C7":"Streaming and temporal aggregation",
 "C8":"Contract conformance and governance",
 "C9":"Security, authority and tenancy",
}
RUST = [
 ("Breeding crosses","BrAPI v2.1 GET/POST /crosses","Rust GET/POST /api/v2/breeding/crosses","Related breeding concept; route roots and contracts differ. No wire-equivalence claim."),
 ("Germplasm identity/passport","BrAPI Germplasm germplasm and passport resources","Rust /api/v2/germplasm/accessions","Candidate relationship to accession identity; payloads, identity authority, and operations must be compared."),
 ("Seed-lot movement","BrAPI SeedLotTransaction at /seedlots/transactions and /seedlots/{seedLotDbId}/transactions","Rust /api/v2/seed-inventory/adjustments","Related material-operations area only. Adjustment is not proven equivalent to a transaction or GenX ledger entry."),
 ("Phenotype observations","BrAPI /observations and /observationunits","Rust /api/v2/phenotype/observations and /api/v2/phenotype/units","Potential domain correspondence; unit identities, variables, studies, value semantics, and response contracts require explicit mapping."),
 ("Scientific terminology","BrAPI /variables, /traits, /methods, /scales","Rust /api/v2/ontology/{variables,traits,methods,scales}","Related terminology responsibilities; object models and lifecycle rules are not asserted to be interchangeable."),
 ("Breeding and trial context","BrAPI /programs, /trials, /studies, /seasons, /locations","Rust /api/v2/trials/{programs,studies,seasons,trials,locations}","Related domain surfaces under a different boundary; compare object semantics and authority before reuse."),
 ("Asynchronous scientific work","GenX /genx/v1/jobs; model inference is a declared job type","Rust /api/v2/compute/jobs and /api/v2/polyglot/jobs","Potentially complementary execution surfaces; no equivalent identifiers, lifecycle mapping, or safe result conversion is established."),
]

def m(v):
    if v is None: return "—"
    return str(v).replace("|", r"\|").replace("\r\n","\n").replace("\r","\n").strip() or "—"

def lst(v):
    return ", ".join(m(x) for x in v) if isinstance(v,list) and v else "—"

def block(lines, label, value):
    if value is None or not str(value).strip(): return
    lines.append("**" + label + ":**")
    for part in str(value).replace("\r\n","\n").replace("\r","\n").split("\n"):
        lines.append("> " + part if part else ">")

def source_url(src):
    return "https://github.com/" + src.get("repository","") + "/blob/" + quote(str(src.get("ref","")),safe="/._-") + "/" + quote(str(src.get("path","")),safe="/._-")

def domain(e):
    c=e.get("classification") or {}; d=c.get("primaryDomain"); out=[]
    out.append(d+" — "+DOMAINS[d] if d in DOMAINS else "No primary domain assigned; cross-cutting or review required")
    if c.get("contextualDomains"): out.append("Context-dependent: "+", ".join(x+" — "+DOMAINS.get(x,x) for x in c["contextualDomains"]))
    if c.get("crossCuttingCapabilities"): out.append("Facets: "+", ".join(x+" — "+CAPS.get(x,x) for x in c["crossCuttingCapabilities"]))
    if c.get("basis"): out.append("Crosswalk basis: "+str(c["basis"]))
    if c.get("reason"): out.append("Crosswalk note: "+str(c["reason"]))
    return "; ".join(out)

def render_entry(e, catalogue=CATALOGUE):
    lines=["### "+m(e.get("method"))+" "+BT+m(e.get("basePath","")+e.get("path",""))+BT,""]
    lines.append("- **Catalogue ID:** "+BT+m(e.get("catalogId"))+BT)
    lines.append("- **BrAPI-GenX operation identity:** "+BT+m(e.get("recommendedOperationId"))+BT+" (advisory where absent from source)")
    if e.get("apiGeneration")=="brapi-v2.1":
        so=e.get("operationIdInSource")
        lines.append("- **Source OpenAPI operationId:** "+(BT+m(so)+BT if so else "not defined in the inspected BrAPI v2.1 source operation. The recommended identifier is advisory only and does not amend the released contract."))
        lines.append("- **Official BrAPI module:** "+m(e.get("brapiModule")))
    else:
        lines.append("- **Source OpenAPI operationId:** "+BT+m(e.get("operationIdInSource"))+BT)
        lines.append("- **GenX source module:** "+BT+m(e.get("genxModule"))+BT)
    if e.get("brapiTag"): lines.append("- **Source tag:** "+m(e["brapiTag"]))
    lines.append("- **Proposed BrAPI-GenX classification:** "+m(domain(e)))
    cl = e.get("classification") or {}
    lines.append("- **Classification review / confidence:** "+BT+m(cl.get("reviewStatus"))+BT+" / "+BT+m(cl.get("confidence"))+BT)
    lines.append("- **Standard / proposal status:** "+BT+m(e.get("standardStatus"))+BT)
    lines.append("- **Implementation status:** "+BT+m(e.get("implementationStatus"))+BT)
    block(lines,"Purpose",e.get("purpose")); block(lines,"Source contract description",e.get("sourceDescription"))
    lines.append("**Can be used for:**")
    for item in e.get("canBeUsedFor") or ["No use case recorded; manual review required."]:
        parts=str(item).replace("\r\n","\n").split("\n")
        lines.extend(("- " if i==0 else "  ")+p for i,p in enumerate(parts))
    lines.append("**Must not be used for / explicit non-goals:**")
    for item in e.get("mustNotBeUsedFor") or ["No explicit non-goal recorded; manual review required."]:
        parts=str(item).replace("\r\n","\n").split("\n")
        lines.extend(("- " if i==0 else "  ")+p for i,p in enumerate(parts))
    for label,key in [("Side effects","sideEffects"),("Retry / idempotency","idempotency"),("Parameters recorded in registry","parameters"),("Request schema refs recorded","requestSchemaRefs"),("Response status codes recorded","responseCodes"),("Response component refs recorded","responseRefs")]:
        val=lst(e.get(key)) if key in {"parameters","requestSchemaRefs","responseCodes","responseRefs"} else m(e.get(key))
        lines.append("- **"+label+":** "+val)
    if e.get("semanticNeighborIds"): lines.append("- **Semantic relationship IDs / labels:** "+lst(e["semanticNeighborIds"]))
    if e.get("semanticNeighborCatalogIds"): lines.append("- **Related catalogue IDs:** "+lst(e["semanticNeighborCatalogIds"]))
    if e.get("decisionReferences"): lines.append("- **Relevant RFC / decision references:** "+lst(e["decisionReferences"]))
    src=e.get("source") or {}
    if src.get("path"):
        link = source_url(src)
        if e.get("apiGeneration") == "genx-v1":
            link = relpath(src["path"], catalogue.parent.relative_to(ROOT).as_posix())
        lines.append("- **Contract source:** ["+BT+m(src["path"])+BT+"]("+link+")")
    if src.get("inventoryLine"):
        n=src["inventoryLine"]; lines.append("- **BijMantra inventory row:** [line "+str(n)+"](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md#L"+str(n)+"); static evidence only.")
    cw=e.get("bijmantraCrosswalk") or {}
    if e.get("apiGeneration")=="brapi-v2.1":
        cand=cw.get("staticPythonDeclarations") or []
        lines.append("- **BijMantra static route crosswalk:** "+str(cw.get("candidateCount",0))+" exact normalized method/path candidate(s); "+str(cw.get("directBrApiAdapterDeclarationCount",0))+" BrAPI-specific source declaration(s). Runtime and conformance are unverified.")
        if cand:
            for c in cand:
                u="https://github.com/denishdholaria/bijmantraorg/blob/main/"+quote(str(c.get("sourcePath","")),safe="/._-")
                if c.get("line"): u+="#L"+str(c["line"])
                lines.append("  - ["+m(c.get("sourcePath"))+"]("+u+") — "+BT+m(c.get("handler"))+BT+"; line "+m(c.get("line"))+"; "+m(c.get("candidateRole"))+".")
        else: lines.append("  - No exact normalized source declaration was found. This is not proof of runtime absence.")
    else:
        cand=cw.get("relativePathCandidates") or []
        lines.append("- **BijMantra relative-route candidates:** "+str(len(cand))+". Matching relative paths do not prove GenX v3 mounting or contract equivalence.")
        for c in cand:
            u="https://github.com/denishdholaria/bijmantraorg/blob/main/"+quote(str(c.get("sourcePath","")),safe="/._-")
            if c.get("line"): u+="#L"+str(c["line"])
            lines.append("  - ["+m(c.get("sourcePath"))+"]("+u+") — "+BT+m(c.get("handler"))+BT+"; "+m(c.get("candidateRole"))+".")
        if cw.get("interpretation"): lines.append("  - Interpretation: "+m(cw["interpretation"]))
    lines.append("")
    return lines

def render_catalog(reg):
    entries=reg["entries"]; v21=[e for e in entries if e.get("apiGeneration")=="brapi-v2.1"]; genx=[e for e in entries if e.get("apiGeneration")=="genx-v1"]
    snap=reg.get("buildIntegrity",{}).get("bijmantraInventorySnapshot",{})
    lines=["# BrAPI-GenX Master Endpoint Catalogue","",
    "> Generated from [ENDPOINT-REGISTRY.json](./ENDPOINT-REGISTRY.json) by Scripts/generateEndpointArtifacts.py on "+str(reg.get("generatedAt","unknown date"))+". Do not edit by hand.","",
    "## Purpose and authority","",
    "This catalogue is the human-readable index for operation contracts and semantic boundaries. Source OpenAPI operations remain authoritative for wire contracts. The JSON registry is authoritative for catalogue identity, proposed crosswalk metadata, implementation-evidence status, and semantic-neighbor relationships.","",
    "A catalogue identifier does not replace a source operationId or route. Classification is a BrAPI-GenX crosswalk, not an official BrAPI community reclassification. Static source declarations do not prove that an endpoint is mounted, reachable, secure, or conformant.","",
    "## Coverage","","| Surface | Operations | Contract status |","|---|---:|---|",
    "| BrAPI v2.1 official modules | "+str(len(v21))+" | Released specification; implementation availability not inferred |",
    "| BrAPI GenX /genx/v1 | "+str(len(genx))+" | Proposed, non-normative |",
    "| **Total** | **"+str(len(entries))+"** | Existing contracts plus proposed operations |","",
    "BijMantra snapshot: "+str(snap.get("declaredTotalRows","unknown"))+" records from the inventory generated "+str(snap.get("generatedDate","unknown"))+"; see [source inventory](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md) and [crosswalk](./BIJMANTRA-CROSSWALK.md).","",
    "## Identity and review rules","",
    "1. Full identity uses API generation/base path, method, complete route template, source operationId when defined, schemas, side-effect/retry semantics, authorization boundary, and semantic neighbors.",
    "2. The inspected BrAPI v2.1 source operations do not define OpenAPI operationId. recommendedOperationId values are advisory catalogue suggestions and do not edit the frozen v2.1 specifications.",
    "3. Every operation should state supported uses and explicit non-goals. An HTTP route or summary alone is not enough.",
    "4. Similar names, nearby domain classes, or shared relative routes do not prove wire equivalence or safe dual-write behavior.",
    "5. BijMantra crosswalk entries are static source evidence; runtime availability and compatibility require separate validation.","",
    "## Semantic relationship register","","| Relationship | Risk | Status | Summary |","|---|---|---|---|"]
    for r in reg.get("semanticRelationships",[]):
        lines.append("| "+BT+m(r.get("id"))+BT+" | "+m(r.get("risk"))+" | "+BT+m(r.get("status"))+BT+" | "+m(r.get("title"))+" — "+m(r.get("relationship"))+" |")
    for r in reg.get("semanticRelationships",[]):
        lines.extend(["","### "+m(r.get("id"))+" — "+m(r.get("title")),"","**Risk / status:** "+m(r.get("risk"))+" / "+BT+m(r.get("status"))+BT,"",m(r.get("relationship")),"",
        "**BrAPI v2.1 catalogue IDs:** "+lst(r.get("brapiV21CatalogIds")),"**GenX catalogue IDs:** "+lst(r.get("genxCatalogIds"))])
        if r.get("brapiV21SchemaReferences"): lines.append("**Schema-level neighbors:** "+lst(r["brapiV21SchemaReferences"]))
        if r.get("decision"): lines.append("**Decision:** "+BT+m(r["decision"])+BT)
        if r.get("doNotAssume"):
            lines.append("**Must not assume:**"); lines.extend("- "+m(x) for x in r["doNotAssume"])
    lines.extend(["","## BrAPI v2.1 — released official modules",""])
    for module in MODULES:
        group=sorted([e for e in v21 if e.get("brapiModule")==module],key=lambda e:(e.get("path",""),e.get("method",""),e.get("catalogId","")))
        lines.extend(["### "+module+" — "+str(len(group))+" operations",""])
        for e in group: lines.extend(render_entry(e))
    lines.extend(["## BrAPI GenX — proposed /genx/v1 operations","","Every operation below is proposal-only. Reference-test-server evidence is not community acceptance or production deployment.",""])
    for module in sorted({e.get("genxModule") or "Unclassified" for e in genx}):
        group=sorted([e for e in genx if (e.get("genxModule") or "Unclassified")==module],key=lambda e:(e.get("path",""),e.get("method",""),e.get("catalogId","")))
        lines.extend(["### "+module+" — "+str(len(group))+" operations",""])
        for e in group: lines.extend(render_entry(e))
    bi=reg.get("buildIntegrity",{})
    lines.extend(["","## Registry quality summary","",
    "- Unique catalogue identifiers: "+BT+str(bi.get("catalogIdsUnique"))+BT+".",
    "- Unique full-base-path/method/route keys: "+BT+str(bi.get("fullBasePathMethodRouteKeysUnique"))+BT+".",
    "- Unique source/advisory operation identifiers where present: "+BT+str(bi.get("recommendedOperationIdsUnique"))+BT+".",
    "- BrAPI v2.1 inventory rows resolved to source YAML operations: "+str(bi.get("brapiV21EntriesAdded",0))+" / "+str(bi.get("brapiV21InventoryRows",0))+".",
    "- GenX operations documented: "+str(bi.get("genxEntriesAdded",0))+".",
    "","See [BIJMANTRA-CROSSWALK.md](./BIJMANTRA-CROSSWALK.md) for inventory evidence and semantic boundaries.",""])
    return "\n".join(lines)

def render_crosswalk(reg):
    entries=reg["entries"]; v21=sorted([e for e in entries if e.get("apiGeneration")=="brapi-v2.1"],key=lambda e:(e.get("brapiModule") or "",e.get("path",""),e.get("method","")))
    genx=sorted([e for e in entries if e.get("apiGeneration")=="genx-v1"],key=lambda e:(e.get("genxModule") or "",e.get("path",""),e.get("method","")))
    bi=reg.get("buildIntegrity",{}); snap=bi.get("bijmantraInventorySnapshot",{}); x=bi.get("v21PythonCrosswalk",{})
    lines=["# BrAPI-GenX ↔ BijMantra Endpoint Crosswalk","",
    "> Generated from [ENDPOINT-REGISTRY.json](./ENDPOINT-REGISTRY.json) by Scripts/generateEndpointArtifacts.py on "+str(reg.get("generatedAt","unknown date"))+". Do not edit by hand.","",
    "## Scope and evidence boundaries","","This crosswalk uses the static [BijMantra endpoint inventory](https://github.com/denishdholaria/bijmantraorg/blob/main/endpoints-inventory.md), generated on 2026-10-17, and the BrAPI-GenX specifications. It compares source declarations and contract paths; it is not a report of successful HTTP probes or production deployment.","",
    "A relative method/path match means the same HTTP verb and relative route template appear after parameter names are normalized. It does not prove that request/response schemas, identity models, authorization, side effects, error semantics, retry behavior, or data ownership are compatible.","",
    "## Inventory reconciliation","","| Inventory surface | Declared rows | Interpretation |","|---|---:|---|",
    "| Legacy Python route table | "+str(snap.get("declaredPythonTableRows","—"))+" | Includes "+str(snap.get("websocketRowsInPythonTable","—"))+" WebSocket row; "+str(snap.get("pythonHttpRouteDeclarations","—"))+" are HTTP declarations; static source only. |",
    "| Rust platform OpenAPI contracts | "+str(snap.get("rustContractOperations","—"))+" | Checked-in contracts; listener/mount status is not inferred. |",
    "| BrAPI v2.1 specification operations | "+str(snap.get("brapiV21SpecificationRows","—"))+" | Specification inventory; not proof of BijMantra implementation. |",
    "| **Total source records** | **"+str(snap.get("declaredTotalRows","—"))+"** | "+m(snap.get("reconciliation"))+" |","","## BrAPI v2.1 ↔ static Python source declaration crosswalk","",
    "**Result:** "+str(x.get("endpointsWithAnyExactRouteDeclaration",0))+" of "+str(len(v21))+" BrAPI v2.1 operations have an exact normalized method/path candidate; "+str(x.get("endpointsWithBrapiSpecificStaticSource",0))+" have a BrAPI-specific source declaration; "+str(x.get("endpointsWithoutExactRouteDeclaration",0))+" have no exact static match. All v2.1 inventory rows resolved to a specification operation.","",
    "| Catalogue ID | Official module | Method and route | Static candidates | Evidence pointers |","|---|---|---|---:|---|"]
    for e in v21:
        cw=e.get("bijmantraCrosswalk") or {}; cand=cw.get("staticPythonDeclarations") or []; refs=[]
        for c in cand:
            p=str(c.get("sourcePath","")); u="https://github.com/denishdholaria/bijmantraorg/blob/main/"+quote(p,safe="/._-")
            if c.get("line"): u+="#L"+str(c["line"])
            refs.append("["+m(p)+"]("+u+") ("+BT+m(c.get("handler"))+BT+", line "+m(c.get("line"))+", "+m(c.get("candidateRole"))+")")
        lines.append("| "+BT+m(e.get("catalogId"))+BT+" | "+m(e.get("brapiModule"))+" | "+BT+m(e.get("method"))+" "+m(e.get("path"))+BT+" | "+str(len(cand))+" | "+("; ".join(refs) if refs else "No exact static declaration found.")+" |")
    lines.extend(["","### Three v2.1 operations without an exact static method/path declaration",""])
    for e in x.get("unmatchedExamples",[]): lines.append("- "+BT+m(e.get("method"))+" "+m(e.get("path"))+BT+" — catalogue ID "+BT+m(e.get("catalogId"))+BT+".")
    lines.extend(["","Absence from this inventory is not proof of runtime unavailability. It means only that no exact normalized declaration was identified.","",
    "### Route-collision candidates requiring mount-graph review","","These are additional same-method/path declarations in other source modules alongside BrAPI-specific declarations. They are not confirmed runtime collisions; actual application mounts must be inspected.","",
    "| Catalogue ID | Method and route | BrAPI source candidates | Other source candidates |","|---|---|---:|---:|"])
    for c in x.get("sameRouteCollisions",[]):
        lines.append("| "+BT+m(c.get("catalogId"))+BT+" | "+BT+m(c.get("method"))+" "+m(c.get("path"))+BT+" | "+str(c.get("brapiSpecific",0))+" | "+str(c.get("other",0))+" |")
    lines.extend(["","## BrAPI GenX ↔ BijMantra static route candidates","","GenX uses /genx/v1. Relative-route matches below are candidate neighbors only; they do not prove v3 wiring, runtime mounting, or contract equivalence.","",
    "| GenX catalogue ID | Method and route | Relative candidates | Interpretation |","|---|---|---:|---|"])
    for e in genx:
        cw=e.get("bijmantraCrosswalk") or {}; cand=cw.get("relativePathCandidates") or []
        lines.append("| "+BT+m(e.get("catalogId"))+BT+" | "+BT+m(e.get("method"))+" "+m(e.get("basePath"))+m(e.get("path"))+BT+" | "+str(len(cand))+" | "+m(cw.get("interpretation"))+" |")
    lines.extend(["","## Rust platform contract comparisons","","The inventory declares "+str(snap.get("rustContractOperations",0))+" Rust OpenAPI operations. BrAPI v2.1 routes use /brapi/v2, while Rust capability routes use distinct /api/v2/... boundaries; no exact relative route matches were found between these surfaces. The following are domain-level candidates, not endpoint-equivalence claims.","",
    "| Domain relationship | BrAPI reference surface | Rust reference surface | Interpretation / guardrail |","|---|---|---|---|"])
    for name,br,ru,note in RUST:
        lines.append("| "+m(name)+" | "+m(br)+" | "+m(ru)+" | "+m(note)+" |")
    lines.extend(["","### Repeated platform operational routes","","Relative routes such as /health, /ready, and /metrics recur across Rust service contracts. This may be intentional where service base paths differ. Use the full base path, contract identity, capability owner, and deployment mount to determine if a real collision exists.","",
    "## Required follow-up evidence","",
    "1. Verify Python and Rust mount graphs and listener configuration before claiming runtime availability.",
    "2. Compare schemas, identifiers, authorization, pagination, errors, side effects, retry guarantees, and data ownership before claiming a compatible implementation.",
    "3. Keep high-risk semantic neighbors explicit. The registry flags seed-lot transaction/ledger (D-20), search/jobs, observations/telemetry, genotyping/matrix references, term governance, package/file transport, and model-registration/inference boundaries.",
    "4. Retain not-verified / not-assessed implementation status until live conformance evidence exists.",""])
    return "\n".join(lines)

def render_genx_catalog(reg):
    genx = [e for e in reg["entries"] if e.get("apiGeneration") == "genx-v1"]
    lines = [
        "# BrAPI-GenX Endpoint Catalogue (Focused View)", "",
        "> Generated from the master registry by Scripts/generateEndpointArtifacts.py on " + str(reg.get("generatedAt", "unknown date")) + ". Do not edit by hand.", "",
        "This is a focused view of the " + str(len(genx)) + " proposed GenX operations, not a separate source of truth. The complete catalogue covering BrAPI v2.1 and GenX is the [master endpoint catalogue](../ENDPOINT-CATALOG.md); authoritative structured records live in the [master registry](../ENDPOINT-REGISTRY.json). The [BijMantra crosswalk](../BIJMANTRA-CROSSWALK.md) records source-level implementation candidates without implying runtime availability or contract equivalence.", "",
        "| Section | Source module | Operation count | Status |", "|---|---|---:|---|"
    ]
    groups = {}
    for entry in genx:
        module = entry["genxModule"]
        module_path = Path(entry["source"]["path"]).parent
        section = module_path.parent.name
        groups.setdefault((section, module), []).append(entry)
    modules = sorted(groups)
    for section, module in modules:
        count = len(groups[section, module])
        lines.append(f"| [{section}](./{section}/) | [{module}](./{section}/{module}/) | {count} | proposed, non-normative |")
    lines.extend(["", "## Operations", ""])
    for section, module in modules:
        group = sorted(groups[section, module],
                       key=lambda e: (e.get("path", ""), e.get("method", ""), e.get("catalogId", "")))
        lines.extend(["### " + m(module) + " — " + str(len(group)) + " operations", ""])
        for e in group:
            lines.extend(render_entry(e, GENX_CATALOGUE))
    lines.extend(["", "## Non-normative status", "",
                  "Every operation in this view remains a proposal. This focused catalogue is generated from operation-level x-brapi-genx metadata and must not be edited independently. Change the OpenAPI operation metadata and master registry inputs, then regenerate this document and the all-generation catalogue.", ""])
    return "\n".join(lines)


def generate(reg):
    return {CATALOGUE: render_catalog(reg), GENX_CATALOGUE: render_genx_catalog(reg), CROSSWALK: render_crosswalk(reg)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true",help="fail if generated documents differ from checked-in files")
    args=parser.parse_args()
    try: reg=json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        print("Cannot read registry: "+str(exc),file=sys.stderr); return 1
    failed=False
    for path, expected in generate(reg).items():
        if args.check:
            try: actual=path.read_text(encoding="utf-8")
            except OSError: actual=""
            if actual!=expected:
                print("Generated output is stale: "+str(path.relative_to(ROOT)))
                print(f"Length: checked={len(actual)} generated={len(expected)}")
                print(f"Checked tail: {actual[-48:]!r}")
                print(f"Generated tail: {expected[-48:]!r}")
                mismatch = next((i for i, pair in enumerate(zip(actual, expected)) if pair[0] != pair[1]), min(len(actual), len(expected)))
                print(f"First character mismatch at offset {mismatch}: checked={actual[mismatch:mismatch+24]!r}; generated={expected[mismatch:mismatch+24]!r}")
                print(f"Newline counts: checked LF={actual.count(chr(10))}, CR={actual.count(chr(13))}; generated LF={expected.count(chr(10))}, CR={expected.count(chr(13))}")
                print(f"Line arrays identical: {actual.splitlines() == expected.splitlines()}")
                diff = list(difflib.unified_diff(
                    actual.splitlines(),
                    expected.splitlines(),
                    fromfile="checked-in",
                    tofile="generated",
                    lineterm="",
                    n=2,
                ))
                for line in diff[:40]:
                    print(line)
                if len(diff) > 40:
                    print(f"... {len(diff) - 40} additional diff lines omitted")
                failed=True
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(expected,encoding="utf-8")
            print("Wrote "+str(path.relative_to(ROOT))+" ("+str(len(expected))+" characters)")
    return 1 if failed else 0

if __name__=="__main__":
    raise SystemExit(main())
