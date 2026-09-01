# Problem Definition, Objectives, and Scope

## 1. Problem Statement

The Training Nomination Workflow in modern organizations frequently relies on manual, fragmented coordination between employees, reviewers/managers, and training administrators. Training requests are submitted through ad-hoc communication channels (emails, physical forms, spreadsheets), supporting documents are exchanged separately, validation is performed manually, and approval decisions lack a single source of truth.

This fragmented process results in:
* Incomplete or invalid submissions
* Redundant and duplicated data entry
* Prolonged approval delays and bottlenecks
* Ambiguous ownership and lack of status visibility
* Limited auditability and inability to track nomination lifecycles

**NominaFlow** provides a centralized, web-based Training Nomination Workflow system enabling employees to discover trainings, submit nominations with verifiable data and documents, reviewers to approve or reject requests, and administrators to maintain end-to-end visibility.

---

## 2. Target Users & Responsibilities

| User Role | Responsibilities |
|---|---|
| **Employee / Nominee** | Creates and submits training nominations, uploads supporting documents, and tracks request lifecycle |
| **Reviewer / Manager** | Evaluates submitted nominations and supporting documents, approves or rejects with feedback |
| **Training Administrator** | Monitors global nomination pipeline, filters requests, inspects audit logs and workflow health |

---

## 3. Stakeholders

### Primary Stakeholders
1. Employees / Trainees
2. Reviewers / Department Managers
3. Training & HR Administrators

### Secondary & Technical Stakeholders
4. DevOps / IT Operations Team
5. Project Sponsor / Business Owner
6. Security & Compliance Officers
7. QA / Testing Engineers

---

## 4. Key Pain Points & Architectural Resolutions

| ID | Existing Pain Point | NominaFlow Architectural Resolution |
|---|---|---|
| **P1** | Fragmented Submission | Centralized web form with structured data fields |
| **P2** | Manual Validation | Automated server-side Pydantic and document validation |
| **P3** | Approval Delays | Dedicated reviewer queue with real-time status transitions |
| **P4** | Poor Status Visibility | Transparent self-service status tracking endpoint for nominees |
| **P5** | Duplicate Data Entry | Single relational database persistence model (PostgreSQL) |
| **P6** | Difficult Workflow Tracking | Administrative dashboards with status filtering |
| **P7** | Limited Auditability | Immutable `audit_events` logging for all workflow mutations |

---

## 5. MVP Objectives & Measurable Success Criteria

### Core Objectives
1. **Centralize Nomination Intake**: Provide a unified platform for creating and submitting training nominations.
2. **Automated Request Validation**: Enforce required field and document integrity prior to submission.
3. **Structured Review Mechanism**: Empower reviewers to inspect details, attachments, and record decisions.
4. **Lifecycle Status Transparency**: Provide real-time visibility across all nomination states.
5. **Comprehensive Traceability**: Persist immutable audit events with timestamps and actor identities.

### Measurable Engineering Targets

| Metric | Target |
|---|---:|
| Valid request submission completion | ≥ 95% of valid submissions |
| Required field validation rate | 100% of required fields validated |
| Invalid submission prevention | 100% of invalid payloads rejected |
| State transition accuracy | 100% compliant with state machine rules |
| Decision persistence | 100% of reviewer actions persisted with timestamps |
| Audit traceability | 100% of mutations generate unique audit entries |
| Automated test pass rate | ≥ 90% pass rate on test suites |
| Build reproducibility | 100% clean checkouts build and run locally |

---

## 6. Scope Boundaries

### In-Scope (15-Week MVP)
* Web application with Python + FastAPI backend
* Relational database persistence (PostgreSQL + SQLAlchemy + Alembic)
* Role-based access control (Employee, Reviewer, Administrator)
* Training nomination creation, draft saving, and submission
* File attachment upload, validation, and storage
* Reviewer queue with approve/reject workflows and comments
* Real-time nomination status tracking and administrative monitoring
* Immutable audit event logging
* Automated testing suite (Pytest) and CI/CD pipelines

### Out-of-Scope (Deferred to Post-MVP)
* Enterprise Learning Management System (LMS) course hosting and delivery
* Payment gateway and budget reimbursement processing
* Attendance tracking and certification generation
* AI-based candidate recommendation or document OCR
* Dynamic multi-level hierarchical approval chains
* Enterprise SSO / SAML integration
* Native iOS / Android mobile applications
