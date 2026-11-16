# Non-Functional Requirements Specification

| Field | Value |
|---|---|
| Doc ID | HAK-DOC-NFR |
| Status | Draft |
| Owner stage | 1 |
| Depends on | HAK-DOC-PRD |
| Requirements | HAK-NFR-019, HAK-NFR-020, HAK-NFR-021, HAK-NFR-022, HAK-NFR-023, HAK-NFR-024, HAK-NFR-025, HAK-NFR-026, HAK-NFR-027, HAK-NFR-028, HAK-NFR-029, HAK-NFR-030, HAK-NFR-031, HAK-NFR-032, HAK-NFR-033, HAK-NFR-034, HAK-NFR-035, HAK-NFR-036, HAK-NFR-037, HAK-NFR-038, HAK-NFR-039 |

## 1. Purpose and Scope

This document specifies the non-functional requirements (`HAK-NFR` entries) governing performance, accessibility, reduced-motion support, browser compatibility, network resilience, security and privacy, maintainability, internationalization readiness, and content integrity for **HAKUREN**.

Per [documentation-authoring-contract.md](../00-governance/documentation-authoring-contract.md), all quantitative performance, memory, and bundle-size budgets defined prior to implementation benchmarking are tagged **`Provisional-Must`** or **`Provisional-Should`**. These provisional targets establish concrete engineering budgets for Stage 10 architecture and Stage 12 performance testing and must be re-baselined once representative 3D meshes and simulation benchmarks run on target hardware.

## 2. Performance Requirements and Measurement Definitions

### 2.1 Reference Benchmark Profiles

Performance budgets are evaluated under two defined client profiles (details to be refined in `docs/12-quality-assurance/performance-test-plan.md`):
- **Reference Desktop Profile:** Modern multi-core CPU, discrete or modern integrated GPU supporting WebGL 2, `1440x900` viewport, standard broadband (`>= 20 Mbps`, `<= 40 ms` RTT).
- **Constrained / Mobile Profile:** Mid-tier mobile/tablet or thin-and-light integrated GPU, `390x844` or `768x1024` viewport, simulated "Slow 4G" (`~4 Mbps`, `~150 ms` RTT) or throttled `4x` CPU slowdown.

### 2.2 Performance Requirements

| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|---|
| HAK-NFR-019 | Initial Application Shell Load Time | Under Reference Desktop broadband conditions, the static application shell (route HTML, critical CSS, and initial UI hydration excluding lazy 3D meshes) shall achieve First Contentful Paint (`FCP`) `<= 1.5 s` and Time to Interactive (`TTI`) `<= 2.5 s` (and `TTI <= 5.0 s` on Simulated Slow 4G). | Provisional-Must | Learners entering `/`, `/simulator`, or `/library` must read and interact immediately without waiting for heavy WebGL assets. | Master Prompt s8 | HAK-PRD-029 | Test | Automated Lighthouse / Playwright performance trace on static production preview records `FCP <= 1.5 s` and `TTI <= 2.5 s` on desktop broadband and `<= 5.0 s` on throttled 4G across 3 consecutive cold-cache runs. | Draft |
| HAK-NFR-020 | 3D Scene Asset Load Time | On `/anatomy` and `/`, Plant-level 3D geometry and materials shall reach first interactive rendered frame within `<= 3.0 s` on Reference Desktop broadband (`<= 7.0 s` on Slow 4G), with Reactor/Component-level detail streamed progressively behind a visible loading progress indicator. | Provisional-Must | Keeps 3D exploration responsive while allowing high geometric fidelity on reactor internals. | Master Prompt s8 | HAK-PRD-020 | Test+Demonstration | Network waterfall and WebGL scene-ready timestamps measure `<= 3.0 s` to first interactive plant render on desktop broadband, with visible percentage/stage progress during progressive chunk fetch. | Draft |
| HAK-NFR-021 | 3D Rendering Frame Rate | During continuous camera orbit, exploded-view adjustment, or section-cut manipulation at `/anatomy` and `/journey`, the 3D viewport shall sustain `>= 60 fps` (frame time `<= 16.7 ms`) on Reference Desktop hardware and `>= 30 fps` (frame time `<= 33.3 ms`) on Constrained/Mobile hardware. | Provisional-Should | Smooth camera motion prevents spatial disorientation and preserves industrial UI responsiveness. | Master Prompt s8 | HAK-PRD-020 | Test | Profiling a scripted 10-second orbit + explode + section-cut sweep reports median `>= 60 fps` (desktop) and `>= 30 fps` (mobile/throttled profile) with zero multi-second stalls. | Draft |
| HAK-NFR-022 | UI and 3D Interaction Latency | Pointer click, hover highlight, tree-node selection, tab switching, and Library client-side search filtering shall reflect visual and state updates within `<= 100 ms` from input event to next painted frame. | Provisional-Must | Sub-100 ms response maintains direct-manipulation feel across 3D picking, component trees, and search. | Master Prompt s8 | HAK-PRD-020 | Test | Browser performance trace of 3D raycast selection, Component Tree click, and Library search query measures input-to-paint latency `<= 100 ms` at the 95th percentile. | Draft |
| HAK-NFR-023 | Simulation Step Execution Latency | Each discrete simulation integration step and derived telemetry snapshot in `/simulator` shall execute in `<= 5 ms` median and `<= 16 ms` maximum (isolated from main UI paint via Web Worker when required) so live chart and UI interactions never drop frames. | Provisional-Must | Ensures real-time educational responsiveness even at accelerated time multipliers without blocking browser rendering. | Master Prompt s8 | HAK-PRD-022 | Test+Analysis | Unit/worker benchmark running 1,000 consecutive transient steps measures `<= 5 ms` median and `<= 16 ms` p99 per step without blocking main-thread animation frames. | Draft |
| HAK-NFR-024 | Client Runtime Memory Budget | Steady-state browser tab memory (JS heap plus WebGL texture/buffer allocations) across any module session shall remain `<= 512 MB` on Reference Desktop and `<= 256 MB` on Constrained/Mobile profiles, with zero unbounded memory growth across repeated route switches. | Provisional-Should | Prevents mobile browser tab crashes and GPU context loss during extended study sessions. | Master Prompt s8 | HAK-PRD-030 | Test | Repeatedly navigating across all six routes and toggling levels 5 times shows peak tab memory `<= 512 MB` (desktop) / `<= 256 MB` (mobile) and `< 5%` residual heap growth after disposal. | Draft |
| HAK-NFR-025 | Static Asset and Bundle Size Budget | Initial route JS + CSS transfer size shall not exceed `500 KB` gzipped (excluding lazy-loaded 3D runtime chunks and math/chart chunks), and total compressed 3D glTF/GLB assets shall not exceed `15 MB` across all detail levels. | Provisional-Should | Supports fast static GitHub Pages delivery over global educational networks and mobile data connections. | Master Prompt s14 | HAK-PRD-029 | Inspection+Test | Production build bundle analyzer verifies initial JS+CSS `<= 500 KB` gzipped and total compressed `.glb`/mesh asset footprint `<= 15 MB`. | Draft |
| HAK-NFR-026 | Low-End Hardware and WebGL Fallback | When GPU frame times exceed budget (`< 24 fps` sustained) or WebGL context initialization fails or is lost, the platform shall automatically scale down Device Pixel Ratio (`DPR`), simplify shader/particle density, or switch cleanly to an interactive 2D SVG/canvas schematic fallback with full metadata and simulation access. | Provisional-Must | Guarantees learners on school Chromebooks, locked-down lab machines, or older devices can still complete every learning objective. | Master Prompt s8 | HAK-PRD-030 | Test+Demonstration | Simulating WebGL context loss or disabled hardware acceleration displays a clean recovery notice and interactive 2D schematic fallback while keeping Component Tree, Info Panel, Simulator, and Library fully functional. | Draft |

## 3. Accessibility Requirements (WCAG 2.2 Level AA)

HAKUREN targets **W3C Web Content Accessibility Guidelines (WCAG) 2.2 Level AA** (`HAK-SRC-021`) across all UI chrome, textual learning content, charts, and interactive controls, paired with **WAI-ARIA Authoring Practices Guide (APG)** keyboard patterns (`HAK-SRC-022`) for custom widgets such as the Component Tree, Tabs, and Sliders. Because a real-time 3D WebGL canvas cannot expose native DOM geometry directly to screen readers, HAKUREN provides full semantic parity via the synchronized Component Tree, structured Info Panel, and keyboard camera/preset controls.

| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|---|
| HAK-NFR-027 | WCAG 2.2 Level AA Baseline Conformance | All six modules and shared navigation shell shall conform to WCAG 2.2 Level A and Level AA success criteria (`HAK-SRC-021`), with documented accessible alternatives wherever spatial WebGL rendering conveys information. | Must | Ensures equitable access for learners using assistive technologies or keyboard-only workflows. | HAK-SRC-021 | HAK-PRD-031 | Test+Inspection | Automated accessibility audit (`axe-core`) yields zero critical/serious WCAG 2.2 AA violations across all 6 routes, supplemented by manual keyboard and screen-reader sign-off. | Draft |
| HAK-NFR-028 | Text and Non-Text Contrast | Visual text shall maintain a contrast ratio `>= 4.5:1` (`>= 3:1` for large text `>= 18 pt` or `>= 14 pt` bold) per WCAG 2.2 SC `1.4.3`, and UI component borders, focus rings, active states, chart series, and boundary icons shall maintain `>= 3:1` contrast against adjacent colors per SC `1.4.11` (`HAK-SRC-021`), without relying on color alone to convey meaning. | Must | Dark graphite/midnight navy themes require strict luminance discipline so cyan/amber/red signals remain legible (`HAK-PRD-034`). | HAK-SRC-021 | HAK-PRD-031 | Inspection+Test | Contrast verification across all design tokens confirms `>= 4.5:1` for body/telemetry text and `>= 3:1` for UI controls, focus indicators, and chart/legend graphics paired with text/pattern cues. | Draft |
| HAK-NFR-029 | Keyboard Operability and Visible Unobscured Focus | Every interactive control—including global navigation, Component Tree (`tree`/`treeitem` arrow navigation per `HAK-SRC-022`), 3D camera/preset triggers, sliders, scenario steps, and library search—shall be fully operable by keyboard alone without keyboard traps (SC `2.1.1`, `2.1.2`), display a visible focus indicator (SC `2.4.7`), and ensure focused elements are never completely hidden by sticky bars or floating drawers (SC `2.4.11`, `HAK-SRC-021`). | Must | Enables full navigation and 3D/simulator interaction without a pointing device. | HAK-SRC-021 | HAK-PRD-031 | Test+Demonstration | Complete Tab/Shift+Tab/Arrow/Enter/Escape walkthrough across all six modules operates every control without mouse input, shows visible focus rings, and keeps focused elements unobscured. | Draft |
| HAK-NFR-030 | Pointer Target Size and Responsive Reflow | Interactive pointer targets (buttons, layer toggles, tree expanders, hotspot pins, tabs) shall measure at least `24x24` CSS pixels or maintain equivalent spacing per WCAG 2.2 SC `2.5.8`, and prose, forms, dashboards, and panels shall reflow cleanly at `320` CSS pixel width without two-dimensional scrolling per SC `1.4.10` (noting the 2D-spatial exception for the 3D canvas and wide data tables wrapped in scroll containers, `HAK-SRC-021`). | Must | Improves touch accuracy on mobile/tablet and prevents clipped UI on narrow viewports or high browser zoom. | HAK-SRC-021 | HAK-PRD-030 | Inspection+Test | Layout inspection at `320 px` width and `200%` zoom confirms zero horizontal page overflow on prose/controls and `>= 24x24` CSS px hit targets or compliant spacing on all interactive controls. | Draft |
| HAK-NFR-031 | Assistive Semantics and Dynamic Status Announcements | Custom UI widgets (tree view, tabs, sliders, drawers) shall expose accurate programmatic Name, Role, Value, and State via semantic HTML/ARIA (WCAG SC `4.1.2`), and non-focused dynamic updates—such as 3D component selection, simulation state transitions (`EducationalTrip`, `WarningBound`), and scenario step completion—shall be announced cleanly via `aria-live` status messages (SC `4.1.3`, `HAK-SRC-021`). | Must | Allows screen-reader users to perceive simulation trips and 3D inspections without unexpected focus jumps. | HAK-SRC-021 | HAK-PRD-031 | Test+Inspection | Screen-reader verification (VoiceOver/NVDA) confirms accurate role/value announcements for sliders and tree items and non-intrusive polite/assertive live announcements on selection and trip events. | Draft |

## 4. Reduced Motion Requirements

| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|---|
| HAK-NFR-032 | Reduced Motion and Animation Controls | HAKUREN shall respect the CSS/DOM media query `prefers-reduced-motion: reduce` (`HAK-SRC-024`) and provide an in-app animation pause/toggle (aligned with WCAG 2.2 SC `2.2.2` Pause, Stop, Hide and SC `2.3.3` Animation from Interactions, `HAK-SRC-021`) that stops decorative camera auto-orbit, replaces smooth camera fly-to animations with instant transitions, and swaps moving Energy Journey flow particles for clear static directional indicators. | Must | Protects learners with vestibular disorders or motion sensitivity from dizziness while preserving all engineering information. | HAK-SRC-024 | HAK-PRD-031 | Test+Demonstration | Enabling OS/browser `prefers-reduced-motion: reduce` (or the in-app Reduced Motion toggle) halts continuous 3D flow particles and camera sweeps immediately while retaining legible static flow arrows and full simulation charts. | Draft |

