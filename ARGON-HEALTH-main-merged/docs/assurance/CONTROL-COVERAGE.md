# Control Coverage Map

**Starter baseline:** 67 controls. Every control begins `NOT_RUN`; counts below describe planned verification scope, not completed verification.

| Domain | Controls |
|---|---:|
| Architecture | 5 |
| Auditability | 1 |
| Build/SDLC | 1 |
| Clinical safety | 4 |
| Compliance | 1 |
| Data integrity | 5 |
| Governance | 9 |
| Incident response | 1 |
| Interoperability | 3 |
| Migration | 1 |
| Operations | 4 |
| Performance | 1 |
| Privacy | 5 |
| Release | 2 |
| Requirements | 1 |
| Resilience | 3 |
| Security | 11 |
| Supply chain | 1 |
| Testing | 5 |
| Usability | 3 |

| Earliest required gate | Controls due at this gate |
|---|---:|
| G0 | 8 |
| G1 | 18 |
| G2 | 15 |
| G3 | 13 |
| G4 | 7 |
| G5 | 6 |

## Coverage interpretation

- G0/G1 cover governance, scope, requirements, design, threat modeling, privacy, clinical safety, data invariants, and service objectives.
- G2 covers the implementation-quality evidence expected once application code exists.
- G3 covers staging/pilot safety, independent security assessment, clinical/privacy review, recovery, performance and migration rehearsals.
- G4 covers exact-build production authorization, operational readiness, and release sign-offs.
- G5 covers ongoing operational and evidence revalidation.

**Do not interpret the number of controls as proof of completeness.** Reconcile the set against ARGON’s actual domain/workflow map, current system behavior, intended use, launch jurisdiction, contracts, and actual risks. The assurance owner must add or retire controls with rationale and a review trail.
