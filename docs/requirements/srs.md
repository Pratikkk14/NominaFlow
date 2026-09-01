# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
This document provides the formal Software Requirements Specification (SRS) for the **NominaFlow Training Nomination Workflow**. It defines the functional and non-functional requirements governing system behavior, interfaces, and constraints.

### 1.2 Scope
NominaFlow is a centralized web application enabling employees to submit training nominations, system validation of required inputs and attachments, reviewer approval/rejection workflows, and comprehensive audit trail maintenance.

---

## 2. Functional Requirements (FR)

### FR-01: Authentication
* The system shall authenticate users with unique username/email and password credentials.
* The system shall issue secure tokens/sessions upon successful authentication.
* The system shall reject invalid authentication attempts with standard error responses.
* The system shall provide a logout mechanism terminating the active session.

### FR-02: Role-Based Authorization
* The system shall support three distinct roles: `Employee`, `Reviewer`, `Administrator`.
* The system shall enforce role-based access control (RBAC) on all protected API endpoints.
* Unauthorized access attempts shall be denied with HTTP 403 Forbidden.

### FR-03: Training Nomination Creation
* An employee shall be able to create a training nomination specifying:
  * Training Title (required)
  * Training Provider / Institution (required)
  * Training Description (required)
  * Training Type (e.g., Technical, Leadership, Compliance)
  * Proposed Training Date (valid future date)
  * Training Duration (e.g., hours/days)
  * Estimated Cost (numeric)
  * Business Justification (required)
* The system shall assign a unique UUID upon initial creation.

### FR-04: Draft Nomination Management
* An employee shall be able to save an incomplete nomination in `DRAFT` status.
* Draft nominations shall remain private to the author and shall not enter the review queue.
* The employee shall be able to update draft fields prior to submission.

### FR-05: Input & Data Validation
* The system shall validate all input payloads using Pydantic schemas.
* Required fields, data types, string length bounds, and date formats must be strictly enforced.
* Non-compliant submissions shall be rejected with structured validation errors (HTTP 422).

### FR-06: Supporting Document Upload & Validation
* An employee shall be able to attach supporting documents (e.g., syllabus, vendor quotes) to a nomination.
* Allowed MIME types: PDF, PNG, JPEG.
* Maximum file size: 5 MB per attachment.
* The system shall store file metadata in PostgreSQL and file contents in the configured storage layer.

### FR-07: Nomination Submission
* An employee shall be able to submit a valid draft nomination.
* Upon submission, the workflow state shall transition from `DRAFT` to `SUBMITTED`.
* The system shall record the submission timestamp and generate an initial submission audit event.

### FR-08: Reviewer Dashboard & Queue
* A reviewer shall be able to retrieve a paginated queue of nominations in `SUBMITTED` or `UNDER_REVIEW` status.
* The reviewer shall be able to view complete nomination details, author info, and attached documents.

### FR-09: Review Lifecycle Initiation
* When a reviewer begins reviewing a nomination, the state shall transition from `SUBMITTED` to `UNDER_REVIEW`.
* The reviewer ID and timestamp shall be associated with the review session.

### FR-10: Nomination Approval
* A reviewer shall be able to approve a nomination in `UNDER_REVIEW` status.
* The workflow state shall transition to `APPROVED`.
* The decision timestamp and reviewer identity shall be permanently recorded.

### FR-11: Nomination Rejection
* A reviewer shall be able to reject a nomination in `UNDER_REVIEW` status.
* The reviewer must provide a mandatory rejection comment explaining the rationale.
* The workflow state shall transition to `REJECTED`.

### FR-12: Status Tracking for Nominees
* Employees shall be able to view the real-time status and timeline of their own nominations.
* Read-only visibility shall be provided for reviewer decisions and comments once rendered.

### FR-13: Administrator Monitoring & Filtering
* Administrators shall have system-wide visibility over all nominations.
* The system shall allow filtering nominations by status, date range, department, or employee.

### FR-14: Immutable Audit Trail
* The system shall record audit events for every critical lifecycle transition:
  * `NOMINATION_CREATED`
  * `NOMINATION_SUBMITTED`
  * `REVIEW_STARTED`
  * `NOMINATION_APPROVED`
  * `NOMINATION_REJECTED`
* Audit records must contain: Event ID, Nomination ID, Actor User ID, Event Type, Timestamp, and Metadata/Comments.

---

## 3. Non-Functional Requirements (NFR)

### NFR-01: Security
* Passwords must be hashed using industry-standard hashing (bcrypt/argon2).
* API authentication must use secure tokens (JWT/Bearer tokens).
* Input sanitization and parameterized queries (via SQLAlchemy) to prevent SQL injection.
* No secrets, API keys, or database credentials committed to version control.

### NFR-02: Workflow Reliability & Invariants
* State transitions must follow the formal finite state machine. Invalid transitions (e.g., modifying an `APPROVED` record to `REJECTED`) must be strictly blocked.
* Database operations affecting state and audit logs must execute within atomic transactions.

### NFR-03: Maintainability & Modularity
* Architecture must follow a clean layered modular monolith (API -> Service -> Data Access -> Database).
* Code must conform to PEP 8 standards with modular package organization.

### NFR-04: Testability
* Business logic, validators, and state machines must be decoupled from HTTP transport for isolated unit testing.
* Minimum target of ≥ 85% code coverage for core workflow services.

### NFR-05: Performance
* Standard REST API endpoints must respond in < 200 ms under baseline local/test load.
* Foreign keys and frequently queried status fields must be indexed in PostgreSQL.

### NFR-06: Deployability & Portability
* The application must run predictably across environments via containerization (Docker) and standard Python virtual environments.
* Configuration must follow 12-Factor principles via environment variables.

### NFR-07: Observability & Logging
* Structured logging must capture application startup, database connection events, authorization failures, and workflow state transitions.
