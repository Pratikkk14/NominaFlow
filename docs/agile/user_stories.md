# Agile Epics, User Stories & Acceptance Criteria

## Epics Overview

| Epic ID | Epic Title | Description |
|---|---|---|
| **E1** | Authentication & RBAC | User credential management, session issuance, and role enforcement |
| **E2** | Nomination Submission | Nomination creation, draft editing, and submission workflows |
| **E3** | Validation & Documents | Field data validation, attachment upload, and size/type verification |
| **E4** | Reviewer Decision Workflow | Review queue, nomination evaluation, approve, and reject mechanisms |
| **E5** | Status Tracking | End-to-end status visibility and history viewing for employees |
| **E6** | Administration & Monitoring | Global nomination views, filtering, and system monitoring |
| **E7** | Audit & Traceability | Immutable audit logging of all lifecycle state transitions |
| **E8** | Automated Testing & QA | Pytest unit, integration, and workflow validation test suites |
| **E9** | CI/CD & Pipeline Automation | Automated build, linting, testing, and deployment workflows |
| **E10** | Operations & Documentation | Configuration management, logging, and technical documentation |

---

## User Stories & Acceptance Criteria

### Epic E1: Authentication & Role Management

#### US-01: User Login
* **As a** system user,
* **I want to** log in securely with my credentials,
* **So that** I can access functionality authorized for my role.
* **Acceptance Criteria:**
  - [x] Valid credentials authenticate successfully and return a secure JWT/session.
  - [x] Invalid credentials return HTTP 401 with a descriptive error.
  - [x] User role (`EMPLOYEE`, `REVIEWER`, `ADMIN`) is embedded in token context.
  - [x] Protected endpoints reject unauthenticated requests with HTTP 401.

#### US-02: Role-Based Access Control (RBAC)
* **As an** administrator,
* **I want** the system to enforce role-based permissions,
* **So that** users only access features permitted for their role.
* **Acceptance Criteria:**
  - [x] Employees can only access employee routes and their own nominations.
  - [x] Reviewers can access reviewer review queues.
  - [x] Admins have access to system-wide dashboards and logs.
  - [x] Cross-role unauthorized access attempts are blocked with HTTP 403.

---

### Epic E2: Training Nomination Submission

#### US-03: Create Draft Nomination
* **As an** employee,
* **I want to** create a training nomination and save it as a draft,
* **So that** I can populate information incrementally before submitting.
* **Acceptance Criteria:**
  - [x] Form captures title, provider, description, type, date, duration, cost, and justification.
  - [x] Initial nomination is assigned a unique UUID and set to `DRAFT` status.
  - [x] Draft nominations are only visible to the creating employee.

#### US-04: Submit Nomination
* **As an** employee,
* **I want to** formally submit my completed nomination,
* **So that** it enters the reviewer queue.
* **Acceptance Criteria:**
  - [x] Submission validates that all mandatory fields and required attachments are present.
  - [x] State transitions to `SUBMITTED`.
  - [x] Submission timestamp is recorded and audit event is emitted.

---

### Epic E3: Validation & Document Handling

#### US-05: Input Data Validation
* **As the** system,
* **I want to** validate all nomination fields against schema rules,
* **So that** malformed or incomplete data is rejected at the API boundary.
* **Acceptance Criteria:**
  - [x] Pydantic schemas validate types, string length bounds, and non-empty strings.
  - [x] Invalid dates (e.g., past dates for future trainings) are rejected.
  - [x] Validation errors return HTTP 422 with structured field error lists.

#### US-06: Upload Supporting Documents
* **As an** employee,
* **I want to** upload supporting documents (e.g., syllabus, invoice),
* **So that** reviewers have necessary context to evaluate my request.
* **Acceptance Criteria:**
  - [x] Supports PDF, PNG, and JPEG files up to 5 MB.
  - [x] Disallowed file types or oversize files are rejected with HTTP 400.
  - [x] File metadata is persisted in the `documents` table and linked to the nomination.

---

### Epic E4: Review & Decision Workflow

#### US-07: Reviewer Dashboard & Queue
* **As a** reviewer,
* **I want to** view a list of nominations pending review,
* **So that** I can prioritize and evaluate employee requests.
* **Acceptance Criteria:**
  - [x] Reviewer can query nominations in `SUBMITTED` or `UNDER_REVIEW` states.
  - [x] Complete details and document links are visible.

#### US-08: Approve Nomination
* **As a** reviewer,
* **I want to** approve a nomination,
* **So that** the employee is authorized to proceed with training.
* **Acceptance Criteria:**
  - [x] Reviewer can transition nomination from `UNDER_REVIEW` to `APPROVED`.
  - [x] Reviewer identity and decision timestamp are recorded.
  - [x] Emits `NOMINATION_APPROVED` audit event.

#### US-09: Reject Nomination
* **As a** reviewer,
* **I want to** reject an unsuitable nomination with a mandatory explanation,
* **So that** the employee understands why the request was not approved.
* **Acceptance Criteria:**
  - [x] Rejection requires a non-empty comment string.
  - [x] State transitions from `UNDER_REVIEW` to `REJECTED`.
  - [x] Emits `NOMINATION_REJECTED` audit event with comment persisted.

---

### Epic E5: Status Tracking & History

#### US-10: Track Nomination Status
* **As an** employee,
* **I want to** view the live status of all my submitted nominations,
* **So that** I can track progress without manual follow-up emails.
* **Acceptance Criteria:**
  - [x] Displays current state (`DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`).
  - [x] Shows reviewer feedback comments if rejected.

---

### Epic E6: Administration & Monitoring

#### US-11: Admin Overview & Filtering
* **As an** administrator,
* **I want to** view and filter all nominations across the organization,
* **So that** I have complete visibility into the training pipeline.
* **Acceptance Criteria:**
  - [x] Admin can list all nominations with pagination and status filters.
  - [x] Admin can view audit logs for compliance tracking.

---

### Epic E7: Audit Trail & Governance

#### US-12: Immutable Audit Event Logging
* **As a** compliance officer / administrator,
* **I want** every workflow state change recorded immutably,
* **So that** all decisions and actions are fully auditable.
* **Acceptance Criteria:**
  - [x] Events logged on creation, submission, review start, approval, and rejection.
  - [x] Logs include event UUID, nomination ID, actor ID, event type, and timestamp.
