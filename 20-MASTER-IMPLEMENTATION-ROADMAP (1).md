# 20 — MASTER IMPLEMENTATION ROADMAP

## Status
TARGET ARCHITECTURE / PROPOSED. This is a recommended sequencing, not an
authorization to begin. Per the originating prompt (section 41/46): this
foundation pass stops here — no Phase 1 implementation work starts as a
consequence of this document existing.

## Purpose
Sequence the target architecture (`01`–`19`) into stages, each gated by a
concrete trigger condition rather than a calendar date, so scope is
pulled by real evidence of need rather than pushed by a fixed schedule.

## Scope
Covers phase sequencing and each phase's entry/exit criteria. It does not
estimate durations or costs — those require inputs (team size,
measured velocity) this document does not have. UNKNOWN — REQUIRES
project-specific inputs before any timeline can be stated.

## Current Assumptions
Later phases are legitimately optional if their trigger never fires — a
hospital-tier module (Phase 4 below) has no reason to exist before a real
hospital-tier customer does.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Phase Sequence

**Phase 0 — Architecture Foundation** *(this document set)*
- Exit criteria: `01`–`20` exist and are internally consistent
  (cross-checked throughout this set).
- Status at time of writing: COMPLETE for this pass.
- Explicitly does not include: any code, any infrastructure, any
  database, any migrated data (section 41 of the originating prompt).

**Phase 1 — Foundational Domains**
- Scope: `Platform`, `Identity`, `Organization`, `Membership`,
  `Authorization` domains (`03`) — the domains every other domain depends
  on.
- Trigger to start: an explicit decision by whoever holds authority over
  this project to proceed past Phase 0, with the ADR log (`19`) reviewed
  and any Proposed→Accepted transitions recorded.
- Exit criteria: a working Identity/Authorization/Organization
  substrate, with the three-layer authorization model (`07`) demonstrably
  enforced (ALLOW+DENY tests passing, `15`).

**Phase 2 — Patient & Clinical Core**
- Scope: `Patient`, `MPI`, `Consent`, `Clinical`, `Specialties`,
  `Scheduling`, `Queue` domains.
- Trigger to start: Phase 1 exit criteria met.
- Exit criteria: a full Outpatient Encounter workflow (`05` §3)
  executable end-to-end against real (non-production) data, with Clinical
  Safety hazards relevant to this scope (`16`: Wrong Patient, Wrong
  Result, Duplicate Orders) verified per `15`.

**Phase 3 — Ancillary Clinical (Pharmacy, Laboratory, Radiology)**
- Trigger to start: Phase 2 exit criteria met **and** a real need for at
  least one of these three exists (not built speculatively ahead of
  demand).
- Exit criteria: each entitled module's core workflow (`05` §6–8)
  executable end-to-end; relevant `16` hazards (Wrong Medication, Wrong
  Dose, Wrong Result) verified.

**Phase 4 — Hospital Operations**
- Trigger to start: a real hospital-tier customer/requirement exists —
  this phase is not started speculatively (mirrors ADR-002/003's
  evidence-driven philosophy applied to business scope, not just infra).
- Exit criteria: Admission→Inpatient workflow (`05` §5) executable
  end-to-end, race-safe bed allocation verified under load (`15`), Wrong
  Procedure/Wrong Patient hazards for inpatient/surgical context verified
  (`16`).

**Phase 5 — Billing, Insurance, Revenue Cycle**
- Trigger to start: Phase 2 (at minimum) exit criteria met — billing can
  begin as soon as chargeable clinical events exist, does not require
  Phase 3/4.
- Exit criteria: `05` §9–10 executable end-to-end against at least one
  real payer adapter (`06`); financial-record immutability verified
  (`15`).

**Phase 6 — Interoperability & Government Adapters**
- Trigger to start: a specific country/integration requirement is active
  — adapters are built per real target, not all eight+ countries listed
  in `06` speculatively.
