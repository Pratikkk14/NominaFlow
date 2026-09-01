# System Architecture

## 1. Architectural Style: Modular Monolith

NominaFlow is architected as a **modular monolith** in Python. A monolithic structure is chosen intentionally to optimize for developer productivity, clear domain boundaries, straightforward testing, and transparent DevOps automation throughout the 15-week development lifecycle.

```text
                           ┌──────────────────────────┐
                           │   Client / Web Browser   │
                           └─────────────┬────────────┘
                                         │ HTTP / REST
                                         ▼
                           ┌──────────────────────────┐
                           │   Nginx (Reverse Proxy)  │
                           └─────────────┬────────────┘
                                         │ Reverse Proxy / WSGI-ASGI
                                         ▼
                           ┌──────────────────────────┐
                           │   Uvicorn (ASGI Server)  │
                           └─────────────┬────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             FastAPI Application                             │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                            API / Routers                              │  │
│  │      /api/auth    /api/nominations    /api/reviewer    /api/admin     │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │                                      │
│  ┌───────────────────────────────────▼───────────────────────────────────┐  │
│  │                           Service Layer                               │  │
│  │   AuthService    NominationService    ValidationService  AuditService │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
│                                      │                                      │
│  ┌───────────────────────────────────▼───────────────────────────────────┐  │
│  │                       Data Access / ORM Layer                         │  │
│  │               SQLAlchemy Models & Repository Patterns                 │  │
│  └───────────────────────────────────┬───────────────────────────────────┘  │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
         ┌────────────────────┐                ┌────────────────────┐
         │ PostgreSQL Database│                │ Local File Storage │
         │   (Relational)     │                │ (Uploaded Syllabus)│
         └────────────────────┘                └────────────────────┘
```

---

## 2. Layering & Separation of Concerns

The application codebase is partitioned into distinct architectural layers:

### 2.1 API & Router Layer (`src/training_nomination/api/`)
* Declares HTTP route definitions and OpenAPI tags.
* Deserializes request payloads and enforces Pydantic schemas.
* Injects security dependencies (authenticated user, RBAC role validation).
* Returns standardized HTTP response status codes.

### 2.2 Service & Business Logic Layer (`src/training_nomination/services/`)
* Encapsulates all domain rules, state transitions, and business validations.
* Manages transactions and orchestrates data access operations.
* Dispatches audit events upon workflow mutations.
* Independent of HTTP request/response constructs for clean unit testability.

### 2.3 Data Access & Persistence Layer (`src/training_nomination/models/` & `db/`)
* SQLAlchemy declarative ORM models.
* Alembic database migrations tracking versioned schema changes.
* PostgreSQL connection pooling and session lifecycle management.

### 2.4 Core & Infrastructure Layer (`src/training_nomination/core/`)
* Global application configuration using `pydantic-settings`.
* Password hashing utilities (`passlib` with bcrypt).
* JWT token encoding/decoding.

---

## 3. Technology Stack Selection Rationale

| Layer | Component | Technical Selection | Justification |
|---|---|---|---|
| **Language** | Runtime | Python 3.12+ | High developer velocity, rich ecosystem, native async support, and broad DevOps tooling integration. |
| **Backend** | Framework | FastAPI | Modern high-performance ASGI framework with automatic OpenAPI docs generation and native Pydantic validation. |
| **App Server** | ASGI | Uvicorn | Lightning-fast ASGI server implementation for async Python applications. |
| **Proxy** | Web Server | Nginx | Robust reverse proxy handling TLS termination, static asset offloading, and standard production edge routing. |
| **Database** | RDBMS | PostgreSQL | ACID-compliant relational database ensuring transactional integrity for critical workflow state transitions. |
| **ORM** | Object Mapper | SQLAlchemy 2.0 | Type-safe, production-proven ORM supporting complex queries and clean abstraction over raw SQL. |
| **Migrations**| Schema Engine | Alembic | Version-controlled, reproducible database schema management. |
| **Testing** | Suite | Pytest & HTTPX | Declarative, robust test execution framework supporting isolated unit tests and API integration testing. |
