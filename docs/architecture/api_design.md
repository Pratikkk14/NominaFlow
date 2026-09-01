# REST API Design Specification

## 1. Overview & Conventions
* Base URL: `/api/v1`
* Content-Type: `application/json`
* Authentication: `Bearer <JWT_TOKEN>` in `Authorization` header.
* Standard Responses:
  * `200 OK`: Successful retrieval / operation.
  * `201 Created`: Resource successfully created.
  * `400 Bad Request`: Business rule violation.
  * `401 Unauthorized`: Missing or invalid credentials.
  * `403 Forbidden`: Insufficient role permissions.
  * `404 Not Found`: Resource does not exist.
  * `422 Unprocessable Entity`: Pydantic validation failure.

---

## 2. Endpoints Summary

### 2.1 Authentication (`/api/v1/auth`)

| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | Authenticate user credentials and return JWT | Public |
| `POST` | `/api/v1/auth/logout` | Revoke session / client-side token discard | Authenticated |
| `GET` | `/api/v1/auth/me` | Retrieve profile and role of authenticated user | Authenticated |

### 2.2 Training Nominations (`/api/v1/nominations`)

| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/api/v1/nominations` | Create a new nomination in `DRAFT` status | Employee |
| `GET` | `/api/v1/nominations` | List nominations belonging to the current employee | Employee |
| `GET` | `/api/v1/nominations/{id}` | Get complete nomination details | Employee / Reviewer / Admin |
| `PUT` | `/api/v1/nominations/{id}` | Update an existing nomination in `DRAFT` status | Employee (Owner) |
| `POST` | `/api/v1/nominations/{id}/submit` | Submit a draft nomination for review (`SUBMITTED`) | Employee (Owner) |
| `GET` | `/api/v1/nominations/{id}/status` | Check current lifecycle status and timeline | Employee / Reviewer / Admin |
| `GET` | `/api/v1/nominations/{id}/history` | Retrieve full audit event log for the nomination | Authenticated |

### 2.3 Supporting Documents (`/api/v1/nominations/{id}/documents`)

| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/api/v1/nominations/{id}/documents` | Upload a supporting file (multipart/form-data) | Employee (Owner) |
| `GET` | `/api/v1/nominations/{id}/documents` | List document metadata attached to a nomination | Employee / Reviewer / Admin |
| `GET` | `/api/v1/documents/{document_id}` | Download a document file stream | Authenticated (Authorized) |

### 2.4 Reviewer Workflow (`/api/v1/reviewer`)

| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/api/v1/reviewer/nominations` | List all nominations pending review | Reviewer |
| `POST` | `/api/v1/reviewer/nominations/{id}/start-review` | Mark nomination as `UNDER_REVIEW` | Reviewer |
| `POST` | `/api/v1/reviewer/nominations/{id}/approve` | Approve nomination (`APPROVED`) | Reviewer |
| `POST` | `/api/v1/reviewer/nominations/{id}/reject` | Reject nomination with reason comment (`REJECTED`) | Reviewer |

### 2.5 Administration & Monitoring (`/api/v1/admin`)

| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/api/v1/admin/nominations` | View and filter all system nominations | Admin |
| `GET` | `/api/v1/admin/audit-events` | Query system-wide audit event logs | Admin |
| `GET` | `/api/v1/admin/users` | List registered system users and assigned roles | Admin |
