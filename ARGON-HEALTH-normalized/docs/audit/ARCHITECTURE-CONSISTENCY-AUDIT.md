# Architecture Consistency Audit

**STATUS:** ACTIVE (audit log — this pass's findings; re-run before next major change)
**EVIDENCE CLASS:** DESIGN

## Purpose
Record every structural or content contradiction found while normalizing
this repository, its severity, and its resolution status. An unresolved
contradiction is recorded honestly here, not hidden by silently picking
a side.

## Severity Definitions
- **CRITICAL** — a contradiction that would cause a wrong technical or
  legal decision if acted on as-is.
- **HIGH** — a contradiction likely to cause real confusion or rework if
  left unresolved.
- **MEDIUM** — a real inconsistency, low risk of immediate harm.
- **LOW** — cosmetic/organizational.

---

## AUDIT-001 — Technology baseline unreconciled against a prior architecture consultation for the same project
**Severity:** CRITICAL
**Document(s):** `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` (ADR-014)
**Location:** ADR-014, "Version drift" entry
**Problem:** This repository's entire technology baseline (Java 25 /
Spring Boot 4.1 / Spring Framework 7 / Spring Modulith / PostgreSQL 18)
is recorded, by this document set's own ADR-014, as **unreconciled**
against a separate, earlier architecture consultation for this same
ARGON project — one that reached a staged, trigger-based evolution plan
for a live, single-developer, 5-clinic production system, explicitly to
avoid a big-bang rewrite.
**Evidence:** ADR-014 itself states the drift exists and does not
resolve it. The separate consultation exists as project context outside
this repository.
**Impact:** If Foundation Implementation (`20`) begins against this
baseline without resolving AUDIT-001, the project risks the exact
failure mode the other consultation's staged-evolution plan was designed
to prevent: rewriting a working production system prematurely rather
than migrating it on evidence-based triggers.
**Resolution:** **NOT RESOLVED BY THIS PASS — by design.** Per
`docs/governance/ARGON-SOURCE-OF-TRUTH.md` §8, a genuine conflict at the
same authority level is recorded, not silently decided.
**Status:** **DECISION REQUIRED** — needs a named decision authority to
either (a) explicitly scope this repository as a long-term North Star
architecture, gated by the other consultation's triggers, or (b)
explicitly supersede the other consultation's staged plan with a
documented rationale. Flagged prominently in `README.md`.

---

## AUDIT-002 — Repository structure not normalized (files flat in root, "(1)" suffixes)
**Severity:** HIGH
**Document(s):** All 23 original files
**Location:** Repository root
**Problem:** 18 of 23 files carried a Google-Drive-style `(1)` suffix
(e.g., `01-MASTER-SYSTEM-ARCHITECTURE (1).md`); none were organized into
the `docs/` hierarchy that the documents themselves already referenced
internally (e.g., `06-MASTER-INTEGRATION-MAP.md` already said "see `13`"
assuming a flat numeric scheme, which happened to still work, but no
`docs/master/` path existed anywhere on disk).
**Evidence:** Direct repository inventory (this pass).
**Impact:** Broken navigability; violates section 5 of the normalization
contract; risk of accidental duplicate uploads compounding over time.
**Resolution:** **FIXED THIS PASS.** All files moved into
`docs/master/`, `docs/evidence/`, `docs/adr/`, `docs/governance/`,
`docs/compliance/`, `docs/audit/`; every `(1)` suffix removed; canonical
filenames applied.
**Status:** RESOLVED.

---

## AUDIT-003 — README.md was a stub
**Severity:** HIGH
**Document(s):** `README.md`
**Location:** Whole file
**Problem:** README contained only the repository title (`# ARGON-HEALTH`),
with no vision, scope, navigation, or "target ≠ implemented" statement —
directly against section 7 of the normalization contract.
**Evidence:** Direct inspection.
**Impact:** No entry point for a new engineer or agent; the "target
architecture ≠ implemented system" distinction — critical given this
repo's own Zero-Fabrication rules — was stated nowhere at the front door.
**Resolution:** **FIXED THIS PASS.** Full README rewritten per section 7,
including the explicit tie to AUDIT-001 under "Before implementation
starts."
**Status:** RESOLVED.

