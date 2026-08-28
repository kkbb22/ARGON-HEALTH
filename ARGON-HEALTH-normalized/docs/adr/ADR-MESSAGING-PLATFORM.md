# ADR — MESSAGING PLATFORM

STATUS: PROPOSED
EVIDENCE CLASS: EXTERNAL STANDARD (live-researched vendor/comparative sources, 2026-08-27)

## ADR ID
ADR-016 (consolidated log entry: `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`).
This file is the full-detail standalone record; the log entry is a
summary pointer to this file, not a duplicate source of truth.

## Title
Internal event backbone technology selection: Google Cloud Pub/Sub
(primary), RabbitMQ (conditional), Apache Kafka (rejected).

## Status
PROPOSED — not yet reviewed by a real decision authority.

## Date
2026-08-27

## Context
`docs/master/06-MASTER-INTEGRATION-MAP.md`'s original target named
RabbitMQ as the sole internal event backbone for the Transactional
Outbox pattern. During the 2026-08-27 Architecture Normalization pass,
this was flagged as a mandatory reconciliation item, requiring a
non-popularity-based, evidence-backed comparison against Google Cloud
Pub/Sub and Apache Kafka before the decision could be confirmed or
changed.

## Problem
Which messaging technology should back the platform's internal
asynchronous event backbone — the transport between the Transactional
Outbox relay and every domain's event consumers (audit, integration,
notification, analytics) — for a platform that is GCP-native,
single-team-operated at its current stage, and has not yet demonstrated
a measured throughput or replay requirement beyond ordinary clinical/
operational event volume?

## Options

### Option A — Google Cloud Pub/Sub
Fully managed, serverless pub/sub messaging service native to GCP.

### Option B — RabbitMQ
Mature, self-hostable (or third-party-managed) AMQP message broker with
strong exchange/queue routing semantics.

### Option C — Apache Kafka
Distributed log-based streaming platform, self-hosted or via Confluent
Cloud, built for high-throughput, long-retention, replay-capable event
streams.

## Evidence
Live web research performed 2026-08-27; full comparative detail in
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §5. Summary:

| Criterion | Pub/Sub | RabbitMQ | Kafka |
|---|---|---|---|
| Ordering | Best-effort by default; per-key ordering available | Strong (per-queue) | Strongest (per-partition) |
| Delivery guarantee | At-least-once; exactly-once achievable with Dataflow | At-least-once, mature DLQ/routing | At-least-once by default; native exactly-once semantics available |
| Operability (single team, GCP-native) | Fully managed, zero broker/partition ops | Requires self-hosting or a managed offering | Highest operational burden of the three |
| Scalability | Provider-managed autoscaling | Manual cluster configuration | Very high but requires capacity planning |
| Retention/Replay | 7-day default, up to 31 days | Not log-oriented | Built for long-window replay |
| Cost model | Pay-per-use, no idle cost | Infra + ops time | Infra/cluster cost or Confluent subscription |
| Cloud-native fit (platform is GCP-first) | Native | Neutral-to-negative | Neutral-to-negative without Confluent Cloud |
| Healthcare workflow fit at current scale | Good | Good | Overkill — no evidenced need |
| Developer burden | Low (topic/subscription model) | Moderate (AMQP concepts) | High (partition/consumer-group model) |

## Decision
- **Google Cloud Pub/Sub — PRIMARY.** Adopted as the internal domain
  event backbone.
- **RabbitMQ — CONDITIONAL.** Retained only for a specific external-facing
  Interoperability Layer adapter that genuinely requires AMQP (e.g., a
  legacy analyzer or PACS integration engine with no other transport
  option). Never the internal domain event backbone.
- **Apache Kafka — REJECTED for the current stage.** No evidenced
  requirement (event-sourcing-at-scale, multi-year replay, extreme
  throughput) justifies its operational complexity today.

## Rationale
Pub/Sub eliminates an entire category of operational burden — no broker
to provision, patch, or scale — for a platform that is already GCP-first
end to end (`docs/master/13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`) and
currently single-team-operated. This directly serves the "single-team
operability" criterion in the Technology Decision Framework
(`docs/master/14-MASTER-TECHNOLOGY-STACK.md`'s Managed Upgrade Policy
philosophy applied to a new-technology decision, not just a version
bump). The one real trade-off — Pub/Sub's best-effort default
ordering — is mitigated by using ordering keys scoped to the relevant
aggregate (e.g., per-patient, per-encounter) wherever the Transactional
Outbox needs order preserved, which is a documented, low-cost mitigation
rather than an unaddressed gap.

## Consequences
- `docs/master/06-MASTER-INTEGRATION-MAP.md`'s Internal Event Backbone
  section names Pub/Sub as primary, RabbitMQ as conditional.
- `docs/master/14-MASTER-TECHNOLOGY-STACK.md`'s Data table reflects the
  same three-way status (ADOPT / CONDITIONAL / REJECTED).
- **Domain code depends on a messaging abstraction, never a broker SDK
  directly** — this was already the architectural rule before this ADR
  (see `06`'s "domain layer must depend on an abstraction, not directly
  on a specific broker") and this decision does not relax it. The
  abstraction interface is owned by the `Platform` domain
  (`docs/master/03-MASTER-DOMAIN-MAP.md`).
- Any integration adapter that uses RabbitMQ under the CONDITIONAL clause
  is isolated behind the Interoperability Layer
  (`docs/master/06-MASTER-INTEGRATION-MAP.md`) and does not leak a
  RabbitMQ dependency into any domain's core logic.

## Security Impact
Pub/Sub inherits GCP IAM scoping natively — no separate broker-credential
surface to manage, unlike a self-hosted RabbitMQ instance, which would
need its own credential/access-control layer on top of GCP IAM.

## Operational Impact
Removes cluster/broker lifecycle management (provisioning, patching,
capacity planning, failover testing) from the platform-ops workload for
the primary event path entirely.

## Compliance Impact
None identified directly. Pub/Sub's regional topic placement should be
checked against per-country data-residency requirements during Phase 6
of the roadmap (`docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md`),
alongside the Government Country Adapter work
(`docs/master/06-MASTER-INTEGRATION-MAP.md`) — flagged as a follow-up,
not resolved by this ADR.

## Revisit Trigger
- A measured requirement for cross-partition, platform-wide strict
  ordering that ordering keys cannot satisfy.
- A real, evidenced event-sourcing/analytics use case needing replay
  windows longer than Pub/Sub's 31-day maximum retention.
- Confirmed evidence that GCP-native operational savings are not
  materializing as expected once real traffic exists.

## Rollback / Exit Strategy
Because domain code depends on the messaging abstraction rather than the
Pub/Sub SDK directly, changing the underlying transport (back to
RabbitMQ, or to Kafka if a future need is evidenced) is an
infrastructure-and-adapter-layer change, not a domain-code rewrite. No
data migration risk exists at the architecture-decision stage since no
implementation currently exists to migrate.

## Related
- `docs/master/06-MASTER-INTEGRATION-MAP.md` — Internal Event Backbone
- `docs/master/14-MASTER-TECHNOLOGY-STACK.md` — Data table
- `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §5 — full
  comparative evidence
- `docs/governance/TECHNOLOGY-BASELINE.md` — consolidated governance
  status board
