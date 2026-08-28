# TECHNOLOGY BASELINE VERIFICATION

STATUS: PROPOSED
EVIDENCE CLASS: EXTERNAL STANDARD (live-researched vendor/standards sources, 2026-08-27)

## Status
EVIDENCE RECORD. This document supersedes any prior technology claim made
without a fresh verification pass. Research performed 2026-08-27 via live
web search against official/authoritative sources per the priority
hierarchy in the governance task (official standards body → official
vendor docs → official release/security advisories → industry evidence →
trusted third-party analysis).

## Purpose
Apply the Technology Decision Framework (Requirement → Candidates →
Evidence → Security → Reliability → Performance → Scalability →
Operability → Cost → Lock-in → Healthcare fit → Migration impact →
Decision → Revisit trigger) to every contested or version-sensitive
technology named in `docs/master/14-MASTER-TECHNOLOGY-STACK.md`, instead
of carrying forward prior conversation decisions unverified.

## Method
Live web search, dated 2026-08-27. Each finding below cites what was
found; where search did not cover a candidate in depth, that gap is
marked rather than filled with assumption.

---

## 1. Runtime — Java

**Candidates:** Java 21 LTS, Java 25 LTS.
**Evidence:** Java 25 LTS shipped September 2025 (current latest LTS,
patch 25.0.3 as of April 2026); Java 21 LTS remains supported through
September 2028 (Premier) / 2031 (Extended). Multiple industry sources
report Java 21 as the more common *current production* target because of
two-plus years of field maturity, while Java 25 is recommended for new
projects wanting current features (e.g., resolved virtual-thread pinning
via JEP 491) and the longer support runway (Premier through 2030,
Extended through 2033).
**Security:** Both receive active patches; Java 21's free (NFTC) update
window narrows after September 2026, after which continued no-cost
updates require moving to Java 25 or paying for Oracle support on 21.
**Reliability/Performance:** Java 25 fixes known Java 21 virtual-thread
issues; otherwise both are production-grade.
**Operability:** Java 25 has a shorter production track record; Spring
Boot 4.1 (see below) supports it as baseline.
**Cost/Lock-in:** Staying on Java 21 past September 2026 without Oracle
Extended Support risks an unplanned licensing cost if using Oracle JDK
specifically — mitigated entirely by using an OpenJDK distribution
(Temurin/Corretto), which remain free for the full support window
regardless.
**Healthcare fit:** Neutral — no healthcare-specific constraint favors
either version.
**Decision: ADOPT Java 25 LTS**, using an OpenJDK distribution (not
Oracle JDK) to remove any NFTC-window cost exposure entirely. This
confirms the existing `14` baseline — no change.
**Revisit trigger:** Java 29 LTS GA (planned September 2027) — evaluate
at that time, not before.

## 2. Backend Framework — Spring Boot / Spring Framework

