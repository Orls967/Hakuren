# Documentation tooling

Run with the project venv (`jsonschema` required for schema checks): `python3 -m venv .venv && .venv/bin/pip install jsonschema`.

| Command | Purpose |
|---|---|
| `.venv/bin/python tools/audit-documentation.py [--json] [--strict]` | all checks |
| `.venv/bin/python tools/validate-links.py` | relative links and anchors |
| `.venv/bin/python tools/validate-requirements.py` | ID uniqueness, cross-references, requirement rows, RTM sync, test coverage |
| `.venv/bin/python tools/validate-schemas.py` | schemas (Draft 2020-12) and examples |
| `.venv/bin/python tools/generate_rtm.py` | regenerate the RTM from requirement tables |
| `.venv/bin/python tools/hakuren_audit.py <check>` | single check: inventory, links, ids, requirements, sources, metadata, status, mermaid, safety, schemas |

Exit codes: 0 no errors, 1 errors, 2 usage/tool failure. Warnings do not fail unless `--strict`.
Error classes: ERROR = violates a mandatory rule; WARNING = needs human review (e.g. requirement without test case, safety keyword hit).

## Conventions the tools enforce
- Every doc has `| Doc ID | HAK-DOC-... |` and `| Status | <vocabulary> |` rows.
- An ID is *defined* by a table row whose first cell is exactly the ID; any other mention is a *reference* and must resolve. Never write ID ranges (e.g. `HAK-SIM-001..010`).
- Requirement tables use columns: `ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status`. Priority: Must, Should, Could, Won't, Provisional-Must, Provisional-Should.
- Test cases: `| HAK-TC-nnn | Title | Preconditions | Actions | Expected | Evidence | Verifies |` (Verifies lists requirement IDs).
- Source registry rows (12 cells): `ID | Title | Issuer | Date | Identifier | URL | Section | Accessed | Category | Claims supported | Limitations | Verified`; Verified is `Verified`, `Partially verified` or `UNV`.
- Definitions inside `14-traceability/` and `15-audit/` are not counted (reference-only).
- Schema examples live in `schemas/examples/<name>.valid*.json` and `<name>.invalid*.json`.
- Mermaid is only type-screened; no renderer is available, so syntax is not fully validated.
