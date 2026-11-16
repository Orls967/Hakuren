# Documentation Authoring Contract

| Field | Value |
|---|---|
| Doc ID | HAK-DOC-CONTRACT |
| Status | Draft |

Binding rules for everyone (human or agent) who writes HAKUREN Phase 0 documents. It complements [DOCUMENTATION_STANDARD.md](../DOCUMENTATION_STANDARD.md) and [tools/README.md](../../tools/README.md).

## 1. Locked product facts
- Name: **HAKUREN**, full name *Nuclear Energy & Reactor Engineering Explorer*, tagline *Understand the Atom. Explore the Energy.*
- Primary reference: **PWR**. Comparison technologies: **BWR** and **SMR** (SMR is a family, never one design). Fusion is future expansion. Weapons, real reactor operation/control and safety-grade simulation are out of scope.
- Six product modules (canonical names and routes): **Overview** (`/`), **Reactor Anatomy** (`/anatomy`), **Energy Journey** (`/journey`), **Reactor Simulator** (`/simulator`), **Safety & Engineering** (`/safety`), **Technical Library** (`/library`).
- Learning path (non-linear, each module standalone): Discover, Explore, Understand, Experiment, Investigate, Master.
- Three 3D levels: Plant, System, Component. Highest detail on the reactor.
- Technology direction (proposed, justify complexity): React, TypeScript, Vite, Three.js with React Three Fiber, Zustand, Web Workers, Rust/WASM only if justified, static GitHub Pages, no mandatory backend. Python only for offline analysis, validation, tooling.
- Visual direction: dark graphite / midnight navy, cool cyan and ice blue accents, white/neutral grey text, controlled amber for thermal quantities, red reserved for true warnings. NVIDIA Omniverse-inspired cinematic 3D plus Siemens-inspired industrial clarity. No generic neon hacker look.
- The reference plant is called **HAKUREN Reference PWR**: a generic, representative educational PWR, not any commercial design. Vendor-specific designs may only appear as clearly labelled examples.
- Canonical vocabulary: reactor coolant system (RCS) = primary circuit; secondary circuit; steam generator (SG); reactor pressure vessel (RPV); reactor coolant pump (RCP); pressurizer (PZR); containment; control rod / control rod drive mechanism (CRDM); fuel assembly / fuel rod; turbine-generator; condenser; feedwater. Use these consistently.

## 2. Scientific integrity rules
1. No invented facts, numbers, dimensions, citations, DOIs, report numbers, URLs, page numbers or validation results. If a value is not found in a source you actually read, it stays a documented gap (record it in the open-issues register, see section 7).
2. Tag significant technical statements with a class: `FACT`, `REF` (published engineering reference), `REP` (representative parameter), `ASM` (model assumption), `SIMP` (educational simplification), `DER` (derived), `ILL` (illustrative), `UNV` (unverified). `FACT`, `REF` and `REP` need a `HAK-SRC-nnn` citation. Illustrative values are never presented as measured data.
3. Numbers you compute must be computed by running code or arithmetic you show; state units (SI canonical). Worked examples must be reproducible.
4. Educational models are never described as safety-grade, operational, predictive beyond their validity range, certified, or qualified. Simulation docs carry this limitation explicitly.
5. Generic PWR architecture must be distinguished from specific designs; do not imply all PWRs share dimensions, loop counts, pressures or safety systems.
6. When sources disagree, record both and say which is more applicable.

## 3. Content boundary (HAK-SAFE)
Allowed: civilian power education, publicly documented architecture, thermodynamics, general principles, conceptual safety engineering, non-operational simulation, public material properties, radiation basics, reliability concepts.
Forbidden everywhere: nuclear weapon design or pathways, weapons-grade material production, acquiring or processing restricted materials, real operating or control procedures, instructions to bypass or defeat protection, exploitation analysis of protection vulnerabilities, procedures for manipulating safety-critical parameters, protection setpoints presented as operating guidance. Do not include sensitive detail merely because a source contains it. Describe safety systems by purpose, principle and architecture, never by operator actions or defeat methods. Accident discussion is conceptual (what barriers and functions exist), not procedural.

## 4. Document format
- Start with `# Title`, then the metadata table with rows `Doc ID` (`HAK-DOC-<UPPERCASE-NAME>`, unique), `Status`, and optionally `Owner stage`, `Depends on`, `Requirements`.
- Authors set Status only to `Research in progress` or `Draft`. `Validated` and `Complete` are reserved for Stage 11 after audit.
- Use the content structure of Master Prompt section 9 where applicable, with real content only. Minimum useful length per specification document is substantial (aim for 1,500 to 5,000 words depending on purpose); no filler, no placeholders, no TODO or TBD text.
- Mermaid diagrams must be technically meaningful. Allowed types: flowchart, graph, sequenceDiagram, stateDiagram-v2, classDiagram, erDiagram, xychart-beta. Quote labels containing special characters.
- Math in `$...$` or `$$...$$`, SI units.
- Links: use relative markdown links **only to files that already exist**. For documents not yet written, name them in backticks (e.g. `docs/06-simulation/parameter-catalog.md`) without a link. Never invent anchors.
- Cite sources only by `HAK-SRC-nnn` that exist in the registry or that you register (section 6). Do not write bibliographic details inside documents.
- Do not edit the integration-managed files (section 7) or files owned by other authors. Do not run any git command. Do not create files outside `docs/`, `schemas/`, `tools/` unless instructed.

