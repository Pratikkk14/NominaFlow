# NominaFlow

> **Training Nomination Workflow — A DevOps Lab Mini Project**

NominaFlow is a Python-based Training Nomination Workflow system designed to streamline the process of discovering training programs, submitting employee nominations, validating eligibility, and managing the nomination lifecycle.

This project is being developed as a **DevOps Lab mini project**, where the objective is not only to build the application but also to demonstrate a structured software development and DevOps lifecycle — from problem definition and requirements engineering to version control, CI/CD, testing, deployment, and monitoring.

---

## 📌 Project Overview

Organizations often manage employee training nominations through emails, spreadsheets, forms, and manual approval processes. This can lead to duplicated nominations, missing information, unclear approval status, and difficulty tracking the overall training lifecycle.

**NominaFlow** provides a centralized, automated web workflow for managing the complete lifecycle of training nominations.

> 📖 **Comprehensive Project Guides**:
> * 📘 [**`docs/README.md` — Technical Architecture & Operational Guide**](docs/README.md): In-depth system design, FSM transitions, database models, RBAC, REST API reference, and quickstart manual.
> * 📙 [**`docs/PROJECT_GUIDE.md` — User Workflow & Feature Manual**](docs/PROJECT_GUIDE.md): Interactive portal walkthroughs, pre-seeded personas, 1-click logins, and state machine transitions.

The system supports the following core workflow:

```text
Employee
   │
   ▼
Create / Edit Draft (Text Boxes)
   │
   ▼
Upload Supporting Documents (PDF/PNG/JPEG)
   │
   ▼
Submit Nomination ➔ SUBMITTED
   │
   ▼
Reviewer Evaluation ➔ UNDER_REVIEW
   │
   ├─── Approve ➔ APPROVED
   └─── Reject with Mandatory Reason ➔ REJECTED
   │
   ▼
Live Status Tracking & Immutable Audit Trail
```

---

## 🎯 Project Objectives

The primary objectives of NominaFlow are to:

* Centralize the training nomination process into a single digital platform.
* Support draft creation in clean text boxes with incremental saving.
* Reduce manual coordination and approval bottlenecks.
* Validate nomination information and supporting document integrity.
* Provide transparent, real-time status tracking for employees.
* Maintain an immutable, auditable log of every workflow state transition.
* Provide administrator monitoring with status filtering.
* Apply continuous DevOps practices throughout development.

---

## 🧩 Project Context

This repository serves **two purposes**:

### 1. Software Application

The actual NominaFlow application is a complete, production-grade Python web application located under:

```text
src/
tests/
```

### 2. DevOps Lab Project

The repository also contains documentation, reports, experiments, and deliverables required for the **DevOps Lab mini project**:

```text
Problem Definition ➔ Requirements ➔ Agile Planning ➔ Git Setup ➔ Development ➔ Testing ➔ CI/CD ➔ Deployment
```

---

## 📂 Repository Structure

```text
NominaFlow/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── requirement_change.md
│   │
│   └── pull_request_template.md
│
├── docs/
│   ├── README.md               # Comprehensive Technical Architecture & Operational Guide
│   ├── PROJECT_GUIDE.md        # Complete Application & Architecture User Guide
│   ├── agile/                  # Epics, User Stories, Sprint Plan, DoD, DevOps Lifecycle
│   ├── architecture/           # System Topology, Database Schema, REST API, State Machine
│   └── requirements/           # Problem Scope & SRS (FR-01 to FR-14, NFR-01 to NFR-07)
│
├── Deliverables/
│   ├── week1.md
│   ├── week2.md
│   ├── week3.md
│   └── week4.md
│
├── src/
│   └── training_nomination/
│       ├── api/                # FastAPI Routers (auth, nominations, documents, reviewer, admin)
│       ├── core/               # Security, Bcrypt Hashing, JWT Token Engine, RBAC Dependencies
│       ├── db/                 # SQLAlchemy Session Engine, Dual-DB (SQLite/Postgres), Auto-Seeder
│       ├── models/             # ORM Entities (Role, User, TrainingNomination, Document, AuditEvent)
│       ├── schemas/            # Pydantic Schemas for Input Validation & Serialization
│       ├── services/           # Business Logic, FSM State Machine, Document Storage Driver
│       ├── static/             # Modern CSS Stylesheet and Interactive JavaScript Helpers
│       ├── templates/          # Jinja2 HTML Portals (Login, Employee, Reviewer, Admin)
│       ├── config.py           # Application Settings & Pydantic Config
│       └── main.py             # FastAPI App Root, Web View Routing, Lifespan Seeder
│
├── tests/
│   ├── conftest.py             # Pytest Global Fixtures & Auto DB Initializer
│   ├── test_admin.py           # Admin Dashboard, Filter & Audit Trail Tests
│   ├── test_auth.py            # Login, Bcrypt, JWT Token, RBAC & Logout Tests
│   ├── test_documents.py       # File Upload, MIME & Size Validation Tests
│   ├── test_health.py          # Liveness Probe & Web Template Rendering Tests
│   ├── test_nominations.py     # Draft CRUD, Submission & History Tests
│   ├── test_reviewer.py        # Review Queue, Approve & Reject Workflow Tests
│   ├── test_state_machine.py   # Deterministic FSM Transition & Invariant Tests
│   └── selenium/
│       └── test_ui_e2e.py      # Automated Selenium Browser Journeys with Failure Screenshots
│
├── .gitignore
├── Jenkinsfile                 # Declarative Jenkins CI Pipeline
├── LICENSE                     # MIT Open Source License
├── pyproject.toml              # Build & Packaging Specification
├── requirements.txt            # Python Dependencies Specification
└── README.md
```

