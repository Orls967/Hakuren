# Risk Register

| Field | Value |
|---|---|
| Doc ID | HAK-DOC-RISKS |
| Status | Draft |

Risks to Phase 0 delivery and to the later implementation phase. Rows are appended by stage integration. Likelihood and impact use Low, Medium, High. Rating is qualitative and not derived from data.

| ID | Risk | Likelihood | Mitigation | Status |
|---|---|---|---|---|
| HAK-RSK-001 | Educational simulator is mistaken for an operational or safety-grade tool | Medium | Mandatory limitation banners, model validity ranges, content boundary rules (HAK-SAFE requirements) | Open |
| HAK-RSK-002 | Citation or numerical parameter is fabricated or misattributed | Medium | Source registry with Verified/UNV status; only verified sources back numeric values; audit tooling checks references | Open |
| HAK-RSK-003 | Documentation volume substitutes for specification quality | Medium | Quality gates A to F; consistency and scientific reference audits in Stage 11 | Open |
| HAK-RSK-004 | Automated anti-bot protections on iaea.org and NRC ADAMS PDF endpoints (HTTP 403 observed on ML023020572.pdf) may hinder verification of international safety standards and detailed NUREG manuals. | Medium | Require Stage 2/7 authors to obtain official IAEA PDFs via open mirror/institutional download or rely on verified NRC/DOE/NUREG publications, marking any unfetched entry UNV. | Open (Stage 1) |
| HAK-RSK-005 | Comparison technologies (BWR and SMR family) may trigger scope creep into full multi-reactor 3D models and independent dynamic solvers during Phase 1. | Medium | Enforce the four-tier boundary in scope-and-boundaries.md during Stage 3, 4, and 6 reviews so BWR/SMR parity stays within documented comparison views unless explicitly promoted. | Open (Stage 1) |
| HAK-RSK-006 | Interactive WebGL 3D exploration in Reactor Anatomy (/anatomy) could exclude keyboard-only or screen-reader learners if non-3D metadata parity is neglected. | Medium | Enforce HAK-CON-015 and HAK-PRD-017 in Stage 9 UX design via keyboard camera presets, structured component-tree alternatives, single-pointer steppers, and reduced-motion toggles. | Open (Stage 1) |
| HAK-RSK-007 | Complex 3D reactor assemblies exceed mobile/integrated GPU frame-rate or memory budgets. | Medium | Enforce progressive Level-of-Detail (LOD) loading, 15 MB GLB asset cap, automated DPR scaling, and an interactive 2D schematic fallback (HAK-NFR-025, HAK-NFR-026). | Open (Stage 1) |
| HAK-RSK-008 | WebGL 3D interactions fail WCAG 2.2 Level AA operability for keyboard-only or screen-reader learners. | Medium | Mandate bidirectional synchronization between 3D canvas selection and an ARIA-compliant Component Tree, keyboard camera presets, and aria-live announcements (HAK-FR-033, HAK-NFR-029, HAK-NFR-031). | Open (Stage 1) |
| HAK-RSK-009 | Learners misinterpret simplified educational simulator outputs or conceptual safety layers as operational plant guidance. | Medium | Display persistent non-operational disclaimers (HAK-SAFE-019, HAK-SAFE-020), global provenance badges (HAK-FR-058), and explicit model validity bounds (HAK-FR-045). | Open (Stage 1) |
| HAK-RSK-010 | Cross-module deep links (?component=, ?scenario=, /library/articles/:slug) could break if downstream Stage 3/4/6 entity IDs drift from IA slug conventions. | Medium | Enforce build-time JSON Schema validation of all cross-links and non-blocking graceful fallback notices when a URL parameter or slug is missing or deprecated. | Open (Stage 1) |
| HAK-RSK-011 | Misconfigured GitHub Pages BASE_URL or faulty 404.html redirect logic could cause broken deep links or open-redirect bugs on subpath deployments. | Medium | Specify same-origin basename prefix validation in 404.html, clear sessionStorage immediately on read, and emit static route entry stubs for the six top-level module paths. | Open (Stage 1) |
| HAK-RSK-012 | Complex 3D WebGL controls and dark-mode charts risk failing WCAG 2.2 AA dragging, focus-not-obscured, or non-text contrast criteria during implementation. | High | Mandate single-pointer steppers/presets, synchronized ARIA Component Tree, tabular telemetry, and automated axe-core plus manual keyboard/screen-reader testing in Stage 12. | Open (Stage 1) |
