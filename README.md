# ARGON Health Platform — Architecture Repository

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Repository Consolidation Notice (2026-09-05)
This repository (`ARGON-HEALTH`) is now the **single canonical
repository** for the ARGON target architecture. It was produced by
consolidating this repository's prior content with `system-ARGON-NEW`
(a later, more complete pass on the same document set) — see
`docs/audit/REPOSITORY-CONSOLIDATION-MATRIX.md` for the full comparison
and `docs/audit/CONSOLIDATION-DECISIONS.md` for the per-file merge
record. **`system-ARGON-NEW` is retired to historical/source material
only; all future ARGON target-architecture work happens here.** Nothing
about this consolidation authorizes implementation — see "Before
implementation starts" below, unchanged in substance from before the
consolidation.

**TARGET ARCHITECTURE ≠ IMPLEMENTED SYSTEM.** Everything in this
repository is a design/target artifact. No claim here is a claim that
any of it has been built, deployed, tested, or certified. See
`docs/governance/ARGON-SOURCE-OF-TRUTH.md` for how document authority is
resolved and `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` for open
findings.

## Vision
ARGON Health Platform is designed to scale from a single clinic to
hospital networks — EMR, pharmacy, laboratory, radiology, hospital
operations, billing, insurance, and government/interoperability
integration — under one control plane and one role-aware application.
Full statement: `docs/MASTER-ARGON-BLUEPRINT.md`.

## Scope
Clinic → Medical Center → Medical Complex → Hospital → Hospital Network,
plus standalone Pharmacy, Laboratory, and Radiology facility types, all
provisionable from a central Control Plane.

## Architecture Status
**TARGET ARCHITECTURE / PROPOSED.** Nothing in `docs/master/` has been
independently reviewed, approved, implemented, or evidenced yet — see
`docs/governance/ARCHITECTURE-STATUS.md` for the per-decision status
register.

## Current Phase
Architecture Baseline Freeze (repository normalization). The next
authorized phase, once this baseline is reviewed and accepted by whoever
owns decision authority for the project, is Foundation Implementation
per `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` — **see the
important caveat about this in "Before implementation starts" below.**

## Source of Truth
Document authority order and contradiction-resolution rules:
`docs/governance/ARGON-SOURCE-OF-TRUTH.md`.

## Master Blueprint
The single navigation entry point over every other document:
`docs/MASTER-ARGON-BLUEPRINT.md`.

## Technology Baseline
Adopted/Conditional/Deferred/Rejected technology decisions and the
evidence behind them: `docs/governance/TECHNOLOGY-BASELINE.md`
(governance layer) → `docs/master/14-MASTER-TECHNOLOGY-STACK.md`
(decision) → `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`
(underlying research).

## Repository Navigation
```
docs/
├── master/         01–20 master architecture documents + the Blueprint
├── adr/             Full-format ADRs: Messaging Platform, ADR-019
│                     (ADR-016/017/018 live in 19 only — no longer
│                     duplicated as standalone files, see consolidation
│                     decision log)
├── evidence/         Technology Baseline Verification (live research)
├── audit/            Consolidation matrix + decisions, GAP register +
│                     analysis, DO-NOT-BUILD-YET, Legacy boundary/mapping/
│                     lessons, completeness + implementation-readiness
│                     reports, consistency audit, normalization report,
│                     continuous-improvement report
├── governance/       Source-of-truth, technology baseline, lint rules,
│                     architecture status, freeze + change rules,
│                     decision authority, version policy, traceability,
│                     performance governance
├── compliance/       Compliance traceability matrix
├── security/         (reserved — security detail lives in docs/master/07
│                     until it outgrows that single file)
├── interoperability/ (reserved — detail lives in docs/master/06 today)
├── workflows/        (reserved — detail lives in docs/master/05 today)
└── operations/       (reserved — operational runbooks, none written yet)
```
Several folders above are placeholders for future material that
currently lives inside a single master document; they exist now so a
future split doesn't require another renumbering pass.

