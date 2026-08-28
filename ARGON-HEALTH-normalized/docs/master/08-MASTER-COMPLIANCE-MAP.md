# 08 — MASTER COMPLIANCE MAP

**STATUS:** TARGET ARCHITECTURE / PROPOSED
**EVIDENCE CLASS:** DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED. This document defines a tracking *system*,
not a compliance *claim*. No control below is asserted as met.

## Purpose
Define the compliance-engineering framework — how a requirement becomes a
control, an implementation, a test, and finally evidence — and prevent any
status from being asserted without that chain.

## Scope
Covers the tracking framework and a starting register of requirement
categories. Country-specific legal requirements are per-country and
REQUIRE LEGAL VERIFICATION before any status beyond DISCOVERED is
assigned — this document does not perform that verification.

## Current Assumptions
Compliance is evidenced, not declared. A feature being "built" is not the
same as a control being "compliant" — these are different lifecycle
stages and must never be collapsed into one status.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Requirement Record Fields
Every compliance requirement is tracked with: Requirement · Jurisdiction ·
Control · Implementation · Test · Evidence · Owner · Review Date · Status.

### Status Lifecycle
```
UNKNOWN
  → DISCOVERED
  → REQUIRES LEGAL REVIEW
  → DESIGNED
  → IMPLEMENTED
  → TESTED
  → EVIDENCED
  → APPROVED
       (→ EXPIRED on review-date lapse)
       (→ NON-COMPLIANT on evidenced failure)
```
**Hard rule:** IMPLEMENTED never converts directly to APPROVED or to any
informal "compliant" label. TESTED and EVIDENCED are mandatory
intermediate gates. A status skip is treated as a documentation defect.

### Starting Requirement Register (illustrative, not exhaustive)

| Requirement | Jurisdiction | Status |
|---|---|---|
| Data protection / personal data processing obligations | Jordan (home jurisdiction) | DISCOVERED — REQUIRES LEGAL REVIEW before DESIGNED |
| Data protection / personal data processing obligations | Saudi Arabia, UAE, Qatar, Kuwait, Bahrain, Oman | UNKNOWN — REQUIRES LEGAL REVIEW per country before any further status |
| Electronic invoicing format & submission | Jordan | DISCOVERED — REQUIRES LEGAL REVIEW; see `06` Government Country Adapter |
| Electronic invoicing format & submission | Other GCC countries | UNKNOWN per country |
| Application security baseline (OWASP ASVS 5 / API Top 10) | Global (not jurisdiction-specific) | DESIGNED (baseline adopted in `07`) — not yet IMPLEMENTED/TESTED |
| Information security management (ISO/IEC 27001/27002) | Global | DESIGNED (referenced as target framework in `07`) |
| Health-sector security overlay (ISO 27799) | Global | DESIGNED (referenced in `07`) |
| PACS/imaging conformance (DICOM) | Per deployment | UNKNOWN — REQUIRES EVIDENCE of an actual conformance statement |
| FHIR conformance | Per deployment | UNKNOWN — REQUIRES EVIDENCE of a published conformance statement/Implementation Guide |
| National health system integration approval | Per country | UNKNOWN — REQUIRES LEGAL REVIEW and REQUIRES a government-issued approval record |
| Payment card handling (if payments module handles cards directly) | Global | Mitigated by design (`03` Payments domain — tokenization, no raw card storage) — REQUIRES independent PCI scope assessment before any claim |
| Controlled-substance chain-of-custody | Per country | UNKNOWN — REQUIRES LEGAL REVIEW per country's pharmacy regulation |

This register is a starting skeleton. Every row above stays at its listed
status — or lower — until independently evidenced; no later document in
this set may assert a higher status without updating this register first.

## Alternatives Considered
- **A single "compliant / not compliant" flag per standard** (rejected) —
  collapses the meaningful difference between "we designed for this" and
  "an auditor evidenced this," which is the exact collapse this framework
  exists to prevent (see section 33 of the originating prompt).

## Security Impact
Security controls designed in `07-MASTER-SECURITY-MAP.md` are the primary
feed into the "Control" and "Implementation" columns for the security-
standard rows above.

## Operational Impact
Every requirement needs an Owner and a Review Date — compliance status
decays over time (EXPIRED) even without any code change, so this is an
ongoing operational responsibility, not a one-time project.

## Performance Impact
N/A.

## Compliance Impact
This document IS the compliance-impact ledger for the rest of the
platform.

## Failure Modes
- A requirement discovered but never assigned an Owner will silently
  stall — the register must be reviewed on a defined cadence, not only
  when a customer or auditor asks.
- Marking a requirement APPROVED without a corresponding Evidence
  artifact is a critical documentation defect.

## Dependencies
Depends on `01`, `06`, `07`. Feeds `20-MASTER-IMPLEMENTATION-ROADMAP.md`
(compliance work becomes roadmap items) and is referenced by every other
master document's "Compliance Impact" section.

## Unknowns
UNKNOWN — REQUIRES LEGAL REVIEW is the default status for every
jurisdiction-specific row above until a qualified legal review is
actually performed. This document does not and cannot substitute for
that review.

## Validation
Every "Compliance Requirements" pointer in `03-MASTER-DOMAIN-MAP.md`
resolves to a row (or row category) in this register. Confirmed at time
of writing.

## Rollback
N/A — this is a tracking system, not a deployed change.

## Definition of Done
Every requirement referenced anywhere in the master document set has a
row here with a real (not placeholder) status, owner field defined as
"TBD" where genuinely unassigned, and a review-date policy stated even if
the date itself is not yet set.