## 5. Identifiers
- A definition is a table row whose first cell is exactly the ID. Any other textual mention is a reference and must resolve to a definition that already exists or that you define. Never write ID ranges or wildcards (`HAK-SIM-xxx to yyy` is forbidden; list IDs individually or reference a table).
- Prefixes: `HAK-PRD, FR, NFR, DOM, SYS, 3D, SIM, DATA, SCI, SAFE, QA, DEP` (requirements); `CMP` component, `SUB` subsystem/system, `PAR` simulation parameter, `MOD` mathematical model, `SCN` scenario, `TC` test case, `SRC` source, `ASM, DEC, RSK, CON, ISS` registers.
- Each author receives an **ID block** (numbers N to M) in the task brief. Use numbers only from your block for every ID you define, for all prefixes, unless the brief grants a different range. Before defining, check you are not colliding: `grep -rn "HAK-<PREFIX>-" docs` .
- A row whose first cell is an ID is a definition. Secondary tables (matrices, mappings, detail tables) must NOT put the ID in the first column; put the name first and the ID in a later column, or the audit reports a duplicate definition.
- IDs are stable: never renumber, never reuse.
- Requirement tables use exactly: `| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |`
  - Priority: Must, Should, Could, Won't, Provisional-Must, Provisional-Should. Verification: one of Test, Inspection, Analysis, Demonstration (combinations allowed with "+"). Acceptance: a concrete, checkable criterion (at least one sentence). Source: `HAK-SRC-nnn`, `User`, or `Master Prompt s<number>`. Parent: ID or `-`. Status: `Draft` unless otherwise instructed.
  - Requirements say what/why, must be unambiguous ("shall"), atomic, and testable; measurable targets not backed by evidence are `Provisional-*`.
- Test case tables use exactly: `| ID | Title | Preconditions | Actions | Expected | Evidence | Verifies |` (ID `HAK-TC-nnn`; Verifies lists requirement IDs, comma separated).

## 6. Research procedure
- Do real research with the web search tool and by fetching pages (for example `curl -sL -m 30 <url>`; PDFs via `curl` then text extraction if a tool exists). Preferred sources: IAEA, NRC, DOE, NEA, national laboratories, peer-reviewed papers, recognised textbooks (Lamarsh, Todreas and Kazimi, Incropera, Cengel, Glasstone and Sesonske, Duderstadt and Hamilton), IAPWS, standards bodies. Vendor documents only for clearly labelled vendor examples.
- A source may be marked `Verified` only if you fetched it and read the passage supporting the claim; otherwise `Partially verified` or `UNV`. If a site presents an anti-bot challenge or requires login, do not attempt to bypass it: mark `UNV` or use another source.
- Report each new source in your result (fields: id, title, issuer, date, identifier, url, section, accessed (YYYY-MM-DD, today is the access date), category, claims, limitations, verified). Use IDs from your SRC block. The integrator writes them into the registry; you cite them immediately by ID. Do not cite sources you did not report. Do not put unverified claims into `Complete` specs.
- Date format everywhere: YYYY-MM-DD. Today is 2026-11-16.

## 7. Integration-managed files (do not edit)
`docs/00-governance/decision-log.md`, `assumptions-register.md`, `risk-register.md`, `open-issues-register.md`, `docs/08-technical-library/source-registry.md`, `docs/CHANGELOG.md`, `docs/PROJECT_STATUS.md`, `docs/14-traceability/requirement-traceability-matrix.md` (generated). Report decisions, assumptions, risks, gaps and sources in your structured result instead; the integrator allocates their IDs. Reference decisions in prose by title, not by ID, since IDs are allocated afterwards.

## 8. Quality bar
Implementation readiness (Gate E): a developer who has never seen the project can tell what to build, why, how it behaves, what data it consumes and produces, how it is tested and when it is done. Prefer fewer, complete documents. Before finishing, run `.venv/bin/python tools/hakuren_audit.py links,ids,metadata,sources,mermaid,status` and fix every error that concerns your files (errors in other authors' in-progress files may be ignored).

## 9. Preferred document structure (use where applicable, omit irrelevant parts)
Purpose; scope; definitions; background; technical principles; system boundaries; requirements; functional behavior; data structures; inputs and outputs; dependencies; interactions with other systems; equations and units; constraints; assumptions; error conditions; edge cases; validation criteria; testing requirements; acceptance criteria; references (`HAK-SRC` IDs); related documents (backticked paths or links to existing files); change history.
