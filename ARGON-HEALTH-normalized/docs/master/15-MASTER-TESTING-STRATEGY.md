# 15 — MASTER TESTING STRATEGY

**STATUS:** TARGET ARCHITECTURE / PROPOSED
**EVIDENCE CLASS:** DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Define the test pyramid and, specifically, the mandatory ALLOW/DENY
discipline for every security-relevant test — so "we have tests" is never
confused with "we have tests that prove access controls actually deny
what they should."

## Scope
Covers test layers and what each must verify. Individual ALLOW/DENY test
hints already seeded per-domain in `03-MASTER-DOMAIN-MAP.md` and
per-workflow in `05-MASTER-WORKFLOW-MAP.md` are the seed backlog for this
strategy, not duplicated here.

## Current Assumptions
Every security-relevant test case is written as a pair: one proving
legitimate access is ALLOWed, one proving illegitimate access is DENIED.
A test suite with only ALLOW cases has not actually tested authorization.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Test Pyramid
```
                    E2E (patient-journey scale, `10`)
                 Interoperability (FHIR / HL7 / DICOM)
              Performance / Load / Stress / Soak / Failure
           Backup–Restore / DR drills
        Accessibility / Mobile / Browser Compatibility
     Security / Authorization / RLS / Tenant Isolation (ALLOW+DENY)
  Contract tests (API backward compatibility, `06`)
API tests
Integration tests
Unit tests   ← largest volume, fastest feedback
```

### Layer Definitions
- **Unit** — single function/module, no external dependencies.
- **Integration** — a domain's commands/queries against a real database
  (or realistic test double), still within one domain's boundary (`03`).
- **API** — HTTP/contract-level behavior of a single service's public
  surface, including RFC 9457 error shapes (`06`).
- **Contract** — producer/consumer contract tests preventing a breaking
  API change from shipping unnoticed (`06`).
- **Security / Authorization / RLS / Tenant Isolation** — the mandatory
  ALLOW+DENY pair discipline. Minimum coverage: every "Permissions" field
  in `03` and every workflow's actor/permission combination in `05` has
  at least one DENY case for an unauthorized actor and one ALLOW case for
  the correct one. RLS tests specifically attempt cross-tenant reads and
  writes and assert they fail at the database layer even if application
  logic were bypassed.
- **E2E** — full patient-journey-scale scenarios (`10`), exercising real
  workflow sequences end to end (e.g., Registration → Encounter → Lab
  Order → Result → Billing).
- **Interoperability** — FHIR profile validation against declared
  Implementation Guides, HL7 v2 message round-trips, DICOM conformance
  scenarios (`06`).
- **Performance / Load / Stress / Soak / Failure** — measured against
  SLOs defined in `18-MASTER-NON-FUNCTIONAL-REQUIREMENTS.md`; failure
  testing specifically includes dependency-outage scenarios (e.g.,
  "Redis down," "PACS unreachable") to verify the degrade-gracefully
  behavior specified per-domain in `03`.
- **Backup–Restore / DR** — a backup is not considered tested until a
  restore drill actually succeeds (`17`); this layer exists specifically
  to prevent "we have backups" from being asserted without evidence.
- **Accessibility / Mobile / Browser Compatibility** — WCAG 2.2 AA
  conformance testing, and cross-device/cross-browser matrices for every
  application in `12-MASTER-APPLICATION-ARCHITECTURE.md`.

### Quality Gate
No release wave (`05` §12) proceeds past canary without: all unit/
integration/API/contract tests passing, and the full Security/
Authorization/RLS/Tenant Isolation ALLOW+DENY suite passing with zero
regressions.

## Alternatives Considered
- **ALLOW-only security test coverage** (rejected) — the exact failure
  mode this strategy exists to prevent; an ALLOW-only suite can pass
  while a critical DENY case (e.g., cross-tenant read) silently fails.

## Security Impact
This document is where `07-MASTER-SECURITY-MAP.md`'s authorization model
becomes falsifiable — every claim in `07` should be traceable to a test
case here.

## Operational Impact
Failure-mode testing (dependency-outage scenarios) directly validates the
"Failure Modes" fields written per-domain in `03` — a domain whose stated
failure mode has never been tested is a gap, not a documented fact.

## Performance Impact
Performance/load/stress targets are defined in `18`, not invented here;
this document defines the test *methodology*, not the numeric targets.

## Compliance Impact
Interoperability and accessibility test evidence feeds directly into
`08-MASTER-COMPLIANCE-MAP.md`'s Evidence column for the relevant
requirement rows.

## Failure Modes
A test suite reporting green while missing an entire layer (e.g., no RLS
tests exist at all) is itself a defect to be caught by test-coverage
review, not assumed away by a passing CI badge.

## Dependencies
Depends on `01` through `14`. Feeds `08` (evidence), `16` (clinical
safety verification), `20` (roadmap — test infrastructure buildout is a
roadmap item, not assumed to pre-exist).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any test infrastructure currently
exists.

## Validation
Every ALLOW/DENY test hint seeded in `03` and `05` is representable in
this pyramid's Security layer. Confirmed at time of writing.

## Rollback
N/A — this is a strategy document, not a deployed artifact.

## Definition of Done
Every domain and workflow's stated Permissions/Failure Modes has at least
one corresponding test case type identified above; zero domains or
workflows are left with no testing story.
