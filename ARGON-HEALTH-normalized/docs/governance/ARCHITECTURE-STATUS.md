# ARCHITECTURE STATUS

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
GOVERNANCE RECORD. Dated 2026-08-27. This document IS the status board —
it has no separate "status" field of its own beyond being current as of
this date.

## Purpose
Give one place to check, for any decision/technology/domain/workflow in
this repository, whether it is merely proposed, formally approved, or
backed by real implementation evidence — so "we documented it" is never
mistaken for "we built it," and "we built it" is never mistaken for "an
auditor verified it."

## Status Model
```
PROPOSED
   → APPROVED
        → APPROVED WITH CONDITIONS
   → IMPLEMENTED
        → VERIFIED
             → EVIDENCED
   → SUPERSEDED   (by a later decision, at any point in the chain)
   → DEFERRED      (explicitly not being pursued now, at any point)
```
- **PROPOSED** — documented, not yet reviewed by a real decision
  authority.
- **APPROVED** — a named decision authority has signed off.
- **APPROVED WITH CONDITIONS** — approved, contingent on a stated
  follow-up (e.g., "approved pending legal review of jurisdiction X").
- **IMPLEMENTED** — code/infrastructure exists matching the decision.
- **VERIFIED** — tests confirm the implementation matches the decision.
- **EVIDENCED** — independent, auditable evidence exists (test results,
  conformance certificates, signed-off drill records) suitable for
  external review.
- **SUPERSEDED** — replaced by a later decision (the record is kept, not
  deleted — see `docs/governance/ARGON-SOURCE-OF-TRUTH.md`).
- **DEFERRED** — consciously not pursued at this time, with a stated
  trigger for revisiting (see `20-MASTER-IMPLEMENTATION-ROADMAP.md`'s
  phase triggers for examples of this pattern).

**This model is distinct from, but related to, two other status models
already in the repository:**
- `08-MASTER-COMPLIANCE-MAP.md`'s compliance lifecycle (UNKNOWN →
  DISCOVERED → REQUIRES LEGAL REVIEW → DESIGNED → IMPLEMENTED → TESTED →
  EVIDENCED → APPROVED → EXPIRED → NON-COMPLIANT) — use `08`'s model for
  compliance/regulatory requirements specifically.
- `16-MASTER-CLINICAL-SAFETY-MODEL.md`'s hazard Evidence status — use
  `16`'s model for clinical-safety hazard mitigations specifically.
This document's model applies to architecture decisions, technology
choices, domains, and workflows generally.

## Current Status — Summary

**Every item in this repository is at PROPOSED status.** No decision
authority external to this documentation pass has reviewed or approved
anything; no implementation exists (confirmed in
`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding 1). This is
stated plainly, once, here — individual tables below do not repeat
"PROPOSED" as commentary, only as the recorded status.

### ADR Status Board (`19-MASTER-ARCHITECTURAL-DECISIONS.md`)
| ADR | Title | Status |
|---|---|---|
| ADR-001 | Three-plane model | PROPOSED |
| ADR-002 | Modular monolith first | PROPOSED |
| ADR-003 | Cloud Run over Kubernetes | PROPOSED |
| ADR-004 | PostgreSQL as sole structural source of truth | PROPOSED |
| ADR-005 | DICOM/large binaries never in PostgreSQL | PROPOSED |
| ADR-006 | Single Interoperability Layer | PROPOSED |
| ADR-007 | Three-layer authorization enforcement | PROPOSED |
| ADR-008 | Control Plane / Clinical Data structural separation | PROPOSED |
| ADR-009 | Compliance status cannot skip IMPLEMENTED → APPROVED | PROPOSED |
| ADR-010 | Saga pattern for Organization Provisioning | PROPOSED |
| ADR-011 | Tiered documentation depth (Domain/Workflow Map) | PROPOSED |
| ADR-012 | RPO/RTO targets deferred pending sign-off | PROPOSED |
| ADR-013 | NFR targets sourced from vision material, labeled unmeasured | PROPOSED |
| ADR-014 | Java/Spring/PostgreSQL stack baseline, unreconciled against prior decisions | PROPOSED |
| ADR-015 | Digital provisioning ≠ legal/regulatory approval | PROPOSED |
| ADR-016 | Messaging: Pub/Sub primary, RabbitMQ conditional, Kafka rejected | **PROPOSED (new, 2026-08-27)** |
| ADR-017 | IaC: OpenTofu replaces Terraform | **PROPOSED (new, 2026-08-27)** |
| ADR-018 | FHIR production baseline corrected to R4/R4B | **PROPOSED (new, 2026-08-27)** |

### Technology Component Status Board (`14-MASTER-TECHNOLOGY-STACK.md`)
| Category | Confidence | Status |
|---|---|---|
| Java 25 LTS, Spring Boot 4.1, PostgreSQL 18, Next.js 16.3, React Native 0.87.x | High — independently re-verified 2026-08-27 | PROPOSED |
| Google Cloud Pub/Sub (primary messaging), OpenTofu (IaC), FHIR R4/R4B (production) | High — independently re-verified 2026-08-27, decision *changed* from prior target | PROPOSED |
| Cloud Run, Keycloak-on-Cloud-Run, GKE (rejected) | High — re-confirmed, no change | PROPOSED |
| Grafana Cloud (observability backend) | **Low — flagged, not independently re-verified to the same depth** | PROPOSED, pending dedicated research before any status increase |
| Cloudflare/Cloud Armor edge split | Not re-verified this pass | PROPOSED (unchanged from prior target) |

### Domain / Workflow Status Board
| Category | Count | Status distribution |
|---|---|---|
| Domains (`03-MASTER-DOMAIN-MAP.md`) | 39 | 39 PROPOSED / 0 APPROVED / 0 IMPLEMENTED |
| Workflows (`05-MASTER-WORKFLOW-MAP.md`) | 30 | 30 PROPOSED / 0 APPROVED / 0 IMPLEMENTED |
| Clinical safety hazards (`16`) | 10 | Tracked under `16`'s own Evidence-status column (all DESIGNED there — see that document, not duplicated here) |
| Compliance requirements (`08`) | Register (illustrative, not exhaustive) | Tracked under `08`'s own lifecycle (all DISCOVERED or lower there — see that document, not duplicated here) |

## Alternatives Considered
- **Reusing `08`'s compliance lifecycle for everything** (rejected) — a
  technology decision like "adopt OpenTofu" isn't a compliance
  requirement and doesn't need a jurisdiction/legal-review step; a
  separate, simpler model fits architecture decisions better.

## Dependencies
Depends on `19` (ADR log), `14` (technology stack), `03`/`05` (domain/
workflow inventories), `08`/`16` (their own status models, referenced not
duplicated). Feeds `docs/governance/TRACEABILITY-MATRIX.md`.

## Unknowns
UNKNOWN who the actual decision authority is for moving any item from
PROPOSED to APPROVED — this is an organizational fact this documentation
pass cannot supply.

## Definition of Done
Every ADR, technology component, domain, and workflow named anywhere in
`docs/master/` appears in one of the boards above with a real (not
placeholder) status; this document is re-generated whenever an ADR status
changes or a new decision is added to `19`.
