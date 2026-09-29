# NominaFlow — Technical Architecture & Operational Guide

> **Centralized Training Nomination Workflow Management System**  
> *A comprehensive, end-to-end guide detailing system architecture, data models, finite state machine, user portals, REST API contracts, test suites, and DevOps automation.*

---

## 📑 Table of Contents

1. [Executive Summary & Problem Statement](#-1-executive-summary--problem-statement)
2. [High-Level System Architecture](#-2-high-level-system-architecture)
3. [Finite State Machine & Workflow Lifecycle](#-3-finite-state-machine--workflow-lifecycle)
4. [User Personas & Web Portal Walkthrough](#-4-user-personas--web-portal-walkthrough)
   - [4.1 Authentication & 1-Click Login](#41-authentication--1-click-login)
   - [4.2 Employee Portal (Drafts & Attachments)](#42-employee-portal-drafts--attachments)
   - [4.3 Reviewer Portal (Evaluation & Decisions)](#43-reviewer-portal-evaluation--decisions)
   - [4.4 Administrator Dashboard (Metrics & Audit Trail)](#44-administrator-dashboard-metrics--audit-trail)
5. [Database Architecture & Data Models](#-5-database-architecture--data-models)
6. [Security, Auth & Role-Based Access Control (RBAC)](#-6-security-auth--role-based-access-control-rbac)
7. [REST API Specifications](#-7-rest-api-specifications)
8. [Zero-Setup Local Quickstart](#-8-zero-setup-local-quickstart)
9. [Automated Testing & Quality Gates](#-9-automated-testing--quality-gates)
10. [DevOps Lifecycle & CI/CD Pipeline](#-10-devops-lifecycle--cicd-pipeline)
11. [Project Documentation & Deliverables Map](#-11-project-documentation--deliverables-map)

---

## 📌 1. Executive Summary & Problem Statement

### 1.1 The Problem
In many corporate and institutional environments, employee training nomination workflows are conducted through disconnected channels — email threads, unstructured spreadsheet trackers, and ad-hoc paper forms. This legacy approach leads to:
* **Nomination Duplication**: Multiple employees submitting identical requests without visibility.
* **Missing Information & Documents**: Incomplete training syllabi, cost details, or business justifications submitted.
* **Reviewer Bottlenecks**: Approvers overwhelmed by email requests with no centralized queue or status audit trail.
* **Lack of Transparency**: Employees left unaware of where their nomination stands in the approval pipeline.
* **Compliance & Audit Deficits**: Inability to verify who approved or rejected a nomination, when, and with what rationale.

### 1.2 The NominaFlow Solution
**NominaFlow** is a modular, event-driven web application built with **Python 3.12+**, **FastAPI**, **SQLAlchemy**, and **Jinja2**. It centralizes the complete nomination lifecycle into a single digital platform:
1. **Interactive Draft Form**: Employees draft nominations using clean, standard HTML form text inputs and textareas with incremental draft saving.
2. **Document Attachments**: Secure multi-part attachment uploading (PDF, PNG, JPEG) with strict file size (<5MB) and MIME-type validation.
3. **Deterministic State Machine**: Enforces strict transitions (`DRAFT` ➔ `SUBMITTED` ➔ `UNDER_REVIEW` ➔ `APPROVED` / `REJECTED`) preventing invalid workflow skips.
4. **Dedicated Review Queue**: Reviewers inspect course details, examine attachments, and make approve/reject decisions with mandatory feedback comments.
5. **Real-Time Governance & Audit**: Administrators monitor organization-wide metrics, filter nominations by status, and inspect an immutable audit log.

---

## 🏗️ 2. High-Level System Architecture

NominaFlow is engineered as a clean 3-tier architecture with modular separation of concerns:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRESENTATION LAYER (UI)                           │
│   Jinja2 Server-Rendered Portals + Vanilla CSS + Interactive JavaScript     │
│   [/login]              [/employee]            [/reviewer]       [/admin]   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / REST / Cookies / JSON
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER (FastAPI)                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ API Routers: /auth  /nominations  /documents  /reviewer  /admin       │  │
│  └──────────────────────────────────┬────────────────────────────────────┘  │
│                                     │                                       │
│  ┌──────────────────────────────────▼────────────────────────────────────┐  │
│  │ Core Services:                                                        │  │
│  │  • State Machine (FSM validation & transition enforcement)            │  │
│  │  • Nomination Service (CRUD, submission, business validation)         │  │
│  │  • Document Service (Multipart storage, MIME/size verification)       │  │
│  │  • Security Engine (Direct Bcrypt hashing, JWT issuance/validation)   │  │
│  │  • RBAC Engine (Role dependencies: EMPLOYEE, REVIEWER, ADMIN)         │  │
│  └──────────────────────────────────┬────────────────────────────────────┘  │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │ SQLAlchemy ORM Engine
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PERSISTENCE LAYER (DB)                            │
│   Dual-Engine Database Layer with Auto-Seeding:                              │
│   • Development/Demo: SQLite (Zero-setup 'nominaflow.db' auto-generated)   │
│   • Production: PostgreSQL (Seamlessly switched via DATABASE_URL)           │
│   • Entities: Users | Roles | Nominations | Documents | AuditEvents         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Architectural Highlights:
* **Zero-Setup Execution**: Automatically initializes SQLite database with all tables and seeds 3 demo personas on startup.
* **Direct Bcrypt Hashing**: Directly utilizes standard `bcrypt` algorithms (`hashpw`/`checkpw`), preventing passlib 72-byte wrap bugs.
* **Dual Auth Context**: Supports both Authorization Bearer JWT headers (for REST clients) and HTTP-only cookie-based sessions (for browser UI).
* **Deterministic FSM**: State transitions are isolated in `state_machine.py` and strictly validated before database commits.

---

## 🔄 3. Finite State Machine & Workflow Lifecycle

All nominations follow a strict, deterministic Finite State Machine (FSM). Any invalid transition attempt raises an `HTTP 400 Bad Request`.

```text
       ┌──────────────┐
       │   (Start)    │
       └──────┬───────┘
              │ create_nomination()  [Actor: EMPLOYEE]
              ▼
       ┌──────────────┐
  ┌───►│    DRAFT     │◄──── (Editable text boxes, attach syllabi)
  │    └──────┬───────┘
  │ edit()    │ submit_nomination()  [Actor: EMPLOYEE]
  └───────────┘
              ▼
       ┌──────────────┐
       │  SUBMITTED   │◄──── (Locked from employee editing; enters reviewer queue)
       └──────┬───────┘
              │ start_review()  [Actor: REVIEWER]
              ▼
       ┌──────────────┐
       │ UNDER_REVIEW │◄──── (Reviewer actively assessing syllabus & justification)
       └──────┬───────┘
              │
       ┌──────┴──────────────────────────┐
       │ approve()                       │ reject(comment)
       │ [Actor: REVIEWER]               │ [Actor: REVIEWER]
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│   APPROVED   │                  │   REJECTED   │
│  (Terminal)  │                  │  (Terminal)  │
└──────────────┘                  └──────────────┘
```

### State Dictionary & Transition Rules:

| State | Who Can Act | Allowed Actions | Next State | Notes / Invariants |
|---|---|---|---|---|
| **`DRAFT`** | `EMPLOYEE` (Owner) | Edit fields, upload files, submit | `DRAFT`, `SUBMITTED` | Only the creator can modify draft fields. |
| **`SUBMITTED`** | `REVIEWER` | Start Review | `UNDER_REVIEW` | Enters reviewer queue. Employee cannot edit fields. |
| **`UNDER_REVIEW`** | `REVIEWER` | Approve, Reject (with comment) | `APPROVED`, `REJECTED` | Rejection strictly requires non-empty feedback string. |
| **`APPROVED`** | *None (Terminal)* | View only | *None* | Final state. Generates audit record with reviewer ID. |
| **`REJECTED`** | *None (Terminal)* | View only | *None* | Final state. Rejection reason is visible to employee. |

---

## 👥 4. User Personas & Web Portal Walkthrough

### 4.1 Authentication & 1-Click Login
* **URL**: `http://localhost:8000/login`
* **Features**:
  * Clean credentials form supporting email and password login.
  * **1-Click Quick Login Buttons**: Instant login cards for Alex Mercer (`EMPLOYEE`), Sarah Jenkins (`REVIEWER`), and Admin User (`ADMIN`) for frictionless demonstration.

| Persona | Role | Email | Password | Primary Duties |
|---|---|---|---|---|
| **Alex Mercer** | `EMPLOYEE` | `employee@nominaflow.com` | `password123` | Create draft nominations, upload syllabi, submit, track progress |
| **Sarah Jenkins** | `REVIEWER` | `reviewer@nominaflow.com` | `password123` | Evaluate submissions, inspect attachments, approve or reject |
| **Admin User** | `ADMIN` | `admin@nominaflow.com` | `password123` | Pipeline monitoring, status filter queries, immutable audit logs |

---

### 4.2 Employee Portal (Drafts & Attachments)
* **URL**: `http://localhost:8000/employee`
* **Features**:
  * **Structured Form Text Inputs**: Fill in Training Program Title, Provider Name, Training Category (Technical, Leadership, Compliance, Domain Specific, Soft Skills), Start Date, Duration (Hours), and Estimated Cost (USD/INR).
  * **Textarea Inputs**: Extensive textareas for Program Syllabus / Description and Business Justification.
  * **Incremental Saving**:
    * **"Save as Draft"**: Persists current form state as `DRAFT` without triggering validation errors for incomplete fields.
    * **"Save & Submit for Review"**: Runs complete validation, validates non-empty requirements, and transitions nomination to `SUBMITTED`.
  * **Document Uploader**: Modal supporting drag-and-drop or file selection for PDF, PNG, and JPEG files with instant upload feedback.
  * **My Nominations Table**: Live table showing status badges, submission date, cost, and a "View Details" drawer with full event timeline.

---

### 4.3 Reviewer Portal (Evaluation & Decisions)
* **URL**: `http://localhost:8000/reviewer`
* **Features**:
  * **Pending Review Queue**: Displays all nominations across the organization currently in `SUBMITTED` or `UNDER_REVIEW` status.
  * **Evaluation Modal**:
    * Full nominee profile (Name, Email, Department).
    * Course details (Title, Category, Dates, Duration, Cost).
    * Employee's Business Justification and Description.
    * Clickable document links to view or download uploaded syllabus/brochure attachments.
  * **Reviewer Actions**:
    * **"Start Review"**: Moves state from `SUBMITTED` to `UNDER_REVIEW`.
    * **"Approve Nomination"**: Marks nomination as `APPROVED` and records approval timestamp.
    * **"Reject Nomination"**: Prompts reviewer for a mandatory rejection comment, records reason, and marks status as `REJECTED`.

---

### 4.4 Administrator Dashboard (Metrics & Audit Trail)
* **URL**: `http://localhost:8000/admin`
* **Features**:
  * **Executive Metrics Cards**: Real-time KPI counters for Total Nominations, Drafts, Submitted, Under Review, Approved, and Rejected requests.
  * **Interactive Status Filter**: Dropdown filter to query and inspect nominations by state (`ALL`, `DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`).
  * **Global Nomination Ledger**: Organization-wide view with employee name, program title, category, cost, and current status badge.
  * **Immutable Audit Trail Log**: Live table displaying every state transition across the system with timestamp, event type (`CREATED`, `SUBMITTED`, `REVIEW_STARTED`, `APPROVED`, `REJECTED`), actor name, and associated comments.

---

## 🗄️ 5. Database Architecture & Data Models

NominaFlow uses SQLAlchemy ORM with a normalized relational schema:

```text
┌─────────────────┐       ┌────────────────────────┐       ┌─────────────────┐
│      roles      │       │         users          │       │  audit_events   │
├─────────────────┤       ├────────────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────┤ role_id (FK)           │◄──────┤ actor_id (FK)   │
│ name            │       │ id (PK)                │       │ id (PK)         │
│ description     │       │ email (Unique)         │       │ event_type      │
└─────────────────┘       │ hashed_password        │       │ from_state      │
                          │ full_name              │       │ to_state        │
                          │ department             │       │ comments        │
                          │ is_active              │       │ created_at      │
                          └───────────┬────────────┘       │ nomination_id ──┼──┐
                                      │                    └─────────────────┘  │
                                      ▼                                         │
                          ┌────────────────────────┐                            │
                          │  training_nominations  │◄───────────────────────────┘
                          ├────────────────────────┤
                          │ id (PK)                │
                          │ employee_id (FK)       │
                          │ reviewer_id (FK)       │
                          │ program_title          │
                          │ provider_name          │
                          │ category               │
                          │ start_date             │
                          │ duration_hours         │
                          │ estimated_cost         │
                          │ description            │
                          │ business_justification │
                          │ status (Enum)          │
                          │ rejection_reason       │
                          │ created_at             │
                          │ updated_at             │
                          └───────────┬────────────┘
                                      │
                                      ▼
                          ┌────────────────────────┐
                          │       documents        │
                          ├────────────────────────┤
                          │ id (PK)                │
                          │ nomination_id (FK)     │
                          │ filename               │
                          │ file_path              │
                          │ file_size              │
                          │ mime_type              │
                          │ uploaded_at            │
                          └────────────────────────┘
```

---

## 🔒 6. Security, Auth & Role-Based Access Control (RBAC)

1. **Password Security**:
   - Implemented using direct `bcrypt.hashpw` with salt generation and `bcrypt.checkpw`.
   - Protects against passlib wrap exceptions and timing attacks.
2. **Session & Token Management**:
   - JSON Web Tokens (JWT) signed with HMAC-SHA256 (`HS256`).
   - Browser portals store token in an `access_token` session cookie.
   - REST API clients can pass standard `Authorization: Bearer <token>` header.
3. **Role-Based Access Control (RBAC)**:
   - Evaluated via FastAPI dependency injection (`require_roles(["EMPLOYEE", "REVIEWER", "ADMIN"])`).
   - Unauthorized access immediately returns `HTTP 403 Forbidden` or redirects browser users to `/login`.

---

## 🔌 7. REST API Specifications

NominaFlow exposes OpenAPI-compliant REST endpoints accessible under `/api/v1`:

### 7.1 Authentication Endpoints (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | Authenticate with email/password; returns JWT | Public |
| `POST` | `/api/v1/auth/logout` | Invalidate cookie session | Public |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile & role | Bearer / Cookie |

### 7.2 Nomination Endpoints (`/api/v1/nominations`)
| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `POST` | `/api/v1/nominations` | Create a new nomination in `DRAFT` state | `EMPLOYEE` |
| `GET` | `/api/v1/nominations` | List nominations owned by logged-in employee | `EMPLOYEE` |
| `GET` | `/api/v1/nominations/{id}` | Retrieve nomination details and history | `EMPLOYEE`, `REVIEWER`, `ADMIN` |
| `PUT` | `/api/v1/nominations/{id}` | Update draft nomination fields | `EMPLOYEE` (Owner) |
| `POST` | `/api/v1/nominations/{id}/submit` | Transition nomination from `DRAFT` to `SUBMITTED` | `EMPLOYEE` (Owner) |
| `GET` | `/api/v1/nominations/{id}/status` | Query live state machine status | `EMPLOYEE`, `REVIEWER`, `ADMIN` |
| `GET` | `/api/v1/nominations/{id}/history` | Query state transition audit events | `EMPLOYEE`, `REVIEWER`, `ADMIN` |

### 7.3 Supporting Documents (`/api/v1/nominations/{id}/documents`)
| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `POST` | `/api/v1/nominations/{id}/documents` | Upload PDF/PNG/JPEG attachment (multipart) | `EMPLOYEE` (Owner) |
| `GET` | `/api/v1/nominations/{id}/documents` | List attached documents for a nomination | `EMPLOYEE`, `REVIEWER`, `ADMIN` |
| `GET` | `/api/v1/documents/{id}` | Download document binary file | `EMPLOYEE`, `REVIEWER`, `ADMIN` |

### 7.4 Reviewer Operations (`/api/v1/reviewer`)
| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/v1/reviewer/nominations` | Query pending review queue (`SUBMITTED`, `UNDER_REVIEW`) | `REVIEWER`, `ADMIN` |
| `POST` | `/api/v1/reviewer/nominations/{id}/start-review` | Move state to `UNDER_REVIEW` | `REVIEWER` |
| `POST` | `/api/v1/reviewer/nominations/{id}/approve` | Approve nomination (`APPROVED`) | `REVIEWER` |
| `POST` | `/api/v1/reviewer/nominations/{id}/reject` | Reject nomination with reason (`REJECTED`) | `REVIEWER` |

### 7.5 Administration (`/api/v1/admin`)
| Method | Endpoint | Description | Allowed Roles |
|---|---|---|---|
| `GET` | `/api/v1/admin/nominations` | Query all organization nominations (supports `?status=`) | `ADMIN` |
| `GET` | `/api/v1/admin/audit-events` | Query global audit trail log | `ADMIN` |
| `GET` | `/api/v1/admin/users` | List registered system users | `ADMIN` |

---

## ⚡ 8. Zero-Setup Local Quickstart

### Step 1: Clone Repository
```bash
git clone https://github.com/Pratikkk14/NominaFlow.git
cd NominaFlow
```

### Step 2: Create & Activate Virtual Environment
**Windows PowerShell**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Application Server
```bash
uvicorn training_nomination.main:app --reload --port 8000
```

### Step 5: Access System
* 🌐 **Web UI Portal**: [http://localhost:8000](http://localhost:8000)
* 📖 **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* 📋 **ReDoc API Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* 💓 **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 9. Automated Testing & Quality Gates

NominaFlow enforces test-driven quality assurance using **Pytest** and **Selenium WebDriver**:

```bash
pytest -v --cov=src --cov-report=term-missing
```

### Test Suite Summary:
* **28 Automated Unit & API Integration Tests** (100% Pass Rate).
* **90% Code Coverage** across all business services, FSM transitions, routers, and models.
* **Coverage Breakdown**:
  * `test_auth.py`: Password hashing, token encoding/decoding, RBAC enforcement.
  * `test_state_machine.py`: Deterministic state transitions and forbidden transition invariant tests.
  * `test_nominations.py`: Draft creation, field validation, submission workflow.
  * `test_documents.py`: MIME-type checking, 5MB file size limits, multipart uploads.
  * `test_reviewer.py`: Queue filtering, review start, approval, and rejection reason enforcement.
  * `test_admin.py`: Global nomination filters, user listing, audit trail queries.
  * `test_health.py`: Liveness probe and Jinja2 template rendering.
  * `tests/selenium/test_ui_e2e.py`: Automated browser journeys for login, draft creation, reviewer decisions, and screenshot capture on failure.

---

## ⚙️ 10. DevOps Lifecycle & CI/CD Pipeline

```text
┌──────────────────────────────┐
│  Continuous Integration (CI) │
│  • Jenkins Declarative Build │
│  • Virtualenv Setup          │
│  • Pytest + Coverage Gate    │
│  • JUnit XML & HTML Reports  │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│   Quality Gate Enforcement   │
│  • Minimum 80% Coverage Gate │
│  • Flake8 / Ruff Lint Checks │
│  • Selenium E2E Automation   │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│   Continuous Delivery (CD)   │
│  • Multi-Stage Docker Build  │
│  • Docker Compose Topology   │
│  • Nginx Reverse Proxy       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│   Configuration Management   │
│  • Ansible Provisioning      │
│  • Systemd Service Config    │
│  • Automated Idempotency     │
└──────────────────────────────┘
```

* **Jenkinsfile**: Automated multi-stage pipeline running test execution, code coverage extraction, and artifact archiving.
* **Conventional Commits**: Strict adherence to atomic commits (`feat:`, `fix:`, `test:`, `docs:`, `chore:`).
* **Branching Strategy**: `main` (Production release), `develop` (Integration), `feature/*` (Feature development).

---

## 📚 11. Project Documentation & Deliverables Map

| Category | Document Link | Description |
|---|---|---|
| **User Manual** | [**`docs/PROJECT_GUIDE.md`**](PROJECT_GUIDE.md) | Step-by-step UI walkthrough and API guide |
| **Requirements** | [**`docs/requirements/srs.md`**](requirements/srs.md) | Formal Software Requirements Specification (FR-01 to FR-14, NFR-01 to NFR-07) |
| **Requirements** | [**`docs/requirements/problem_scope.md`**](requirements/problem_scope.md) | Problem definition, target personas, and MVP boundaries |
| **Architecture** | [**`docs/architecture/system_architecture.md`**](architecture/system_architecture.md) | 3-tier architecture topology and technology decisions |
| **Architecture** | [**`docs/architecture/database_design.md`**](architecture/database_design.md) | Entity relationship model and PostgreSQL schema |
| **Architecture** | [**`docs/architecture/workflow_state_machine.md`**](architecture/workflow_state_machine.md) | Finite State Machine transition matrix and invariants |
| **Architecture** | [**`docs/architecture/api_design.md`**](architecture/api_design.md) | REST API endpoints, schemas, and status codes |
| **Agile** | [**`docs/agile/user_stories.md`**](agile/user_stories.md) | Epics, User Stories, and Acceptance Criteria |
| **Agile** | [**`docs/agile/sprint_plan.md`**](agile/sprint_plan.md) | 15-Week Scrum sprint plan and milestone roadmap |
| **Agile** | [**`docs/agile/definition_of_done.md`**](agile/definition_of_done.md) | Quality thresholds, test coverage rules, and PR checklist |
| **Agile** | [**`docs/agile/devops_lifecycle.md`**](agile/devops_lifecycle.md) | End-to-end DevOps process flow diagram |
| **Deliverables** | [**`Deliverables/week1.md`**](../Deliverables/week1.md) | Week 1: Problem definition and MVP scope report |
| **Deliverables** | [**`Deliverables/week2.md`**](../Deliverables/week2.md) | Week 2: Agile planning and DevOps workflow report |
| **Deliverables** | [**`Deliverables/week3.md`**](../Deliverables/week3.md) | Week 3: Software requirements and system architecture report |
| **Deliverables** | [**`Deliverables/week4.md`**](../Deliverables/week4.md) | Week 4: Git and GitHub repository initialization report |

---

*NominaFlow — Developed for the DevOps Lab Mini Project.*
