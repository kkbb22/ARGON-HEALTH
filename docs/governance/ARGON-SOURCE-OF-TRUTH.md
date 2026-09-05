# ARGON SOURCE OF TRUTH

STATUS: PROPOSED
EVIDENCE CLASS: DESIGN

## Status
GOVERNANCE RECORD. Dated 2026-08-27.

## Purpose
Define which artifact wins when two sources of information about ARGON
disagree — so no future contributor (human or AI agent) has to guess, and
so chat/conversation history can never outrank the repository's own
governed documentation.

## Precedence Order
```
1. Executable evidence
      (passing tests, deployed and verified infrastructure, a signed
       conformance-test result, a restore drill that actually passed)
2. Approved ADR
      (docs/master/19-MASTER-ARCHITECTURAL-DECISIONS.md entries with
       Status: APPROVED or APPROVED WITH CONDITIONS — never PROPOSED)
3. Master Architecture
      (docs/master/01–20 and docs/MASTER-ARGON-BLUEPRINT.md)
4. Detailed design
      (any future docs/adr/, docs/security/, docs/compliance/,
       docs/interoperability/, docs/workflows/ document not yet promoted
       into the master set)
5. Informational documentation
      (docs/evidence/, docs/audit/, README files, code comments)
6. Conversation / history
      (chat transcripts, prior AI-assisted consultations, verbal
       decisions not yet written into any governed document)
```

## Rules
- **A lower-precedence source never overrides a higher one.** If a chat
  conversation states a technology decision that conflicts with an
  Approved ADR, the ADR wins until a new ADR supersedes it — the chat
  statement is not itself authority, no matter how recent or how
  confidently stated.
- **PROPOSED is not APPROVED.** Every ADR in `19` created in the
  2026-08-27 Architecture Normalization pass (ADR-016, ADR-017, ADR-018)
  is Level 2 *only once* a real decision authority moves its status from
  PROPOSED to APPROVED — until then, it sits at the precedence of the
  document that proposed it (effectively Level 3, since it lives inside
  the Master Architecture set) and is clearly marked PROPOSED wherever
  referenced.
- **Executable evidence beats documentation when they conflict.** If a
  test suite or a production system demonstrably behaves differently
  from what a master document claims, the documentation is wrong and
  must be corrected — the code/evidence is not wrong by default.
- **No claim skips levels.** A statement made only in conversation cannot
  be treated as equivalent to an Approved ADR just because it sounds
  final — it must be written into a governed document and go through
  that document's own review path first.
- **Conflicts between documents at the same level** are resolved by
  running (or re-running) `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md`,
  not by informal judgment call in a single conversation.

## Applicability to AI Agents Specifically
Any AI agent (this one or a future one) working on this repository must
treat this precedence order as binding on itself: an instruction given in
a chat session that contradicts an Approved ADR or the Master Architecture
is not sufficient grounds to change governed documentation without
following the same ADR process every other change follows. A chat
instruction CAN propose a new ADR (as this pass did — see ADR-016/017/018)
but cannot self-approve it.

## Alternatives Considered
- **Documentation-always-wins** (rejected) — would let a stale document
  override a passing test or a real production incident, which is
  backwards; executable evidence is deliberately ranked highest.
- **No formal precedence, resolve case by case** (rejected) — this is
  exactly the ambiguity that let FHIR-version and messaging-technology
  claims go unverified for an entire prior pass (see
  `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md` Finding 3).

## Dependencies
Referenced by every document in `docs/master/`, `docs/governance/`, and
by `docs/audit/ARCHITECTURE-CONSISTENCY-AUDIT.md`.

## Definition of Done
Every future ADR, design document, or status update names its own
precedence level explicitly (or is unambiguous from its location in this
directory structure), so no contributor has to ask "which document wins"
again.
