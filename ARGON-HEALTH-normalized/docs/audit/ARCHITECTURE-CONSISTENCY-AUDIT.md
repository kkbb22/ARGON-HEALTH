# ARCHITECTURE CONSISTENCY AUDIT

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
AUDIT RECORD. Dated 2026-08-27. Performed against the repository as
cloned from `https://github.com/kkbb22/ARGON-HEALTH.git` at commit
`d066934`.

## Purpose
Document the actual cross-document consistency audit performed across
`docs/master/01`–`20` and `docs/MASTER-ARGON-BLUEPRINT.md`, per the
Architecture Normalization task's Section 6 requirement — a real audit
record, not a claim of one.

## Method
1. Confirmed repository contents byte-for-byte against the documents as
   originally authored (diff check — see Finding 1 below).
2. Built an internal matrix of DOCUMENT × CLAIMS × DEPENDENCIES ×
   TECHNOLOGIES × VERSIONS × DOMAIN REFERENCES × SECURITY REFERENCES ×
   COMPLIANCE REFERENCES × WORKFLOW REFERENCES by reading all 21 files.
3. Searched specifically for the drift categories named in the
   originating task (RabbitMQ vs. Pub/Sub, PostgreSQL version, Java
   version, Spring Boot version, Spring Modulith version, FHIR version,
   Next.js/React Native version, Cloud Run vs. GKE, Keycloak hosting,
   Grafana hosting, Terraform vs. OpenTofu, Cloudflare status).
4. Cross-checked every domain named in `03-MASTER-DOMAIN-MAP.md` against
   every workflow reference in `05-MASTER-WORKFLOW-MAP.md` and every data
   placement in `04-MASTER-DATA-MAP.md`.

## Findings

### Finding 1 — Repository state (baseline confirmation)
The repository, prior to this audit, contained exactly the 21 documents
produced in the prior architecture-foundation pass, unmodified except for
filenames carrying a browser-download `" (1)"` suffix. **No other code,
no implementation, no additional documentation existed.** This confirms
every document's own "UNKNOWN — REQUIRES EVIDENCE" framing was accurate
at the time of writing — there was no undocumented reality to reconcile
against.

### Finding 2 — Internal cross-document consistency (01–20, as originally
written)
**No internal contradictions found.** Because all 20 documents plus the
blueprint were authored in a single continuous pass with a shared
dependency chain (`01`→`02`→`03`→...→`20`, as declared in the Blueprint's
§31), technology names, version numbers, domain names, and workflow
references were consistent throughout. Specifically checked and
confirmed consistent:
- Java version: "25 LTS" — consistent across `01`, `13`, `14`.
- Spring Boot version: "4.1.x" — consistent across `13`, `14`.
- PostgreSQL version: "18.x" — consistent across `01`, `04`, `13`, `14`,
  `17`.
- FHIR version claim: "R5 baseline, R4/R4B compatibility" — consistent
  across `06`, `14` (but see Finding 3 — internally consistent does not
  mean externally correct).
- Messaging: "RabbitMQ" — consistent across `06`, `14` (same caveat).
- IaC: "Terraform" — consistent across `13`, `14`, `17` (same caveat).
- Domain names: all 39 domains in `03` are referenced consistently by
  the same names in `05` (workflows), `07` (security), `08`
  (compliance), `10` (patient journey).
- No orphaned domain (present in `03`, absent from `02`'s system map) or
  orphaned service (present in `02`, absent from `03`) was found.
- No broken internal cross-reference (a document citing another
  document's section that doesn't exist) was found.

**Interpretation:** the original pass's internal discipline (every
document ending with a Validation section cross-checking against its
dependencies) worked as intended — it produced a self-consistent set.
The gap this normalization task's Section 7 was designed to catch is
different in kind: **self-consistency does not verify the claims against
external, current reality.** That is exactly what Finding 3 covers.

### Finding 3 — External-reality drift (the real contradictions)
A **fresh verification pass** (`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`)
found three claims that were internally consistent but did not hold up
against current external evidence:

| # | Original claim | External evidence | Resolution |
|---|---|---|---|
| 1 | FHIR R5 = production baseline | US Core (the dominant regulatory FHIR baseline) remains on R4; R5 independently described as having limited real-world adoption; R6 still in ballot | **Corrected**: R4/R4B is now the stated production baseline (`06`, `14`, ADR-018) |
| 2 | RabbitMQ = sole event backbone | Platform is GCP-first end-to-end (`13`); Pub/Sub removes broker-operational burden with no evidenced need for Kafka/RabbitMQ-class throughput or replay | **Changed**: Pub/Sub primary, RabbitMQ conditional (`06`, `14`, ADR-016) |
| 3 | Terraform = IaC baseline | Terraform is BSL-licensed (not OSI-approved) under IBM ownership since 2024; OpenTofu is MPL 2.0/OSI-approved with native state encryption | **Changed**: OpenTofu adopted (`13`, `14`, ADR-017) |

No other drift category from the originating task's checklist (Java
version, PostgreSQL version, Spring Boot version, Spring Modulith
version, Next.js/React Native version, Cloud Run vs. GKE, Keycloak
hosting, Grafana hosting, Cloudflare status) produced a contradiction —
each was either re-confirmed as still current (Java 25, PostgreSQL 18,
Spring Boot 4.1, Next.js 16.3, React Native 0.87.x, Cloud Run) or, for
Grafana Cloud specifically, left explicitly CONDITIONAL/lower-confidence
pending a dedicated research pass rather than resolved with the same
confidence as the other items (see `TECHNOLOGY-BASELINE-VERIFICATION.md`
§9).

