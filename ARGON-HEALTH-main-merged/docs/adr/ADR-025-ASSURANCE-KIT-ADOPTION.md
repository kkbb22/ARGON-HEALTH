# ADR-025 — ASSURANCE & VERIFICATION KIT ADOPTION

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN (process/tooling proposal; no product assurance implied)

## ADR ID
ADR-025. Standalone record, per `docs/governance/ARCHITECTURE-FREEZE.md` Change Process step 5. A summary pointer in `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` and a row in `docs/governance/ARCHITECTURE-STATUS.md` are to be added only after the decision authority reviews this ADR; neither frozen document was edited by this change.

## Title
Adopt `docs/assurance/` (Assurance & Verification Kit v1.0) as a subordinate evidence-and-gate layer.

## Status
PROPOSED — not yet reviewed by the decision authority (`docs/governance/DECISION-AUTHORITY.md`). No AI agent may approve it.

## Date
2026-10-10

## Context
The repository has design/governance documents and no implementation. It has three status models (`ARCHITECTURE-STATUS.md`, compliance lifecycle in `08`, hazard evidence in `16`) but no register tying a requirement to a test, an evidence artifact, a reviewer and a release gate. The kit supplies that: 67 controls (all NOT_RUN), 7 risk hypotheses, empty evidence/sign-off/revalidation registers, a standard-library Python checker with tests, and fail-closed gates G0–G5.

## Problem
Without an evidence register, "documented" can drift into "verified" by omission — the failure mode `ARGON-SOURCE-OF-TRUTH.md` already guards against.

## Decision requested
1. Adopt `docs/assurance/` as a layer **subordinate** to `ARGON-SOURCE-OF-TRUTH.md` and approved ADRs. It adds no domain, workflow, or product technology; ACR-1..5 and the 40-domain/30-workflow baseline are untouched.
2. Approve the tooling: `scripts/argon_assurance_lint.py` (Python standard library only) and `tests/test_argon_assurance_lint.py`. GitHub Actions is already ADOPT in `docs/master/14`; Python is not listed there and needs this approval.
3. Keep the workflows, PR/issue templates and SECURITY.md **disabled** in `docs/assurance/phase-2-ci/` until Phase P2.

## Findings against this repository (from inspection)
- **Sole decision authority.** `DECISION-AUTHORITY.md`: the repository owner is the only decision-maker; no second engineer or board. The kit's separation-of-duties (Plan §3) cannot be met as written. The authority must record role combinations and compensating checks (Plan §3 allows this) — at minimum: no AI approval of any status; external qualified review for CRITICAL security/clinical/privacy controls before Gate G3. The kit does not name anyone and none is invented here.
- **Tier inflation.** 28 CRITICAL + 35 HIGH of 67 controls (94%). Recalibrate to Plan §6 definitions in P1.
- **Overlapping status vocabularies.** Kit statuses/evidence states are a fourth vocabulary. Proposed mapping to be confirmed by the authority: evidence `ACCEPTED` ≈ EVIDENCED; verification `PASS` with `REVIEWED` evidence ≈ VERIFIED. UNKNOWN until approved.
- **Gate names.** No `G-n`-style gate identifiers were found in this repository snapshot; kit gates G0–G5 do not collide with anything present. Any such gates defined elsewhere: UNKNOWN — REQUIRES EVIDENCE.
- **Derived workbook.** The xlsx is a derived view; the CSVs are the single source.
- **Pre-existing, out of scope here:** `ARCHITECTURE-STATUS.md` lists ADR-020..023 but not ADR-024 (found in `19`).

## Alternatives Considered
- Do nothing — keeps the traceability gap above.
- Fold controls into `TRACEABILITY-MATRIX.md` / `COMPLIANCE-TRACEABILITY-MATRIX.md` — avoids a parallel register but those cover design traceability, not evidence/gates; may be the right long-run merge (decide in P1).

## Phases
- **P0 (this change):** files added, CI not enabled.
- **P1:** map each control to its authoritative doc/ADR (VFY-GOV-001); merge or drop duplicates; recalibrate tiers; record role combinations; link ADR-024 (PROPOSED) to the object-storage retrieval control as a G1 blocker.
- **P2:** enable `phase-2-ci/` workflows informationally after reviewing permissions and branch protection.
- **P3:** first real evidence (tenant isolation, authorization, ADR-024).
- **P4:** enforce gates.

## Consequences
Omissions become visible; G1/G4 fail by design until real evidence exists (verified: G1 = 26 errors, G4 = 69 errors on the starter state). A green structural check proves record integrity only — not that ARGON is implemented, secure, clinically safe, or compliant.

## Revisit Trigger
A second engineer or organization forms (then `DECISION-AUTHORITY.md` and Plan §3 need substantive rewrite); first implementation begins; or the authority rejects the layer.

## Unknowns
Whether the authority accepts the status-vocabulary mapping; who external reviewers would be; whether a Python dependency is acceptable.

## Definition of Done
Authority has approved or rejected this ADR in a governed record, and `ARCHITECTURE-STATUS.md` / `19` reflect that outcome.
