# ARGON Health Platform — Architecture Repository

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
Full statement: `docs/master/MASTER-ARGON-BLUEPRINT.md`.

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
`docs/master/MASTER-ARGON-BLUEPRINT.md`.

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
├── adr/             Full-format Architecture Decision Records (one per file)
├── evidence/         Technology Baseline Verification (live research)
├── audit/            Architecture Consistency Audit
├── governance/       Source-of-truth, technology baseline, lint rules,
│                     architecture status, version policy, traceability,
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
Lightweight decisions (ADR-001–015): `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`.
Full-format decisions (ADR-016–018), one file each: `docs/adr/`.
An ADR is Proposed until a real decision authority (not this document
set itself) reviews and accepts it — see `docs/master/19` "Current
Assumptions."

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
- ADR-014 (`docs/master/19`) — this document set's technology baseline
  (Java/Spring Boot/PostgreSQL) is **explicitly recorded as unreconciled**
  against an earlier architecture consultation for the same project. See
  "Before implementation starts" below — this is not a minor footnote.
- RTO/RPO and performance figures throughout `17`/`18` are unmeasured
  targets pending business sign-off, not capacity claims.
- Jurisdiction-specific legal/compliance status is UNKNOWN /
  REQUIRES LEGAL REVIEW for every country in `docs/master/08`.

## Before implementation starts
**Read this before writing any code against this baseline.** This
repository's own ADR-014 records that its Java/Spring Boot/PostgreSQL
stack was never reconciled against a prior, separate architecture
decision for this same project. If that prior decision concluded — as a
"reality over ambition" staged-evolution plan — that the live production
system should NOT be rewritten onto a new stack except when triggered by
real client signals, then this repository is best treated as a **long-
term North Star**, not a near-term build order, until someone with
authority over both documents explicitly resolves ADR-014 one way or the
other. Building against this baseline immediately, without resolving
that reconciliation, risks repeating the exact "rewrite everything before
Phase 2" failure mode that staged-evolution planning exists to prevent.

## Next Authorized Phase
Per the Final Gate in this normalization pass: this baseline is
**NORMALIZED, CONSISTENT, TRACEABLE, GOVERNED** — see
`docs/governance/ARCHITECTURE-STATUS.md` and the full
`docs/audit/FINAL-NORMALIZATION-REPORT.md`. It is explicitly **NOT**
PRODUCTION READY, and Foundation Implementation should not start until
(a) an actual decision authority reviews/accepts the ADR log in
`docs/master/19` + `docs/adr/`, and (b) ADR-014's stack-reconciliation
question above is resolved (tracked as Finding AUDIT-001 in
`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md`).
