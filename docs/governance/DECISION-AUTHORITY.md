# DECISION AUTHORITY

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

> New document, added during repository consolidation (2026-09-05). No
> prior version of this file existed in either source repository —
> both `docs/governance/ARCHITECTURE-STATUS.md` and
> `docs/governance/ARCHITECTURE-FREEZE.md` note "who holds real
> change-approval authority" as an open UNKNOWN across every prior pass.
> This document does not resolve that UNKNOWN; it makes the rule around
> it explicit so the UNKNOWN cannot be quietly treated as resolved.

## Purpose
State, in one place, who is authorized to approve an ADR, accept the
architecture baseline, or declare a phase of
`docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md` open for
implementation — and, just as importantly, who and what is **not**
authorized to do those things.

## Who Holds Decision Authority
The **repository owner** — the person who owns and operates the live
ARGON production system referenced throughout this document set as
"LEGACY ARGON" — is the sole decision authority for this project today.
There is no second engineer, no architecture board, and no
organizational approval chain. This is stated plainly rather than
implied, because every other governance document in this repository
(`ARGON-SOURCE-OF-TRUTH.md`, `ARCHITECTURE-STATUS.md`,
`ARCHITECTURE-FREEZE.md`) assumes a decision authority exists without
naming who it is.

## What Decision Authority Actually Approves
1. Moving an ADR's status from PROPOSED to APPROVED (or APPROVED WITH
   CONDITIONS) in `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` or
   a standalone `docs/adr/` file.
2. Confirming that a row in ADR-000's Staged Trigger Table
   (`argon-platform-target-architecture` skill) has actually fired —
   this is a real-world business/client-signal judgment, not a
   documentation judgment, and cannot be made by inspecting this
   repository alone.
3. Accepting this consolidated baseline as reviewed (closing the open
   item in `docs/governance/ARCHITECTURE-STATUS.md`).
4. Authorizing a documented exception to the freeze in
   `docs/governance/ARCHITECTURE-FREEZE.md` (see ADR-020 for the one
   precedent on record).

## What No AI Agent May Do
Restating `argon-governance`'s core rule for this specific context: **no
AI agent — including the one that authored this consolidation — may
mark an ADR APPROVED, declare a trigger fired, or declare the baseline
"reviewed and accepted."** An agent may draft, propose, analyze, compare
evidence, and flag conflicts. It may not self-approve its own output or
imply approval by omission (e.g., by quietly changing a status field).
Every STATUS field in this repository reading PROPOSED is a direct,
literal consequence of this rule, not a stylistic default.

## Escalation Path
There is no multi-party escalation path today because there is only one
decision-maker. If a second engineer or a formal organization forms
around this project, this document is the first one that needs a
substantive rewrite — not a footnote update — since "sole owner decides"
stops being an accurate description of reality at that point.

## Dependencies
Read alongside `docs/governance/ARGON-SOURCE-OF-TRUTH.md` (precedence
order — Approved ADR is Level 2 *only* once this document's authority
has actually approved it) and `docs/governance/ARCHITECTURE-FREEZE.md`
(the change process this authority executes).

## Unknowns
UNKNOWN whether the repository owner has, in fact, reviewed and accepted
any ADR in this log — no such review is recorded anywhere in either
source repository as of this consolidation.

## Definition of Done
This document is done when it accurately describes who decides — it is
explicitly not done when it invents a governance body that does not
exist to make the repository look more "enterprise" than it is.