- Exit criteria: the specific adapter's conformance tests pass (`15`);
  legal verification for that jurisdiction obtained (updates `08`).

**Phase 7 — Analytics & AI**
- Trigger to start: enough event history exists across prior phases to
  make analytics/CDS meaningful — not built ahead of data.
- Exit criteria: dashboards regenerable from the event log alone (`03`
  Analytics domain DoD); any AI/CDS feature's human-confirmation
  guardrail verified (`16`-adjacent, `AI` domain in `03`).

**Phase 8 — Production Hardening & Compliance Evidencing**
- Trigger to start: ongoing, in parallel with every phase above — this
  is not a final phase so much as a continuous exit gate: no phase's
  output is called "production ready" (originating prompt, section 41)
  until its relevant `08` compliance rows and `16` hazard rows reach
  EVIDENCED, and its `17` DR drills have passed.

### Sequencing Diagram
```
Phase 0 (Foundation, this pass)
   │
   ▼
Phase 1 (Foundational Domains)
   │
   ▼
Phase 2 (Patient & Clinical Core)
   │
   ├──────────────┬──────────────┐
   ▼              ▼              ▼
Phase 3        Phase 4        Phase 5
(Ancillary,    (Hospital,     (Billing/
 if triggered)  if triggered)  Insurance)
   │              │              │
   └──────────────┴──────────────┘
                  │
                  ▼
         Phase 6 (Interop/Gov,
            per-country trigger)
                  │
                  ▼
         Phase 7 (Analytics/AI)

Phase 8 (Hardening & Evidencing) — continuous, alongside every phase
```

## Alternatives Considered
- **Fixed calendar-date roadmap** (rejected) — would require inventing
  velocity/team-size assumptions this document has no basis for; a
  trigger-based roadmap is honest about what's actually known.
- **Big-bang single-phase implementation** (rejected) — directly
  contradicts the evidence-driven, staged philosophy already established
  in ADR-002/ADR-003 and the Phase-4/6/7 trigger conditions above.

## Security Impact
Phase 1 deliberately front-loads Authorization/Identity — no later phase
builds clinical functionality on top of an unverified authorization
substrate.

## Operational Impact
Phase 8's "continuous, alongside every phase" framing means DR drills and
compliance evidencing are never deferred to "later" — they're a
per-phase exit condition.

## Performance Impact
No timeline estimates given — see Scope. Performance budgets (`18`) get
real numbers once a phase produces something measurable.

## Compliance Impact
Phase 6's per-country trigger directly reflects `08`'s REQUIRES LEGAL
REVIEW default status — no country adapter ships ahead of that review.

## Failure Modes
Starting any phase without its stated trigger condition met is exactly
the "chase the vision without evidence" pattern this roadmap is designed
to prevent — a phase started early is a process failure to flag, not a
sign of progress.

## Dependencies
Synthesizes `01` through `19` into a sequence. Nothing in this document
introduces a new architectural decision — ADRs live only in `19`.

## Unknowns
UNKNOWN — REQUIRES project-specific input (team size, available hours,
existing codebase state) before any phase can be given a realistic
duration estimate.

## Validation
Every phase's scope maps to specific domains/workflows already fully
specified in `03`/`05` — no phase invents new scope not already covered
in `01`–`19`. Confirmed at time of writing.

## Rollback
N/A — this is a sequencing recommendation, not a deployed change.

## Definition of Done
This document is complete when every domain in `03` and every workflow in
`05` is assigned to exactly one phase above, with no domain left
unsequenced. Confirmed: all 39 domains and 30 workflows map into Phases
1–7 (Phase 0 and 8 are foundation/continuous, not domain-scoped).

---

**STATUS: TARGET ARCHITECTURE COMPLETE.**
Not PRODUCTION READY. Business implementation has not started. Phase 1
has not started. This roadmap is a recommendation for what comes next,
pending a real decision to proceed.
