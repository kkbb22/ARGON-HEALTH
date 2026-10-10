# FINAL GAP REGISTER

STATUS: PROPOSED
EVIDENCE CLASS: RUNTIME EVIDENCE (closure verified against the actual edited files, 2026-09-02, under ADR-020)

## Purpose
Executive register of every gap found in
`docs/audit/FINAL-GAP-ANALYSIS.md`, with its closure status verified
against the real document edits made this pass — not asserted.

## Register

| ID | Domain | Gap | Severity | Evidence (of closure) | Blocking? | Dependency | Recommended Action | Status |
|---|---|---|---|---|---|---|---|---|
| GAP-001 | Security | No service-identity/M2M auth model | P2 | `07` §Identity & Session Baseline — Service identities subsection added | No | `06`, `13` | Elaborated with GCP workload identity + OAuth2 client-credentials pattern | **CLOSED** |
| GAP-002 | Security | No refresh-token lifecycle detail | P2 | `07` §Identity & Session Baseline — rotation + reuse-detection + conditional device-binding added | No | Keycloak config (`14`) | Elaborated | **CLOSED** |
| GAP-003 | Security | No bulk-access/search-restriction model for PHI | **P1** | `07` — new §Bulk Access Control | Should block Phase 2 sign-off | `Patient`, `Documents`, `Analytics` (`03`) | Elaborated: bulk classified separately, rate-limited, own audit category, approval-gated for high-volume | **CLOSED** |
| GAP-004 | Control Plane | No licensing lifecycle beyond initial grant | P2 | `09` — new §Licensing Lifecycle | No | `Billing`, `Organization` (`03`) | State machine + data-safety guarantees added; **exact durations remain a business decision** | **PARTIALLY CLOSED** — architecture done, numeric parameters open (see DO-NOT-BUILD-YET) |
| GAP-005 | Data/Multi-tenancy | Background jobs/exports/caching isolation not explicit | **P1** | `04` — new §Tenant Isolation Beyond Synchronous Requests | Should block Phase 1 sign-off | `07`, `Observability` | Explicit rules added for all three async paths | **CLOSED** |
| GAP-006 | Security | OWASP attack classes not named | P2 | `07` — new §OWASP Attack-Class Mapping (5-row table) | No | Every domain in `03` | Explicit control-per-attack-class mapping added | **CLOSED** |
| GAP-007 | Security/DevSecOps | Artifact signing, license scanning absent | P3 | `07` §Security Architecture Components — both added to the supply-chain list | No | `05` §12 | Elaborated | **CLOSED** |
| GAP-008 | Patient App | No account recovery / device-session management | P2 | `12` §Patient App — both added | Should block Phase 2 Patient App work | `Identity` (`03`), `07` | Step-up recovery + self-service session revocation added; **specific recovery-channel method deferred to Phase 1 detail** | **PARTIALLY CLOSED** — architecture done, implementation-level method choice open |
| GAP-009 | Data Governance | No legal-hold or deletion-policy treatment | **P1** | `04` — new §Retention, Legal Hold, and Deletion; `08` cross-referenced | Would block a "delete my data" feature specifically | `08`, every clinical domain (`03`) | Anonymization-not-erasure principle + legal-hold flag added; **exact retention periods per jurisdiction REQUIRES LEGAL VERIFICATION** | **PARTIALLY CLOSED** — architecture/mechanism done, legal parameters open |
| GAP-010 | DR | No named catastrophic scenarios | P2 | `17` — new §Named Scenario Runbooks (ransomware, regional outage, identity-provider outage) | Would block a real DR drill | `13`, every Data Plane component | Three scenario runbooks added, cross-referencing the per-component register | **CLOSED** |
| GAP-011 | Billing/Insurance | Co-pay/deductible/currency not explicit | P3 | `03` `Insurance` (CoverageTerms entity) + `Billing` (currency field) | No | `Billing`, `Insurance` (`03`) | Both named explicitly as distinct entities/fields | **CLOSED** |
| GAP-012 | Control Plane | Template cloning/versioning not explicit | P3 | `11` — new bullet under Saga Guarantees | No | `09`, `11` | Versioning + pinned-at-creation + cloning-as-saga-variant added | **CLOSED** |
| GAP-013 | Testing | Privilege-escalation/break-glass not named test categories | P2 | `15` §Security/Authorization/RLS/Tenant Isolation — both named explicitly | No | `07`, `15` | Explicit ALLOW/DENY cases named for both | **CLOSED** |

## Summary
- **CLOSED: 10 / 13** (77%)
- **PARTIALLY CLOSED: 3 / 13** (23%) — GAP-004, GAP-008, GAP-009. Every
  one of these three has its architecture/mechanism fully closed; each
  has a specific, named, non-architectural remainder (a business
  decision, an implementation-level method choice, or a legal review)
  that this pass correctly does not invent an answer for.
- **DEFERRED: 0 / 13** — nothing was pushed off without at least a
  partial architectural answer.

## Consistency Verification
Cross-checked against the actual repository (not asserted): every
`GAP-0xx` closure reference in the register above resolves to (a) a
real, edited section in the named document, and (b) the corresponding
gap definition in `docs/audit/FINAL-GAP-ANALYSIS.md`. Full sweep results
in `docs/audit/FINAL-ARCHITECTURE-COMPLETENESS.md`-style verification,
run live this pass — 13/13 closures found real matches, zero orphaned
references.

## Dependencies
Depends on `docs/audit/FINAL-GAP-ANALYSIS.md`. Feeds
`docs/audit/DO-NOT-BUILD-YET.md`,
`docs/audit/FINAL-IMPLEMENTATION-READINESS.md`.

## Definition of Done
Every one of the 13 gaps has a verified, non-asserted closure status
above; the 3 PARTIALLY CLOSED items have their exact remaining scope
named, not left vague.
