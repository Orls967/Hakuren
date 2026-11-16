# Decision Log

| Field | Value |
|---|---|
| Doc ID | HAK-DOC-DECISIONLOG |
| Status | Draft (living) |

| ID | Date | Decision | Rationale | Alternatives | Status |
|---|---|---|---|---|---|
| HAK-DEC-001 | 2026-11-16 | HAKUREN is the locked project name | User approval | other candidates (rejected by user) | Accepted |
| HAK-DEC-002 | 2026-11-16 | PWR is primary reference reactor; BWR and SMR are comparison technologies | Rich 3D/system content, clear primary/secondary loops | BWR, SMR, fusion | Accepted (user) |
| HAK-DEC-003 | 2026-11-16 | Fusion, weapons, real operation, safety-grade simulation excluded | Scope control and safety boundary | none | Accepted (user) |
| HAK-DEC-004 | 2026-11-16 | Docs live in `docs/`, schemas in `schemas/`, tooling in `tools/` | Master Prompt blueprint | flat layout | Accepted |
| HAK-DEC-005 | 2026-11-16 | Audit tooling language: Python 3 (stdlib plus `jsonschema` for schema checks) | Minimal dependencies; Python is allowed offline tooling | Node | Proposed; confirm environment in Stage 9 |
| HAK-DEC-006 | 2026-11-16 | Delivery is staged with one commit and verified push per validated stage | Master Prompt section 21 | single final commit | Accepted |
