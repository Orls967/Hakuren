#!/usr/bin/env python3
"""HAKUREN Phase 0 documentation audit library and CLI.

Usage: python tools/hakuren_audit.py <check> [--json] [--strict]
Checks: inventory, links, ids, requirements, sources, metadata, status, mermaid,
        safety, schemas, all
Exit codes: 0 no errors; 1 errors found; 2 tool/usage failure.
Warnings do not change the exit code unless --strict is given.
Rules are never relaxed to obtain a pass; add exceptions only in tools/README.md with a decision-log entry.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SCHEMAS = ROOT / "schemas"

PREFIXES = "PRD|FR|NFR|DOM|SYS|3D|SIM|DATA|SCI|SAFE|QA|DEP|CMP|SUB|PAR|MOD|SCN|SRC|TC|ASM|DEC|RSK|CON|ISS"
REQ_PREFIXES = {"PRD", "FR", "NFR", "DOM", "SYS", "3D", "SIM", "DATA", "SCI", "SAFE", "QA", "DEP"}
ID_RE = re.compile(r"\bHAK-(%s)-(\d{3})\b" % PREFIXES)
DOCID_RE = re.compile(r"\bHAK-DOC-[A-Z0-9-]+\b")
STATUSES = ["Not started", "Research in progress", "Draft", "Under review",
            "Validation in progress", "Validated", "Complete", "Blocked", "Deferred"]
REQ_HEADER = ["ID", "Name", "Requirement", "Priority", "Rationale", "Source", "Parent",
              "Verification", "Acceptance", "Status"]
SRC_HEADER_MIN = 12
NO_DEF_DIRS = ("14-traceability", "15-audit")  # reference-only locations
SAFETY_TERMS = [r"weapons?-grade", r"nuclear (explosive|weapon) design", r"bypass(ing)? (the )?(reactor )?(protection|trip|safety)",
                r"defeat(ing)? (the )?(safety|protection)", r"enrichment (procedure|cascade design)", r"reprocessing procedure",
                r"critical mass (of|for|calculation)"]
SAFETY_EXEMPT = ("07-safety/safety-content-boundaries.md", "00-governance/scope-and-boundaries.md",
                 "00-governance/risk-register.md", "00-governance/project-charter.md",
                 "00-governance/terminology-standard.md", "06-simulation/simulation-scope-and-boundaries.md",
                 "15-audit/")


class Report:
    def __init__(self):
        self.errors, self.warnings, self.info = [], [], []

    def err(self, check, where, msg):
        self.errors.append({"check": check, "where": where, "message": msg})

    def warn(self, check, where, msg):
        self.warnings.append({"check": check, "where": where, "message": msg})

    def note(self, msg):
        self.info.append(msg)


def md_files():
    return sorted(DOCS.rglob("*.md")) if DOCS.exists() else []


def rel(p):
    return str(Path(p).relative_to(ROOT))


def strip_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def table_rows(text):
    """Yield list-of-cells for markdown table rows (excluding separator rows)."""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            yield cells


def definitions():
    """Return dict id -> list of (file, cells) for table rows whose first cell is exactly an ID."""
    defs = {}
    for f in md_files():
        r = rel(f)
        if any(("docs/" + d) in r for d in NO_DEF_DIRS):
            continue
        for cells in table_rows(f.read_text(encoding="utf-8")):
            m = re.fullmatch(r"HAK-(%s)-(\d{3})" % PREFIXES, cells[0]) if cells else None
            if m:
                defs.setdefault(cells[0], []).append((r, cells))
    return defs


def check_inventory(rep):
    lst = ROOT / "tools" / "required-documents.txt"
    if not lst.exists():
        rep.err("inventory", rel(lst), "required document list missing")
        return
    missing = empty = 0
    for line in lst.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        p = DOCS / line
        if not p.exists():
            rep.err("inventory", "docs/" + line, "required document missing")
            missing += 1
        elif len(p.read_text(encoding="utf-8").strip()) < 600:
            rep.err("inventory", "docs/" + line, "document is effectively empty (<600 chars)")
            empty += 1
    rep.note(f"inventory: {len(md_files())} markdown files under docs/; missing={missing}, empty={empty}")


def check_links(rep):
    n = 0
    for f in md_files():
        text = strip_code(f.read_text(encoding="utf-8"))
        for m in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)", text):
            tgt = m.group(1)
            if re.match(r"^(https?:|mailto:|#)", tgt):
                continue
            path, _, frag = tgt.partition("#")
            n += 1
            dest = (f.parent / path).resolve()
            if not dest.exists():
                rep.err("links", rel(f), f"broken relative link: {tgt}")
            elif frag and dest.suffix == ".md":
                heads = [re.sub(r"[^\w\- ]", "", h.lower()).strip().replace(" ", "-")
                         for h in re.findall(r"^#+\s+(.*)$", strip_code(dest.read_text(encoding="utf-8")), flags=re.M)]
                if frag.lower() not in heads:
                    rep.err("links", rel(f), f"missing anchor in target: {tgt}")
    rep.note(f"links: {n} relative links checked")


def check_ids(rep):
    defs = definitions()
    for i, locs in defs.items():
        if len(locs) > 1:
            rep.err("ids", i, "defined more than once: " + ", ".join(l[0] for l in locs))
    refs = {}
    for f in md_files():
        for m in ID_RE.finditer(f.read_text(encoding="utf-8")):
            refs.setdefault(m.group(0), set()).add(rel(f))
    for i, files in sorted(refs.items()):
        if i not in defs:
            rep.err("ids", i, "referenced but never defined (in " + ", ".join(sorted(files)[:3]) + ")")
    # doc ids
    seen = {}
    for f in md_files():
        for cells in table_rows(f.read_text(encoding="utf-8")):
            if len(cells) >= 2 and cells[0] == "Doc ID":
                seen.setdefault(cells[1], []).append(rel(f))
    for d, fs in seen.items():
        if len(fs) > 1:
            rep.err("ids", d, "Doc ID duplicated in " + ", ".join(fs))
    rep.note(f"ids: {len(defs)} defined IDs, {len(refs)} distinct referenced IDs")
    return defs


def check_requirements(rep):
    defs = definitions()
    reqs = {i: l[0] for i, l in defs.items() if i.split("-")[1] in REQ_PREFIXES}
    for i, (f, cells) in reqs.items():
        if len(cells) < len(REQ_HEADER):
            rep.err("requirements", i, f"requirement row in {f} has {len(cells)} cells, expected {len(REQ_HEADER)}")
            continue
        for idx in (1, 2, 3, 7, 8, 9):
            if not cells[idx] or cells[idx] in ("-", "TBD", "TODO"):
                rep.err("requirements", i, f"empty/placeholder column '{REQ_HEADER[idx]}' in {f}")
        if cells[3] not in ("Must", "Should", "Could", "Won't", "Provisional-Must", "Provisional-Should"):
            rep.err("requirements", i, f"invalid priority '{cells[3]}'")
        if not any(cells[9].startswith(s) for s in STATUSES):
            rep.err("requirements", i, f"invalid status '{cells[9]}'")
        if not cells[8] or len(cells[8]) < 15:
            rep.err("requirements", i, "acceptance criterion too short to be verifiable")
        par = cells[6]
        if par not in ("-", "") and par not in defs:
            rep.err("requirements", i, f"parent {par} undefined")
    rtm = DOCS / "14-traceability" / "requirement-traceability-matrix.md"
    if not rtm.exists():
        rep.err("requirements", "RTM", "requirement-traceability-matrix.md missing")
        return reqs
    in_rtm, tc_map = {}, {}
    for cells in table_rows(rtm.read_text(encoding="utf-8")):
        if cells and re.fullmatch(r"HAK-(%s)-\d{3}" % "|".join(REQ_PREFIXES), cells[0]):
            in_rtm[cells[0]] = cells
    for i in reqs:
        if i not in in_rtm:
            rep.err("requirements", i, "missing from RTM (run tools/generate_rtm.py)")
    for i in in_rtm:
        if i not in reqs:
            rep.err("requirements", i, "in RTM but not defined (stale RTM)")
    # test coverage
    for f in md_files():
        for cells in table_rows(f.read_text(encoding="utf-8")):
            if cells and re.fullmatch(r"HAK-TC-\d{3}", cells[0]):
                for m in ID_RE.finditer(cells[-1]):
                    tc_map.setdefault(m.group(0), []).append(cells[0])
    uncovered = [i for i in reqs if i not in tc_map]
    for i in uncovered:
        rep.warn("requirements", i, "no test case (HAK-TC) verifies this requirement")
    by_cat = {}
    for i in reqs:
        by_cat[i.split("-")[1]] = by_cat.get(i.split("-")[1], 0) + 1
    rep.note(f"requirements: {len(reqs)} total {by_cat}; in RTM={len(in_rtm)}; without test={len(uncovered)}")
    return reqs


def check_sources(rep):
    reg = DOCS / "08-technical-library" / "source-registry.md"
    defs = definitions()
    srcs = {i: l for i, l in defs.items() if i.startswith("HAK-SRC-")}
    if not reg.exists():
        rep.err("sources", "registry", "source-registry.md missing")
        return
    unv = 0
    for i, locs in srcs.items():
        f, cells = locs[0]
        if "source-registry" not in f:
            rep.err("sources", i, f"defined outside the registry: {f}")
            continue
        if len(cells) < SRC_HEADER_MIN:
            rep.err("sources", i, f"registry row has {len(cells)} cells, expected {SRC_HEADER_MIN}")
            continue
        url, accessed, verified = cells[5], cells[7], cells[11]
        if verified.strip().upper().startswith("UNV"):
            unv += 1
        elif not url.startswith("http"):
            rep.err("sources", i, "verified source without http(s) URL")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", accessed) and not verified.upper().startswith("UNV"):
            rep.err("sources", i, "access date missing/invalid (YYYY-MM-DD)")
        if verified.strip() not in ("Verified", "UNV", "Partially verified"):
            rep.err("sources", i, f"Verified column must be Verified/Partially verified/UNV, got '{verified}'")
    rep.note(f"sources: {len(srcs)} registered, {unv} unverified")


def check_metadata(rep):
    for f in md_files():
        text = f.read_text(encoding="utf-8")
        rows = {c[0]: c[1] for c in table_rows(text) if len(c) >= 2}
        r = rel(f)
        if "Doc ID" not in rows or not rows["Doc ID"].startswith("HAK-DOC-"):
            rep.err("metadata", r, "missing '| Doc ID | HAK-DOC-... |' metadata row")
        if "Status" not in rows:
            rep.err("metadata", r, "missing '| Status | ... |' metadata row")
        elif not any(rows["Status"].startswith(s) for s in STATUSES):
            rep.err("metadata", r, f"invalid status '{rows['Status']}'")
        if not text.lstrip().startswith("#"):
            rep.err("metadata", r, "document must start with a heading")


def check_status(rep):
    for f in md_files():
        text = f.read_text(encoding="utf-8")
        rows = {c[0]: c[1] for c in table_rows(text) if len(c) >= 2}
        st = rows.get("Status", "")
        if st.startswith(("Complete", "Validated")):
            if re.search(r"\b(TODO|TBD|FIXME|PLACEHOLDER|lorem ipsum)\b", strip_code(text), re.I):
                rep.err("status", rel(f), f"status '{st}' but contains TODO/TBD/placeholder text")
    ps = DOCS / "PROJECT_STATUS.md"
    if ps.exists():
        t = ps.read_text(encoding="utf-8")
        if "Phase 0 overall" not in t:
            rep.warn("status", rel(ps), "no 'Phase 0 overall' line")


def check_mermaid(rep):
    kinds = ("flowchart", "graph", "sequenceDiagram", "stateDiagram", "classDiagram", "erDiagram", "xychart-beta")
    n = 0
    for f in md_files():
        text = f.read_text(encoding="utf-8")
        if text.count("```") % 2:
            rep.err("mermaid", rel(f), "unbalanced code fences")
        for m in re.finditer(r"```mermaid\n(.*?)```", text, flags=re.S):
            n += 1
            first = m.group(1).strip().splitlines()[0] if m.group(1).strip() else ""
            if not first.startswith(kinds):
                rep.err("mermaid", rel(f), f"unsupported/missing diagram type: '{first[:30]}'")
    rep.note(f"mermaid: {n} diagrams syntax-screened (type only; no renderer available)")


def check_safety(rep):
    for f in md_files():
        r = rel(f)
        if any(e in r for e in SAFETY_EXEMPT):
            continue
        text = strip_code(f.read_text(encoding="utf-8"))
        for t in SAFETY_TERMS:
            for m in re.finditer(t, text, re.I):
                rep.warn("safety", r, f"boundary keyword '{m.group(0)}' needs manual review")


def check_schemas(rep):
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError:
        rep.err("schemas", "env", "jsonschema not installed (use .venv/bin/python); schema check NOT performed")
        return
    names = ["component", "subsystem", "simulation-parameter", "simulation-result", "energy-flow", "scenario", "technical-reference"]
    ok = bad = 0
    for n in names:
        p = SCHEMAS / f"{n}.schema.json"
        if not p.exists():
            rep.err("schemas", rel(p), "schema missing")
            continue
        try:
            sch = json.loads(p.read_text(encoding="utf-8"))
            Draft202012Validator.check_schema(sch)
        except Exception as e:  # noqa
            rep.err("schemas", rel(p), f"invalid schema: {e}")
            continue
        if sch.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            rep.err("schemas", rel(p), "$schema must be Draft 2020-12")
        for k in ("$id", "title", "version"):
            if k not in sch and k != "version":
                rep.err("schemas", rel(p), f"missing {k}")
        if "x-schema-version" not in sch:
            rep.err("schemas", rel(p), "missing x-schema-version")
        val = Draft202012Validator(sch)
        valid = sorted((SCHEMAS / "examples").glob(f"{n}.valid*.json"))
        invalid = sorted((SCHEMAS / "examples").glob(f"{n}.invalid*.json"))
        if not valid:
            rep.err("schemas", n, "no valid example")
        if not invalid:
            rep.warn("schemas", n, "no invalid example")
        for e in valid:
            errs = list(val.iter_errors(json.loads(e.read_text(encoding="utf-8"))))
            if errs:
                rep.err("schemas", rel(e), "valid example fails: " + errs[0].message[:150])
                bad += 1
            else:
                ok += 1
        for e in invalid:
            if not list(val.iter_errors(json.loads(e.read_text(encoding="utf-8")))):
                rep.err("schemas", rel(e), "invalid example unexpectedly validates")
                bad += 1
            else:
                ok += 1
    rep.note(f"schemas: example outcomes as expected={ok}, unexpected={bad}")


CHECKS = {"inventory": check_inventory, "links": check_links, "ids": check_ids, "requirements": check_requirements,
          "sources": check_sources, "metadata": check_metadata, "status": check_status, "mermaid": check_mermaid,
          "safety": check_safety, "schemas": check_schemas}


def run(names):
    rep = Report()
    for n in names:
        CHECKS[n](rep)
    return rep


def main(argv=None, default=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    strict = "--strict" in argv
    argv = [a for a in argv if not a.startswith("--")]
    sel = argv[0] if argv else default
    if sel is None or (sel != "all" and sel not in CHECKS and not all(s in CHECKS for s in sel.split(","))):
        print(__doc__)
        return 2
    names = list(CHECKS) if sel == "all" else sel.split(",")
    rep = run(names)
    if as_json:
        print(json.dumps({"errors": rep.errors, "warnings": rep.warnings, "info": rep.info}, indent=2))
    else:
        for e in rep.errors:
            print(f"ERROR   [{e['check']}] {e['where']}: {e['message']}")
        for w in rep.warnings:
            print(f"WARNING [{w['check']}] {w['where']}: {w['message']}")
        for i in rep.info:
            print("INFO    " + i)
        print(f"RESULT: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s) [{','.join(names)}]")
    return 1 if rep.errors or (strict and rep.warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
