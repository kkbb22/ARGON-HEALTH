# 18 — MASTER NON-FUNCTIONAL REQUIREMENTS

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED. Every figure below is an aspirational
target, not a measured capacity claim.

## Purpose
Define the platform's non-functional targets — availability, performance,
scalability, reliability, extensibility, portability, observability,
accessibility, localization, compliance posture — as SLO/SLI definitions
to measure against once an implementation exists.

## Scope
Covers cross-cutting quality attributes. Component-specific detail
(exact RTO/RPO, exact accessibility standard, exact tech choices) is
defined in `17`, `12`, `14` respectively and referenced, not repeated.

## Current Assumptions
Numeric targets below reflect the aspiration already captured in the
project's own vision material; none are asserted as measured or achieved.
Per the originating prompt (section 29): performance budgets and SLOs may
be *defined* here; capacity claims are only *accepted* after measured
tests.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`). Target figures below are sourced
from the project's own architecture vision material, not from any
measurement.

## Decision

### Target NFR Summary

| Attribute | Target | Mechanism / owning document |
|---|---|---|
| Availability | 99.95%+ per tenant | Plane-independent degradation (`01`), managed HA (`13`), DR register (`17`) |
| Performance | API p95 < 2s (aspirational target, unmeasured) | Full p50/p95/p99 SLI framework below |
| Scalability | Horizontal | Cloud Run autoscaling (`13`) |
| Reliability | Auto-recovery | Managed HA failover, restore-tested backups (`13`, `17`) |
| Extensibility | Plugin/adapter pattern | Country Adapters, Payer Adapters (`06`); Specialty Extensions (`03`) |
| Portability | Cloud-native | Containerized services, IaC (`13`) |
| Observability | Full-stack | OpenTelemetry, `Observability` domain (`03`) |
| Accessibility | WCAG 2.2 AA | `12-MASTER-APPLICATION-ARCHITECTURE.md` |
| Localization | Multi-language, Arabic RTL first | `12` |
| Compliance | Multi-jurisdiction | Country Adapters (`06`), Compliance register (`08`) |

### Performance SLI Framework
For every service boundary defined in `06`'s API conventions, track:
- **p50 / p95 / p99** latency per endpoint.
- **Throughput** (requests/sec) per endpoint under normal and peak load.
- **DB latency** and **DB saturation** (connection pool utilization).
- **Cache hit rate** (Redis) — a falling hit rate is itself a signal, not
  just a performance detail.
- **Queue latency** (RabbitMQ) — time from publish to successful
  consumption.
- **Cold start** — Cloud Run cold-start latency distribution (`13`).
- **External integration latency** — per-adapter, since these are the
  least controllable tail-latency source (`06`).

None of the above have accepted numeric budgets yet — budgets are set
once a real baseline exists to measure against, per `15-MASTER-TESTING-STRATEGY.md`'s
Performance/Load/Stress/Soak layer.

## Alternatives Considered
- **Skipping numeric targets entirely until measured** (rejected as a
  total approach) — the project's own vision material already states
  aspirational figures; recording them as explicitly-labeled *targets*
  (not measurements) is more useful than omitting them, provided the
  distinction is never blurred.
- **Treating the vision material's figures as already-achieved
  benchmarks** (rejected) — would violate Zero Fabrication; every figure
  above is marked aspirational/unmeasured.

## Security Impact
Availability targets interact with `07`'s failure-closed authorization
rule — a system tuned purely for uptime must not achieve it by failing
open on auth checks during a partial outage.

## Operational Impact
The SLI framework above is the direct input to on-call alerting
thresholds, owned operationally by the `Observability` domain (`03`).

## Performance Impact
This document *is* the performance-impact ledger for the rest of the
platform.

## Compliance Impact
Multi-jurisdiction compliance posture here is a target statement, not a
claim — actual status per jurisdiction lives exclusively in `08`.

## Failure Modes
A dashboard presenting an aspirational target as a current measurement is
itself a defect (parallel to `16`'s Evidence-status discipline) —
targets and measurements must be visually and structurally distinct.

## Dependencies
Depends on `01`, `06`, `07`, `08`, `12`, `13`, `17`. Feeds `15` (test
thresholds once budgets are set), `20` (roadmap — measurement
infrastructure is itself a roadmap item).

## Unknowns
UNKNOWN — REQUIRES MEASUREMENT for every numeric figure in this document
before any capacity claim can be accepted, per section 29 of the
originating prompt.

## Validation
Every attribute in the Target NFR Summary traces to a named mechanism in
an existing master document — none are freestanding claims. Confirmed at
time of writing.

## Rollback
N/A — targets document, not a deployed change.

## Definition of Done
Every target above has, at minimum, an identified owning mechanism; full
Definition of Done for this document is reached only once each target has
a measured baseline to compare against (tracked as roadmap work in `20`).
