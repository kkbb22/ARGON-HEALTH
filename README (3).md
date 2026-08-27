# ARGON Health Platform

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

**TARGET ARCHITECTURE ≠ IMPLEMENTED SYSTEM.** Everything in this
repository, as of 2026-08-27, is documentation of a target architecture.
No code, no infrastructure, and no production system exist yet. Read
that sentence again before reading anything else here.

## Vision
ARGON Health Platform is a healthcare operating system designed to scale
from a single clinic to hospital networks — EMR, pharmacy, laboratory,
radiology, hospital operations, billing, insurance, and government/
interoperability integration, under one control plane and one
role-aware application design.

## Scope
Clinic → Medical Center → Medical Complex → Hospital → Hospital Network,
plus standalone Pharmacy, Laboratory, and Radiology Center facility
types — all provisionable from a central Control Plane.

## Architecture Status
**ARGON ARCHITECTURE BASELINE — NORMALIZED, CONSISTENT, TRACEABLE,
GOVERNED.** Not production ready. Not certified. Not compliant with any
named standard — every such claim requires independent evidence this
repository does not yet contain. See
`docs/governance/ARCHITECTURE-STATUS.md` for the live status of every
decision, domain, and workflow.

## Current Phase
**Phase 0 — Architecture Foundation: complete for this pass, including
the 2026-08-27 Normalization pass** (repository restructuring, fresh
technology verification, consistency audit, governance layer). **Phase
1 — Foundational Domains: not started.** See
`docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` for the full,
trigger-gated phase sequence — phases start on evidence of real need,
not on a calendar date.

## Source of Truth
When two documents disagree, `docs/governance/ARGON-SOURCE-OF-TRUTH.md`
defines which one wins (Executable evidence → Approved ADR → Verified
Technology Baseline → Master Blueprint → Master Architecture → Detailed
design → Supporting documents → Historical documents). Chat/conversation
history is never authoritative over this repository's own governed
documents.

## Master Blueprint
`docs/MASTER-ARGON-BLUEPRINT.md` is the single highest-level navigational
document — start there for a guided tour through every domain, workflow,
and cross-cutting concern, each pointing to its full detail document.

## Technology Baseline
`docs/governance/TECHNOLOGY-BASELINE.md` is the authoritative, current
ADOPT/CONDITIONAL/DEFERRED/REJECTED/SUPERSEDED decision table for every
technology in the stack, backed by
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`'s live research
(dated 2026-08-27). `docs/master/14-MASTER-TECHNOLOGY-STACK.md` carries
the same decisions in architecture-narrative form.

## Repository Navigation
```
docs/
├── MASTER-ARGON-BLUEPRINT.md      ← start here
├── master/                         20 master architecture documents (01–20)
├── adr/                            standalone Architecture Decision Records
├── governance/                     source-of-truth, status, version policy,
│                                    performance governance, lint rules,
│                                    traceability matrix, technology baseline
├── security/                       (reserved — detailed security design docs)
├── compliance/                     compliance traceability matrix
├── interoperability/               interoperability governance (FHIR/HL7/DICOM)
├── workflows/                      (reserved — detailed workflow design docs)
├── architecture/                   (reserved — supplementary architecture detail)
├── operations/                     (reserved — runbooks, once implementation exists)
├── evidence/                       technology verification, research findings
└── audit/                          architecture consistency audit records
```
Directories marked "(reserved)" exist in the governed structure but have
no content yet — they are not placeholders for fabricated content; they
are created so future documents land in the right place from day one.

## ADR Governance
Every architectural decision lives in
`docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` (the consolidated
log) or as a standalone file in `docs/adr/` for decisions significant
enough to warrant their own document (e.g.,
`docs/adr/ADR-MESSAGING-PLATFORM.md`). Every ADR carries a status —
**PROPOSED is not APPROVED** — see
`docs/governance/ARCHITECTURE-STATUS.md`'s ADR Status Board for the
current state of every decision. As of this Normalization pass, every
decision in the repository is at PROPOSED status; none has been reviewed
by a real decision authority yet.

## Security Principles
Three-layer authorization enforcement (application + Authorization
Service + PostgreSQL Row-Level Security); structural separation between
Control-Plane (platform-management) access and Clinical-Data access —
Super Admin does not imply PHI access. Full detail:
`docs/master/07-MASTER-SECURITY-MAP.md`.

## Compliance Principles
Compliance is engineering, not a claim: every requirement moves through
Requirement → Control → Implementation → Test → Evidence → Review, and a
status can never jump directly from IMPLEMENTED to APPROVED without
passing through TESTED and EVIDENCED. Full detail:
`docs/master/08-MASTER-COMPLIANCE-MAP.md`,
`docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`.

## Implementation Status
**None.** Confirmed by direct repository inspection during the
2026-08-27 Consistency Audit
(`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md`, Finding 1): this
repository contains architecture documentation only.

## Current Blockers
- No decision authority has yet reviewed or approved any ADR (all
  PROPOSED).
- RPO/RTO numeric targets and performance budgets remain undefined
  pending real business/operational sign-off (`docs/master/17`,
  `docs/governance/PERFORMANCE-GOVERNANCE.md`).
- Jurisdiction-specific legal/compliance status is UNKNOWN or REQUIRES
  LEGAL REVIEW for every covered country, including the home
  jurisdiction (`docs/master/08`).
- Grafana Cloud vs. self-hosted observability was not independently
  re-verified to the same confidence level as other 2026-08-27 findings
  (`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §9).

## Next Authorized Phase
Per `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md`: **Phase 1 —
Foundational Domains** (Platform, Identity, Organization, Membership,
Authorization), gated on an explicit decision by a real decision
authority to proceed, with the ADR log reviewed and PROPOSED entries
formally moved to APPROVED where accepted. **No business-module
implementation, infrastructure deployment, or IaC apply is authorized by
this repository's existence.**
