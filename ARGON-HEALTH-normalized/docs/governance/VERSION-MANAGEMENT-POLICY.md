# VERSION MANAGEMENT POLICY

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
GOVERNANCE RECORD. Dated 2026-08-27. Policy definition only — no
implementation (dependency-lock files, CI enforcement) exists yet; this
is the target policy those future artifacts must satisfy.

## Purpose
Define how ARGON tracks, updates, and retires dependency versions —
separating what `14-MASTER-TECHNOLOGY-STACK.md` states as a baseline
*target* from what an actual build locks as an exact *patch* version, per
the Managed Upgrade Policy already introduced there.

## Scope
Covers every dependency category in `14`: language runtime, frameworks,
database, frontend, messaging, IaC, and interoperability/terminology
libraries. Does not cover business-logic versioning (API versioning is
`06`'s concern; ADR status versioning is `19`'s).

## Policy

### Supported Version Window
- **Language runtime (Java):** track the current LTS and, at most, the
  immediately prior LTS. Per
  `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §1, this means
  Java 25 LTS (adopted) with Java 21 LTS as the only acceptable fallback
  if a specific dependency has not yet certified Java 25 — never older
  than N-1 LTS.
- **Application framework (Spring Boot):** track only lines within
  official OSS support (per `14`, currently 4.0.x and 4.1.x) — a line
  past its OSS-support end is treated as a security risk, not a stable
  choice, per the EOL evidence in
  `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md` §2.
- **Database (PostgreSQL):** track the current major version (18.x);
  never run a major version past its official fix-support end date (e.g.,
  PostgreSQL 14's November 12, 2026 end-of-fixes date, found during
  verification, is a concrete example of the kind of deadline this
  policy exists to track).
- **Frontend (Next.js, React Native):** track the current Active-LTS-
  equivalent line; React Native's own "latest 3 minor lines supported"
  policy is adopted as-is rather than ARGON inventing a stricter one.
- **Everything else:** default to "within the upstream project's own
  official support window," re-checked at each Technology Baseline
  Verification cycle (see Revisit Trigger below).

### Security Patch SLA
Exact numeric SLA (e.g., "critical CVEs patched within N business days")
is **UNKNOWN — REQUIRES a real decision from whoever owns this project's
operational capacity**; inventing a specific number here would violate
Zero Fabrication. The **process**, once that number is set, is:
1. Automated dependency/CVE scanning (SAST/dependency-scanning per `07`)
   flags a new advisory.
2. Severity triaged (Critical/High/Medium/Low) using the upstream
   project's own CVSS scoring.
3. Critical/High findings get prioritized ahead of any non-security
   roadmap work (`20`); a fix or mitigation ships through the normal
   Release workflow (`05` §12), potentially fast-tracked past a full wave
   sequence for a Critical finding with active exploitation evidence.
4. Every patch (security or otherwise) is logged, feeding
   `08-MASTER-COMPLIANCE-MAP.md`'s evidence trail where a compliance
   control depends on patch currency.

### Dependency Updates
- Patch-level updates: applied on a regular, non-disruptive cadence
  (automated PR + CI + fast review), consistent with `14`'s "patch
  versions are never frozen blindly" principle.
- Minor-level updates: reviewed against the changelog, applied within a
  normal sprint/release cycle.
- Major-level updates: treated as an architecture-affecting change,
  requiring the same compatibility-validation gate as any other Release
  workflow change (`05` §12) and, if the major version changes a
  documented target in `14`, a new ADR (`19`) rather than a silent bump.

### Breaking Upgrade Process
1. Identify the breaking change via the upstream changelog/migration
   guide.
2. Assess impact against the module boundaries in `03`/Spring Modulith
   (`14`) — a breaking change contained to one module is lower-risk than
   one crossing module boundaries.
3. Run the full contract-test suite (`15`) before merging.
4. Ship through canary → waves (`05` §12), never a direct 100% rollout.
5. Update the relevant `docs/master/` document and, if the decision
   itself changed (not just the version number), add an ADR (`19`).

### Rollback
Follows the Release Rollback workflow (`05` Tier 2) and the per-component
DR register (`17`) — a dependency upgrade rollback is not a special case,
it's a normal release rollback.

### Compatibility Testing
Owned by `15-MASTER-TESTING-STRATEGY.md`'s Contract test layer —
dependency upgrades are exactly the class of change contract tests exist
to catch before they reach a release wave.

### End-of-Life Monitoring
- Every dependency in `14`'s tables gets its official EOL/support-window
  date tracked (source: the vendor's own published policy — e.g., the
  PostgreSQL versioning policy, the Spring Boot OSS-support-window policy,
  Oracle's Java SE support roadmap, all cited with dates in
  `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`).
- A dependency approaching its EOL date within a defined lead time (exact
  lead time TBD — same Zero-Fabrication caveat as the Security Patch SLA
  above) triggers a scheduled upgrade task, not a reactive scramble.
- This tracking can be automated in the future via an EOL-tracking
  service/API (e.g., the kind of aggregator used during this
  verification pass) — TARGET, not yet implemented.

## Alternatives Considered
- **Freezing exact versions in the architecture documents themselves**
  (rejected) — this is precisely what `14`'s Managed Upgrade Policy
  already rejects; this document operationalizes that principle rather
  than reversing it.
- **Inventing a specific SLA number to look complete** (rejected) — would
  violate Zero Fabrication; an honest "REQUIRES a real decision" is
  preferred over a plausible-looking fake number, consistent with how
  `17`'s RPO/RTO targets were handled.

## Dependencies
Depends on `14`, `05` §12, `15`, `17`, `07`. Feeds
`docs/governance/ARCHITECTURE-STATUS.md` (EOL tracking becomes a status
input once implemented).

## Unknowns
UNKNOWN — the exact Security Patch SLA and EOL lead-time numbers, pending
a real operational-capacity decision. UNKNOWN — whether any automated
dependency-scanning or EOL-tracking tooling currently exists in any
environment for this project.

## Definition of Done
Every dependency named in `14-MASTER-TECHNOLOGY-STACK.md` has a
documented supported-version-window rule above (directly or via the
"everything else" default), and no dependency is left with an undefined
upgrade path.
