# Documentation Standard

| Field | Value |
|---|---|
| Doc ID | HAK-DOC-STANDARD |
| Status | Draft |

Baseline: TIANEDGE Phase 0 rigor (completeness, consistency, traceability, validation, audit, readiness).

## 1. Document header
Every document starts with a title and a metadata table:

| Field | Meaning |
|---|---|
| Doc ID row | `HAK-DOC-<NAME>` stable, unique |
| Status row | one of the statuses in section 3 |
| Owner stage | Stage number that completes it |
| Depends on | Doc IDs |
| Requirements | requirement IDs defined or referenced |

## 2. Identifier conventions
| Prefix | Domain |
|---|---|
| HAK-PRD | product | 
| HAK-FR / HAK-NFR | functional / non-functional |
| HAK-DOM | domain | 
| HAK-SYS | system engineering |
| HAK-3D | 3D experience |
| HAK-SIM | simulation |
| HAK-DATA | data contracts |
| HAK-SCI | scientific validation |
| HAK-SAFE | safety/content boundary |
| HAK-QA | testing |
| HAK-DEP | deployment |
| HAK-SRC | source registry entry |
| HAK-ASM, HAK-CON, HAK-RSK, HAK-DEC | assumption, constraint, risk, decision |
| HAK-CMP, HAK-SUB, HAK-PAR, HAK-MOD, HAK-SCN | component, subsystem, parameter, model, scenario |
| HAK-TC | test case |
| HAK-ISS | open issue or specification gap |

IDs are `PREFIX-NNN` (3 digits), never reused, never renumbered.

## 3. Status vocabulary
`Not started`, `Research in progress`, `Draft`, `Under review`, `Validation in progress`, `Validated`, `Complete`, `Blocked`, `Deferred`.
A file existing never implies `Complete`. `Complete` requires the document's acceptance criteria and applicable audit checks to have passed with recorded evidence.

## 4. Claim classification
Technical claims are tagged where significant: `FACT`, `REF` (published engineering reference), `REP` (representative parameter), `ASM` (model assumption), `SIMP` (educational simplification), `DER` (derived), `ILL` (illustrative), `UNV` (unverified).
Illustrative values are never presented as measured data. No claim is `FACT`/`REF` without a source ID from the source registry.

## 5. Sources
Cite by `HAK-SRC-NNN` only. Bibliographic details live solely in the source registry (`docs/08-technical-library/source-registry.md`). Unverifiable sources are marked `UNV`.

## 6. Units
SI canonical. Conversions explicit. Parameters without units are not allowed unless dimensionless and declared so.

## 7. Content boundary
Civilian nuclear education only. See `docs/07-safety/safety-content-boundaries.md` (to be written in Stage 7); until then the Master Prompt section 6 applies.

## 8. Links and diagrams
Relative links only. Mermaid for relationships; no decorative diagrams.

## 9. Change history
Significant changes recorded in `docs/CHANGELOG.md`.
