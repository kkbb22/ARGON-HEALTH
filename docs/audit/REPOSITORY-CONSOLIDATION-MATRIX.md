# REPOSITORY CONSOLIDATION MATRIX

STATUS: PROPOSED
EVIDENCE CLASS: RUNTIME EVIDENCE (every row below was produced by cloning and diffing the actual repositories on 2026-09-05, not by reading filenames or descriptions)

## Method
Both repositories were cloned directly (`github.com/kkbb22/ARGON-HEALTH`,
`github.com/kkbb22/system-ARGON-NEW`). Single-commit histories confirm
`ARGON-HEALTH` = commit `4a8df56`, dated 2026-08-28; `system-ARGON-NEW` =
commit `f4f32f7`, dated 2026-09-04. Every "IDENTICAL/DIFF" verdict below
is a byte-level `diff`, not a filename or size comparison. Every content
verdict (e.g., "39 vs 40 domains") was read from the actual file text.

## Repository Identity
Both repositories contain the **same underlying document set**: a
40-domain ARGON Health Platform target architecture authored in a
2026-08-27 "Architecture Normalization" pass. `ARGON-HEALTH` is that
pass's direct output (committed one day later). `system-ARGON-NEW` is
the same tree carried forward through one additional, later pass — a
2026-09-02 "Gap Analysis / Continuous Improvement" pass, explicitly
logged as **ADR-020** ("Deliberate Freeze Exception") — then committed
2026-09-04. They are not two competing designs; they are two points on
one timeline, confirming the premise of this consolidation task.

## Matrix