### Directory Responsibilities

| Directory       | Purpose                                                 |
| --------------- | ------------------------------------------------------- |
| `.github/`      | GitHub workflows, issue templates, and PR configuration |
| `docs/`         | Technical and project documentation                     |
| `src/`          | **Actual application source code**                      |
| `tests/`        | **Application test suite**                              |
| `deliverables/` | DevOps Lab academic deliverables                        |
| `reports/`      | DevOps Lab reports and documentation artifacts          |

### ⚠️ Important Note for Developers

If you are interested in **actually implementing or running NominaFlow**, you can largely ignore directories such as:

```text
deliverables/
reports/
```

These directories exist primarily because NominaFlow is being developed as a **DevOps Lab mini project** and contain academic/project-submission artifacts.

The application implementation is centered around:

```text
src/
tests/
requirements.txt
```

while `docs/` contains the engineering documentation that explains the system and its requirements.

---

## 🛠️ Technology Stack

The project is being developed using the Python ecosystem.

| Component         | Technology        |
| ----------------- | ----------------- |
| Language          | Python            |
| Backend           | FastAPI           |
| Database          | PostgreSQL        |
| ORM               | SQLAlchemy        |
| API Specification | OpenAPI           |
| Testing           | Pytest            |
| Version Control   | Git               |
| Repository        | GitHub            |
| CI/CD             | To be implemented |
| Deployment        | To be implemented |
| Monitoring        | To be implemented |

The stack may evolve as the project progresses through the DevOps lifecycle.

---

## 🔄 Development Methodology

NominaFlow follows an iterative Agile development approach.

The project is divided into development phases/weeks, with each phase producing specific artifacts or implementation outcomes.

The early phases focus on:

```text
Problem Definition
        ↓
Project Scope
        ↓
Requirements
        ↓
Agile Planning
        ↓
Architecture
```

Later phases progressively introduce:

```text
Implementation
        ↓
Testing
        ↓
CI
        ↓
CD
        ↓
Deployment
        ↓
Monitoring
```

This allows the project to demonstrate the complete lifecycle rather than only presenting a finished application.

---

## 🌿 Git Branching Strategy

The project follows a structured branching convention.

```text
main
develop
feature/<short-description>
bugfix/<short-description>
docs/<short-description>
refactor/<short-description>
test/<short-description>
```

Examples:

```text
feature/nomination-api
feature/training-catalog
bugfix/duplicate-nomination
docs/update-requirements
test/nomination-workflow
```

### Branch Responsibilities

**`main`**

Stable and releasable code.

**`develop`**

Integration branch for completed development work.

**`feature/*`**

Development of new functionality.

**`bugfix/*`**

Fixes for existing functionality.

**`docs/*`**

Documentation changes.

**`refactor/*`**

Code restructuring without changing intended functionality.

**`test/*`**

Testing-related changes.

---

## 📝 Commit Convention

NominaFlow follows a Conventional Commit-style format:

```text
type: description
```

Examples:

```text
feat: add training nomination endpoint
fix: prevent duplicate nominations
docs: update nomination requirements
test: add nomination validation tests
refactor: separate nomination service
chore: configure project dependencies
```

Commit messages should describe the actual change rather than using generic messages such as:

