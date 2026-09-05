# CONSOLIDATION DECISIONS

STATUS: PROPOSED
EVIDENCE CLASS: RUNTIME EVIDENCE (every decision below reflects an actual file present in one or both source repositories, verified by direct inspection on 2026-09-05)

## Purpose
Record what happened to every file that existed in either source
repository, so nothing disappears silently. Cross-reference with
`docs/audit/REPOSITORY-CONSOLIDATION-MATRIX.md` for the content-level
comparison behind each decision.

## Decision Log

| Source | Destination | Decision | Reason | Unique Content Preserved? |
|---|---|---|---|---|
| `system-ARGON-NEW:/ARGON-HEALTH-normalized (1)/docs/**` (43 files) | `ARGON-HEALTH:/docs/**` (canonical) | ADOPT AS BASE | Later commit (2026-09-04 vs 2026-08-28), strictly more complete on every checked axis, zero contradictions found | Yes — this IS the canonical tree |
| `ARGON-HEALTH:/ARGON-HEALTH-normalized/docs/master/{01,02,06,13,14,17,18,19,20}.md` and `MASTER-ARGON-BLUEPRINT.md` | *(superseded, not copied)* | DISCARD (superseded) | Each file's content is a strict subset of `system-ARGON-NEW`'s post-correction version (39→40 domains, R5→R4/R4B, RabbitMQ→Pub/Sub, Terraform→OpenTofu, cross-references repaired) | Yes — every A-only sentence in these files also appears, corrected, in the adopted B version; no content unique to A's version was found in any of these files |
| `ARGON-HEALTH:/ARGON-HEALTH-normalized/docs/master/{03,04,05,07,08,09,10,11,12,15,16}.md` | *(superseded, not copied — B's identical-or-superset versions used)* | DISCARD (superseded/tie) | 4 of these 11 are byte-identical between repos (05, 08, 10, 16); the remaining 7 are strict supersets in B (GAP-closure content) | Yes — identical files have no unique content by definition; superset files were confirmed to contain 100% of A's text plus additions |
| `ARGON-HEALTH:/docs/adr/ADR-016-MESSAGING-PLATFORM.md` | *(not copied — content already in canonical `19`)* | DELETE (duplicate) | Byte-for-byte identical to the ADR-016 entry already inside `docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md` in both repos; `system-ARGON-NEW` itself already dropped this standalone file for the same reason | Yes — full text lives on in `19` |
| `ARGON-HEALTH:/docs/adr/ADR-017-INFRASTRUCTURE-AS-CODE.md` | *(not copied — content already in canonical `19`)* | DELETE (duplicate) | Same reasoning as ADR-016 | Yes — full text lives on in `19` |
| `ARGON-HEALTH:/docs/adr/ADR-018-FHIR-PRODUCTION-BASELINE.md` | *(not copied — content already in canonical `19`)* | DELETE (duplicate) | Same reasoning as ADR-016 | Yes — full text lives on in `19` |
| `docs/adr/ADR-019-RECONCILIATION-WITH-ADR-000.md` (system-ARGON-NEW only) | `docs/adr/ADR-019-RECONCILIATION-WITH-ADR-000.md` | ADOPT (unique, material) | Resolves A's own README "Current Blocker #1"; single most important document in either repository for governance correctness | Yes — copied verbatim |
| `docs/adr/ADR-MESSAGING-PLATFORM.md` (byte-identical in both repos — a pre-normalization top-level file) | `docs/adr/ADR-MESSAGING-PLATFORM.md` | KEEP AS-IS | Identical in both sources; superseded in substance by ADR-016 (now folded into `19`) but kept per no-information-loss — deleting a named ADR file outright, rather than marking it superseded, was judged the higher-risk action | Yes — unchanged |
| `docs/audit/FINAL-GAP-REGISTER.md`, `FINAL-GAP-ANALYSIS.md`, `DO-NOT-BUILD-YET.md`, `CONTINUOUS-IMPROVEMENT-FINAL-REPORT.md` (system-ARGON-NEW only) | Same paths, unchanged | ADOPT (unique) | No equivalent exists anywhere in `ARGON-HEALTH`; these four documents are the entire substance of the GAP-001…013 closure work | Yes — copied verbatim |
| `docs/audit/FINAL-ARCHITECTURE-QUALITY-REPORT.md` (system-ARGON-NEW) | `docs/audit/FINAL-ARCHITECTURE-COMPLETENESS.md` | RENAME + ADOPT | Task's Section 14 requires this exact canonical filename; equivalent content already existed under a different name — renamed rather than duplicated, per the "merge existing, no unnecessary duplicates" rule | Yes — full content carried forward; 2 internal cross-references (`ARCHITECTURE-FREEZE.md`, `FINAL-GAP-REGISTER.md`) updated to the new filename |
| `docs/audit/IMPLEMENTATION-READINESS-REPORT.md` (system-ARGON-NEW, both top-level and `docs/audit/` copies — byte-identical to each other) | `docs/audit/FINAL-IMPLEMENTATION-READINESS.md` | RENAME + ADOPT (de-duplicated) | Same reasoning as above; the top-level and `docs/audit/` copies were already identical duplicates of each other even before consolidation, so only one survives | Yes — full content carried forward; 3 internal cross-references (`19`, `FINAL-GAP-ANALYSIS.md`, `FINAL-GAP-REGISTER.md`) updated |
| `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` (both repos, differ only in the 39/40 domain-count line) | `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` (B's version) | ADOPT (B's version, minor correction) | Single-line difference is the same stale-reference issue tracked everywhere else in this log | Yes — the only difference (a stale number) is not "content," it's the error being corrected |
| `docs/governance/ARCHITECTURE-FREEZE.md`, `FINAL-GATE-CONTINUOUS-IMPROVEMENT.md` (system-ARGON-NEW only) | Same paths, unchanged | ADOPT (unique) | No equivalent in `ARGON-HEALTH` | Yes — copied verbatim |
| `docs/governance/{ARCHITECTURE-LINT-RULES, ARCHITECTURE-STATUS, ARGON-SOURCE-OF-TRUTH, FINAL-GATE, PERFORMANCE-GOVERNANCE, TECHNOLOGY-BASELINE, TRACEABILITY-MATRIX, VERSION-MANAGEMENT-POLICY}.md` | Same paths, B's versions | ADOPT (B's version — superset or corrected) | `ARCHITECTURE-LINT-RULES.md` gains Rule L15 in B; others differ only in domain-count/ADR-019 cross-references | Yes — every A-only sentence confirmed present in B's version |
| `README.md` (both repos, plus `README (3).md` duplicate in A) | `README.md` (B's version, updated during this consolidation) | ADOPT + UPDATE | B's README already reflects ADR-019's resolution; A's `README (3).md` is an unlabeled duplicate with no unique content found | Yes — nothing unique found in the discarded duplicate |
| `ARGON-HEALTH:/*.md` top-level loose files (20 files: `01…20-MASTER-*.md` with `" (1)"` suffixes, `MASTER-ARGON-BLUEPRINT (1).md`, `TECHNOLOGY-BASELINE*.md`, `COMPLIANCE-TRACEABILITY-MATRIX.md`, `INTEROPERABILITY-GOVERNANCE.md`, `FINAL-GATE.md`, `FINAL-NORMALIZATION-REPORT.md`, `ADR-MESSAGING-PLATFORM.md`) | *(not copied)* | DELETE (pre-push delivery duplicates) | `APPLY-INSTRUCTIONS.md` confirms these are the un-applied flat/hybrid state the prior pass tried and failed to push to `origin/main` (no credentials); content is 100% duplicated inside `ARGON-HEALTH-normalized/docs/` | Yes — every one of these files has a verified-identical or superseded counterpart already accounted for above |
| `ARGON-HEALTH:/ARGON-HEALTH-normalized.bundle`, `/ARGON-HEALTH-normalized.zip`, `/argon-normalization.bundle`, `/normalization.patch`, `/APPLY-INSTRUCTIONS.md` | *(not copied)* | DELETE (delivery mechanism, not content) | These are packaging artifacts for pushing A's normalization to `origin/main` — a step this consolidation performs directly by producing the canonical tree, making the delivery mechanism moot | No unique content — verified these are re-encodings of files already accounted for above, not independent content |
| `ARGON-HEALTH-normalized/docs/master/~$-MASTER-SYSTEM-ARCHITECTURE.md` | *(not copied)* | DELETE (Office lock file) | Zero-content artifact (a `~$`-prefixed Word/Office lock file accidentally committed), not a document | None — confirmed empty/non-document by file type |
| `system-ARGON-NEW:/*.md` top-level loose files (`DO-NOT-BUILD-YET.md`, `FINAL-GAP-REGISTER.md`, `IMPLEMENTATION-READINESS-REPORT.md`) | *(not copied — already adopted from `docs/audit/` path above)* | DELETE (duplicate) | Byte-identical to their `docs/audit/` counterparts, already adopted | Yes — accounted for under their `docs/audit/` entries above |
| New: `docs/audit/REPOSITORY-CONSOLIDATION-MATRIX.md` | Same path | CREATE (new) | Required by Section 3 of the consolidation task; did not exist in either source | N/A — new document |
| New: `docs/audit/CONSOLIDATION-DECISIONS.md` (this file) | Same path | CREATE (new) | Required by Section 6 of the consolidation task | N/A — new document |
| New: `docs/audit/LEGACY-VS-TARGET-BOUNDARY.md`, `LEGACY-TO-TARGET-MAPPING.md`, `LEGACY-LESSONS-AND-REQUIREMENTS.md` | Same paths | CREATE (new) | Required by Section 14; neither repository describes LEGACY ARGON at all — content sourced from the `argon-governance` and `argon-platform-target-architecture` skill files, with explicit UNKNOWNs where those sources are silent | N/A — new synthesis documents, sourced and cited, not fabricated |
| New: `docs/governance/ARCHITECTURE-CHANGE-RULES.md`, `DECISION-AUTHORITY.md` | Same paths | CREATE (new) | Required by Section 15; neither existed, and both governance gaps ("who approves" / "what's the process for a rename-only pass") were open items in every prior pass's own reports | N/A — new documents |

## Files With No Decision Required
`docs/MASTER-ARGON-BLUEPRINT.md`, `docs/compliance/COMPLIANCE-TRACEABILITY-MATRIX.md`,
`docs/evidence/TECHNOLOGY-BASELINE-VERIFICATION.md`,
`docs/interoperability/INTEROPERABILITY-GOVERNANCE.md`: present in both
repositories with no content-affecting differences beyond the
domain-count/ADR-019 cross-references already logged above under their
respective governance-doc rows. B's copy adopted for tree consistency.

## Verification
Every file present in either source repository's `find` output appears
in exactly one row above, either as ADOPTED, RENAMED, or DELETED with a
stated reason. No file was silently omitted from this log.