**Candidates:** Spring Boot 3.x (EOL-adjacent), Spring Boot 4.1.
**Evidence:** Spring Boot 4.0 released 20 November 2025; 4.1.0 released
10 June 2026; latest patch 4.1.1 (20 August 2026), paired with Spring
Framework 7.0.8. Only the 4.0 and 4.1 lines remain in open-source support
as of mid-2026; the 3.x line (3.0–3.5) is progressively reaching EOL
(3.4 EOL'd December 2025). Spring Boot 4.1 adds first-class gRPC support,
an OpenTelemetry integration overhaul, SSRF mitigation tooling, and Redis
listener auto-configuration.
**Security:** 3.x lines past EOL receive no free patches — a material
risk for any document still assuming Spring Boot 3.x.
**Decision: ADOPT Spring Boot 4.1.x / Spring Framework 7**, confirming
the existing `14` baseline. Any assumption of Spring Boot 3.x elsewhere
in the repository is now stale and must be corrected (see Cross-Document
Audit, `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md`).
**Revisit trigger:** Spring Boot 4.1 OSS support window close (12-month
cycle from release) — track and re-verify before it lapses.

## 3. Database — PostgreSQL

**Candidates:** PostgreSQL 16, 17, 18.
**Evidence:** PostgreSQL 18 is current major (released 2025), now at
patch 18.6 (11 August 2026). PostgreSQL 18 adds asynchronous I/O (AIO)
improving sequential scan/vacuum/bitmap-heap-scan performance, OAuth
authentication support, `uuidv7()` for timestamp-ordered UUIDs, virtual
generated columns, and parallel FULL/RIGHT OUTER JOIN execution.
PostgreSQL 14 reaches end of fixes November 12, 2026.
**Decision: ADOPT PostgreSQL 18.x**, confirming the existing `14`
baseline. `uuidv7()` is directly useful for the platform's identifier
strategy (time-ordered IDs without a separate sequence) — noted as an
implementation-detail opportunity, not a new architectural decision.
**Revisit trigger:** PostgreSQL 19 reaching stable (currently in Beta as
of August 2026) — evaluate after GA plus one patch cycle, never on a beta.

## 4. Frontend — Next.js / React Native

**Candidates (Next.js):** 15.5.x (Maintenance LTS), 16.3.x (Active LTS).
**Evidence:** Next.js 16.3 is current stable (August 2026), with 16.3.3
and 15.5.24 as the latest security-patched releases (25 August 2026,
addressing critical vulnerabilities). 16.3 added Instant Navigations,
lower dev-server memory use, and faster builds — no breaking change from
the `14` baseline's "Next.js 16.x" designation.
**Decision: ADOPT Next.js 16.x (track the 16.3 minor line)**, confirming
`14`.

**Candidates (React Native):** 0.8x line vs. 0.87.
**Evidence:** React Native 0.87 shipped in August 2026, described by the
community as paving the way toward v1.0. React Native's support policy
covers the latest three minor lines at any time.
**Decision: ADOPT React Native, track current minor (0.87.x as of this
verification)**, updating `14`'s prior unversioned "React Native" entry
to be explicit. Because React Native ships a monthly release train, `14`
records a tracked *line*, not a frozen patch — consistent with the
Managed Upgrade Policy already defined there.
**Revisit trigger:** React Native 1.0 GA — re-evaluate the whole mobile
stack's stability assumptions at that point, since 1.0 is an explicit
stability milestone per the project's own communication.

## 5. Messaging — RabbitMQ vs. Google Pub/Sub vs. Kafka

**Requirement:** Reliable, tenant-safe asynchronous event backbone for
the Transactional Outbox pattern (`06`), supporting retry/DLQ,
correlation IDs, and moderate-to-eventually-high throughput for a
platform starting single-team-operated on GCP.

**Candidates evaluated:**

| Criterion | RabbitMQ (self-managed or managed) | Google Cloud Pub/Sub | Apache Kafka |
|---|---|---|---|
| Ordering | Strong (per-queue) | Best-effort by default; per-key ordering available, not global | Strongest (per-partition, deterministic) |
| Delivery guarantee | At-least-once, mature DLQ/routing | At-least-once by default; exactly-once achievable with Dataflow | At-least-once by default; exactly-once semantics natively supported with idempotent/transactional producers |
| Operability (single team, GCP-native) | Requires self-hosting or a managed RabbitMQ offering — cluster/broker ops burden | Fully managed, serverless, zero broker/partition management — native GCP integration (IAM, VPC, Cloud Run triggers) | Highest operational burden — broker sizing, partition planning, upgrades; managed offerings (Confluent) reduce but don't eliminate this |
| Scalability | Clusters horizontally but with manual config | Near-infinite, provider-managed autoscaling | Very high, but requires capacity planning |
| Retention/Replay | Time/size-limited, not designed as a log | 7-day default, up to 31 days, seekable | Configurable, often long/indefinite — built for replay |
| Cost model | Infra cost + ops time | Pay-per-use, no idle broker cost | Infra/cluster cost + ops time, or Confluent subscription |
| Cloud-native fit (this platform is GCP-first, `13`) | Neutral-to-negative — another stateful service to run on Cloud Run/GKE | Native — designed for exactly this GCP-first, Cloud-Run-first architecture | Neutral-to-negative on GCP without Confluent Cloud |
| Healthcare workflow fit | Good — routing-heavy, moderate volume (clinical events, orders, results) matches RabbitMQ's design center | Good — the platform's actual event volume (per-tenant clinical events) does not need Kafka-scale replay/log semantics | Overkill for current evidenced need; no event-sourcing-at-scale requirement has been demonstrated |
| Developer burden | Moderate (AMQP concepts, exchange/queue topology) | Low (topic/subscription model, GCP SDKs) | High (partition/consumer-group mental model) |

**Decision:**
- **Google Cloud Pub/Sub — ADOPT as PRIMARY** event backbone. Rationale:
  this platform is already GCP-first end to end (`13`); Pub/Sub removes
  an entire class of operational burden (no broker to run, patch, or
  scale) that directly serves the single-team-operability criterion in
  the Technology Decision Framework, at the cost of weaker default
  ordering — which is mitigated by using ordering keys per-tenant/
  per-aggregate (e.g., per-patient or per-encounter) wherever the
  Transactional Outbox (`06`) needs order preserved.
- **RabbitMQ — CONDITIONAL/RETAIN as a documented alternative**, not the
  primary. If a specific integration genuinely needs AMQP-native routing
  topology (e.g., a legacy analyzer or PACS integration engine that only
  speaks AMQP) the Interoperability Layer (`06`) may use RabbitMQ for
  that specific adapter — but the internal domain event backbone
  standardizes on Pub/Sub.
- **Kafka — REJECTED for the current stage**, on the explicit ground
  that no evidenced requirement (event-sourcing-at-scale, cross-years
  replay, partition-level exactly-once for financial ledgers beyond what
  PostgreSQL's transactional guarantees already provide) has been
  demonstrated. This mirrors ADR-002/ADR-003's evidence-driven rejection
  of unneeded operational complexity (`19`). REVISIT if a real,
  measured requirement for long-retention replay or extreme throughput
  emerges.

**Architectural consequence:** `06-MASTER-INTEGRATION-MAP.md`'s Internal
Event Backbone section is updated to name Pub/Sub as the primary
transport, with the domain layer depending on a messaging abstraction
(not a direct broker SDK) so this decision remains swappable — per the
governance task's explicit instruction that "the domain layer must
depend on an abstraction, not directly on a specific broker."

**Revisit trigger:** A measured requirement for cross-partition ordering
at platform scale, or a real analytics/event-sourcing use case that
needs long-window replay beyond Pub/Sub's 31-day maximum retention.

## 6. Infrastructure as Code — Terraform vs. OpenTofu

**Evidence:** HashiCorp relicensed Terraform from MPL 2.0 to BSL 1.1 in
August 2023 (not OSI-approved); IBM completed acquiring HashiCorp in
December 2024. OpenTofu (Linux Foundation-governed, MPL 2.0, OSI-approved)
has since diverged with features Terraform's open CLI lacks — notably
native state/plan encryption and provider-defined functions ahead of
Terraform. As of 2026, OpenTofu holds roughly 12% adoption among IaC
practitioners with 27% evaluating/expanding use; Terraform retains the
larger installed base (33–62% depending on measurement) but adoption
commentary specifically flags regulated/compliance-sensitive
organizations (banking, aerospace cited as examples) choosing OpenTofu
specifically for licensing clarity.
**Security:** OpenTofu's native state encryption is a direct, concrete
security improvement over Terraform's open-source CLI, which requires
backend-level encryption bolted on separately — directly relevant given
this platform's Data Plane (`04`) already treats Terraform state as a
DR-tracked component (`17`) containing sensitive configuration.
**Cost/Lock-in:** MPL 2.0 / OSI-approved license reduces legal-review
friction for a healthcare platform expecting compliance/legal review
(`08`) — matching the governance task's own instruction to prefer
license clarity in regulated contexts.
**Operability:** Near-identical HCL syntax and provider ecosystem; the
CLI swap is low-friction (`terraform` → `tofu`), and both read the same
state format currently, keeping migration risk low.
**Decision: ADOPT OpenTofu** as the IaC baseline, replacing Terraform in
`13-MASTER-INFRASTRUCTURE-ARCHITECTURE.md`'s stack table. This is a
license-and-security-driven decision, not a feature-driven one — no
Terraform-exclusive feature (e.g., HCP Terraform Stacks) is required by
anything in this architecture.
**Revisit trigger:** A specific need for an HCP-Terraform-exclusive
capability, or evidence that OpenTofu's provider compatibility has
regressed for a GCP provider this platform depends on.

## 7. Compute — Cloud Run vs. GKE

**Decision: RETAIN Cloud Run** (no change from `13`/ADR-003). The
governance task's own instruction — "GKE must NOT be included merely
because enterprise systems use Kubernetes" — confirms rather than
overturns the existing evidence-driven rejection. No new evidence in
this pass shows a Cloud-Run autoscaling ceiling being reached.
**Revisit trigger:** unchanged from ADR-003 — measured autoscaling
ceiling evidence.

## 8. Identity Provider Hosting — Keycloak

**Decision: ADOPT Keycloak as a container on Cloud Run**, backed by its
own Cloud SQL (PostgreSQL) instance (already specified in `04`/`17` as
"Keycloak DB"), consistent with the Cloud Run decision above — Keycloak
does not require a Kubernetes-specific feature to run correctly, and
running it as a stateless container against an external managed database
fits the same modular-monolith-first, Cloud-Run-first posture as every
other service in `13`.
**Revisit trigger:** A specific Keycloak feature (e.g., a cluster-only
capability) that Cloud Run cannot host — no such requirement is evidenced
today.

## 9. Observability Backend — Grafana Cloud vs. self-hosted

**Decision: CONDITIONAL — lean ADOPT Grafana Cloud (managed) over
self-hosted Grafana/Loki/Tempo**, on single-team-operability grounds
consistent with the Cloud Run/Pub/Sub reasoning above: self-hosting an
observability stack is exactly the kind of operational burden the
Technology Decision Framework (`8`) weighs against for a single-team
platform. **This entry is explicitly marked lower-confidence than
items 1–8** — it was not backed by the same depth of fresh source
verification in this pass as the messaging and IaC decisions were, and
should be re-verified with a dedicated research pass before being
promoted to APPROVED status in `19`.
**Revisit trigger:** Cost-at-scale evidence once real telemetry volume
exists; re-verify with dedicated research before finalizing.

## 10. FHIR Version Strategy — Correction

**This is the most consequential finding of this verification pass** and
corrects a claim made in the prior architecture pass (`06`'s original
"R5 baseline" framing).

**Evidence:** FHIR R4 remains the *regulatory* baseline in the most
mature regulatory market (US Core / ONC Cures Act / CMS mandates are
built on R4); US Core has **not** moved to R5, and its planned v10 targets
**R6**, not R5. Multiple independent sources describe FHIR R5 as having
"limited adoption" and functioning best as a transitional stepping stone
for teams preparing for R6, rather than as a durable production target in
its own right. FHIR R6 is still in ballot (first full ballot,
v6.0.0-ballot4, dated May 2026; a further HL7 consensus ballot round ran
July–August 2026); HL7's own product director frames R6, not R5, as "the
clear long-term direction," with production-grade R6 adoption not
expected before late 2027.

**Consequence:** The prior architecture's framing of "FHIR R5 baseline,
R4/R4B compatibility" characterized R5 as the primary target and R4 as a
legacy compatibility concession. The evidence found in this pass shows
the opposite is closer to reality for a platform targeting real-world
interoperability (government systems, payers, external labs) in the
near term: **R4 (with the R4B subscription backport where needed) is the
safer production baseline today; R5 is a transitional/optional layer;
R6 is a tracked future target, explicitly not a production baseline**
until it reaches final stable status — consistent with the "Zero
Fabrication" instruction not to treat a ballot draft as a shipped
standard.

**Decision: CORRECT `06-MASTER-INTEGRATION-MAP.md` and
`14-MASTER-TECHNOLOGY-STACK.md`** to state: **FHIR R4/R4B = current
production target; FHIR R5 = optional/transitional, adopted only where a
specific integration partner requires it; FHIR R6 = tracked, not
adopted, until final stable publication.** This does not mean "ARGON
uses FHIR" as an unqualified claim — the canonical internal clinical
model (`03` Clinical domain) remains the source of truth, with FHIR as a
mapping/exchange layer at the Interoperability boundary, per the
governance task's explicit instruction against that exact misleading
phrasing.
**Revisit trigger:** FHIR R6 reaching final/normative publication
(tracked HL7 target: 2026–2027, not before).

---

## Summary Decision Table

| Technology | Status | Decision |
|---|---|---|
| Java 25 LTS (OpenJDK distribution) | ADOPT | Confirmed |
| Spring Boot 4.1.x / Spring Framework 7 | ADOPT | Confirmed |
| PostgreSQL 18.x | ADOPT | Confirmed |
| Next.js 16.x (16.3 line) | ADOPT | Confirmed |
| React Native (0.87.x, tracked line) | ADOPT | Confirmed, now version-explicit |
| Google Cloud Pub/Sub | ADOPT (primary event backbone) | **Changed from RabbitMQ-only** |
| RabbitMQ | CONDITIONAL (adapter-specific only) | **Changed from primary to conditional** |
| Apache Kafka | REJECTED (current stage) | New entry, explicitly rejected with reason |
| OpenTofu | ADOPT (replaces Terraform) | **Changed from Terraform** |
| Cloud Run | RETAIN | Confirmed |
| GKE | REJECTED (current stage) | Confirmed |
| Keycloak on Cloud Run | ADOPT | Clarified |
| Grafana Cloud | CONDITIONAL (lower confidence) | New entry, flagged for deeper research |
| FHIR R4/R4B | ADOPT (production baseline) | **Corrected from R5-primary** |
| FHIR R5 | CONDITIONAL (transitional/optional) | **Corrected from baseline to optional** |
| FHIR R6 | DEFERRED (tracked, not adopted) | Confirmed as not-yet-adoptable |

## Dependencies
Feeds updates to `docs/master/06`, `docs/master/13`, `docs/master/14`,
new ADR entries in `docs/master/19`.

## Unknowns
UNKNOWN — Grafana Cloud vs. self-hosted was not researched to the same
depth as the other nine items; treat as CONDITIONAL only, not APPROVED,
until a dedicated pass is run. UNKNOWN — no cost modeling was performed
for Pub/Sub-at-scale vs. RabbitMQ-at-scale; the decision above is an
operability/licensing/fit decision, not a cost-verified one.
