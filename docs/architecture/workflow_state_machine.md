# Workflow State Machine & Lifecycle Model

## 1. State Transition Diagram

The nomination lifecycle is strictly governed by a deterministic Finite State Machine (FSM). State mutations are validated at the service layer before any database commit.

```text
       ┌──────────┐
       │  (Init)  │
       └────┬─────┘
            │ create()
            ▼
       ┌──────────┐
  ┌───►│  DRAFT   │
  │    └────┬─────┘
  │ edit()  │ submit()
  └─────────┘
            ▼
       ┌──────────┐
       │SUBMITTED │
       └────┬─────┘
            │ start_review()
            ▼
      ┌────────────┐
      │UNDER_REVIEW│
      └─────┬──────┘
            │
      ┌─────┴──────────────┐
      │ approve()          │ reject() (requires comment)
      ▼                    ▼
┌───────────┐        ┌───────────┐
│ APPROVED  │        │ REJECTED  │
└───────────┘        └───────────┘
```

---

## 2. State Definitions & Invariants

| State | Allowed Transitions | Permitted Actor | Preconditions & Invariants |
|---|---|---|---|
| `DRAFT` | `SUBMITTED` | Employee (Owner) | Incomplete or unsubmitted. Can be freely edited. Cannot be seen by Reviewers. |
| `SUBMITTED` | `UNDER_REVIEW` | Reviewer | All required fields and documents must be present. Locked from employee modification. |
| `UNDER_REVIEW` | `APPROVED`, `REJECTED` | Reviewer | Active review underway. Decision controls enabled for assigned reviewer. |
| `APPROVED` | *(Terminal)* | System / Reviewer | Approved state. Locked permanently. Audit record created with timestamp. |
| `REJECTED` | *(Terminal)* | System / Reviewer | Rejection requires non-empty feedback comment. Audit record created. |

---

## 3. Disallowed Transitions

Any attempt to execute an invalid transition results in a HTTP 400 Bad Request error from the state machine validator:
* `DRAFT` -> `APPROVED` (Direct approval without submission is prohibited)
* `SUBMITTED` -> `APPROVED` (Review must be initiated first)
* `APPROVED` -> `REJECTED` (Terminal states are immutable in MVP)
* `REJECTED` -> `APPROVED` (Terminal states are immutable in MVP)
* `APPROVED` -> `DRAFT` (Resubmission workflow is outside initial MVP scope)
