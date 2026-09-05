# ARCHITECTURE FREEZE

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Purpose
Formally freeze the ARGON v2/v3 target architecture as of this pass. A
frozen baseline is not immutable — it is protected from casual,
undocumented change. This document defines the only path by which the
frozen baseline may change going forward.

## What Is Frozen
Everything under `docs/master/`, `docs/MASTER-ARGON-BLUEPRINT.md`,
`docs/governance/`, `docs/adr/`, `docs/compliance/`,
`docs/interoperability/`, as of local commit `dd994c3` and the
documents added in this closing pass
(`docs/governance/ARCHITECTURE-FREEZE.md`,
`docs/audit/FINAL-ARCHITECTURE-COMPLETENESS.md`). This is a
**documentation and governance freeze**, not a code freeze — no code
exists yet to freeze.

## What Freezing Means
- No document above is edited for style, preference, or "improvement"
  without following the Change Process below.
- The 19 ADRs in `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` plus
  the 2 standalone ADRs in `docs/adr/` represent the complete, current
  decision set. All remain **PROPOSED** — freezing the baseline does
  **not** approve any ADR; approval is a separate, human decision.
- **ADR-019's authority is unaffected and unweakened by this freeze**:
  every phase of `docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md`
  remains gated by ADR-000's Staged Trigger Table. Freezing the
  documentation does not change what's authorized to be built — nothing
  is authorized to be built.

## Change Process (the only way to modify a frozen document)
1. **Problem** — state what's actually wrong or missing, with a specific
   document/section reference.
2. **Evidence** — cite the source (live research, a real audit finding,
   a fired ADR-000 trigger, measured data). Preference alone is not
   evidence.
3. **Impact** — which documents, domains, or workflows does this touch?
4. **Alternatives** — what else was considered, per the Technology
   Decision Framework already established in `docs/master/14`.
5. **ADR** — a new numbered ADR recording the decision (`docs/master/19`
   or a new standalone file in `docs/adr/`), never a silent edit.
6. **Approval** — a real decision authority reviews the ADR. This
   document set has never had one; that gap remains open (see
   `docs/governance/ARCHITECTURE-STATUS.md`).
7. **Document updates** — the affected documents are updated to match
   the approved ADR, including every cross-reference (this session found
   repeatedly that a correction applied to one document but not its
   cross-references is the single most common failure mode — see
   `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding AUD-004 and
   `docs/audit/CONTINUOUS-IMPROVEMENT-FINAL-REPORT.md`).
8. **Consistency scan** — re-run the lint checks in
   `docs/governance/ARCHITECTURE-LINT-RULES.md` before considering the
   change complete.

## What Does NOT Require This Process
- Fixing a genuinely broken link, a wrong file path, or a factual
  transcription error (like the domain-count correction in this
  session) — these are bug fixes, not architecture changes, and should
  be fixed on sight with a clear commit message, the same way this
  session handled them.
- Adding evidence to an existing UNKNOWN/TBD field (e.g., a real
  measured RPO number once business sign-off happens) — this fills a
  gap the document already anticipated, it doesn't change a decision.

## Why This Freeze Exists Now
This session ran five successive "final" passes (Master Foundation,
Architecture Normalization, Reconciliation, Continuous Improvement,
this Hardening pass), each finding genuine issues the previous one
missed. That pattern is useful for catching real errors but is not
sustainable as an open-ended process — the Stop Condition in the
originating task for this pass (and confirmed independently in this
document) exists specifically to end that cycle once the real,
findable issues are exhausted rather than continuing indefinitely on
diminishing returns.

## Un-Freeze Trigger
This freeze is automatically superseded — not violated — by any of the
following, each of which is itself a legitimate reason to reopen a
specific document, not the whole baseline:
- A row in **ADR-000's Staged Trigger Table** fires, moving a phase from
  "documented" toward "authorized to implement" — the affected phase's
  documents may then need implementation-level detail this pass didn't
  produce.
- A future technology-verification pass finds that a "current" choice
  (Java 25, Spring Boot 4.1, PostgreSQL 18, Pub/Sub, OpenTofu, FHIR
  R4/R4B) has been superseded — per each ADR's own stated Revisit
  Trigger.
- A real decision authority reviews the ADR log and either approves
  entries or sends specific ones back with required changes.

## Alternatives Considered
- **No formal freeze, treat the baseline as always-editable** — rejected:
  this is exactly what allowed five successive passes to each still find
  real problems; a freeze with an explicit change process is what makes
  the *next* change traceable instead of another undocumented drift.
- **A hard, no-exceptions freeze (bug fixes also require the full
  process)** — rejected as impractical; distinguishing bug fixes from
  architecture changes (as this document does) is what the entire
  Verification phase of this session actually did in practice.

## Dependencies
Governs all of `docs/master/`, `docs/adr/`, `docs/governance/`,
`docs/compliance/`, `docs/interoperability/`. Referenced by
`docs/governance/ARGON-SOURCE-OF-TRUTH.md` as the process that produces
new precedence-level-3 (Master Architecture) content.

## Unknowns
UNKNOWN who holds real change-approval authority — same open item as
every prior report in this session.

## Definition of Done
This document is in force from the moment it's committed. Any edit to a
frozen document from this point forward should be checkable against the
Change Process above — either it's a bug fix (fixed on sight, logged in
a commit message) or it has a Problem/Evidence/Impact/Alternatives/ADR
trail. No third category.
