# ARCHITECTURE CHANGE RULES

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

> New filename, added during repository consolidation (2026-09-05) to
> satisfy the canonical governance-document set named in the
> consolidation task. The substantive Change Process this file names
> already exists, in full, in
> `docs/governance/ARCHITECTURE-FREEZE.md` — that document is not
> duplicated here per the "no unnecessary duplicates" rule; this file is
> a short index pointing to it, plus the two rules that don't fit neatly
> under "freeze."

## The Actual Change Process
Defined in full in `docs/governance/ARCHITECTURE-FREEZE.md` → **Change
Process** section: Problem → Evidence → Impact → Alternatives → ADR →
Approval → Document updates → Consistency scan. That section is the
canonical text; this file does not restate it a second time.

## Two Rules Not Covered by the Freeze Document

### Rule 1 — Bug fixes are not architecture changes
Correcting a factual transcription error (a miscounted domain total, a
broken internal link, a stale cross-reference left after a real
correction) does not require the 8-step Change Process. It requires a
clear commit message stating what was wrong and what evidence showed
it. `ARCHITECTURE-FREEZE.md` → "What Does NOT Require This Process"
already states this; repeated here only because it is the single most
common category of change this repository has actually seen (11 files /
15 locations in the 39→40 domain-count correction alone).

### Rule 2 — A consolidation pass is not exempt from the process
Merging two repositories, renaming files, or reorganizing structure — as
this consolidation itself does — still follows the Change Process for
any *content* decision made along the way (e.g., which of two
conflicting technology claims wins). Purely mechanical actions (moving a
file, fixing a cross-reference to match) are Rule 1 bug fixes. Every
content decision made during this consolidation is logged in
`docs/audit/CONSOLIDATION-DECISIONS.md`, which functions as this pass's
ADR-equivalent trail — it is not a substitute for a numbered ADR where
one is actually warranted (see `docs/audit/REPOSITORY-CONSOLIDATION-MATRIX.md`
for the one case in this pass, domain-count correction aside, that
plausibly warrants one: none were found — see that document's
Conflicts section).

## Dependencies
`docs/governance/ARCHITECTURE-FREEZE.md` (the process itself),
`docs/governance/DECISION-AUTHORITY.md` (who executes Approval),
`docs/audit/CONSOLIDATION-DECISIONS.md` (this pass's change log).

## Definition of Done
A future contributor asking "how do I change something in this
repository" reaches an answer in two hops (this file → Freeze
document) without re-deriving the process from scratch.
