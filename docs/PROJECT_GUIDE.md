# NominaFlow — Application & User Guide

> **Centralized Training Nomination Workflow Management System**  
> Complete technical guide, user workflow walkthrough, API reference, and local execution manual.

---

## 📌 1. Introduction & Overview

**NominaFlow** is a modern, modular web application built with **Python 3.12+**, **FastAPI**, **SQLAlchemy**, and **Jinja2**. It digitizes and streamlines the organizational training nomination process — eliminating fragmented emails, manual spreadsheets, and approval bottlenecks.

### Core Capabilities:
* 📝 **Employee Draft & Submission Portal**: Form text inputs and textareas for creating, editing, and formally submitting training nominations.
* 📎 **Supporting Document Management**: Multi-part attachment uploader supporting PDF, PNG, and JPEG files up to 5 MB.
* 🔍 **Reviewer Decision Queue**: Dedicated queue for department reviewers to inspect course outlines, evaluate business justifications, and record approval or rejection with mandatory feedback comments.
* 👑 **Administrator Governance Dashboard**: Pipeline monitoring with status filters, statistical counters, and an immutable real-time audit trail.
* ⚡ **Zero-Setup Local Execution**: Out-of-the-box SQLite database (`nominaflow.db`) with automatic table creation and demo account seeding, plus seamless PostgreSQL support when `DATABASE_URL` is set.
* 🧪 **Comprehensive Automated Testing**: 28 passing unit & API integration tests (**90% code coverage**) and Selenium E2E browser journeys.

---

## 👥 2. User Roles & Pre-Seeded Demo Accounts

NominaFlow automatically initializes three demo accounts upon first startup:

| Persona | Role | Email | Password | Access & Responsibilities |
|---|---|---|---|---|
| **Alex Mercer** | `EMPLOYEE` | `employee@nominaflow.com` | `password123` | Create draft nominations in text boxes, attach syllabus docs, submit for review, track live status |
| **Sarah Jenkins** | `REVIEWER` | `reviewer@nominaflow.com` | `password123` | Inspect pending nominations, view attachments, start review, approve or reject with comments |
| **Admin User** | `ADMIN` | `admin@nominaflow.com` | `password123` | Global pipeline monitoring, status distribution stats, query all nominations, view immutable audit logs |

> 💡 **Quick Login**: The `/login` page includes **1-Click Instant Login** buttons for all three personas during demonstrations.

---

## 🔄 3. Finite State Machine & Workflow Lifecycle

All training nominations follow a deterministic state machine enforced at the service layer:

```text
       ┌──────────────┐
       │   (Start)    │
       └──────┬───────┘
              │ create_nomination()
              ▼
       ┌──────────────┐
  ┌───►│    DRAFT     │◄──── (Editable via Form Text Boxes)
  │    └──────┬───────┘
  │ edit()    │ submit_nomination()
  └───────────┘
              ▼
       ┌──────────────┐
       │  SUBMITTED   │◄──── (Locked from Employee modification)
       └──────┬───────┘
              │ start_review()
              ▼
       ┌──────────────┐
       │ UNDER_REVIEW │◄──── (Reviewer evaluating justification & docs)
       └──────┬───────┘
              │
       ┌──────┴──────────────────────────┐
       │ approve()                       │ reject(comment)
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│   APPROVED   │                  │   REJECTED   │
│  (Terminal)  │                  │  (Terminal)  │
└──────────────┘                  └──────────────┘
```

### State Definitions:
1. **`DRAFT`**: Initial editable state. Nominee inputs training details (Title, Provider, Category, Date, Duration, Cost, Syllabus, Justification).
2. **`SUBMITTED`**: Formal submission. Enters reviewer queue with recorded timestamp.
3. **`UNDER_REVIEW`**: Reviewer opens and starts active evaluation.
4. **`APPROVED`**: Reviewer approves request. Timestamp and reviewer ID are permanently recorded in audit logs.
5. **`REJECTED`**: Reviewer rejects request with a mandatory explanation.

---

## 💻 4. Web Portal Walkthrough

### 1. Authentication (`/login`)
* Clean login form with JWT token and cookie-based session issuance.
* Includes one-click quick login buttons for Employee, Reviewer, and Admin personas.

