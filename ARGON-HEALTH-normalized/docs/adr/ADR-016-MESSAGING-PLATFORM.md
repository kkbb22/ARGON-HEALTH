# ADR-016 — Internal Event Backbone: Google Cloud Pub/Sub (primary), RabbitMQ (conditional), Kafka (rejected)

**STATUS:** PROPOSED — not yet independently reviewed/accepted
**EVIDENCE CLASS:** DESIGN (decision), backed by EXTERNAL RESEARCH (see Evidence link below)

> Promoted out of `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` during the
> repository normalization pass so this decision has one full, standalone,
> linkable record per section 10 of the normalization contract. `19` now
> carries only the short index entry; this file is the canonical full text.

**ADR-016 — Internal event backbone: Google Cloud Pub/Sub (primary),
RabbitMQ (conditional), Kafka (rejected)**
- Status: **PROPOSED** (not Approved — requires sign-off per ADR-009's
  discipline applied to itself)
- Date: 2026-08-27
- Context: `06`'s original target named RabbitMQ as the sole internal
  event backbone. The Architecture Normalization task required a fresh,
  non-popularity-based comparison against Google Cloud Pub/Sub and Apache
  Kafka.
- Problem: Which messaging technology should back the Transactional
  Outbox pattern for a single-team-operated, GCP-native platform at its
  current stage?
- Options: RabbitMQ (self/managed), Google Cloud Pub/Sub (managed),
  Apache Kafka (self-managed or Confluent).
- Evidence: `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §5 (live
  research, 2026-08-27).
- Decision: Pub/Sub primary; RabbitMQ conditional (AMQP-only external
  adapters only); Kafka rejected for the current stage.
- Rationale: Pub/Sub eliminates broker/partition operational burden
  entirely on a platform that is already GCP-first end to end (`13`);
  no evidenced requirement justifies Kafka's added operational
  complexity; RabbitMQ remains available where a specific external
  system requires AMQP.
- Consequences: `06`'s Internal Event Backbone section and `14`'s Data
  table are both updated; the domain layer depends on a messaging
  abstraction, not a broker SDK, keeping this reversible.
- Security Impact: Pub/Sub inherits GCP IAM scoping natively; no new
  broker-credential surface to manage versus a self-hosted RabbitMQ.
- Operational Impact: Removes cluster/broker management from the
  platform-ops workload entirely for the primary path.
- Compliance Impact: None identified; data-residency implications of
  Pub/Sub (regional topic placement) should be checked per country
  during Phase 6 (`20`) alongside the Government Country Adapter work.
- Revisit Trigger: A measured requirement for cross-partition ordering
  at platform scale, or a real long-window event-replay/event-sourcing
  need beyond Pub/Sub's 31-day maximum retention.
- Rollback/Exit Strategy: Because domain code depends on the messaging
  abstraction rather than the Pub/Sub SDK, swapping the underlying
  transport (including back to RabbitMQ or to Kafka) is an
  infrastructure-and-adapter change, not a domain-code rewrite.

