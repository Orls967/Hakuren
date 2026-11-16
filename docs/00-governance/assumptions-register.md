# Assumptions Register

| Field | Value |
|---|---|
| Doc ID | HAK-DOC-ASSUMPTIONS |
| Status | Draft (living) |

| ID | Assumption | Impact if wrong | Status |
|---|---|---|---|
| HAK-ASM-001 | `github.com/Orls967/Hakuren` is the intended repository | Work would be published to the wrong place | Open; verified only by name/identity consistency |
| HAK-ASM-002 | Push access to `origin/main` is available | Push blocked; report and stop | Unverified until first push |
| HAK-ASM-003 | Work on branch `main` directly is acceptable (user authorised pushing to the verified branch) | Need feature branches | Accepted |
| HAK-ASM-004 | Web research tooling is available for source verification | Source registry would have unverified entries | To be confirmed in Stage 2 |
| HAK-ASM-005 | Educators and students accessing HAKUREN have modern desktop or tablet browsers supporting WebGL and standard glTF 2.0 rendering without requiring institutional VPNs or server-side plugins. | If target classrooms restrict WebGL hardware acceleration or run older hardware, Stage 4 performance budgets and fallback UI controls will require lower polygon/texture tiers. | Open (Stage 1) |
| HAK-ASM-006 | A single-thread Web Worker running TypeScript numerical integration is sufficient for the educational lumped-parameter reactor simulator without requiring Rust/WebAssembly compilation in Phase 1. | If Stage 6 numerical stability or solver step-rate requires higher throughput, Stage 8 architecture allows gated introduction of Rust/WASM under HAK-CON-004. | Open (Stage 1) |
| HAK-ASM-007 | Quantitative usability targets such as the 60-second orientation threshold in HAK-PRD-003 and WCAG 2.2 AA compliance across non-3D controls in HAK-PRD-017 are achievable within static client-side constraints. | Targets marked Provisional-Must will require adjustment if Stage 10 accessibility or pilot usability validation reveals friction on complex interactive workflows. | Open (Stage 1) |
| HAK-ASM-008 | Target learners access HAKUREN on modern browsers supporting ES2022, Web Workers, and WebGL 2, with low-end devices served via automated DPR scaling and 2D schematic fallback. | Determines 3D scene budget tiers and fallback UI complexity for Overview, Anatomy, Journey, and Safety modules. | Open (Stage 1) |
| HAK-ASM-009 | English is the primary instructional language for MVP Release 1.0 learners, with Indonesian localization deferred to Tier 2 (Release 1.1) via externalized resource bundles. | Avoids premature translation drift during Phase 0/1 terminology stabilization while keeping UI and data layers i18n-ready. | Open (Stage 1) |
| HAK-ASM-010 | Representative PWR physical dimensions and thermodynamic parameters are sourced in Stage 2/3/6 specifications rather than hardcoded at the product requirements layer. | Keeps product requirements decoupled from specific reference numbers until verified domain and simulation models are authored. | Open (Stage 1) |
| HAK-ASM-011 | Target desktop and mobile browsers run modern ES2022 engines with standard History API, CSS prefers-reduced-motion support, and WebGL 2 (with an interactive 2D SVG fallback when WebGL is unavailable). | If legacy browsers without History API or modern CSS layout are targeted later, navigation and reflow specs would require polyfills or degraded views. | Open (Stage 1) |
| HAK-ASM-012 | GitHub Pages custom 404.html SPA redirect combined with optional static route entry stubs for the six top-level routes is permitted by repository CI/build configuration. | If project-site subpath deployment (/Hakuren/) is used instead of a custom root domain, Vite BASE_URL must be configured consistently across router and asset loaders. | Open (Stage 1) |
| HAK-ASM-013 | Optional client-local storage (localStorage) for learner difficulty preference and resettable Concept Check progress remains acceptable in educational browser contexts without cookie banners. | If institutional environments disable localStorage, preferences fall back gracefully to in-memory per-tab state. | Open (Stage 1) |
