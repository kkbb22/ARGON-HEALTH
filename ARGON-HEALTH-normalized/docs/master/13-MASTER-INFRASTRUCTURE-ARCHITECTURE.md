# 13 — MASTER INFRASTRUCTURE ARCHITECTURE

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Define the target cloud infrastructure and deployment model — where the
three planes (`01`) actually run.

## Scope
Covers compute, networking, and CI/CD shape. Data-store specifics are in
`04-MASTER-DATA-MAP.md`; exact dependency versions are in
`14-MASTER-TECHNOLOGY-STACK.md`.

## Current Assumptions
Start as a **modular monolith deployed on a small number of Cloud Run
services**, not a full microservices-per-domain deployment — the module
boundaries defined in `03-MASTER-DOMAIN-MAP.md` are logical/code
boundaries first; physical service-per-domain splitting is a later,
evidence-driven decision (consistent with `01`'s rejection of
"microservices from day one").

## Evidence
UNKNOWN — REQUIRES EVIDENCE for repository/implementation state (see
`01`). **Partially superseded 2026-08-27**: the IaC tool choice below is
now backed by live research — see
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §6. Cloud Run vs. GKE
was re-confirmed (§7) rather than changed.

## Decision

### Infrastructure Diagram
```
                        Cloudflare (CDN / WAF / DDoS)
                                    |
                          GCP Load Balancer (Global LB)
                                    |
                              Cloud Armor (protection)
                                    |
              +---------------------+---------------------+
              |                                             |
        Cloud Run                                     Cloud Run
   (Application Plane services,                  (Control Plane services,
    modular monolith, autoscaled)                 isolated deployment)
              |                                             |
              +---------------------+---------------------+
                                    |
                    VPC (private network, no public DB)
                                    |
        +---------------+---------------+---------------+
        |               |               |               |
   Cloud SQL       Memorystore      Cloud Storage    Secret Manager
   (PostgreSQL,     (Redis)         (documents,       + Cloud KMS
    HA + PITR)                       DICOM, backups)   (encryption)
```

### Component Choices
- **Cloud Run** — serverless containers for both Application Plane and
  Control Plane services; independently deployable per `01`'s
  plane-separation requirement, independently scalable.
- **Cloud SQL (PostgreSQL)** — managed primary OLTP store, HA
  configuration, automated backups with PITR (`04`, `17`).
- **Memorystore (Redis)** — managed cache/queue backing; never a primary
  data store (`04`).
- **Cloud Storage** — object storage for documents, DICOM instances,
  backups (`04`).
- **Secret Manager + Cloud KMS** — secrets and encryption key management,
  feeding `07`'s security baseline.
- **Cloud Armor + Cloudflare** — WAF/DDoS at the edge, CDN where static
  content justifies it; Cloudflare adopted only where it adds value over
  Cloud Armor alone (e.g., global edge caching), not duplicated by
  default.
- **VPC** — private networking; Cloud SQL and Memorystore are never
  publicly reachable; only Cloud Run services inside the VPC connect to
  them.
- **OpenTofu** (changed 2026-08-27, was Terraform — see
  `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §6) — infrastructure
  as code for every environment (dev/staging/prod), with
  environment-specific variable sets, never hand-provisioned resources in
  any environment beyond a local dev sandbox. OSI-approved (MPL 2.0)
  licensing and native state/plan encryption were the deciding factors
  over Terraform's BSL-licensed CLI. A Terraform CLI fallback remains
  available (near-identical HCL, same state format) if a future need
  arises for an HCP-Terraform-exclusive feature — not currently required
  by anything in this architecture.
- **Docker** — container images for every deployable service.
- **GitHub Actions** — CI/CD pipeline feeding the Release workflow (`05`
  §12): build → test → compatibility validation → canary → waves.

### Environments
Minimum three: **dev** (developer iteration), **staging** (pre-release
validation, mirrors production topology at smaller scale), **production**
(the only environment serving real tenants). OpenTofu state is isolated
per environment; no shared state file across environments.

## Alternatives Considered
- **Kubernetes from day one** (rejected) — adds operational surface
  (cluster management, node pools, ingress controllers) without evidence
  that Cloud Run's autoscaling ceiling has been reached; revisit only on
  measured need (`29` performance-budget principle in the originating
  prompt).
- **Terraform instead of OpenTofu** (superseded 2026-08-27) —
  re-evaluated on licensing and state-encryption grounds; see
  `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §6.
- **Multi-cloud from day one** (rejected) — no stated requirement
  justifies the added complexity; a single well-understood cloud provider
  is the lower-risk starting point, and country-specific data-residency
  needs are handled via GCP region selection first (`06` Government
  Country Adapter), not via multi-cloud.

## Security Impact
VPC-only database access and Cloud Armor/Cloudflare at the edge are
concrete implementations of `07`'s WAF/DDoS/rate-limiting requirements.

## Operational Impact
Cloud Run's per-service autoscaling means Control Plane load spikes
(e.g., a bulk provisioning run) cannot starve Application Plane capacity,
and vice versa — a direct infrastructure expression of `01`'s plane
independence requirement.

## Performance Impact
No numbers asserted. Cold-start latency on Cloud Run is a known
characteristic to measure once real traffic patterns exist — REQUIRES
MEASUREMENT.

## Compliance Impact
GCP region selection is the primary lever for data-residency requirements
per country (`06`, `08`) — the specific region-per-country mapping
REQUIRES LEGAL VERIFICATION before being finalized.

## Failure Modes
- A Cloud SQL failover must not require Cloud Run redeployment — connection
  handling must tolerate a primary failover transparently.
- An OpenTofu apply against the wrong environment's state is a
  release-blocking-class incident — environment isolation above exists
  specifically to prevent this.

## Dependencies
Depends on `01`, `04`, `06`, `07`. Feeds `14` (exact versions), `17`
(disaster recovery specifics per component), `20` (roadmap sequencing).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any infrastructure currently exists
matching this target.

## Validation
Every data-plane component in `04-MASTER-DATA-MAP.md`'s matrix appears in
the infrastructure diagram above with a concrete GCP service. Confirmed
at time of writing.

## Rollback
Infrastructure changes via OpenTofu are reviewed and applied through the
same wave-gated Release discipline as application code (`05` §12) —
never a direct manual change to a running environment.

## Definition of Done
Every service in `02-MASTER-SYSTEM-MAP.md` has a named deployment target
in this diagram, and no stateful component lacks a managed, backed-up
GCP service backing it.