### 2. Employee Portal (`/employee`)
* **Create & Edit Drafts in Text Boxes**: Form text boxes for Title, Provider, Category dropdown, Date picker, Duration, Cost, Description textarea, and Business Justification textarea.
* **Draft Actions**: "Save as Draft" allows incremental population without submitting; "Save & Submit for Review" executes formal validation and moves state to `SUBMITTED`.
* **Attachments**: Multi-part modal file uploader for syllabi/brochures (PDF, PNG, JPEG).
* **My Nominations Table**: Live table displaying all user nominations with color-coded status badges and detailed history timelines.

### 3. Reviewer Portal (`/reviewer`)
* **Pending Review Queue**: Displays all nominations in `SUBMITTED` or `UNDER_REVIEW` states.
* **Evaluation Modal**: Displays nominee profile, course overview, cost, business justification, and clickable attachment links.
* **Review Controls**: "Start Review" (moves to `UNDER_REVIEW`), "Approve Nomination", and "Reject Nomination" (opens modal requiring feedback comment).

### 4. Administrator Dashboard (`/admin`)
* **Metric Statistics Cards**: Total requests, Drafts, Submitted, Under Review, Approved, and Rejected counts.
* **Filter Dropdown**: Real-time filtering by status (`DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`).
* **Global Pipeline Table**: Organization-wide view of all submitted training requests.
* **Immutable Audit Trail**: Real-time log table showing timestamp, event type, actor name, nomination ID, and comments.

---

## 🚀 5. Local Setup & Execution Guide

### Prerequisites
* Python 3.12+ (or Python 3.10+)
* Standard virtual environment (`venv`)
* Optional: PostgreSQL (SQLite is used automatically if PostgreSQL is not configured)

### Step 1: Clone and Navigate
```bash
git clone https://github.com/Pratikkk14/NominaFlow.git
cd NominaFlow
```

### Step 2: Create and Activate Virtual Environment
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

### Step 5: Open Browser
* **Web UI Portal**: [http://localhost:8000](http://localhost:8000)
* **Interactive API Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Health Check Probe**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🔌 6. REST API Reference

### Authentication (`/api/v1/auth`)
* `POST /api/v1/auth/login`: Authenticate and obtain JWT token.
* `POST /api/v1/auth/logout`: Invalidate session cookie.
* `GET /api/v1/auth/me`: Get profile of authenticated user.

### Training Nominations (`/api/v1/nominations`)
* `POST /api/v1/nominations`: Create a new draft nomination.
* `GET /api/v1/nominations`: List all nominations for the logged-in employee.
* `GET /api/v1/nominations/{id}`: Get complete nomination details.
* `PUT /api/v1/nominations/{id}`: Update draft fields.
* `POST /api/v1/nominations/{id}/submit`: Formally submit draft into review queue.
* `GET /api/v1/nominations/{id}/status`: Query live lifecycle status.
* `GET /api/v1/nominations/{id}/history`: Retrieve nomination audit event log.

### Documents (`/api/v1/nominations/{id}/documents`)
* `POST /api/v1/nominations/{id}/documents`: Upload file attachment (multipart).
* `GET /api/v1/nominations/{id}/documents`: List attached files.
* `GET /api/v1/documents/{id}`: Download file content.

### Reviewer Workflow (`/api/v1/reviewer`)
* `GET /api/v1/reviewer/nominations`: Query review queue.
* `POST /api/v1/reviewer/nominations/{id}/start-review`: Move to `UNDER_REVIEW`.
* `POST /api/v1/reviewer/nominations/{id}/approve`: Approve nomination.
* `POST /api/v1/reviewer/nominations/{id}/reject`: Reject nomination with comment.

### Administration (`/api/v1/admin`)
* `GET /api/v1/admin/nominations?status={STATUS}`: Query all organization nominations.
* `GET /api/v1/admin/audit-events`: Query global audit logs.
* `GET /api/v1/admin/users`: List registered system users.

---

## 🧪 7. Automated Testing

Run the test suite with coverage report:

```bash
pytest -v --cov=src --cov-report=term-missing
```

### Test Coverage Highlights:
* **28 Passed Unit & API Tests** with **90% Code Coverage**.
* **FSM Invariant Tests**: Confirms forbidden transitions raise HTTP 400.
* **Auth & RBAC Tests**: Confirms role enforcement for Employee, Reviewer, and Admin.
* **Document Handling Tests**: Confirms valid PDF/image uploads, oversize rejection (>5MB), and invalid MIME rejection.
* **Selenium E2E Tests** (`tests/selenium/test_ui_e2e.py`): Ready for browser automation with failure screenshot capture.
