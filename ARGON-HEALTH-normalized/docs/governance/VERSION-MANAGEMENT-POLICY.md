# Version Management Policy

**STATUS:** ACTIVE (governance policy)
**EVIDENCE CLASS:** DESIGN

## Purpose
Define how ARGON tracks, patches, upgrades, and eventually retires the
technology versions named in `docs/master/14-MASTER-TECHNOLOGY-STACK.md`,
so "the architecture says Java 25" never quietly becomes "the codebase
is pinned to whatever Java 25 patch happened to be current the day
someone ran an install command."

## Core Rule
**Architecture documents specify a baseline; implementation pins an
exact version.** `docs/master/14` may say "Java 25 LTS" or "Spring Boot
4.1.x" — that is a target, not a build-file value. The first time actual
code exists, a `build.gradle`/`package.json`/lockfile pins an exact
version (e.g., `25.0.3`, `4.1.1`), and **that pin, not the architecture
document, is what a build actually uses.**

**"latest" is never a production dependency version.** Every pin is
exact, every time, everywhere a version is written into a build/deploy
artifact.

## Supported Versions
| Layer | Supported line | Notes |
|---|---|---|
| Java | Current LTS per `14` (Java 25 as of this pass) | Track Oracle/OpenJDK LTS release cadence; move to next LTS before the current one's free-patch window (NFTC) closes |
| Spring Boot / Framework | Current major.minor per `14` | Move within 1 minor version of latest within a normal release cycle |
| PostgreSQL | Current major per `14` | Track major-version EOL; plan the next major upgrade before EOL, not at it |
| Frontend (Next.js, React Native) | Current major per `14` | Frontend deps track faster; patch continuously, evaluate major bumps quarterly |
| IaC (OpenTofu) | Current stable | Track state-format compatibility notes on every upgrade |

## Patch Policy
- **Security patches:** applied on the vendor's release cadence, not
  batched with feature work. A security patch is never delayed to "the
  next planned release" once a fix is available and verified compatible.
- **Routine patches:** batched on a regular cadence (recommended:
  monthly), verified against the existing test suite before promotion.

## Upgrade Windows
- **Minor/patch upgrades:** go through the same compatibility-validation
  step as any other release (`docs/master/05` §12 Release workflow —
  canary → staged wave rollout).
- **Major upgrades:** require an explicit compatibility-validation pass
  plus a rollback plan before starting, consistent with
  `docs/master/17-MASTER-DISASTER-RECOVERY.md`'s restore-test discipline
  applied to code, not just data.

## Dependency Update Automation
Not yet implemented — no codebase exists. Recommended for Foundation
Implementation: automated dependency-update tooling (e.g., Renovate or
Dependabot) configured to open patch/security updates automatically and
gate minor/major updates behind the compatibility-validation step above.
Marked here as a Foundation Implementation requirement, not fabricated
as already running.

## Breaking-Change Procedure
1. Identify the breaking change and its blast radius (which modules/
   domains from `docs/master/03` are affected).
2. File or update an ADR if the change alters a platform-wide decision
   (see `docs/governance/ARGON-SOURCE-OF-TRUTH.md` §6).
3. Run compatibility validation in an isolated environment before any
   production-adjacent rollout, per `argon-governance` skill's core
   principle of isolated-project testing.
4. Roll out via the staged wave pattern (`docs/master/05` Release Flow),
   never a single-shot deploy, once real production traffic exists.

## Compatibility Testing
Every version bump — patch or major — runs the existing automated test
pyramid (`docs/master/15-MASTER-TESTING-STRATEGY.md`) before promotion.
No version bump ships on the assumption that "it's just a patch."

## Rollback
Every upgrade has a stated rollback path before it starts, consistent
with the pre-deploy checklist in the `argon-governance` skill
(`references/no-breaking-changes.md`): "rollback plan written down
before deploy" is not optional.

## EOL Monitoring
No automated EOL monitoring exists yet (no codebase to monitor).
Recommended for Foundation Implementation: a recurring check (manual or
automated) against each pinned dependency's published EOL/support
timeline, feeding back into `docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`
on roughly the same 3–6 month cadence recommended there.
