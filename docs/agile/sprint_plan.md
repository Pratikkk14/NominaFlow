# 15-Week Sprint Plan & Definition of Done

## 1. 15-Week Development Roadmap

The project is structured into iterative weekly milestones combining Agile delivery and DevOps maturity.

```text
┌───────────────────────────────────────────────────────────────────────────────┐
│                            15-WEEK PROJECT TIMELINE                           │
├───────────────┬───────────────────────────────────────────────────────────────┤
│ Phase 1       │ Weeks 1–3: Ideation, Problem Scope, Agile & SRS Architecture  │
├───────────────┤───────────────────────────────────────────────────────────────┤
│ Setup         │ Week 4: Git/GitHub Repo Initialization & Conventions (Current)│
├───────────────┤───────────────────────────────────────────────────────────────┤
│ Development   │ Weeks 5–7: Data Models, Auth & Core Nomination API (FastAPI)  │
├───────────────┤───────────────────────────────────────────────────────────────┤
│ Review/Docs   │ Weeks 8–9: Reviewer Workflow, File Storage & Audit Trail      │
├───────────────┤───────────────────────────────────────────────────────────────┤
│ Quality & CI  │ Weeks 10–11: Pytest Test Suite & Jenkins CI Pipeline Setup    │
├───────────────┤───────────────────────────────────────────────────────────────┤
│ Deploy & CD   │ Weeks 12–13: Docker Containerization & Deployment Pipeline    │
├───────────────┤───────────────────────────────────────────────────────────────┤
│ Monitoring    │ Weeks 14–15: Observability, Metrics & Final Review            │
└───────────────┴───────────────────────────────────────────────────────────────┘
```

---

## 2. Weekly Sprint Milestones

| Week | Focus Area | Key Deliverables & Outcomes | Status |
|---|---|---|---|
| **Week 1** | Problem Definition & Scope | Problem statement, stakeholders, pain points, MVP boundaries | Completed |
| **Week 2** | Agile & DevOps Planning | Epics, user stories, acceptance criteria, DevOps workflow | Completed |
| **Week 3** | SRS & Technical Architecture | Requirements spec, system architecture, database & API models | Completed |
| **Week 4** | Git & Repository Initialization | Repo layout, .gitignore, issue/PR templates, Python skeleton | Completed |
| **Week 5** | Data Modeling & Database Setup | PostgreSQL schemas, SQLAlchemy ORM models, Alembic migrations | **Current** |
| **Week 6** | Auth & User Management | Password hashing, JWT token authentication, RBAC middleware | Planned |
| **Week 7** | Nomination Intake Service | Draft creation, validation engine, submission endpoints | Planned |
| **Week 8** | Document Management Service | File upload, MIME validation, local disk/S3 storage driver | Planned |
| **Week 9** | Reviewer & Decision Engine | Review queue, approval/rejection state transitions, comments | Planned |
| **Week 10** | Status Tracking & Audit Logging | Nominee status tracking, admin filter dashboard, audit logs | Planned |
| **Week 11** | Automated Testing & QA | Pytest unit, service, API integration test suites | Planned |
| **Week 12** | Continuous Integration (CI) | Jenkins / GitHub Actions pipeline for linting and test runs | Planned |
| **Week 13** | Containerization & Reverse Proxy| Dockerfile, Docker Compose, Nginx reverse proxy configuration | Planned |
| **Week 14** | Deployment & Infrastructure | Automated deployment scripts, environment configuration | Planned |
| **Week 15** | Observability, Handover & Demo | Health metrics, structured logging, final release & demo | Planned |

---

## 3. Definition of Done (DoD)

A user story or backlog task is marked **Done** only when:

1. **Implementation**: Code meets all acceptance criteria defined in the story.
2. **Coding Standards**: Code passes formatting and PEP 8 guidelines.
3. **Automated Tests**: Unit and integration tests are written and passing with no regressions.
4. **Documentation**: Corresponding API, architecture, and markdown docs in `docs/` are updated.
5. **No Secrets**: No passwords, tokens, `.env` files, or private keys are present in Git history.
6. **Code Review**: Pull request created using `.github/pull_request_template.md` and approved.
7. **Clean CI**: Build and automated test suites pass cleanly in the CI pipeline.
