# ARGON — Source of Truth Governance

**STATUS:** ACTIVE (governance document, not itself an architecture decision)
**EVIDENCE CLASS:** DESIGN

## Purpose
Define which document wins when two documents in this repository — or
this repository and any external document about the same project —
disagree, and define how a contradiction gets resolved rather than
silently ignored.

## 1. Document Authority Order
When two documents disagree, the higher item below governs, unless it
explicitly defers to a lower one:

1. **Executable evidence** — real running code, real test results, real
   deployment logs. (None exists for this repository today; see
   `docs/master/README` implementation-status note.)
2. **Approved ADR** — an ADR in `docs/master/19` or `docs/adr/` marked
   **Accepted**, not Proposed, by an actual decision authority.
3. **Verified Technology Baseline** — `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`,
   as long as its research date is current; a stale evidence date does
   not automatically lose authority, but should trigger a re-verification
   pass.
4. **Master Blueprint** — `docs/master/MASTER-ARGON-BLUEPRINT.md`, as a
   synthesis index; it introduces no decision not already made in `01`–`20`.
5. **Master Architecture documents** — `docs/master/01`–`20`.
6. **Detailed design docs** — anything more granular than a master
   document that expands on one master document's content without
   contradicting it.
7. **Supporting documents** — diagrams, appendices, worked examples.
8. **Historical documents** — anything explicitly marked HISTORICAL,
   SUPERSEDED, or MIGRATION NOTE. These are kept for provenance and
   **never** govern a current decision.

## 2. ADR Authority
- An ADR is **Proposed** by default. It becomes governing only when
  marked **Accepted** by whoever holds decision authority for the
  project — this document set does not self-approve its own entries
  (see `docs/master/19`, "Current Assumptions").
- A Proposed ADR still documents intent and should be followed unless a
  reason to deviate is recorded, but it is not evidence of sign-off.
- A changed decision gets a **new** ADR number that explicitly
  supersedes the old one. ADRs are never silently edited in place.

## 3. Technology Baseline Authority
`docs/governance/TECHNOLOGY-BASELINE.md` is the governance-level summary;
`docs/master/14-MASTER-TECHNOLOGY-STACK.md` is the architecture decision;
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` is the evidence
behind it. If these three ever disagree, the **evidence document wins**
for factual claims (e.g., "is Spring Boot 3.x EOL"), and the **master
document wins** for the actual ADOPT/CONDITIONAL/DEFERRED/REJECTED
decision (evidence informs decisions; it doesn't make them).

## 4. Implementation Evidence Authority
No implementation evidence exists in this repository. Once it does
(code, IaC, deployed environments, test runs), it becomes the **highest**
authority per §1 — a target architecture document can describe intent,
but a running system's actual observed behavior is what actually
happened. A conflict between a master document and real running code is
resolved by updating the master document (or filing a new ADR), never by
asserting the document is "still correct" over observed reality.

## 5. Historical Documents & Superseded Decisions
- Any statement no longer current must be marked **HISTORICAL**,
  **SUPERSEDED (date)**, or **MIGRATION NOTE** inline, at the point it
  appears — not just in a changelog elsewhere.
- A superseded statement is retained for provenance (why a decision
  changed matters), never deleted outright, unless it is a pure
  duplicate of content that still exists in the canonical location.

## 6. Change Control
- A change to a master document that alters a platform-wide decision
  requires a corresponding ADR entry (new or superseding).
- A change that is purely editorial (typo, link fix, formatting) does
  not require an ADR.
- Every master document's own "Dependencies" section states which
  earlier documents it depends on; a later document may cite, but must
  never silently contradict, an earlier one without a superseding ADR.

## 7. Who/What Can Override Architecture
- Only a named decision authority for the ARGON project can move an ADR
  from Proposed to Accepted, or authorize a phase transition (e.g.,
  Architecture Baseline Freeze → Foundation Implementation).
- No AI agent, and no document in this repository, self-authorizes that
  transition. `docs/master/20`'s own status line makes this explicit
  ("a recommended sequencing, not an authorization to begin").

## 8. How Contradictions Are Resolved
1. Identify the two conflicting statements and their document locations.
2. Apply the Document Authority Order (§1) to determine which currently
   governs.
3. If both are at the same authority level and genuinely conflict, do
   **not** silently pick one — record it as a finding in
   `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` with status
   **DECISION REQUIRED**.
4. Once resolved, update the losing statement to point to the winning
   one and mark it SUPERSEDED, or file a new ADR if the resolution
   itself constitutes a platform-wide decision.

## 9. The One Contradiction Already on Record
`docs/master/19` ADR-014 records, by design, an **unreconciled**
discrepancy between this document set's technology baseline and an
earlier architecture consultation for the same project. Per §8 above,
this is correctly left as **DECISION REQUIRED** rather than silently
resolved by this normalization pass — see
`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding AUDIT-001 and the
README's "Before implementation starts" section.
