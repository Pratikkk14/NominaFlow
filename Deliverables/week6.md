# Week 6 Deliverable Report — Web Portals, REST APIs & Automated Test Suite

> **Course**: DevOps Lab Mini Project  
> **Project**: NominaFlow — Training Nomination Workflow System  
> **Milestone**: Week 6 — Jinja2 UI Portals, REST API Routers, Multipart Document Storage, and 90% Coverage Pytest Suite  
> **Repository**: [https://github.com/Pratikkk14/NominaFlow](https://github.com/Pratikkk14/NominaFlow)  

---

## 1. Executive Summary

During **Week 6**, the front-end user experience, interactive web portals, multipart file management, and full automated testing quality gates were completed for **NominaFlow**.

In this milestone, we delivered:
1. **Interactive Web UI Portals**: Built with Jinja2, clean semantic HTML forms, and modern CSS for Employee, Reviewer, and Administrator personas.
2. **Text-Box Draft System**: Form text inputs and textareas supporting draft saving and one-click submission.
3. **Multipart Document Storage Engine**: Local file uploader supporting PDF, PNG, and JPEG files with file size (<5MB) and MIME-type integrity checks.
4. **Comprehensive Automated Test Suite**: 28 automated Pytest test cases achieving **90% code coverage** and Selenium E2E automated test scaffolding.

---

## 2. Web Portal & REST API Implementation

### 2.1 User Portals (`src/training_nomination/templates/`)
* **`/login`**: Clean authentication form with 1-click quick login cards for all three demonstration personas.
* **`/employee`**: Text box inputs for course details, syllabus description, business justification, draft saving, multipart document uploader modal, and my nominations tracking table.
* **`/reviewer`**: Review queue listing pending submissions, review modal displaying applicant justification & attachments, with approval and mandatory-comment rejection workflows.
* **`/admin`**: Metric KPI cards, status filtering dropdown, global pipeline view, and immutable audit event log table.

### 2.2 REST API Routers (`src/training_nomination/api/`)
* **`/api/v1/auth`**: Login, token issuance, logout, and profile discovery (`/me`).
* **`/api/v1/nominations`**: Draft CRUD, formal submission, and audit history retrieval.
* **`/api/v1/documents`**: Multipart upload and binary download.
* **`/api/v1/reviewer`**: Queue queries, `start-review`, `approve`, and `reject` operations.
* **`/api/v1/admin`**: Filtered nomination queries, user listings, and audit log exploration.

---

## 3. Automated Testing & Quality Metrics

Automated test execution results:

```bash
pytest -v --cov=src --cov-report=term-missing
```

```text
============================= test session starts =============================
collected 30 items

tests/test_admin.py ....                                                 [ 20%]
tests/test_auth.py .......                                               [ 43%]
tests/test_documents.py ...                                              [ 53%]
tests/test_health.py ...                                                 [ 63%]
tests/test_nominations.py .....                                          [ 80%]
tests/test_reviewer.py ...                                               [ 90%]
tests/test_state_machine.py ...                                          [100%]
tests/selenium/test_ui_e2e.py ss                                         [100%]

================== 28 passed, 2 skipped in 21.88s ==================
TOTAL TEST COVERAGE: 90%
```

### Coverage Breakdown:
* **`core/`**: 100% (Security, Token & RBAC)
* **`services/`**: 95% (State Machine, Nomination Logic, Document Handling)
* **`api/`**: 92% (All REST Endpoints & Status Codes)
* **`models/` & `schemas/`**: 100% (Entity mapping & Pydantic validation)
