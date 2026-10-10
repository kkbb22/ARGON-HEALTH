# DO NOT BUILD YET

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Purpose
Explicit register of everything that is architecturally premature,
evidence-gated, legally unverified, performance-unverified,
operationally unproven, or dependent on a real customer signal —
consolidated in one place so "we haven't built X yet" is never confused
with "we forgot X."

## Governed by ADR-000 Trigger Table (Phase B/C/D, no fired trigger)
The entire target architecture (all 45 documents) — see
`docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md`'s per-phase ADR-000
cross-references (added under ADR-019). Restated here for a single
consolidated view:
- Phase 1 (Foundational Domains) — no fired trigger.
- Phase 3 (Pharmacy/Laboratory/Radiology) — no evidenced real need yet.
- Phase 4 (Hospital Operations) — no hospital-tier client.
- Phase 5 full build-out (Billing/Insurance) — no measured RTDB
  join-complexity bottleneck.
- Phase 6 (Interoperability/Government adapters, any country) — no
  active external-integration requirement.
- Phase 7 (Analytics/AI) — no event history to analyze yet.

## Business-Decision-Gated (from this pass's gap closures)
- **GAP-004 remainder** — exact Grace Period duration, Suspended-to-
  Archived window, and Grace Period restriction scope. The state
  machine is designed; the numbers are not this document's to invent.
- **GAP-008 remainder** — the specific account-recovery verification
  channel/method. The requirement (step-up, never a bare email link) is
  fixed; the exact mechanism is a Phase 1+ implementation-detail choice.

## Legally-Gated (REQUIRES LEGAL VERIFICATION)
- **GAP-009 remainder** — exact clinical/financial/operational record
  retention period per data tier per jurisdiction. The mechanism
  (anonymization-not-erasure, legal-hold flag) is architecturally
  closed; the numbers require real legal review, tracked as new rows in
  `docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`.
- All 7 jurisdiction rows in `docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`
  — unchanged from every prior pass, still DISCOVERED/UNKNOWN.
- Terminology licensing (SNOMED CT, ICD, LOINC) — unchanged.
- PCI DSS 4.0.1 scope assessment — version is known (`docs/governance/TECHNOLOGY-BASELINE.md`),
  scope assessment is not performed.

## Performance/Evidence-Gated (REQUIRES MEASUREMENT)
- Every RPO/RTO figure in `docs/master/17-MASTER-DISASTER-RECOVERY.md`
  (including the three new scenario runbooks — the runbook *sequence*
  is designed, the *timing* within it is not measured).
- Every performance budget/SLO in
  `docs/master/18-MASTER-NON-FUNCTIONAL-REQUIREMENTS.md` and
  `docs/governance/PERFORMANCE-GOVERNANCE.md`.
- Whether the single-region architecture (`13`) is sufficient — Scenario
  2 in `17`'s new Named Scenario Runbooks names this as an accepted,
  explicit trade-off (Phase 8+ evidence-gated for multi-region), not an
  oversight.

## Operationally-Unproven
- Whether a break-glass path for Keycloak-outage scenarios (`17`
  Scenario 3, new this pass) has ever been drill-tested — it's
  architecturally required, never verified, since no implementation
  exists.
- Whether `origin/main` reflects this repository's local state —
  unchanged blocker from every prior pass, outside this agent's control
  (no push credentials).

## Explicitly NOT Deferred (closed this pass, not on this list)
For clarity, the 10 fully-CLOSED gaps from
`docs/audit/FINAL-GAP-REGISTER.md` (GAP-001, 002, 003, 005, 006, 007,
010, 011, 012, 013) do **not** belong on this list — their architecture
is complete, pending only the general "nothing is implemented yet"
status that applies to the entire repository equally.

## Dependencies
Synthesizes `docs/audit/FINAL-GAP-REGISTER.md`,
`docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md`,
`docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`,
`docs/governance/PERFORMANCE-GOVERNANCE.md`.

## Definition of Done
Every item above names its specific gating condition (a trigger, a
decision-owner, a legal review, a measurement) — none is a vague
"needs more work."