---

## AUDIT-004 — ADR-016/017/018 decided but not propagated into dependent documents
**Severity:** HIGH
**Document(s):** `docs/master/01`, `02`, `17`, `18`,
`docs/master/MASTER-ARGON-BLUEPRINT.md`, `docs/master/19` (self-reference)
**Location:** Multiple — see fixes below
**Problem:** Three decisions had been made and fully justified in
`19`'s Full-Format ADR section (Pub/Sub over RabbitMQ, OpenTofu over
Terraform, FHIR R4/R4B over R5), but the documents that originally
stated the old position had not all been updated to match, in direct
violation of each ADR's own "Consequences" clause (each explicitly says
"X is updated" for documents that, on inspection, were not fully
updated) and of contract sections 10/11/12/33 ("update every document,"
"no stale decision may remain").
**Evidence — specific stale statements found:**
- `01-MASTER-SYSTEM-ARCHITECTURE.md`: system diagram labeled the
  messaging box "Messaging (RabbitMQ)" with no Pub/Sub mention.
- `02-MASTER-SYSTEM-MAP.md`: tree diagram listed "Messaging / RabbitMQ
  (event backbone, outbox relay)" as if RabbitMQ were still primary.
- `17-MASTER-DISASTER-RECOVERY.md`: DR table had a RabbitMQ row treated
  as the primary/only messaging DR target, with no Pub/Sub row at all;
  two mentions of "Terraform state" instead of "OpenTofu state."
- `18-MASTER-NON-FUNCTIONAL-REQUIREMENTS.md`: SLI list said "Queue
  latency (RabbitMQ)" with no Pub/Sub qualifier.
- `MASTER-ARGON-BLUEPRINT.md`: Interoperability section still said
  "FHIR R5 (R4/R4B compatible)" — the exact framing ADR-018 corrects;
  Infrastructure section still said "Terraform" instead of "OpenTofu."
- `19-MASTER-ARCHITECTURAL-DECISIONS.md` itself: its own "Validation"
  section referenced "`06`'s RabbitMQ" in passing, even though `06`'s
  own primary decision had already been corrected in-line.
**Impact:** A reader relying on any one of these documents in isolation
— which the Blueprint explicitly invites, since it's meant to be
skimmable without reading all 20 documents — would form the wrong
picture of the current technology decision.
**Resolution:** **FIXED THIS PASS.** All six locations above corrected,
each with an inline note pointing to the governing ADR (ADR-016 or
ADR-018) rather than a silent edit, per
`docs/governance/ARGON-SOURCE-OF-TRUTH.md` §5.
**Status:** RESOLVED.

---

## AUDIT-005 — Missing STATUS / EVIDENCE CLASS header on every major document
**Severity:** MEDIUM
**Document(s):** All of `docs/master/*.md`, `docs/evidence/*.md`
**Location:** Top of file
**Problem:** Every master document had a `## Status` *section* further
down the file with a status sentence, but none had the compact
`**STATUS:**` / `**EVIDENCE CLASS:**` header line required by contract
section 32, so a reader (or a tool grepping for it) couldn't find status
at a glance without reading into the body.
**Evidence:** Direct inspection; confirmed via repository-wide grep for
`^STATUS:` returning zero matches before this pass.
**Impact:** Low-severity but directly against an explicit contract
requirement; makes automated status-scanning (e.g., for
`docs/governance/ARCHITECTURE-STATUS.md`) harder than it needs to be.
**Resolution:** **FIXED THIS PASS.** A `**STATUS:**` / `**EVIDENCE
CLASS:**` banner added immediately under the title of every file in
`docs/master/` and `docs/evidence/`.
**Status:** RESOLVED.

