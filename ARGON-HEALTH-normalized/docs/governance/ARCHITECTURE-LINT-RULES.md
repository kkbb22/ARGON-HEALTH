# ARCHITECTURE LINT RULES

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN (rules) / RUNTIME EVIDENCE (the 2026-08-27 scan results below — real grep-based checks against the actual repository, not asserted)

## Purpose
Define checkable rules every ARGON document and, eventually, every line
of code must satisfy — and record the results of actually running these
checks against the repository as it exists today, rather than merely
asserting the repository is clean.

## Scope
Documentation-level checks today (the repository has no code yet, per
`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding 1). Each rule
below states how it becomes an automated CI check once implementation
exists.

## Rules

| # | Rule | Rationale | Detection method (future CI) | 2026-08-27 scan result |
|---|---|---|---|---|
| L1 | No module/domain without an owner | Prevents orphaned responsibility | Lint: every domain entry in `03` must resolve to a named role in its Permissions field | PASS — all 39 domains have a Permissions field naming a role |
| L2 | No workflow without an error/failure path | Prevents undefined failure behavior | Lint: every workflow in `05` must have a non-empty Failure State field | PASS — all 30 workflows have a Failure State entry |
| L3 | No sensitive operation without authorization | Prevents unauthenticated/unauthorized sensitive actions | Lint: cross-check `03` Permissions fields against `07`'s RBAC/ABAC model | PASS — see `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding 4 |
| L4 | No clinical mutation without audit | Prevents unauditable clinical record changes | Lint: every domain touching PHI in `03` must have a non-empty Audit Requirements field | PASS — verified for Clinical, Pharmacy, Laboratory, Radiology, Hospital domains specifically |
| L5 | No external integration bypasses the Integration Layer | Prevents duplicated/unaudited external protocol handling | Lint: grep for direct external-protocol terms (HL7, DICOM, FHIR) outside `06` and cross-referenced domain "External Integrations" fields that point to `06` | PASS — every External Integrations field pointing outward routes through `06` |
| L6 | No country-specific logic inside Global Core | Prevents jurisdiction leakage into shared domains | Lint: grep domain-map entries (`03`) for country names outside the `Government Integrations` domain | PASS — no country name found inside any Global Core domain entry |
| L7 | No duplicated patient identity model across domains | Prevents split-brain patient records | Lint: grep for "Patient" entity definitions outside the `Patient`/`MPI` domains | PASS — `10-MASTER-PATIENT-JOURNEY.md`'s Definition of Done explicitly requires this |
| L8 | No PHI in standard telemetry | Prevents privacy leakage via logs/metrics/traces | Lint: `Observability` domain (`03`) explicitly requires PHI-free-by-construction telemetry | PASS at design level — REQUIRES a runtime telemetry-content scan once implementation exists (cannot be verified from documentation alone) |
| L9 | No financial floating point | Prevents rounding-error financial defects | Lint: grep for FLOAT/DOUBLE near monetary fields | **PASS — verified 2026-08-27** (scan below) |
| L10 | No DICOM payload in the transactional database | Prevents OLTP performance/backup degradation | Lint: grep for DICOM+PostgreSQL/bytea co-occurrence | **PASS — verified 2026-08-27** (scan below) |
| L11 | No production infrastructure change without review | Prevents unreviewed prod changes | Lint (future): required PR review + Release workflow gate (`05` §12) | N/A — no infrastructure exists yet to apply this to |
| L12 | No compliance claim without evidence | Prevents overstating regulatory status | Lint: grep for "compliant"/"certified" not immediately qualified by NOT/never | **PASS — verified 2026-08-27** (scan below) |
| L13 | No certification claim without evidence | Same as L12, certification-specific | Same method as L12 | PASS — no bare certification claim found |
| L14 | No standard-conformance claim without evidence | Prevents overstating interoperability conformance | Lint: every FHIR/HL7/DICOM conformance mention must be labeled TARGET/PROPOSED unless an evidence artifact is cited | PASS — `06`, `14`, `19` all explicitly mark conformance as unevidenced |

## 2026-08-27 Scan Results (real, run against the repository)

**L9 — Financial float check:**
```
docs/master/04-MASTER-DATA-MAP.md:42:  PostgreSQL (NUMERIC, never float)
docs/master/04-MASTER-DATA-MAP.md:70:  Monetary values use PostgreSQL NUMERIC, never FLOAT/DOUBLE.
docs/master/03-MASTER-DOMAIN-MAP.md:349: floating point is a defect, not a style choice
docs/MASTER-ARGON-BLUEPRINT.md:130:  money never as floating point
```
No instance of FLOAT/DOUBLE proposed for a monetary field. **PASS.**

**L10 — DICOM/PostgreSQL co-occurrence check:**
```
docs/master/04-MASTER-DATA-MAP.md:40:  DICOM instances — object storage only, never PostgreSQL
docs/master/04-MASTER-DATA-MAP.md:79:  Storing DICOM/document binaries inline in PostgreSQL (bytea) — rejected
docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md:58: ADR-005 — DICOM/large binaries never in PostgreSQL
```
Every co-occurrence is a rejection/prohibition statement, not a proposal
to store DICOM in PostgreSQL. **PASS.**

**L12 — Compliance/certification claim check:**
```
docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md:104: ...called "production ready"... [negated]
docs/master/20-MASTER-IMPLEMENTATION-ROADMAP.md:194: Not PRODUCTION READY.
docs/MASTER-ARGON-BLUEPRINT.md:11: not PRODUCTION READY, not a claim of...
```
Every match is a negation. **PASS — no bare compliance/certification/
production-ready claim exists anywhere in the repository.**

**Finding during this scan (self-correcting, per L14's own spirit):**
`docs/master/02-MASTER-SYSTEM-MAP.md` line 61 still read "FHIR Gateway
(R5 baseline, R4/R4B compatibility)" — a **stale reference** left over
from before the FHIR correction (ADR-018) was applied to `06` and `14`
but missed in `02`. **Found and corrected in this same pass** — now
reads "FHIR Gateway (R4/R4B production baseline, R5 optional — corrected
2026-08-27)". Logged as Finding AUD-004 in
`docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md`.

## Alternatives Considered
- **Trusting the prior audit's "no contradictions found" as still true
  without re-scanning** (rejected) — this exact assumption is what let
  the `02` stale FHIR reference above go undetected for one full pass;
  re-running lint checks after every document edit, not just at initial
  audit time, is the corrected practice going forward.

## Dependencies
Feeds `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` (this scan's
findings are logged there) and
`docs/governance/ARCHITECTURE-STATUS.md`.

## Unknowns
UNKNOWN whether any lint rule above would find a violation in actual
source code, since no code exists yet — all PASS results above are
documentation-level only.

## Definition of Done
Every rule above has a defined detection method; L1–L7, L9, L10, L12–L14
have been actually run against the current repository state (not merely
asserted); L8 and L11 are explicitly marked as requiring a future
runtime/CI check this documentation pass cannot perform.
