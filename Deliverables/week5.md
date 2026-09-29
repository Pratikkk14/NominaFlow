# Week 5 Deliverable Report — Data Modeling, Authentication & Core Backend Services

> **Course**: DevOps Lab Mini Project  
> **Project**: NominaFlow — Training Nomination Workflow System  
> **Milestone**: Week 5 — Relational Data Modeling, Dual-Engine DB Setup, Security/Auth Engine, and Core Business Logic  
> **Repository**: [https://github.com/Pratikkk14/NominaFlow](https://github.com/Pratikkk14/NominaFlow)  

---

## 1. Executive Summary

Following the Git repository initialization in Week 4, **Week 5** focuses on implementing the foundational data architecture, security layer, and core domain services for **NominaFlow**.

In this milestone, we designed and implemented:
1. **Relational Data Entities**: Normalized SQLAlchemy ORM models covering Users, Roles, Training Nominations, Supporting Documents, and Audit Events.
2. **Dual-Engine Database Layer**: Automated zero-setup SQLite engine (`nominaflow.db`) with automatic table creation and demo account seeding, with immediate support for PostgreSQL via `DATABASE_URL`.
3. **Security & Authentication Subsystem**: High-security direct `bcrypt` password hashing, JWT token generation/verification (`python-jose`), and FastAPI dependency-based Role-Based Access Control (RBAC).
4. **Deterministic Finite State Machine (FSM)**: Strict state transition validation service preventing illegal nomination status modifications.

---

## 2. Technical Architecture & Component Implementation

### 2.1 Database Models (`src/training_nomination/models/`)
* **`Role`**: Pre-seeded role definitions (`EMPLOYEE`, `REVIEWER`, `ADMIN`).
* **`User`**: User entity with unique email, bcrypt-hashed credentials, full name, department, and foreign key link to `Role`.
* **`TrainingNomination`**: Core workflow entity holding program title, provider, category, dates, duration, cost, description, business justification, status enum (`DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`), and reviewer feedback.
* **`Document`**: File metadata attachment entity storing file paths, MIME types, byte sizes, and timestamps.
* **`AuditEvent`**: Append-only immutable log recording state transitions, actor ID, timestamps, and comments.

### 2.2 Security & Authentication (`src/training_nomination/core/`)
* Direct invocation of standard `bcrypt` algorithms (`hashpw`, `checkpw`) eliminating compatibility pitfalls.
* JWT Bearer token generation with configurable expiration and secret keys.
* Session extraction supporting both HTTP `Authorization: Bearer <token>` headers and `access_token` session cookies.
* RBAC dependency `require_roles(["EMPLOYEE", "REVIEWER", "ADMIN"])`.

### 2.3 Finite State Machine (`src/training_nomination/services/state_machine.py`)
Enforces mathematical state transition constraints:
* `DRAFT` ➔ `SUBMITTED` (Initiated by Employee)
* `SUBMITTED` ➔ `UNDER_REVIEW` (Initiated by Reviewer)
* `UNDER_REVIEW` ➔ `APPROVED` (Initiated by Reviewer)
* `UNDER_REVIEW` ➔ `REJECTED` (Initiated by Reviewer with mandatory comments)
* All forbidden transitions trigger an immediate `HTTP 400 Bad Request` with state validation errors.

---

## 3. Pre-Seeded Personas for Instant Verification

| Persona | Role | Email | Password |
|---|---|---|---|
| **Alex Mercer** | `EMPLOYEE` | `employee@nominaflow.com` | `password123` |
| **Sarah Jenkins** | `REVIEWER` | `reviewer@nominaflow.com` | `password123` |
| **Admin User** | `ADMIN` | `admin@nominaflow.com` | `password123` |

---

## 4. Verification & Status
* ORM schemas validated across SQLite and PostgreSQL dialect engines.
* Zero-setup database initialization verified with automatic table creation and demo seeding upon server launch.
