# Performance Governance

**STATUS:** ACTIVE (governance policy)
**EVIDENCE CLASS:** DESIGN

## Purpose
Define the *process* by which ARGON's performance targets move from
aspiration to measured SLO, and how they're monitored afterward. The
actual target figures and the SLI list being measured live in
`docs/master/18-MASTER-NON-FUNCTIONAL-REQUIREMENTS.md` — this document
is deliberately not a second copy of that table.

## SLI (Service Level Indicator)
A measured signal (e.g., API p95 latency, queue latency, cache hit
rate). The full current SLI list is in `18`'s "Performance SLI
Framework" section.

## SLO (Service Level Objective)
A target value for an SLI, accepted as a commitment. **No SLO exists yet
in this repository** — `18` explicitly records its figures (99.95%
availability, p95 < 2s, etc.) as unmeasured, aspirational targets, not
accepted SLOs, per ADR-013. An aspirational target becomes an SLO only
after:
1. A real measured baseline exists (post-implementation, under
   representative load).
2. The business owner accepts the resulting number as a commitment, not
   just a design intention.
3. It is recorded with a date and owner in `18`'s target table, with its
   "unmeasured" caveat removed for that specific line only.

## Error Budget
Not defined yet — depends on an accepted SLO existing first (see above).
When SLOs are accepted, each one gets an explicit error budget (e.g.,
"99.95% monthly availability = ~21.9 minutes/month allowed downtime")
and a policy for what happens when the budget is exhausted (e.g., freeze
non-essential releases until burn rate recovers).

## Measurement Method
- Every SLI in `18` is measured via OpenTelemetry
  (`Observability` domain, `docs/master/03`), never estimated or
  inferred from anecdote.
- A metric with no working collection pipeline is not "measured" — it's
  still a target, and must keep its unmeasured label in `18`.

## Performance Budget
A performance budget (e.g., "checkout flow must not exceed N ms
end-to-end") is defined per critical user journey once that journey is
implemented and measurable. None exist yet; this is a Foundation
Implementation-phase deliverable, not fabricated here.

## Test Types and When Each Applies
| Test type | Purpose | When run |
|---|---|---|
| Load test | Confirm behavior at expected normal/peak traffic | Before any capacity claim is made |
| Stress test | Find the actual breaking point | Before any autoscaling-ceiling claim |
| Spike test | Confirm behavior under sudden traffic surges | Before any "handles flash demand" claim |
| Soak test | Find slow leaks/degradation over sustained duration | Before any long-running-reliability claim |
| Capacity test | Establish how many tenants/users a given deployment size supports | Before any "supports N clinics/users" claim |

**No numeric capacity claim (e.g., "supports X million users") is ever
made in this repository without a corresponding test run and dated
result recorded here or in `18`.** This is the same Zero-Fabrication
discipline `18`/ADR-013 already apply, restated as a standing rule.

## Promotion Path (Target → Measured → SLO)
```
Aspirational target (18, ADR-013)
   → Implementation exists
   → Load/stress/spike/soak test run, result recorded
   → Business owner reviews measured result
   → Accepted as SLO (18 updated, unmeasured label removed, owner + date added)
   → Error budget defined
   → Ongoing monitoring against the SLO (Observability domain, 03)
```

## Current State
Every performance figure in this repository is at the leftmost step of
the diagram above ("Aspirational target"). None have progressed further,
because no implementation exists to measure yet.