| Area | ARGON-HEALTH | system-ARGON-NEW | Better/Complete Version | Evidence | Conflict | Final Action |
|---|---|---|---|---|---|---|
| Repository hygiene | 105 files: clean `docs/` tree **plus** a parallel flat top-level copy with `" (1)"` suffixes, a `.bundle`, a `.zip`, and a `.patch` (undelivered normalization — see `APPLY-INSTRUCTIONS.md`, which states the agent had no push credentials) | 77 files: clean `docs/` tree plus 3 loose top-level duplicates of that pass's 3 new files (byte-identical to their `docs/audit/` copies) | **system-ARGON-NEW** | Byte diff confirms A's top-level files are pre-push delivery artifacts, not divergent content; B's loose files are exact duplicates, not drift | No — same content, different delivery packaging | Canonical tree uses the `docs/` structure only; all top-level duplicates, the `.bundle`, `.zip`, and `.patch` are DELETED (content already inside `docs/`, nothing lost) |
| Domain count (`03-MASTER-DOMAIN-MAP.md`) | States "39 domains" in 3 locations within this file (15 across the whole repo per its own audit) | States "40 domains" in the same 3 locations | **system-ARGON-NEW** | Direct text read of both files; corroborated by `docs/audit/FINAL-ARCHITECTURE-COMPLETENESS.md` item 10, which documents the manual recount and fix | OBSOLETE (A) vs. corrected (B) — not a live disagreement, a stale reference | Adopt B's corrected text; verified zero "39 domain" strings remain in the canonical tree |
| ADR log (`19-MASTER-ARCHITECTURAL-DECISIONS.md`) | 15 lightweight ADRs + ADR-016/017/018 in full format (also duplicated as standalone files in `docs/adr/`) | Same 15 + ADR-016/017/018 (full text, single-source in `19` only, no standalone duplicate files) **+ ADR-019 + ADR-020** | **system-ARGON-NEW** (MORE COMPLETE) | Byte diff of `19`: B is a strict superset; standalone `ADR-016/017/018` files in A duplicate content already inside A's own `19` (a DUPLICATE finding, not unique content) | No — additive, not contradictory | Adopt B's `19` and `docs/adr/ADR-019-RECONCILIATION-WITH-ADR-000.md`; drop A's redundant standalone `ADR-016/017/018` files (content fully preserved in `19`) |
| **ADR-014 / ADR-000 stack reconciliation** | ADR-014 logged as "explicitly unreconciled" against the `argon-platform-target-architecture` skill's ADR-000; README calls this "Current Blocker" #1 and warns against implementing against this baseline until resolved | **ADR-019 formally resolves ADR-014**: ADR-000 remains governing; B's tech baseline supersedes ADR-000's inherited NestJS reference as content-only; every roadmap phase re-gated by ADR-000's trigger table; new Rule L15 added | **system-ARGON-NEW** — this is the single most material item in this consolidation | Full text of `ADR-019-RECONCILIATION-WITH-ADR-000.md`, cross-checked against the `argon-platform-target-architecture` skill's own ADR-000 text | This *was* a real, named, unresolved conflict in A — B contains its resolution, not a competing answer | Adopt ADR-019 into canonical tree; canonical `19`'s ADR-014 entry reads "RESOLVED by ADR-019" |
| GAP register (GAP-001…013) | **Not present in any form** | Full register: `docs/audit/FINAL-GAP-REGISTER.md` — 10/13 CLOSED, 3/13 PARTIALLY CLOSED (GAP-004, 008, 009, each with a named non-architectural remainder) | **system-ARGON-NEW** (UNIQUE) | `grep` for `GAP-0` across A returns zero matches; B returns 110 matches across 14 files | No — genuinely absent in A, not contradicted | Adopt B's register verbatim as `docs/audit/FINAL-GAP-REGISTER.md`; already verified self-consistent (see B's own "Consistency Verification" section) |
| Security — service identity / M2M (GAP-001) | Not present | `07-MASTER-SECURITY-MAP.md` §Identity & Session Baseline — GCP workload identity + OAuth2 client-credentials pattern | **system-ARGON-NEW** (UNIQUE) | `grep -l "service identity"`: 0 files in A, 1 in B | No | Adopt B's `07` |
| Security — refresh-token lifecycle (GAP-002) | Not present | `07` — rotation, reuse-detection, conditional device-binding | **system-ARGON-NEW** (UNIQUE) | `grep -l "refresh token"`: 0 in A, 2 in B | No | Adopt B's `07` |
| Security — bulk PHI access control (GAP-003, P1) | Not present | `07` — new §Bulk Access Control: separate classification, rate-limiting, dedicated audit category, approval-gating for high-volume access | **system-ARGON-NEW** (UNIQUE, highest-severity gap in the register) | Text present only in B's `07` | No | Adopt B's `07` |
| Data — tenant isolation for async jobs/exports/cache (GAP-005, P1) | Not present | `04-MASTER-DATA-MAP.md` — new §Tenant Isolation Beyond Synchronous Requests, covering background jobs, exports, and cache explicitly | **system-ARGON-NEW** (UNIQUE) | `grep -l "tenant isolation"`: 3 files in A (general mentions), 6 in B (including the dedicated async-path section) | No | Adopt B's `04` |
| Security — OWASP attack-class mapping (GAP-006) | General OWASP mentions (4 files) | Dedicated 5-row §OWASP Attack-Class Mapping in `07`, cross-referenced to every domain in `03` | **system-ARGON-NEW** (MORE COMPLETE) | `07` byte diff (7,583 vs 12,273 bytes) | No | Adopt B's `07` |
| Security — artifact signing / license scanning (GAP-007) | Not present | `07` §Security Architecture Components — both added to supply-chain list | **system-ARGON-NEW** (UNIQUE) | `grep -l "artifact signing"`: 0 in A, 2 in B | No | Adopt B's `07` |
| Control Plane — licensing lifecycle (GAP-004, partial) | Initial-grant only, no lifecycle | `09-MASTER-CONTROL-PLANE.md` — new §Licensing Lifecycle: state machine + data-safety guarantees; exact durations explicitly left as an open business decision | **system-ARGON-NEW** (MORE COMPLETE, honestly partial) | `09` byte diff (5,779 vs 8,319 bytes); B's own register marks this PARTIALLY CLOSED, not falsely CLOSED | No | Adopt B's `09`; numeric parameters remain open in `docs/audit/DO-NOT-BUILD-YET.md`, not invented |
| Control Plane — template cloning/versioning (GAP-012) | Not present | `11-MASTER-ORGANIZATION-PROVISIONING.md` — versioning + pinned-at-creation + cloning-as-saga-variant | **system-ARGON-NEW** (UNIQUE) | `grep -l "template clon"`: 0 in A, 3 in B | No | Adopt B's `11` |
| Patient App — account recovery (GAP-008, partial) | Not present | `12-MASTER-APPLICATION-ARCHITECTURE.md` — step-up recovery + self-service session revocation; exact recovery channel explicitly deferred | **system-ARGON-NEW** (MORE COMPLETE, honestly partial) | `12` byte diff (6,329 vs 7,290 bytes) | No | Adopt B's `12` |
| Data Governance — legal hold / deletion policy (GAP-009, partial, P1) | Not present | `04` — new §Retention, Legal Hold, and Deletion: anonymization-not-erasure + legal-hold flag; exact retention periods explicitly marked REQUIRES LEGAL VERIFICATION | **system-ARGON-NEW** (MORE COMPLETE, honestly partial) | Text present only in B's `04` | No | Adopt B's `04`; jurisdictional numbers remain UNKNOWN, not invented |
| Disaster Recovery — named scenarios (GAP-010) | Generic DR register, no named catastrophic scenarios | `17-MASTER-DISASTER-RECOVERY.md` — new §Named Scenario Runbooks: ransomware, regional outage, identity-provider/Keycloak outage (incl. break-glass test) | **system-ARGON-NEW** (UNIQUE) | `17` byte diff (5,322 vs 9,967 bytes — the largest single-document delta in the set) | No | Adopt B's `17` |
| Billing/Insurance — co-pay/deductible/currency (GAP-011) | Implicit only | `03-MASTER-DOMAIN-MAP.md` — explicit `CoverageTerms` entity (Insurance) + explicit currency field (Billing) | **system-ARGON-NEW** (MORE COMPLETE) | Named entities present only in B's `03` | No | Adopt B's `03` |
| Testing — privilege escalation / break-glass as named test categories (GAP-013) | `break-glass` referenced generally (8 files) | `15-MASTER-TESTING-STRATEGY.md` — explicit §Security/Authorization/RLS/Tenant Isolation with named ALLOW/DENY test cases for both | **system-ARGON-NEW** (MORE COMPLETE) | `15` byte diff (5,585 vs 6,365 bytes) | No | Adopt B's `15` |
| Governance — Architecture Freeze | Not present | `docs/governance/ARCHITECTURE-FREEZE.md` — formal freeze + 8-step Change Process + Un-Freeze triggers | **system-ARGON-NEW** (UNIQUE) | File absent from A entirely | No | Adopt B's file |
| Governance — Architecture Lint Rules | Present, does not include Rule L15 | Present, **includes Rule L15** (build-verification-before-implementation-claim gate, sourced from the 2026-08-23 blocked-rebuild forensic finding) | **system-ARGON-NEW** | Text diff of `ARCHITECTURE-LINT-RULES.md` | No — additive rule | Adopt B's file |
| Audit — Continuous Improvement / Gap Analysis / Quality reports | Not present | `CONTINUOUS-IMPROVEMENT-FINAL-REPORT.md`, `FINAL-GAP-ANALYSIS.md`, `DO-NOT-BUILD-YET.md`, `FINAL-ARCHITECTURE-QUALITY-REPORT.md` — all unique to this pass | **system-ARGON-NEW** (UNIQUE, all four) | Absent from A's `docs/audit/` (2 files) vs. present in B's (8 files) | No | Adopt all four; rename per Section 14 naming where applicable (see `CONSOLIDATION-DECISIONS.md`) |
| Master docs 01, 02, 06, 13, 14, 18, 20 (technology/system-map corrections) | Pre-correction versions: stale FHIR-R5-as-primary and/or stale RabbitMQ/Terraform references in some cross-referenced locations | Post-correction versions: FHIR R4/R4B baseline, Pub/Sub-primary, OpenTofu, cross-references repaired (documented in B's own `FINAL-ARCHITECTURE-COMPLETENESS.md` items 1–9) | **system-ARGON-NEW** | Byte diffs on all seven files; B's own completeness report itemizes each fix with a "before" state matching A | No — sequential corrections, not competing claims | Adopt B's versions of all seven files |
| Master docs 05, 08, 10, 16 (Workflow Map, Compliance Map, Patient Journey, Clinical Safety) | Present | **Byte-identical to A** | TIE (DUPLICATE, no conflict) | `cmp` returned true for all four files | No | Either source is correct; B's copy adopted for tree consistency (no content difference) |
| `docs/adr/ADR-MESSAGING-PLATFORM.md` (legacy top-level ADR file, pre-normalization) | Present, byte-identical to B's copy | Present, byte-identical to A's copy | TIE | `cmp` confirms identity | No | Retained as-is (superseded in substance by ADR-016, but kept per "no information loss" — see `CONSOLIDATION-DECISIONS.md`) |
| Compliance Traceability Matrix | Present | Byte-identical to A except for the domain-count-driven cross-references already covered above | TIE, no unique content either direction | Full-file diff shows no PCI/jurisdiction differences | No | Adopt B's copy for tree consistency |
| Technology Baseline Verification (evidence) | Present | Byte-identical to A | TIE | `cmp` confirms identity | No | Adopt B's copy |

## Overall Finding
Across every row checked, **zero CONTRADICTORY items were found.** Every
difference is either OBSOLETE→CORRECTED (domain count, stale
cross-references), UNIQUE→ADD (GAP-closure content, ADR-019/020,
freeze/lint additions), or DUPLICATE→CONSOLIDATE (standalone ADR files,
top-level delivery copies). `system-ARGON-NEW` is later, strictly more
complete, and internally self-verified (its own
`FINAL-ARCHITECTURE-COMPLETENESS.md` documents a second independent
consistency pass finding zero new issues). This supports Final Verdict
**A** in the executive report — with the explicit condition that ADR-019
and its "PROPOSED, not authorized to build" status are carried forward
unweakened, not quietly dropped in the merge.

## Dependencies
Feeds `docs/audit/CONSOLIDATION-DECISIONS.md` (per-file decisions),
`docs/governance/ARCHITECTURE-STATUS.md`,
`docs/audit/FINAL-GAP-REGISTER.md` (adopted, not re-derived).