## ADR Governance
Lightweight decisions (ADR-001–015) and full-format decisions ADR-016
through ADR-020, all indexed in
`docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`. Two of those
(Messaging Platform, ADR-019) also have a standalone full file in
`docs/adr/` for direct linking; ADR-016/017/018 do not — their
standalone duplicates were removed during consolidation since `19`
already carries their full text (see
`docs/audit/CONSOLIDATION-DECISIONS.md`). An ADR is Proposed until a
real decision authority (not this document set itself) reviews and
accepts it — see `docs/governance/DECISION-AUTHORITY.md` and
`docs/master/19` "Current Assumptions."

## Security Principles
Three-layer authorization (application + service + PostgreSQL RLS),
structural separation of Control Plane privilege from clinical PHI
access, break-glass-only elevation for sensitive data. Full detail:
`docs/master/07-MASTER-SECURITY-MAP.md`.

## Compliance Principles
Compliance is treated as engineering: every requirement moves through
Requirement → Control → Implementation → Test → Evidence → Review, and
"we built it" is never read as "an auditor approved it." Full detail:
`docs/master/08-MASTER-COMPLIANCE-MAP.md`,
`docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`.

## Implementation Status
**Nothing described in this repository has been implemented.** This
repository contains architecture and planning documents only — no
application code, no infrastructure-as-code, no deployed environment.

## Current Blockers
- RTO/RPO and performance figures throughout `17`/`18` are unmeasured
  targets pending business sign-off, not capacity claims.
- Jurisdiction-specific legal/compliance status is UNKNOWN /
  REQUIRES LEGAL REVIEW for every country in `docs/master/08`.
- *(Resolved 2026-08-27 — see below)* ~~ADR-014's stack reconciliation~~

## Before implementation starts
**Read this before writing any code against this baseline.** ADR-014's
reconciliation question is now **RESOLVED by ADR-019**
(`docs/adr/ADR-019-RECONCILIATION-WITH-ADR-000.md`): this repository's
Java/Spring Boot/PostgreSQL baseline is the *updated technical content*
of an existing, separate governing decision — **ADR-000** (the
`argon-platform-target-architecture` skill, dated 2026-08-22, "reality
over ambition" staged-evolution plan) — and is fully subordinate to
ADR-000's Staged Trigger Table and AI Agent Rules. **This repository is
a long-term North Star, not a near-term build order.** No phase in
`docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` is authorized to start
merely because it's documented here — each phase now carries an explicit
ADR-000 trigger cross-reference, and **Phase 1 has no fired trigger
today.** The actual next real step toward this vision is ADR-000's own
"build now" list: `license_tier`/`enabled_modules` fields added
additively inside the current live Firebase schema, enforced
server-side — zero rewrite risk, buildable today. ADR-019 also adds a
permanent gate (Rule L15,
`docs/governance/ARCHITECTURE-LINT-RULES.md`) requiring a verified
functional build environment *and* an adversarial code audit before any
future phase may be marked implemented — sourced directly from a real,
dated (2026-08-23) blocked/defective rebuild attempt on an earlier
version of this same stack.

## Next Authorized Phase
Per the Final Gate in this normalization pass: this baseline is
**NORMALIZED, CONSISTENT, TRACEABLE, GOVERNED** — see
`docs/governance/ARCHITECTURE-STATUS.md` and the full
`docs/audit/FINAL-NORMALIZATION-REPORT.md`. It is explicitly **NOT**
PRODUCTION READY. With ADR-014 now resolved by ADR-019, the two
remaining preconditions before Foundation Implementation (Phase 1 of
this document set) may start are: (a) an actual decision authority
reviews/accepts the ADR log in `docs/master/19` + `docs/adr/`, and (b) a
row in **ADR-000's Staged Trigger Table** actually fires — a real client
signal, not a document existing. Until then, the actionable next step is
ADR-000's "build now" list above, inside the live Firebase system, not
this repository's stack.
