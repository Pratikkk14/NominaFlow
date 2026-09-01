# Database Design & Schema Specification

## 1. Entity-Relationship Overview

NominaFlow uses PostgreSQL as its primary relational store. The schema ensures referential integrity, supports audit traceability, and maintains strict workflow states.

```text
┌──────────────────────┐               ┌──────────────────────────┐
│        ROLES         │               │          USERS           │
├──────────────────────┤               ├──────────────────────────┤
│ PK  id (INT)         │◄───1:N────────│ PK  id (UUID)            │
│     name (VARCHAR)   │               │     name (VARCHAR)       │
└──────────────────────┘               │     email (VARCHAR, UQ)  │
                                       │     password_hash (TEXT) │
                                       │ FK  role_id (INT)        │
                                       │     created_at (TS)      │
                                       └────────────┬─────────────┘
                                                    │ 1:N
                                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                      TRAINING_NOMINATIONS                       │
├─────────────────────────────────────────────────────────────────┤
│ PK  id (UUID)                                                   │
│ FK  employee_id (UUID) -> users(id)                             │
│     title (VARCHAR)                                             │
│     provider (VARCHAR)                                          │
│     description (TEXT)                                          │
│     training_type (VARCHAR)                                     │
│     training_date (DATE)                                        │
│     duration (VARCHAR)                                          │
│     cost (NUMERIC(10,2))                                        │
│     justification (TEXT)                                        │
│     status (VARCHAR)  [DRAFT, SUBMITTED, UNDER_REVIEW, ...]     │
│     created_at (TIMESTAMP)                                      │
│     submitted_at (TIMESTAMP, NULL)                              │
│     updated_at (TIMESTAMP)                                      │
└──────────────────┬───────────────────────────────┬──────────────┘
                   │ 1:N                           │ 1:N
                   ▼                               ▼
┌──────────────────────────────────┐   ┌──────────────────────────┐
│            DOCUMENTS             │   │       AUDIT_EVENTS       │
├──────────────────────────────────┤   ├──────────────────────────┤
│ PK  id (UUID)                    │   │ PK  id (UUID)            │
│ FK  nomination_id (UUID)         │   │ FK  nomination_id (UUID) │
│     file_name (VARCHAR)          │   │ FK  user_id (UUID)       │
│     file_path (VARCHAR)          │   │     event_type (VARCHAR) │
│     file_type (VARCHAR)          │   │     comment (TEXT, NULL) │
│     file_size (INTEGER)          │   │     timestamp (TIMESTAMP)│
│     uploaded_at (TIMESTAMP)      │   └──────────────────────────┘
└──────────────────────────────────┘
```

---

## 2. Table Definitions

### 2.1 `roles`
Stores application roles (`Employee`, `Reviewer`, `Administrator`).

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique role identifier |
| `name` | VARCHAR(50) | UNIQUE, NOT NULL | Role name (`EMPLOYEE`, `REVIEWER`, `ADMIN`) |

### 2.2 `users`
Stores user credentials, profile metadata, and role association.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier |
| `name` | VARCHAR(100) | NOT NULL | User's full name |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Primary email used for authentication |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt password hash |
| `role_id` | INTEGER | FOREIGN KEY -> roles(id), NOT NULL | Associated user role |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Account creation timestamp |

### 2.3 `training_nominations`
Core entity tracking individual training requests and their lifecycle state.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique nomination identifier |
| `employee_id` | UUID | FOREIGN KEY -> users(id), NOT NULL, INDEX | Submitting employee |
| `title` | VARCHAR(255) | NOT NULL | Course or program title |
| `provider` | VARCHAR(255) | NOT NULL | Training institution / platform |
| `description` | TEXT | NOT NULL | Scope and syllabus overview |
| `training_type` | VARCHAR(50) | NOT NULL | Category (e.g., Technical, Leadership) |
| `training_date` | DATE | NOT NULL | Target training start date |
| `duration` | VARCHAR(50) | NOT NULL | Duration (e.g., "3 days", "40 hours") |
| `cost` | NUMERIC(10,2) | NOT NULL, DEFAULT 0.00 | Estimated cost |
| `justification` | TEXT | NOT NULL | Business rationale |
| `status` | VARCHAR(30) | NOT NULL, INDEX | Current state (`DRAFT`, `SUBMITTED`, etc.) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Initial creation timestamp |
| `submitted_at` | TIMESTAMP WITH TIME ZONE | NULL | Formal submission timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Last modification timestamp |

### 2.4 `documents`
Tracks supporting files uploaded for a nomination.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique document identifier |
| `nomination_id` | UUID | FOREIGN KEY -> training_nominations(id), NOT NULL, INDEX | Associated nomination |
| `file_name` | VARCHAR(255) | NOT NULL | Original filename |
| `file_path` | VARCHAR(500) | NOT NULL | Relative disk path or storage key |
| `file_type` | VARCHAR(100) | NOT NULL | MIME type (`application/pdf`, etc.) |
| `file_size` | INTEGER | NOT NULL | File size in bytes |
| `uploaded_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Upload timestamp |

### 2.5 `audit_events`
Immutable audit log recording every state transition and administrative action.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique audit event ID |
| `nomination_id` | UUID | FOREIGN KEY -> training_nominations(id), NOT NULL, INDEX | Related nomination |
| `user_id` | UUID | FOREIGN KEY -> users(id), NOT NULL | Actor who triggered the event |
| `event_type` | VARCHAR(50) | NOT NULL | Event name (`SUBMIT`, `REVIEW_START`, `APPROVE`, `REJECT`) |
| `comment` | TEXT | NULL | Context or review feedback |
| `timestamp` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW(), INDEX | Event timestamp |