---

## AUDIT-006 — ADR log mixed lightweight and full-format entries in one file, against its own stated intent
**Severity:** LOW
**Document(s):** `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md`
**Location:** "Full-Format ADRs" section
**Problem:** ADR-016/017/018 were written in full detail directly inside
`19`, while standard ADR practice (and the section 10 contract
requirement for a standalone messaging-platform ADR file) calls
for one decision per file.
**Evidence:** Direct inspection of `19`'s structure.
**Impact:** Low — content was correct, just not organized per standard
ADR practice or the explicit section 10 file requirement.
**Resolution:** **FIXED THIS PASS.** ADR-016, ADR-017, ADR-018 promoted
to standalone files under `docs/adr/`; `19` now carries a short index
table pointing to each, per the pattern in
`docs/governance/ARGON-SOURCE-OF-TRUTH.md`.
**Status:** RESOLVED.

---

## AUDIT-007 — No document owners assigned anywhere
**Severity:** MEDIUM
**Document(s):** All of `docs/master/*.md`
**Location:** N/A — absence, not a specific location
**Problem:** No document in `01`–`20` names an individual or role as its
owner, so "who reviews this next" has no answer.
**Evidence:** Direct inspection; reflected in
`docs/governance/ARCHITECTURE-STATUS.md`'s Owner column, currently
UNKNOWN for every row.
**Impact:** Documents can silently go stale with no one accountable for
noticing.
**Resolution:** **NOT RESOLVED — cannot be resolved by a normalization
pass alone.** Assigning owners requires the project's actual org
structure, which this repository does not state and this pass cannot
invent.
**Status:** **DECISION REQUIRED** (organizational, not architectural) —
recommended before Foundation Implementation begins.

---

## AUDIT-008 — Traceability and compliance matrices only exist at Tier 1 depth
**Severity:** MEDIUM
**Document(s):** `docs/governance/TRACEABILITY-MATRIX.md`,
`docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`
**Location:** Whole documents
**Problem:** A full Requirement→Domain→Workflow→...→Release trace across
all 39 domains / 30 workflows, and a fully-evidenced per-country legal
register across all 7 jurisdictions, are both genuinely large undertakings
requiring implementation and licensed-counsel input this pass cannot
fabricate.
**Evidence:** Domain/workflow count from `03`/`05`; jurisdiction count
from `08`/contract section 21.
**Impact:** Medium — the frameworks and Tier 1 depth are real and usable
today; Tier 2 depth and per-country legal evidence are explicitly
labeled as open rather than silently thin.
**Resolution:** **PARTIALLY RESOLVED.** Both matrices exist with real,
usable Tier 1 / global content; Tier 2 backfill and per-country legal
review are explicitly listed as open next steps in each document, not
fabricated.
**Status:** OPEN (tracked, not hidden) — see each document's "Next Step" /
"Definition of Done" section.

---

## Summary Table

| ID | Severity | Status |
|---|---|---|
| AUDIT-001 | CRITICAL | DECISION REQUIRED |
| AUDIT-002 | HIGH | RESOLVED |
| AUDIT-003 | HIGH | RESOLVED |
| AUDIT-004 | HIGH | RESOLVED |
| AUDIT-005 | MEDIUM | RESOLVED |
| AUDIT-006 | LOW | RESOLVED |
| AUDIT-007 | MEDIUM | DECISION REQUIRED |
| AUDIT-008 | MEDIUM | OPEN (tracked) |

**No CRITICAL finding was resolved by silent decision.** AUDIT-001, the
one CRITICAL finding, is intentionally left as DECISION REQUIRED per
`docs/governance/ARGON-SOURCE-OF-TRUTH.md` §8 — this audit does not
pick a side on a real, unresolved conflict.
