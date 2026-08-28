# Architecture Status Register

**STATUS:** ACTIVE (governance register)
**EVIDENCE CLASS:** DESIGN

## Purpose
One table showing the status of every major document/module/decision in
this repository, so "is X approved yet" has a single place to check
without opening every file.

## Status Values Used
PROPOSED · APPROVED · APPROVED WITH CONDITIONS · IMPLEMENTED · VERIFIED ·
EVIDENCED · SUPERSEDED · DEFERRED · REJECTED

## Master Documents
| Name | Status | Dependencies | Evidence | Owner | Last Reviewed | Next Review | Revisit Trigger |
|---|---|---|---|---|---|---|---|
| 01 System Architecture | PROPOSED | none (foundation) | DESIGN | UNKNOWN | 2026-08-27 | On any plane-boundary change | New plane or boundary violation found |
| 02 System Map | PROPOSED | 01 | DESIGN | UNKNOWN | 2026-08-27 | With any domain-group addition | New domain group added |
| 03 Domain Map | PROPOSED | 01, 02 | DESIGN | UNKNOWN | 2026-08-27 | On new domain / merge / split | New domain, or Tier-2 expansion request |
| 04 Data Map | PROPOSED | 01, 03 | DESIGN | UNKNOWN | 2026-08-27 | On new datastore type | New datastore or partitioning need |
| 05 Workflow Map | PROPOSED | 03, 04 | DESIGN | UNKNOWN | 2026-08-27 | On new workflow / Tier-2 expansion | New workflow or expansion request |
| 06 Integration Map | PROPOSED | 03, 05 | DESIGN + EXTERNAL RESEARCH | UNKNOWN | 2026-08-27 | On new external system class | New country, payer, or protocol |
| 07 Security Map | PROPOSED | 01, 03 | DESIGN | UNKNOWN | 2026-08-27 | On any authZ model change | New access pattern or incident |
| 08 Compliance Map | PROPOSED | 07 | DESIGN | UNKNOWN | 2026-08-27 | Per jurisdiction added | New target country |
| 09 Control Plane | PROPOSED | 01, 07 | DESIGN | UNKNOWN | 2026-08-27 | On new Control Plane capability | New platform-ops need |
| 10 Patient Journey | PROPOSED | 03, 04 | DESIGN | UNKNOWN | 2026-08-27 | On MPI/identity model change | Duplicate-identity incident |
| 11 Organization Provisioning | PROPOSED | 09 | DESIGN | UNKNOWN | 2026-08-27 | On saga-step change | Failed-provisioning incident |
| 12 Application Architecture | PROPOSED | 03 | DESIGN | UNKNOWN | 2026-08-27 | On new app/console | New role-specific console |
| 13 Infrastructure Architecture | PROPOSED | 14 | DESIGN + EXTERNAL RESEARCH | UNKNOWN | 2026-08-27 | On infra tech change | Measured scaling ceiling |
| 14 Technology Stack | PROPOSED | none (baseline) | DESIGN + EXTERNAL RESEARCH | UNKNOWN | 2026-08-27 | Per Version Management Policy cadence | EOL date, CVE, or new major release |
| 15 Testing Strategy | PROPOSED | 03, 07 | DESIGN | UNKNOWN | 2026-08-27 | On new test category need | Gap found in test pyramid |
| 16 Clinical Safety Model | PROPOSED | 03, 05 | DESIGN | UNKNOWN | 2026-08-27 | On new hazard identified | Near-miss or incident |
| 17 Disaster Recovery | PROPOSED | 04, 13 | DESIGN | UNKNOWN | 2026-08-27 | Per restore-test cadence (TBD) | Any real incident |
| 18 Non-Functional Requirements | PROPOSED | none (targets) | DESIGN | UNKNOWN | 2026-08-27 | On measured baseline availability | First load test |
| 19 Architectural Decisions | PROPOSED (index) | 01–18 | DESIGN | UNKNOWN | 2026-08-27 | Per new ADR | Any platform-wide decision |
| 20 Implementation Roadmap | PROPOSED | 01–19 | DESIGN | UNKNOWN | 2026-08-27 | Per phase-gate decision | Phase-gate sign-off |
| Master Blueprint | TARGET ARCHITECTURE COMPLETE (per its own closing status) | 01–20 | DESIGN | UNKNOWN | 2026-08-27 | On any master-doc change | Any of the above |
| Technology Baseline Verification | EVIDENCE RECORD | 14 | EXTERNAL RESEARCH | UNKNOWN | 2026-08-27 | Recommended every 3–6 months | Any EOL/relicense/major-release event |

## Architecture Decision Records
Full per-ADR status lives in `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`
(ADR-001–015, lightweight format) and `docs/adr/` (ADR-016–018,
full format). **All 18 ADRs are currently PROPOSED** — none have been
marked Accepted by a named decision authority. This is not a gap unique
to any one ADR; it reflects that this normalization pass has not itself
performed a review/sign-off step, per
`docs/governance/ARGON-SOURCE-OF-TRUTH.md` §2.

## This Normalization Pass
| Name | Status | Source | Dependencies | Evidence | Owner | Last Reviewed | Next Review | Revisit Trigger |
|---|---|---|---|---|---|---|---|---|
| Repository Normalization / Architecture Baseline Freeze | COMPLETE for this pass's scope; NOT independently reviewed | This document set | All of the above | DESIGN | UNKNOWN | 2026-08-27 | Before Foundation Implementation begins | Decision authority reviews ADR-014 reconciliation (see audit AUDIT-001) |

## Known Owner Gap
Every row above lists Owner as UNKNOWN. This repository does not name
individuals/roles as document owners anywhere in `01`–`20`. Assigning
real owners is recommended before Foundation Implementation begins, so
each document has a person accountable for its next review — tracked as
a governance gap, not silently assumed.