## 5. Browser Compatibility and Network Resilience

| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|---|
| HAK-NFR-033 | Modern Browser and WebGL 2 Support Matrix | HAKUREN shall support the latest two major stable releases of Google Chrome, Microsoft Edge, Mozilla Firefox, and Apple Safari (macOS and iOS/iPadOS) supporting ES2022, Web Workers, CSS Grid/Flexbox, and WebGL 2 (with graceful degradation under `HAK-NFR-026`). | Must | Covers standard university, personal laptop, and tablet browser environments without legacy polyfill bloat. | Master Prompt s14 | HAK-PRD-029 | Test | Cross-browser smoke suite passes across current Chrome, Firefox, Edge, and Safari desktop/mobile targets with zero fatal runtime errors. | Draft |
| HAK-NFR-034 | Offline Tolerance and Asset Fetch Failure Recovery | Once core shell assets are loaded, already-fetched Technical Library entries and the Reactor Simulator shall continue operating if network connectivity drops; if a lazy-loaded module chunk or 3D `.glb` asset fails to download, the UI shall display a clear error banner with a manual **Retry** action and keep unaffected modules usable. | Should | Protects classroom and unstable-network learners from blank white screens on transient fetch failures. | Master Prompt s14 | HAK-PRD-029 | Test+Demonstration | Simulating offline/404 failure on a 3D asset request displays a recoverable error banner with working Retry while Simulator and already-loaded Library pages remain operational. | Draft |

## 6. Security and Privacy Requirements

| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|---|
| HAK-NFR-035 | Zero-Account and Privacy-by-Default Operation | HAKUREN shall require no user accounts, login credentials, or server-side personal data collection, and shall deploy zero third-party advertising trackers or analytics cookies by default; any optional learner preferences (e.g., reduced motion toggle, completed scenario checklist) shall remain strictly client-local in browser storage with a clear reset option. | Must | Maximizes student privacy, eliminates backend auth attack surface, and simplifies institutional adoption. | Master Prompt s14 | HAK-PRD-029 | Inspection+Test | Network inspection across all six modules shows zero outbound telemetry/tracking requests and zero cookies set; clearing local storage resets optional UI preferences cleanly. | Draft |
| HAK-NFR-036 | Content Security Policy and Static XSS Hardening | HAKUREN shall enforce a strict Content Security Policy (`CSP`, `HAK-SRC-025`) restricting script execution to `'self'` (disallowing unsafe inline scripts and `eval`), disallowing external `<object>`/`<frame>` embeds, sanitizing any rendered Markdown/math HTML, and serving all static assets exclusively over HTTPS. | Must | Protects static GitHub Pages deployments against cross-site scripting (`XSS`) and unexpected third-party script injection. | HAK-SRC-025 | HAK-PRD-029 | Inspection+Test | CSP meta/header configuration passes automated CSP validation with no `unsafe-inline` script allowances and blocks injected script payloads in Library/search inputs. | Draft |

## 7. Maintainability and Internationalization Readiness

### 7.1 Indonesian / English Internationalization Decision

- **Product Decision (Internationalization Language Strategy):** HAKUREN will launch MVP (Release 1.0) in **English (`en`)** as the single active user-facing language, while **Indonesian (`id`)** is designated as the **first planned localization target** for post-MVP release (Release 1.1+).
- **Rationale:** Authoritative primary nuclear engineering references, canonical terminology (`RCS`, `RPV`, `SG`, `PZR`, `CRDM`), and Phase 0 validation sources (`NRC`, `DOE`, `W3C`) are authored in English; launching MVP in English preserves terminology consistency and avoids premature translation drift while Phase 0–1 physics and UI settle. Designing externalized locale keys and BCP 47 language-switching hooks from Day 1 eliminates costly UI refactoring when adding Indonesian educational support.
- **Alternatives Considered:** (1) Dual-language `en`/`id` launch in MVP — rejected due to double copy-validation workload during Phase 0/1; (2) Hardcoded English-only strings — rejected because retrofitting localization across 3D labels, glossary terms, and scenario instructions creates high technical debt.

| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|---|
| HAK-NFR-037 | Modular Schema-Driven Maintainability | Domain definitions, 3D component metadata, simulator parameter catalogs, guided scenarios, and library articles shall be stored as structured JSON/Markdown artifacts validated against JSON Schemas (`docs/11-data-contracts/`) decoupled from React/Three.js UI components. | Should | Lets subject-matter authors update educational content or add scenarios without editing simulation solver or WebGL rendering code. | Master Prompt s8 | HAK-PRD-029 | Inspection | Code/architecture review confirms component metadata, scenarios, parameters, and library entries load from schema-validated static data modules rather than hardcoded UI components. | Draft |
| HAK-NFR-038 | Internationalization-Ready Externalization and BCP 47 Tagging | All user-facing UI strings, ARIA labels, glossary keys, and scenario copy shall be externalized into typed locale resource bundles (with `en` active at MVP and `id` scaffolded as the first target locale), programmatically declaring the active document language via BCP 47 `lang` on the root `<html>` element (WCAG SC `3.1.1`, `HAK-SRC-021`, `HAK-SRC-023`) and formatting numbers without altering canonical SI unit symbols. | Must | Supports the English-first, Indonesian-next localization strategy cleanly without breaking screen-reader pronunciation (`HAK-SRC-023`) or SI unit integrity. | HAK-SRC-023 | HAK-PRD-031 | Inspection+Test | Source audit confirms UI chrome uses translation-key lookups rather than hardcoded copy, `<html lang="en">` is set dynamically per active locale, and a pseudo-locale or partial `id` test bundle renders without layout breakage. | Draft |

## 8. Content Integrity

| ID | Name | Requirement | Priority | Rationale | Source | Parent | Verification | Acceptance | Status |
|---|---|---|---|---|---|---|---|---|---|
| HAK-NFR-039 | Static Content Provenance and Build-Time Integrity | Build and CI validation checks shall verify that every numerical engineering parameter, formula, and article in the static data bundle includes a valid provenance classification (`Computed`, `Reference`, `Illustrative`, or `Simulated`), canonical SI units (or explicit dimensionless declaration), and a resolving `HAK-SRC` reference where `Reference` is claimed. | Must | Enforces Phase 0 scientific integrity guarantees automatically in production builds, preventing unlabelled or unverified claims from reaching learners. | Master Prompt s2 | HAK-PRD-026 | Test+Inspection | Running the static data validation pipeline against production JSON/Markdown bundles exits cleanly with zero missing units, zero invalid provenance tags, and zero dangling `HAK-SRC` citations. | Draft |

## 9. Provisional Performance Budget Summary

| Metric Category | Target (Reference Desktop) | Target (Constrained / Mobile) | Provisional Status | Governing Requirement |
|---|---|---|---|---|
| Initial Shell Load (`FCP` / `TTI`) | `FCP <= 1.5 s`, `TTI <= 2.5 s` | `TTI <= 5.0 s` (Slow 4G) | Provisional | `HAK-NFR-019` |
| 3D Plant First Frame Load | `<= 3.0 s` (broadband) | `<= 7.0 s` (Slow 4G) | Provisional | `HAK-NFR-020` |
| 3D Viewport Frame Rate | `>= 60 fps` (`<= 16.7 ms`) | `>= 30 fps` (`<= 33.3 ms`) | Provisional | `HAK-NFR-021` |
| UI & 3D Picking Latency | `<= 100 ms` (p95) | `<= 100 ms` (p95) | Provisional | `HAK-NFR-022` |
| Simulation Step Latency | `<= 5 ms` median / `<= 16 ms` max | `<= 16 ms` max | Provisional | `HAK-NFR-023` |
| Tab Peak Memory (JS + WebGL) | `<= 512 MB` | `<= 256 MB` | Provisional | `HAK-NFR-024` |
| Initial Bundle / Total 3D Assets | `<= 500 KB` gzip / `<= 15 MB` GLB | `<= 500 KB` gzip / LOD streaming | Provisional | `HAK-NFR-025` |

## 10. References

- `HAK-SRC-021` — W3C Web Content Accessibility Guidelines (WCAG) 2.2
- `HAK-SRC-022` — W3C WAI ARIA Authoring Practices Guide (APG): Tree View Pattern
- `HAK-SRC-023` — W3C Internationalization: Declaring language in HTML
- `HAK-SRC-024` — MDN Web Docs: `prefers-reduced-motion`
- `HAK-SRC-025` — MDN Web Docs: Content Security Policy (CSP)

## 11. Related Documents

- [Product Requirements Document (PRD)](product-requirements-document.md)
- [Functional Requirements Specification](functional-requirements.md)
- [Feature Catalog](feature-catalog.md)
- [Documentation Authoring Contract](../00-governance/documentation-authoring-contract.md)
- `docs/01-product/accessibility-requirements.md` (planned Stage 1)
- `docs/11-data-contracts/data-contract-overview.md` (planned Stage 11)
- `docs/12-quality-assurance/performance-test-plan.md` (planned Stage 12)
