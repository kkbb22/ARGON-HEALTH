# TRACEABILITY MATRIX

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Purpose
Demonstrate — with real, worked examples rather than an abstract empty
template — that a critical business capability can be traced end to end:
Requirement → Domain → Workflow → API → Data → Security Control →
Compliance Requirement → Test → Evidence → Release.

## Scope
Full traceability for three representative critical capabilities (chosen
for coverage breadth: a clinical-safety-critical action, a
financial-integrity-critical action, and a security-critical action).
Every other domain/workflow follows the same pattern — this document
shows the pattern proven, not exhaustively repeated 39 times.

## Worked Trace 1 — "A pharmacist must not dispense a medication that
conflicts with a documented patient allergy"

| Stage | Reference |
|---|---|
| Business Requirement | Prevent adverse drug events from allergy conflicts |
| Domain | `Pharmacy` (`docs/master/03-MASTER-DOMAIN-MAP.md`) |
| Workflow | Pharmacy (Prescription → Dispense), `docs/master/05-MASTER-WORKFLOW-MAP.md` §6 |
| API | Internal Pharmacy Service API — `CheckInteractions` command (`03`) |
| Data | `Allergy` entity (Clinical domain), `Prescription`/`DispenseRecord` (Pharmacy domain) — PHI classification, `docs/master/04-MASTER-DATA-MAP.md` |
| Security Control | Pharmacist-role write access to dispense; interaction-check gate is a hard block, not advisory (`docs/master/07-MASTER-SECURITY-MAP.md` RBAC model) |
| Compliance Requirement | N/A directly regulatory, but a `docs/master/16-MASTER-CLINICAL-SAFETY-MODEL.md` hazard: "Wrong Medication" |
| Test | Security layer — DENY dispense on unresolved allergy flag; `docs/master/15-MASTER-TESTING-STRATEGY.md` |
| Evidence | Hazard Evidence status: DESIGNED (not yet TESTED/EVIDENCED — `docs/master/16` hazard register) |
| Release | Gated by the Release workflow's quality gate (`docs/master/05` §12) — no wave proceeds without the full Security/Authorization ALLOW+DENY suite passing |

**Trace verdict: COMPLETE at the design/documentation level.** No gap
found in the chain above; the only open item is that Test/Evidence are
not yet executed (expected — no implementation exists, per
`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding 1).

## Worked Trace 2 — "A posted invoice must never be silently altered"

| Stage | Reference |
|---|---|
| Business Requirement | Financial-record integrity, auditability for tax/e-invoicing compliance |
| Domain | `Billing` (`03`) |
| Workflow | Billing (Charge → Payment), `docs/master/05-MASTER-WORKFLOW-MAP.md` §9 |
| API | Internal Billing Service API — `IssueCreditNote` command, never an in-place `UpdateInvoice` command (`03` — deliberately absent) |
| Data | `Invoice`, `CreditNote` entities — PostgreSQL `NUMERIC`, financial classification, append-only (`docs/master/04-MASTER-DATA-MAP.md`) |
| Security Control | Finance role required for credit notes; billing staff cannot directly edit a posted record (`docs/master/07-MASTER-SECURITY-MAP.md`) |
| Compliance Requirement | Jordan / GCC e-invoicing requirements — `docs/master/08-MASTER-COMPLIANCE-MAP.md` register row "Electronic invoicing format & submission," status DISCOVERED, REQUIRES LEGAL REVIEW |
| Test | Security layer — DENY in-place edit of a posted invoice; ALLOW correction only via credit note (`docs/master/15`) |
| Evidence | Compliance status: DISCOVERED only — REQUIRES LEGAL REVIEW before DESIGNED (`docs/master/08`) |
| Release | Same Release workflow gate as Trace 1 |

**Trace verdict: COMPLETE, with an explicitly flagged open compliance
gap** (legal review not yet performed) — this is the trace working
correctly, not a defect: it surfaces the real gap instead of hiding it.

## Worked Trace 3 — "A Control Plane operator must not read patient
clinical data without an audited, time-boxed, reason-documented
exception"

| Stage | Reference |
|---|---|
| Business Requirement | Structural separation between platform administration and PHI access |
| Domain | `Control Plane` (`03`), enforced jointly with `Authorization` (`03`) |
| Workflow | Cross-cutting — applies to every workflow, not one specific sequence; enforced at the Authorization layer, not a workflow step |
| API | Authorization Service `Evaluate(actor, resource, action, context)` (`Authorization` domain, `03`) |
| Data | `BreakGlassGrant` entity — audit-classified, `docs/master/04-MASTER-DATA-MAP.md` |
| Security Control | Three-layer enforcement (app + Authorization Service + PostgreSQL RLS); break-glass requires step-up MFA + reason + time-box (`docs/master/07-MASTER-SECURITY-MAP.md`) |
| Compliance Requirement | Purpose-of-use and least-privilege controls — feeds `docs/master/08-MASTER-COMPLIANCE-MAP.md`'s security-baseline rows |
| Test | DENY Control-Plane-operator PHI access by default; ALLOW only via audited, time-boxed break-glass (`docs/master/15`) |
| Evidence | Not yet tested/evidenced — design-stage only |
| Release | Same Release workflow gate |

**Trace verdict: COMPLETE.**

## Traceability Pattern (for any of the remaining 36+ domains)
```
Business Requirement
  → find the owning Domain in docs/master/03-MASTER-DOMAIN-MAP.md
  → find the owning Workflow in docs/master/05-MASTER-WORKFLOW-MAP.md
  → the Domain's "APIs"/"Commands"/"Queries" fields are the API stage
  → the Domain's "Entities"/"Data Classification" fields are the Data stage
  → the Domain's "Permissions" field, cross-checked against
    docs/master/07-MASTER-SECURITY-MAP.md, is the Security Control stage
  → the Domain's "Compliance Requirements" field, resolved against
    docs/master/08-MASTER-COMPLIANCE-MAP.md, is the Compliance stage
  → the Domain's testing hints, formalized in
    docs/master/15-MASTER-TESTING-STRATEGY.md, are the Test stage
  → status in docs/master/08 or docs/master/16 (whichever applies) is
    the Evidence stage
  → docs/master/05 §12's Release workflow is the Release stage for all
```

## Alternatives Considered
- **A single giant matrix attempting all 40 domains × 30 workflows**
  (rejected for this pass) — would be either shallow-and-mechanical
  (low value) or enormous (low legibility); three fully worked examples
  plus a reusable pattern is more genuinely checkable than a
  half-completed exhaustive table.

## Dependencies
Depends on `docs/master/03`, `05`, `07`, `08`, `15`, `16`. Feeds
`docs/governance/ARCHITECTURE-STATUS.md`.

## Unknowns
UNKNOWN whether the pattern above holds cleanly for every one of the
remaining domains without adaptation — the three chosen here were picked
for breadth (clinical safety, financial integrity, security) precisely
because they are likely to expose any gap in the pattern, but this is
not a guarantee every domain is friction-free.

## Definition of Done
The three worked traces above are complete with no missing stage;
the reusable pattern is documented; full expansion to all 40 domains is
explicitly deferred, not silently skipped — trigger: a specific domain
enters Phase 1+ implementation (`docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md`),
at which point its full trace should be written before that phase's
Definition of Done is considered met.
