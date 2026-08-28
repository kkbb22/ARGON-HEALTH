# 12 — MASTER APPLICATION ARCHITECTURE

**STATUS:** TARGET ARCHITECTURE / PROPOSED
**EVIDENCE CLASS:** DESIGN

## Status
TARGET ARCHITECTURE / PROPOSED.

## Purpose
Define the client applications built on top of the Application Plane
domains (`03`) and the shared frontend architecture they follow.

## Scope
Covers web/mobile technology choice, the unified design system, RTL/LTR
and accessibility requirements, and a per-application breakdown. API
conventions are defined once in `06-MASTER-INTEGRATION-MAP.md` and not
repeated here.

## Current Assumptions
One design system serves every application; no app maintains its own
component library or accessibility baseline.

## Evidence
UNKNOWN — REQUIRES EVIDENCE (see `01`).

## Decision

### Frontend Technology
- **Web** — Next.js, TypeScript, React.
- **Mobile** — React Native, TypeScript (shared business-logic layer with
  web where practical, native platform APIs where required).
- **Design System** — one shared component library across every app
  listed below; a new app never starts its own.

### Internationalization & Accessibility
- **Arabic RTL first, English LTR** — layout, iconography, and date/number
  formatting are built RTL-native, not RTL-as-an-afterthought mirror of an
  LTR design.
- **Accessibility target** — WCAG 2.2 AA across every application,
  including the Control Plane console.
- **UX model** — ISO 9241-210 (human-centered design) principles govern
  the design process, not a specific deliverable.

### Application Inventory
```
 ┌───────────────────────┬─────────────┬───────────────────────────────┐
 │ Application            │ Plane        │ Primary users                  │
 ├───────────────────────┼─────────────┼───────────────────────────────┤
 │ Patient App (mobile+web)│ Application  │ Patients                       │
 │ Clinician Experience    │ Application  │ Physicians, nurses             │
 │ Administration          │ Application  │ Facility admins, reception     │
 │ Pharmacy Console        │ Application  │ Pharmacists, pharmacy techs    │
 │ Laboratory Console      │ Application  │ Lab techs, pathologists        │
 │ Radiology Console       │ Application  │ Technologists, radiologists    │
 │ Hospital Ops Console    │ Application  │ Nursing, bed management, ED    │
 │ Control Plane Console   │ Control      │ Platform operators             │
 └───────────────────────┴─────────────┴───────────────────────────────┘
```

Each console is a thin presentation layer over its domain's API (`03`) —
no console contains business logic that isn't also enforceable
server-side; the UI never becomes a second source of authorization truth
(see `07`).

### Per-Application Notes
- **Patient App** — read-mostly (Patient 360 subset per `10`), plus
  self-service commands (book, message, pay, manage consent). Offline
  read of last-synced data is a target capability, not a guarantee of
  offline writes.
- **Clinician Experience** — the primary Outpatient/Emergency/Admission
  encounter surface (`05` §3–5); optimized for fast order entry and
  results review (`05` "Doctor Workflow").
- **Administration** — Scheduling, Queue, Registration, and
  facility-level configuration surfaces.
- **Pharmacy / Laboratory / Radiology Consoles** — one console per
  domain, each exposing its own worklist (dispense queue, accession
  worklist, reading worklist respectively).
- **Hospital Ops Console** — ADT, bed board, MAR execution surface.
- **Control Plane Console** — Organization lifecycle, licensing,
  release/incident management (`09`); structurally separate login and
  session context from every other console (`07`).

## Alternatives Considered
- **Per-domain bespoke frontend stacks** (rejected) — multiplies design
  and accessibility debt; a shared design system is materially cheaper to
  keep WCAG-compliant than eight independent ones.
- **Native iOS/Android instead of React Native** (deferred, not rejected
  outright) — revisit only if a measured performance or platform-API gap
  justifies the added maintenance surface; no such evidence exists yet.

## Security Impact
The Control Plane Console's session/auth context must never be
reachable from within any Application-Plane console's session, and vice
versa (`07`).

## Operational Impact
A shared design system means a single accessibility regression can affect
every app — accessibility testing (`15`) runs against the shared
component library, not per-app in isolation only.

## Performance Impact
No numbers asserted. REQUIRES MEASUREMENT once implemented — mobile
performance on low-end devices is a particular risk given the target
markets (`06` Government Country Adapter list).

## Compliance Impact
WCAG 2.2 AA is a design commitment here; independent evidence/audit
status is tracked in `08`.

## Failure Modes
An app rendering a permission-gated action as visible-but-non-functional
(instead of simply not rendering it) is treated as a UX defect that risks
being mistaken for a security control — see `07`'s "UI hiding is not a
security control" principle.

## Dependencies
Depends on `01`, `02`, `03`, `06`, `07`. Feeds `14` (frontend stack
versions), `15` (accessibility/mobile/browser test matrix).

## Unknowns
UNKNOWN — REQUIRES EVIDENCE whether any of these applications exist today
in any form.

## Validation
Every application above maps to one or more domains in `03` with no
domain lacking a client surface. Confirmed at time of writing.

## Rollback
N/A at design stage. For implementation: a new app version ships behind
the same wave-based Release workflow (`05` §12) as backend changes.

## Definition of Done
Every domain that has a human user (i.e., every domain except pure
platform/data-plane domains) has exactly one owning console/app, and no
domain's UI logic duplicates a server-side authorization decision.
