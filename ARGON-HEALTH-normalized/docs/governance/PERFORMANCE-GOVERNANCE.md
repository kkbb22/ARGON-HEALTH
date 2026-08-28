# PERFORMANCE GOVERNANCE

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Purpose
Define the *process* by which ARGON sets, measures, and enforces
performance targets — separate from
`docs/master/18-MASTER-NON-FUNCTIONAL-REQUIREMENTS.md`, which states the
current aspirational *targets themselves*. This document is the policy;
`18` is the current target snapshot governed by this policy.

## Scope
Covers SLI/SLO definition, performance-budget enforcement, and the test
types that validate them. Does not restate `18`'s target table.

## Policy

### SLI (Service Level Indicator) — what gets measured
Per service boundary (`docs/master/06-MASTER-INTEGRATION-MAP.md`'s API
conventions):
- Request latency distribution (p50/p95/p99)
- Throughput (requests/sec)
- Error rate
- Database latency and saturation
- Cache hit rate
- Queue/messaging latency (publish-to-consume)
- Cold-start latency (Cloud Run)
- External-integration latency (per adapter)

### SLO (Service Level Objective) — the target for each SLI
**No SLO in this repository is asserted as final.** Every numeric figure
in `18-MASTER-NON-FUNCTIONAL-REQUIREMENTS.md` is explicitly labeled an
aspirational target sourced from the project's own vision material, not
a measured or committed figure. This document's policy is: an SLO
becomes "accepted" only after a **measured baseline** exists to compare
it against — never before. Inventing a specific number here beyond what
`18` already records would violate Zero Fabrication.

### Performance Budget
A performance budget is a per-change ceiling (e.g., "this endpoint's p95
must not regress by more than X%") — the exact ceiling values are
**UNKNOWN — REQUIRES a measured baseline first**, per the same
Zero-Fabrication constraint. The *mechanism* is defined now:
1. Contract/performance tests (`docs/master/15-MASTER-TESTING-STRATEGY.md`
   Performance/Load/Stress/Soak layer) run against every release
   candidate.
2. A regression beyond the (future, measured) budget blocks promotion
   past canary in the Release workflow (`docs/master/05` §12).
3. Budgets are revisited every time a major dependency changes (see
   `docs/governance/VERSION-MANAGEMENT-POLICY.md`).

### Measurement Method
- **Load tests** — sustained expected traffic, verifying SLIs hold at
  target.
- **Stress tests** — traffic beyond expected peak, to find the actual
  breaking point (not to prove a specific capacity number in advance).
- **Spike tests** — sudden traffic surges, verifying autoscaling
  (Cloud Run, `docs/master/13`) responds correctly.
- **Soak tests** — sustained load over an extended duration, to catch
  memory leaks, connection-pool exhaustion, and slow degradation that
  short tests miss.
- **Capacity testing** — determines the actual maximum sustainable load
  for the current infrastructure configuration; **this is the only
  source from which a "supports N concurrent users/clinics" claim may
  ever be made** — never asserted without this evidence.

### The "Never Invent Numbers" Rule
No document, pitch deck, CV, or portfolio description originating from
this repository may state a specific capacity, latency, or throughput
number ("supports 10,000 concurrent users," "sub-100ms response times")
unless that number traces to an actual Capacity Testing result recorded
here. Aspirational targets (as in `18`) must always be labeled as
targets, never presented as achieved capacity.

## Alternatives Considered
- **Setting placeholder SLO numbers now "to look complete"** (rejected) —
  the exact failure mode `docs/master/17`'s RPO/RTO handling and `18`'s
  NFR framing already reject; a policy document exists to prevent
  exactly this shortcut, not to take it.

## Security Impact
Performance testing under load can itself be a source of accidental
denial-of-service against shared test infrastructure — load/stress/spike
tests must run in isolated environments per
`docs/master/13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`'s Environments
section, never against production.

## Operational Impact
Capacity test results, once they exist, directly inform Cloud Run
autoscaling configuration and Cloud SQL sizing
(`docs/master/13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`).

## Compliance Impact
None directly identified.

## Failure Modes
A performance regression shipped without a budget check in place (before
one is defined) is expected and acceptable at this stage — the policy
gap is explicit, not hidden, until real budgets exist.

## Dependencies
Depends on `docs/master/15` (test types), `docs/master/18` (current
targets), `docs/master/05` §12 (Release workflow gating). Feeds
`docs/governance/ARCHITECTURE-STATUS.md`.

## Unknowns
UNKNOWN — every specific numeric budget, pending a real measured
baseline. UNKNOWN — what infrastructure/tooling will run these tests,
since none exists yet.

## Definition of Done
This document is complete as a *policy*; it will not be considered fully
"in force" until at least one full measurement cycle (load + stress +
soak + capacity) has actually been run and its results recorded in a
future `docs/evidence/` document.