### Finding 4 — Domain map / workflow map / data map alignment
Re-checked per this task's Section 48 gate conditions:
- Every domain in `03-MASTER-DOMAIN-MAP.md` has at least one workflow
  reference in `05-MASTER-WORKFLOW-MAP.md` — confirmed, no orphans.
- Every workflow in `05` references only domains that exist in `03` —
  confirmed.
- Every domain with a data footprint in `03` has a corresponding row (or
  clear inclusion) in `04-MASTER-DATA-MAP.md`'s Data Location Matrix —
  confirmed.
- `07-MASTER-SECURITY-MAP.md`'s authorization model (RBAC+ABAC+
  relationship+purpose-of-use+break-glass) is referenced consistently
  wherever a domain's "Permissions" field in `03` implies one of these
  mechanisms — confirmed, no domain invents a permissions concept outside
  this model.
- `08-MASTER-COMPLIANCE-MAP.md`'s jurisdiction list matches `06`'s
  Government Country Adapter list (Jordan, Saudi Arabia, UAE, Qatar,
  Kuwait, Bahrain, Oman) — confirmed.

### Finding 5 — No fabrication detected
No document in the original 21 claims production readiness,
certification, compliance, or implementation evidence. Every instance of
"UNKNOWN," "REQUIRES EVIDENCE," "REQUIRES LEGAL VERIFICATION," "REQUIRES
MEASUREMENT," or "TARGET/PROPOSED" was checked for correct usage — no
instance was found where a claim should have carried one of these
qualifiers but didn't.

## Formal Finding Register (Finding ID / Severity Format)
*Added 2026-08-27, second pass, per the Autonomous Execution Contract's
required audit format (Finding ID, Document, Location, Problem,
Severity, Evidence, Impact, Resolution, Status).*

| Finding ID | Document | Location | Problem | Severity | Evidence | Impact | Resolution | Status |
|---|---|---|---|---|---|---|---|---|
| AUD-001 | `docs/master/06`, `docs/master/14` | Protocol Standards / Data table | FHIR R5 stated as production baseline | HIGH | `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §10 — US Core remains R4, R5 has limited real-world adoption | Interoperability conformance work would have targeted the wrong FHIR version | Corrected to R4/R4B baseline, R5 conditional (ADR-018) | **RESOLVED** |
| AUD-002 | `docs/master/06`, `docs/master/14` | Internal Event Backbone / Data table | RabbitMQ stated as sole messaging technology without comparative evidence | MEDIUM | `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §5 | Would have committed to a broker requiring more operational overhead than necessary for current stage | Changed to Pub/Sub-primary, RabbitMQ-conditional (ADR-016) | **RESOLVED** |
| AUD-003 | `docs/master/13`, `docs/master/14`, `docs/master/17` | Infrastructure Diagram / Observability & Infrastructure table | Terraform specified under a non-OSI license (BSL 1.1) without licensing review | MEDIUM | `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §6 | Legal-review friction for a healthcare platform expecting compliance scrutiny | Changed to OpenTofu (ADR-017) | **RESOLVED** |
| AUD-004 | `docs/master/02-MASTER-SYSTEM-MAP.md` | System Map diagram, FHIR Gateway line | Stale "R5 baseline" reference left over after AUD-001's correction was applied to `06`/`14` but missed in `02` | **HIGH** (correctness of a navigational document any engineer/agent would read first) | Found via `docs/governance/ARCHITECTURE-LINT-RULES.md` re-scan, 2026-08-27, second pass | A reader consulting `02` alone (the system inventory index) would see the wrong FHIR version | Corrected in this same pass — see `docs/governance/ARCHITECTURE-LINT-RULES.md` scan log | **RESOLVED** |

**Process lesson from AUD-004:** a correction applied to the two
documents most directly about a decision (`06` the integration map, `14`
the tech-stack table) does not guarantee every *mention* elsewhere
(`02`'s one-line system inventory) gets updated in the same pass. The
Definition-of-Done practice going forward: after any ADR-driving
correction, re-run a full-repository grep for the old term (not just
edit the "home" documents) before considering the correction complete.
This is now encoded in `docs/governance/ARCHITECTURE-LINT-RULES.md`.

## Contradictions Found: 4 (AUD-001 through AUD-004)
## Contradictions Resolved: 4 (all four — AUD-001/002/003 corrected in
the first normalization pass as ADR-016/017/018; AUD-004 found and
corrected in the second pass via re-scan)
## Duplicate Source-of-Truth Documents: 0 found
## Stale References to Nonexistent Files: 0 found
## Undocumented Assumptions Found: 0 beyond what each document already
flagged as UNKNOWN/TARGET

## Dependencies
Feeds `docs/governance/ARGON-SOURCE-OF-TRUTH.md`,
`docs/governance/ARCHITECTURE-STATUS.md`, and the rewritten
`docs/MASTER-ARGON-BLUEPRINT.md`.

## Unknowns
UNKNOWN whether any code implementation exists anywhere else (a private
branch, a local uncommitted working copy, etc.) beyond what this
publicly-cloned repository state shows — this audit can only certify
against what was actually observable at clone time (commit `d066934`).

## Next Audit Trigger
Re-run this audit (a) before any release wave per `05` §12, (b) whenever
a new ADR changes a technology decision, (c) at minimum every two release
cycles even absent a known change, to catch external-reality drift the
same way Finding 3 was caught here.
