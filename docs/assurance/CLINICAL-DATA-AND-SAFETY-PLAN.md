# Clinical Data Integrity and Safety Assurance Plan

**Status: PROPOSED.** Applicable depth depends on intended use and product classification. A qualified clinical safety lead and local regulatory/legal specialists must determine applicability; this document does not classify the product or certify compliance.

Map hazards and test evidence to the [verification matrix](VERIFICATION-MATRIX.csv) and [risk register](RISK-REGISTER.csv); record completed runs in the [evidence register](EVIDENCE-REGISTER.csv).

## 1. Clinical-safety envelope

For every intended clinical workflow, specify: user/patient population, clinical purpose, inputs, outputs, decisions influenced, known limitations, foreseeable misuse, failure consequences, human oversight, downtime procedure, and prohibited reliance. Distinguish administrative software from any function that may qualify as medical-device software or clinical decision support under applicable law.

## 2. Hazard analysis

Maintain a hazard log linked to verification control IDs. For each hazard record: hazard ID; hazardous situation; foreseeable sequence of events; harm; severity; likelihood/exposure assumptions; risk owner; controls; verification evidence; residual risk; decision authority; and reassessment trigger. Avoid fake precision: state uncertainty and evidence gaps. Do not treat a low numeric score as permission to accept a severe hazard.

Start by considering at least these scenario classes where the associated feature is in scope:

- wrong-patient or duplicate-identity association;
- stale, missing, mislabelled, or incorrectly unit-converted observations/results;
- allergy/medication reconciliation omissions or incorrect patient context;
- wrong dose/route/frequency or unintended prescription change (if prescribing is in scope);
- delayed/duplicate/misrouted lab or imaging result;
- silent overwrite or loss of clinical note/result during concurrent edits;
- timezone/date-boundary errors affecting scheduling or interpretation;
- misleading status, stale cache, or partial workflow presented as complete;
- alert suppression, alert fatigue, or unsafe default values;
- downtime/restore causing missing, duplicated, or out-of-order records;
- unauthorized change to a clinical record without attributable audit trail;
- a language, accessibility, or workflow ambiguity causing operator error.

## 3. Data integrity invariants

Define and test, as applicable:

- stable patient identity and governed merge/unmerge workflow;
- provenance (who/what/when/source) for clinical facts;
- units, precision, reference ranges, status, and timestamps preserved through transformations;
- signed/finalized records cannot be silently overwritten; corrections are additive, attributed, and auditable;
- concurrent updates have an explicit conflict policy and cannot silently drop clinically material information;
- duplicate/replayed integration messages do not create duplicate orders/results/charges;
- cancelled/retracted/amended results remain distinguishable from current results;
- relationships among patient, encounter, order, result, author, facility, and time are validated;
- migrated record counts/checksums and critical-field reconciliation meet pre-approved criteria.

## 4. Human factors and clinical review

Use representative clinicians/staff to test end-to-end tasks, interruptions, error recovery, accessibility, language, and high-pressure conditions. Capture task success, time, error type, near misses, comprehension of statuses/alerts, and observed workarounds. Have clinical experts review test cases and unexpected behaviours; generic software QA cannot alone sign off clinical semantics.

## 5. Clinical release conditions

Before a clinical workflow is enabled for real users: hazards are documented; controls are implemented and tested; residual risks have accountable review; downtime and correction workflows are trained; traceability ties safety requirements to test evidence; unresolved unacceptable hazards block release; and post-release incident capture/escalation is active.

If a function is not in scope (e.g. no prescribing or decision support), record why and who confirmed non-applicability. Reassess when the feature set or marketing/labelled intended use changes.