```text
update
changes
final
new code
working
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NominaFlow
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the Uvicorn ASGI server:

```bash
uvicorn training_nomination.main:app --reload --port 8000
```

Access the application in your browser:
* **Web UI Portal**: [http://localhost:8000](http://localhost:8000)
* **Interactive OpenAPI Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Probe**: [http://localhost:8000/health](http://localhost:8000/health)

### 5. Pre-Seeded Demo Accounts (1-Click Login)

The database automatically initializes three demo personas with password `password123`:
* 👤 **Employee**: `employee@nominaflow.com` (Create & submit draft nominations)
* 🔍 **Reviewer**: `reviewer@nominaflow.com` (Review queue, approve/reject decisions)
* 👑 **Administrator**: `admin@nominaflow.com` (Pipeline monitoring & audit trail)

---

## 🧪 Testing

The project uses **Pytest** for automated testing and **Selenium** for end-to-end user journeys:

```bash
pytest -v --cov=src --cov-report=term-missing
```

### Test Suite Status
* **28 Passed Tests** (100% Pass Rate).
* **90% Code Coverage** across all models, routers, state machine, and service components.
* Includes finite state machine validation, JWT auth, draft CRUD, document upload, reviewer workflows, and admin filters.

---

## 📚 Documentation & Deliverables

Project documentation and engineering specifications are maintained under [`docs/`](docs/) and [`Deliverables/`](Deliverables/):

* **[Technical Architecture & Operational Guide](docs/README.md)**: Full system architecture, database ER model, FSM transitions, and REST API contracts.
* **[Application & User Guide](docs/PROJECT_GUIDE.md)**: Detailed feature walkthrough, UI portals, 1-click demo logins, and user manual.
* **[Requirements & SRS](docs/requirements/)**: Problem scope and formal Functional/Non-Functional requirements (FR-01 to FR-14, NFR-01 to NFR-07).
* **[Architecture & Database](docs/architecture/)**: System topology, PostgreSQL schema, REST API specs, and state machine transitions.
* **[Agile & DevOps Workflow](docs/agile/)**: User stories, sprint roadmap, definition of done, and branching conventions.
* **[Weekly Deliverable Reports](Deliverables/)**: Milestone submission reports (`week1.md` through `week4.md`).

---

## ⚙️ DevOps Lifecycle

A major purpose of this project is to demonstrate how a software system progresses through a DevOps lifecycle:

```text
┌─────────────────────┐
│ Problem & Planning  │ ➔ Completed (Weeks 1–3)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Architecture & SRS  │ ➔ Completed (Week 3)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Git & Repo Setup    │ ➔ Completed (Week 4)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Application Code    │ ➔ Completed (Weeks 5–6)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Automated Testing   │ ➔ Completed (28 Tests, 90% Coverage)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ CI Pipeline         │ ➔ Configured (Jenkinsfile & JUnit Reporting)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Docker / CD         │ ➔ Next Phase
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Ansible Deploy      │ ➔ Next Phase
└─────────────────────┘
```

---

## 📊 Current Project Status

**Current Phase: Application MVP & Testing Completed (Weeks 5–6)**

* ✅ Core FastAPI application and REST APIs fully implemented.
* ✅ Responsive Web UI Portals (Employee, Reviewer, Admin) operational.
* ✅ Full automated test suite (28 tests, 90% coverage) verified.
* ✅ Git branching, atomic conventional commits, and issue tracking completed.
* 🚀 Ready for Jenkins CI, Docker containerization, and Ansible configuration management.

---

## 🎓 Academic Context

NominaFlow is developed as a **DevOps Lab Mini Project**.

The project intentionally combines:

> **Software Engineering + Application Development + DevOps Practices**

Therefore, this repository may contain academic deliverables, reports, screenshots, diagrams, and other artifacts that would not normally be part of a production application repository.

These artifacts are retained to demonstrate the complete development process and satisfy the requirements of the DevOps Lab.

For someone interested only in the software implementation, the primary areas of interest are:

```text
src/
tests/
docs/
requirements.txt
```

---

## 🤝 Contribution Workflow

All changes should follow the project's development workflow:

```text
GitHub Issue
     ↓
Create Branch
     ↓
Implement Change
     ↓
Write / Update Tests
     ↓
Commit
     ↓
Pull Request
     ↓
Review
     ↓
Merge
```

Changes to requirements should be documented through the project's requirement-change process rather than silently modifying existing requirements.

---


## 📄 License

This project is developed for educational and academic purposes as part of a DevOps Lab mini project.

See `LICENSE` for additional information.
