# NominaFlow

> **Training Nomination Workflow — A DevOps Lab Mini Project**

NominaFlow is a Python-based Training Nomination Workflow system designed to streamline the process of discovering training programs, submitting employee nominations, validating eligibility, and managing the nomination lifecycle.

This project is being developed as a **DevOps Lab mini project**, where the objective is not only to build the application but also to demonstrate a structured software development and DevOps lifecycle — from problem definition and requirements engineering to version control, CI/CD, testing, deployment, and monitoring.

---

## 📌 Project Overview

Organizations often manage employee training nominations through emails, spreadsheets, forms, and manual approval processes. This can lead to duplicated nominations, missing information, unclear approval status, and difficulty tracking the overall training lifecycle.

**NominaFlow** aims to provide a centralized workflow for managing training nominations.

The system is intended to support a workflow such as:

```text
Employee
   │
   ▼
Browse Training Programs
   │
   ▼
Select Training
   │
   ▼
Submit Nomination
   │
   ▼
Eligibility / Validation
   │
   ▼
Approval Workflow
   │
   ▼
Nomination Status
   │
   ▼
Training Enrollment
```

The exact functional scope and requirements are documented under the project's documentation directories.

---

## 🎯 Project Objectives

The primary objectives of NominaFlow are to:

* Centralize the training nomination process.
* Reduce manual coordination involved in nominations.
* Provide a structured nomination workflow.
* Validate nomination information and eligibility.
* Provide visibility into nomination status.
* Maintain a reliable record of nominations.
* Design the system using maintainable and scalable software practices.
* Apply DevOps principles throughout the software lifecycle.

---

## 🧩 Project Context

This repository serves **two purposes**.

### 1. Software Application

The actual NominaFlow application is being developed as a Python-based software system.

The application-related code is primarily located under:

```text
src/
tests/
```

### 2. DevOps Lab Project

The repository also contains documentation, reports, experiments, and other artifacts required for the **DevOps Lab mini project**.

These artifacts document the development journey, including:

```text
Problem Definition
       ↓
Requirements
       ↓
Agile Planning
       ↓
Repository Setup
       ↓
Development
       ↓
Testing
       ↓
CI/CD
       ↓
Deployment
       ↓
Monitoring
```

Therefore, some directories in this repository exist specifically to satisfy the academic/DevOps Lab requirements.

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
│   ├── agile/
│   ├── architecture/
│   ├── requirements/
│   └── ...
│
├── deliverables/
│   └── ...
│
├── reports/
│   └── ...
│
├── src/
│   └── training_nomination/
│       ├── __init__.py
│       └── main.py
│
├── tests/
│   └── ...
│
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
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

The application entry point will be available under:

```text
src/training_nomination/main.py
```

Application startup instructions will be expanded as implementation progresses.

---

## 🧪 Testing

Tests are maintained separately from application code:

```text
tests/
```

The project uses **Pytest** for automated testing.

Run the test suite with:

```bash
pytest
```

As development progresses, testing will cover areas such as:

* Unit testing
* API testing
* Workflow validation
* Integration testing
* End-to-end testing

---

## 📚 Documentation

Project documentation is maintained under:

```text
docs/
```

This includes artifacts related to:

* Problem definition
* Requirements
* Scope
* Agile planning
* Architecture
* Technical design
* Development decisions

The documentation represents the reasoning behind the system and should be considered alongside the source code.

---

## ⚙️ DevOps Lifecycle

A major purpose of this project is to demonstrate how a software system progresses through a DevOps lifecycle.

The planned lifecycle is:

```text
┌─────────────────────┐
│ Problem & Planning  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Requirements        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Development         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Version Control     │
│       Git           │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Automated Testing   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ CI Pipeline         │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ CD / Deployment     │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Monitoring          │
└─────────────────────┘
```

The repository will evolve as each stage is implemented.

---

## 📊 Current Project Status

**Current Phase: Repository Initialization**

The initial phases of the project have established:

* Problem definition
* Project scope
* Agile planning
* Requirements documentation
* Initial project structure
* Git/GitHub conventions
* Issue and pull request workflow

The application itself is currently in the early development stage.

Upcoming work will progressively introduce the actual Training Nomination Workflow and its DevOps automation.

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
