# Task 3 — Requirements, Architecture and Technology Setup

## 1. Objective

The objective of this task is to convert the approved Training Nomination Workflow MVP into a concrete technical design.

This task defines:

- Software Requirements Specification (SRS) summary
- Functional and non-functional requirements
- Use-case model
- Minimum application architecture
- Technology stack
- Database design
- API design
- Application components
- Deployment architecture
- Local development environment
- Initial project structure

The architecture is intentionally designed as a **small Python-based web application** rather than a complex enterprise or microservices system.

---

# 2. System Overview

The Training Nomination Workflow will be implemented as a centralized web application that manages the complete lifecycle of a training nomination.

The core workflow is:

```text
Employee
    |
    v
Create Nomination
    |
    v
Validate Data
    |
    v
Upload / Validate Document
    |
    v
Submit Nomination
    |
    v
Reviewer
    |
    v
Review Request
    |
    +------------------+
    |                  |
 Approve             Reject
    |                  |
    v                  v
APPROVED            REJECTED
    |                  |
    +--------+---------+
             |
             v
       Status Tracking
             |
             v
      Audit / History
````

---

# 3. SRS Summary

## 3.1 Purpose

The system will provide a centralized platform for submitting, validating, reviewing, approving/rejecting and tracking employee training nominations.

The application will replace a fragmented manual workflow with a structured digital workflow.

---

# 4. Functional Requirements

## FR-01 — Authentication

The system shall allow registered users to authenticate using valid credentials.

The system shall:

* Accept username/email and password.
* Validate credentials.
* Create an authenticated session/token.
* Prevent unauthenticated access to protected resources.
* Allow users to log out.

---

## FR-02 — Role-Based Authorization

The system shall support the following roles:

* Employee
* Reviewer
* Training Administrator

The system shall restrict functionality based on the authenticated user's role.

---

## FR-03 — Training Nomination Creation

An employee shall be able to create a training nomination.

The nomination shall contain required information such as:

* Training title
* Training provider
* Training description
* Training type
* Proposed training date
* Training duration
* Training cost, if applicable
* Business justification
* Employee information

The exact fields may be refined during implementation without changing the overall workflow.

---

## FR-04 — Draft Nomination

An employee shall be able to save an incomplete nomination as a draft.

Draft nominations shall not enter the reviewer workflow.

---

## FR-05 — Nomination Validation

The system shall validate:

* Required fields
* Data formats
* Allowed values
* Invalid or missing information

Invalid nominations shall not be submitted.

---

## FR-06 — Document Upload

An employee shall be able to attach supporting documents to a nomination.

The system shall validate:

* File type
* File size
* Required document presence

---

## FR-07 — Nomination Submission

The employee shall be able to submit a valid nomination.

On successful submission:

```text
DRAFT
  |
  | Submit
  v
SUBMITTED
```

The system shall generate:

* Unique nomination ID
* Submission timestamp
* Initial workflow status

---

## FR-08 — Reviewer Dashboard

A reviewer shall be able to view nominations requiring review.

The reviewer shall be able to:

* View pending nominations
* Open nomination details
* View supporting documents
* Start a review

---

## FR-09 — Review Workflow

When a reviewer starts reviewing a nomination:

```text
SUBMITTED
    |
    v
UNDER_REVIEW
```

The system shall record the review action.

---

## FR-10 — Approval

A reviewer shall be able to approve a nomination.

The workflow shall become:

```text
UNDER_REVIEW
      |
      | Approve
      v
  APPROVED
```

The system shall record:

* Reviewer
* Decision
* Timestamp

---

## FR-11 — Rejection

A reviewer shall be able to reject a nomination.

The workflow shall become:

```text
UNDER_REVIEW
      |
      | Reject
      v
  REJECTED
```

The reviewer shall be able to provide a rejection comment.

The system shall record:

* Reviewer
* Decision
* Comment
* Timestamp

---

## FR-12 — Status Tracking

Employees shall be able to view the current status of their nominations.

Supported statuses:

```text
DRAFT
SUBMITTED
UNDER_REVIEW
APPROVED
REJECTED
```

---

## FR-13 — Administrator Monitoring

Training Administrators shall be able to:

* View all nominations
* Filter nominations by status
* View nomination details
* View workflow history

---

## FR-14 — Audit History

The system shall record important workflow events.

Examples:

```text
Nomination Created
Nomination Submitted
Review Started
Nomination Approved
Nomination Rejected
```

Each event shall contain:

* Event ID
* Nomination ID
* User ID
* Event type
* Timestamp
* Optional metadata/comment

---

# 5. Non-Functional Requirements

## NFR-01 — Security

The application shall:

* Authenticate users.
* Enforce role-based authorization.
* Validate user input.
* Validate uploaded files.
* Protect passwords using secure hashing.
* Avoid storing sensitive information in plain text.
* Prevent unauthorized access to resources.

---

## NFR-02 — Reliability

The system should maintain consistent workflow state.

A nomination should not be able to transition to an invalid state.

For example:

```text
APPROVED
   |
   X
Reject
```

An already approved nomination cannot simply be rejected through a normal workflow action.

---

## NFR-03 — Maintainability

The application should use a modular architecture so that:

* API logic
* Business logic
* Database access
* Authentication
* File handling

are separated.

---

## NFR-04 — Testability

Core business logic should be independently testable.

The system should support:

* Unit testing
* API/integration testing
* Workflow testing

---

## NFR-05 — Performance

For the MVP:

* Normal API requests should respond within a reasonable time under local/test workloads.
* Database queries should be indexed where appropriate.
* File uploads should have size limits.

The MVP does not target high-scale production traffic.

---

## NFR-06 — Availability

The MVP should be deployable as a continuously running web application.

High availability, load balancing and multi-region deployment are outside the initial scope.

---

## NFR-07 — Observability

The application shall produce useful logs for:

* Application errors
* Authentication failures
* Important workflow events
* Deployment/runtime problems

---

# 6. Use-Case Diagram

The major actors and interactions are:

```text
                         +--------------------------------------+
                         | Training Nomination Workflow System |
                         |                                      |
Employee --------------->| (Login)                              |
   |                     |                                      |
   +-------------------->| (Create Nomination)                 |
   |                     |                                      |
   +-------------------->| (Upload Document)                    |
   |                     |                                      |
   +-------------------->| (Submit Nomination)                  |
   |                     |                                      |
   +-------------------->| (Track Status)                       |
                         |                                      |
Reviewer --------------->| (Login)                              |
   |                     |                                      |
   +-------------------->| (View Pending Nominations)           |
   |                     |                                      |
   +-------------------->| (Review Nomination)                  |
   |                     |                                      |
   +-------------------->| (Approve Nomination)                 |
   |                     |                                      |
   +-------------------->| (Reject Nomination)                  |
                         |                                      |
Training Admin --------->| (Login)                              |
   |                     |                                      |
   +-------------------->| (View All Nominations)               |
   |                     |                                      |
   +-------------------->| (Filter Nominations)                 |
   |                     |                                      |
   +-------------------->| (View Audit History)                 |
                         +--------------------------------------+
```

---

# 7. Use-Case Relationships

The main workflow can be represented as:

```text
Employee
   |
   +--> Login
   |
   +--> Create Nomination
   |         |
   |         +--> Upload Document
   |         |
   |         +--> Validate Data
   |
   +--> Submit Nomination
   |
   +--> Track Status


Reviewer
   |
   +--> Login
   |
   +--> View Pending Nominations
   |
   +--> Review Nomination
             |
             +--> Approve
             |
             +--> Reject


Training Administrator
   |
   +--> Login
   |
   +--> View All Nominations
   |
   +--> Filter Nominations
   |
   +--> View Audit History
```

---

# 8. High-Level Architecture

The MVP will use a **modular monolithic architecture**.

This is preferred over microservices because the application is small and the primary objective is to learn the complete software development and DevOps lifecycle.

```text
                    +----------------------+
                    |      User Browser    |
                    +----------+-----------+
                               |
                               | HTTP/HTTPS
                               v
                    +----------------------+
                    |        Nginx         |
                    | Reverse Proxy        |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    FastAPI Backend   |
                    |                      |
                    |  API Layer           |
                    |  Auth Layer          |
                    |  Business Logic      |
                    |  Validation          |
                    |  File Handling       |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
        +----------------+          +----------------+
        |  PostgreSQL    |          | File Storage   |
        |    Database    |          | Local / Disk   |
        +----------------+          +----------------+
                 |
                 v
        +----------------+
        | Audit Records  |
        +----------------+
```

---

# 9. Architecture Components

## 9.1 Frontend

The frontend will provide the user interface for:

* Login
* Nomination creation
* Nomination listing
* Reviewer dashboard
* Administrator dashboard
* Status tracking

For the MVP, the frontend will use:

* HTML
* CSS
* JavaScript

A lightweight frontend approach will be preferred to avoid unnecessary complexity.

---

# 9.2 Backend

The backend will use **Python + FastAPI**.

FastAPI will be responsible for:

* REST APIs
* Request validation
* Authentication
* Authorization
* Business logic
* Workflow transitions
* File handling
* Database interaction
* Error handling

---

# 9.3 Database

The primary database will be **PostgreSQL**.

It will store:

* Users
* Roles
* Training nominations
* Documents metadata
* Workflow history
* Audit events

---

# 9.4 Reverse Proxy

**Nginx** will be used as the reverse proxy.

Its responsibilities will include:

* Receiving HTTP/HTTPS traffic
* Forwarding requests to FastAPI
* Serving static assets where appropriate
* Providing a clear deployment boundary

---

# 9.5 Application Server

FastAPI will run using **Uvicorn**.

The deployment flow will therefore be:

```text
Client
   |
   v
Nginx
   |
   v
Uvicorn
   |
   v
FastAPI
   |
   v
PostgreSQL
```

---

# 10. Technology Stack

## 10.1 Programming Language

**Python 3.12+**

Python is selected because:

* It is already familiar to the development team.
* It has a mature web ecosystem.
* FastAPI provides strong API development capabilities.
* Python has excellent testing and automation support.
* It integrates naturally with DevOps tooling.

---

## 10.2 Backend Framework

**FastAPI**

Reasons:

* Modern Python web framework
* Automatic API documentation
* Built-in request validation through Pydantic
* Good support for asynchronous operations
* Simple REST API development
* Strong developer experience

---

## 10.3 Frontend

Initial MVP:

* HTML
* CSS
* JavaScript
* Jinja2 templates where server-side rendering is useful

A separate React frontend is intentionally excluded from the initial architecture to keep the MVP focused.

---

## 10.4 Database

**PostgreSQL**

Reasons:

* Reliable relational database
* Strong transaction support
* Suitable for workflow-oriented data
* Good Python integration
* Easy to run locally
* Appropriate for future scaling

---

## 10.5 ORM / Database Access

**SQLAlchemy**

SQLAlchemy will be used to:

* Define database models
* Execute database operations
* Manage relationships
* Abstract database access from business logic

---

## 10.6 Database Migration

**Alembic**

Alembic will manage:

* Schema creation
* Schema changes
* Versioned migrations
* Reproducible database setup

---

## 10.7 Validation

**Pydantic**

Pydantic will be used for:

* API request validation
* API response schemas
* Data type validation
* Configuration validation

---

## 10.8 Authentication

The MVP will use:

* Password hashing
* Token/session-based authentication
* Role-based authorization

The exact authentication implementation can be finalized during implementation.

Enterprise SSO is outside the MVP.

---

## 10.9 Testing

The testing stack will use:

* Pytest
* FastAPI TestClient
* HTTP/API integration tests

Testing layers:

```text
Unit Tests
    |
    v
Service / Business Logic Tests
    |
    v
API Tests
    |
    v
Integration Tests
    |
    v
End-to-End Workflow Tests
```

---

# 11. Build and Dependency Management

The original project requirement mentions:

```text
Maven / Gradle / Ant
```

These tools are primarily associated with the Java ecosystem and are **not appropriate for the selected Python stack**.

Therefore, the project will not use Maven, Gradle or Ant.

The Python equivalent will be:

```text
Python
   |
   +--> pip
   |
   +--> requirements.txt
   |
   +--> virtual environment
```

Optionally, a modern Python dependency manager such as `uv` may be introduced later if it provides a clear DevOps benefit.

For the initial MVP, **pip + requirements.txt + virtual environment** will be used to keep the setup simple and transparent.

---

# 12. Database Model

The minimum database model will contain the following entities:

```text
+----------------+
|     USERS      |
+----------------+
| id             |
| name           |
| email          |
| password_hash  |
| role_id        |
| created_at     |
+-------+--------+
        |
        | belongs to
        v
+----------------+
|     ROLES      |
+----------------+
| id             |
| name           |
+----------------+


+-------------------------+
| TRAINING_NOMINATIONS    |
+-------------------------+
| id                      |
| employee_id             |
| title                   |
| provider                |
| description             |
| training_type           |
| training_date           |
| duration                |
| cost                    |
| justification            |
| status                  |
| created_at              |
| submitted_at            |
| updated_at              |
+-----------+-------------+
            |
            +----------------------+
            |                      |
            v                      v
+----------------------+   +----------------------+
|      DOCUMENTS       |   |    AUDIT_EVENTS      |
+----------------------+   +----------------------+
| id                   |   | id                   |
| nomination_id        |   | nomination_id        |
| file_name            |   | user_id              |
| file_path            |   | event_type           |
| file_type            |   | comment              |
| file_size            |   | timestamp            |
| uploaded_at          |   +----------------------+
+----------------------+
```

---

# 13. Entity Relationships

The primary relationships are:

```text
ROLE
  |
  | 1
  |
  | N
USER
  |
  | 1
  |
  | N
TRAINING_NOMINATION
  |
  +-------------------+
  |                   |
  | 1                 | 1
  |                   |
  N                   N
DOCUMENT          AUDIT_EVENT
```

Additional relationship:

```text
USER
 |
 +---- Employee creates nomination
 |
 +---- Reviewer performs review
 |
 +---- Admin monitors workflow
```

---

# 14. Database Tables

## 14.1 users

| Column        | Type           | Description           |
| ------------- | -------------- | --------------------- |
| id            | UUID / Integer | Primary key           |
| name          | VARCHAR        | User name             |
| email         | VARCHAR        | Unique email          |
| password_hash | VARCHAR        | Secure password hash  |
| role_id       | FK             | User role             |
| created_at    | TIMESTAMP      | Account creation time |

---

## 14.2 roles

| Column | Type    | Description                 |
| ------ | ------- | --------------------------- |
| id     | Integer | Primary key                 |
| name   | VARCHAR | Employee / Reviewer / Admin |

---

## 14.3 training_nominations

| Column        | Type           | Description            |
| ------------- | -------------- | ---------------------- |
| id            | UUID / Integer | Primary key            |
| employee_id   | FK             | Employee who submitted |
| title         | VARCHAR        | Training title         |
| provider      | VARCHAR        | Training provider      |
| description   | TEXT           | Training description   |
| training_type | VARCHAR        | Type of training       |
| training_date | DATE           | Proposed date          |
| duration      | VARCHAR        | Training duration      |
| cost          | DECIMAL        | Training cost          |
| justification | TEXT           | Business justification |
| status        | VARCHAR        | Workflow status        |
| created_at    | TIMESTAMP      | Creation timestamp     |
| submitted_at  | TIMESTAMP      | Submission timestamp   |
| updated_at    | TIMESTAMP      | Last update            |

---

## 14.4 documents

| Column        | Type           | Description          |
| ------------- | -------------- | -------------------- |
| id            | UUID / Integer | Primary key          |
| nomination_id | FK             | Related nomination   |
| file_name     | VARCHAR        | Original filename    |
| file_path     | VARCHAR        | Stored file location |
| file_type     | VARCHAR        | File type            |
| file_size     | Integer        | File size            |
| uploaded_at   | TIMESTAMP      | Upload time          |

---

## 14.5 audit_events

| Column        | Type           | Description        |
| ------------- | -------------- | ------------------ |
| id            | UUID / Integer | Primary key        |
| nomination_id | FK             | Related nomination |
| user_id       | FK             | User responsible   |
| event_type    | VARCHAR        | Event performed    |
| comment       | TEXT           | Optional comment   |
| timestamp     | TIMESTAMP      | Event time         |

---

# 15. Workflow State Model

The backend will enforce valid state transitions.

```text
                    +---------+
                    |  DRAFT  |
                    +----+----+
                         |
                         | Submit
                         v
                    +---------+
                    |SUBMITTED|
                    +----+----+
                         |
                         | Start Review
                         v
                  +--------------+
                  | UNDER_REVIEW |
                  +------+-------+
                         |
                +--------+--------+
                |                 |
             Approve            Reject
                |                 |
                v                 v
          +-----------+     +-----------+
          | APPROVED  |     | REJECTED |
          +-----------+     +-----------+
```

Invalid transitions will be rejected by the business logic.

---

# 16. API Design

The backend will expose REST APIs.

## 16.1 Authentication APIs

### POST `/api/auth/login`

Authenticate a user.

### POST `/api/auth/logout`

End the authenticated session/token.

### GET `/api/auth/me`

Return the currently authenticated user's information.

---

# 17. Nomination APIs

### POST `/api/nominations`

Create a new nomination.

### GET `/api/nominations`

Return nominations visible to the authenticated user.

### GET `/api/nominations/{id}`

Return nomination details.

### PUT `/api/nominations/{id}`

Update a draft nomination.

### POST `/api/nominations/{id}/submit`

Submit a nomination.

---

# 18. Document APIs

### POST `/api/nominations/{id}/documents`

Upload a supporting document.

### GET `/api/nominations/{id}/documents`

List documents associated with a nomination.

### GET `/api/documents/{id}`

Retrieve/download a permitted document.

---

# 19. Reviewer APIs

### GET `/api/reviewer/nominations`

Return nominations requiring reviewer attention.

### POST `/api/nominations/{id}/review`

Start the review process.

### POST `/api/nominations/{id}/approve`

Approve a nomination.

### POST `/api/nominations/{id}/reject`

Reject a nomination.

Request body:

```json
{
  "comment": "Training does not meet the current eligibility criteria."
}
```

---

# 20. Status and Audit APIs

### GET `/api/nominations/{id}/status`

Return the current nomination status.

### GET `/api/nominations/{id}/history`

Return workflow history and important audit events.

---

# 21. Administration APIs

### GET `/api/admin/nominations`

Return all nominations for administrators.

### GET `/api/admin/nominations?status=SUBMITTED`

Filter nominations by status.

### GET `/api/admin/audit-events`

Return audit events accessible to administrators.

---

# 22. API Workflow Example

## Employee Submission

```text
POST /api/nominations
        |
        v
Create DRAFT
        |
        v
POST /api/nominations/{id}/documents
        |
        v
Validate Document
        |
        v
POST /api/nominations/{id}/submit
        |
        v
SUBMITTED
```

---

## Reviewer Approval

```text
GET /api/reviewer/nominations
        |
        v
GET /api/nominations/{id}
        |
        v
POST /api/nominations/{id}/review
        |
        v
UNDER_REVIEW
        |
        v
POST /api/nominations/{id}/approve
        |
        v
APPROVED
```

---

## Reviewer Rejection

```text
GET /api/nominations/{id}
        |
        v
POST /api/nominations/{id}/review
        |
        v
UNDER_REVIEW
        |
        v
POST /api/nominations/{id}/reject
        |
        v
REJECTED
```

---

# 23. Application Layering

The backend will use a layered structure.

```text
                API / ROUTER LAYER
                        |
                        v
              SERVICE / BUSINESS LAYER
                        |
                        v
                 DATA ACCESS LAYER
                        |
                        v
                    DATABASE
```

### API Layer

Responsible for:

* HTTP endpoints
* Request parsing
* Authentication dependencies
* Response formatting

### Service Layer

Responsible for:

* Nomination workflow
* Validation rules
* Approval/rejection logic
* Status transitions
* Audit event generation

### Data Access Layer

Responsible for:

* Database queries
* CRUD operations
* Transaction handling

### Model Layer

Responsible for:

* SQLAlchemy database models
* Pydantic request/response schemas

---

# 24. Proposed Project Structure

```text
training-nomination-workflow/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── nominations.py
│   │   ├── reviewer.py
│   │   ├── admin.py
│   │   └── documents.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── nomination.py
│   │   ├── document.py
│   │   └── audit_event.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── nomination.py
│   │   ├── document.py
│   │   └── review.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── nomination_service.py
│   │   ├── document_service.py
│   │   ├── review_service.py
│   │   └── audit_service.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── migrations/
│   │
│   └── templates/
│       ├── login.html
│       ├── employee/
│       ├── reviewer/
│       └── admin/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── uploads/
│
├── requirements.txt
├── .env.example
├── .gitignore
├── alembic.ini
├── README.md
└── Dockerfile
```

---

# 25. Local Development Architecture

The initial development environment will be:

```text
Developer Machine
        |
        +----------------+
        |                |
        v                v
   FastAPI App       PostgreSQL
        |
        v
     Uvicorn
```

The developer will run:

```text
Browser
   |
   v
localhost
   |
   v
FastAPI
   |
   v
PostgreSQL
```

Nginx will be introduced during deployment-oriented development.

---

# 26. Local Technology Requirements

The developer machine should have:

* Python 3.12+
* pip
* Git
* PostgreSQL
* Code editor / IDE
* Browser
* Optional Docker installation

---

# 27. Python Virtual Environment

The project will use an isolated Python environment.

Conceptually:

```text
Operating System
      |
      v
Python 3.12+
      |
      v
Virtual Environment
      |
      +------------------------+
      |                        |
 FastAPI                  Project Dependencies
 SQLAlchemy               Pytest
 Pydantic                 Alembic
 Uvicorn                  PostgreSQL Driver
```

This prevents project dependencies from interfering with system Python packages.

---

# 28. Dependency Management

The initial dependency file will contain packages such as:

```text
fastapi
uvicorn
sqlalchemy
alembic
psycopg
pydantic
python-multipart
pytest
httpx
passlib / compatible password hashing library
```

The exact versions will be pinned after the initial environment is verified.

---

# 29. Environment Configuration

Configuration should not be hard-coded into source code.

An environment configuration file will contain values such as:

```text
DATABASE_URL
SECRET_KEY
UPLOAD_DIRECTORY
APPLICATION_ENV
```

A `.env.example` file will document required configuration without containing real secrets.

Example:

```text
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/training_nomination
SECRET_KEY=<development-secret>
UPLOAD_DIRECTORY=uploads/
APPLICATION_ENV=development
```

Actual secrets will not be committed to Git.

---

# 30. Local Setup Flow

The initial local setup will follow:

```text
Clone Repository
       |
       v
Create Python Virtual Environment
       |
       v
Activate Environment
       |
       v
Install Dependencies
       |
       v
Configure Environment Variables
       |
       v
Create PostgreSQL Database
       |
       v
Run Database Migrations
       |
       v
Start FastAPI Application
       |
       v
Open Browser
       |
       v
Application Running
```

---

# 31. Local Application Startup

The development server will use Uvicorn.

Conceptually:

```text
Uvicorn
   |
   v
FastAPI Application
   |
   +----> PostgreSQL
   |
   +----> File Storage
```

The application will expose:

```text
http://localhost:<port>
```

FastAPI's automatically generated API documentation will also be available during development.

---

# 32. Deployment Architecture

The initial deployment architecture will be:

```text
                  INTERNET / CLIENT
                         |
                         v
                +----------------+
                |     NGINX      |
                | Reverse Proxy  |
                +-------+--------+
                        |
                        v
                +----------------+
                |    Uvicorn     |
                | App Server     |
                +-------+--------+
                        |
                        v
                +----------------+
                |    FastAPI     |
                | Application    |
                +-------+--------+
                        |
              +---------+---------+
              |                   |
              v                   v
       +-------------+     +-------------+
       | PostgreSQL  |     | File Storage|
       +-------------+     +-------------+
```

---

# 33. Why Nginx Instead of Tomcat?

The original requirement mentions:

```text
Tomcat / Nginx
```

Tomcat is primarily used for Java servlet-based applications.

Since this project uses Python + FastAPI:

```text
Java Application
     |
     v
Tomcat
```

is not appropriate.

For the Python architecture:

```text
Client
  |
  v
Nginx
  |
  v
Uvicorn
  |
  v
FastAPI
```

is the appropriate deployment model.

Therefore, **Nginx is selected as the deployment/reverse-proxy target**.

---

# 34. File Storage Strategy

For the MVP, uploaded documents will be stored using local filesystem storage.

```text
Training Nomination
        |
        v
Document Upload
        |
        v
Validation
        |
        v
Local File Storage
        |
        v
Database stores metadata
```

The database will store metadata rather than the complete file contents.

Example:

```text
Database
---------
file_name
file_type
file_size
file_path
uploaded_at
nomination_id
```

Cloud object storage can be introduced later if required.

---

# 35. Security Architecture

The minimum security flow will be:

```text
User
 |
 v
Login
 |
 v
Credential Validation
 |
 v
Authenticated Identity
 |
 v
Role Check
 |
 +----------------------+
 |                      |
Authorized          Unauthorized
 |                      |
 v                      v
Access Resource      Reject Request
```

The application must also enforce authorization at the backend rather than relying only on frontend visibility.

For example:

```text
Employee
   |
   X
Approve Nomination
```

must be rejected even if the employee manually sends the approval API request.

---

# 36. Document Validation Flow

```text
Upload File
     |
     v
Check File Exists
     |
     v
Check File Size
     |
     v
Check File Type
     |
     v
Check Allowed Extension
     |
     +------------+
     |            |
   Invalid       Valid
     |            |
     v            v
  Reject       Store File
                  |
                  v
           Store Metadata
```

---

# 37. Nomination Submission Flow

```text
Employee
    |
    v
Create Draft
    |
    v
Enter Details
    |
    v
Upload Documents
    |
    v
Validate Data
    |
    +----------------+
    |                |
  Invalid           Valid
    |                |
    v                v
Show Errors       Validate Files
                       |
                       +----------+
                       |          |
                    Invalid      Valid
                       |          |
                       v          v
                    Reject      Submit
                                  |
                                  v
                              SUBMITTED
                                  |
                                  v
                            Create Audit Event
```

---

# 38. Reviewer Workflow

```text
Reviewer Login
      |
      v
Reviewer Dashboard
      |
      v
Pending Nominations
      |
      v
Select Nomination
      |
      v
View Details + Documents
      |
      v
Start Review
      |
      v
UNDER_REVIEW
      |
      +-------------------+
      |                   |
   APPROVE              REJECT
      |                   |
      v                   v
 APPROVED              REJECTED
      |                   |
      +---------+---------+
                |
                v
          Audit Event
```

---

# 39. Administrator Workflow

```text
Admin Login
     |
     v
Admin Dashboard
     |
     +-----------------------+
     |                       |
     v                       v
View All Nominations     Filter by Status
     |                       |
     +-----------+-----------+
                 |
                 v
          View Nomination
                 |
                 v
          View Audit History
```

---

# 40. Error Handling Strategy

The API will return appropriate HTTP responses.

Examples:

| Situation                   | HTTP Response |
| --------------------------- | ------------: |
| Successful request          |     200 / 201 |
| Invalid request data        |           400 |
| Authentication required     |           401 |
| Insufficient permissions    |           403 |
| Resource not found          |           404 |
| Invalid workflow transition |           409 |
| Unexpected server failure   |           500 |

The API should return structured error responses rather than exposing internal implementation details.

---

# 41. Logging Strategy

The application will maintain structured logs for:

### Application Events

* Application startup
* Application shutdown
* Configuration problems

### Security Events

* Failed login
* Unauthorized access attempts

### Workflow Events

* Nomination submission
* Review started
* Approval
* Rejection

### Error Events

* Database errors
* File upload errors
* Unexpected application exceptions

Sensitive information such as passwords and authentication secrets must never be logged.

---

# 42. Testing Architecture

Testing will occur at multiple levels.

```text
                  Application
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
      Unit          API Tests     Integration
      Tests                         Tests
        |              |              |
        +--------------+--------------+
                       |
                       v
                Workflow Tests
                       |
                       v
                 End-to-End
```

### Unit Tests

Test isolated business logic.

Examples:

* Validation rules
* Status transitions
* Permission checks

### API Tests

Test REST endpoints.

Examples:

* Login
* Create nomination
* Submit nomination
* Approve nomination
* Reject nomination

### Integration Tests

Test:

```text
FastAPI
   +
PostgreSQL
```

### End-to-End Tests

Test the complete workflow:

```text
Employee Submission
       ↓
Reviewer Review
       ↓
Approval/Rejection
       ↓
Status Tracking
```

---

# 43. CI/CD Technical Flow

Once the application is developed, the CI/CD pipeline will follow:

```text
Developer
    |
    v
Git Push
    |
    v
CI Pipeline
    |
    +-------------------+
    |                   |
    v                   v
Install Dependencies   Static Checks
    |                   |
    +---------+---------+
              |
              v
           Build
              |
              v
        Run Unit Tests
              |
              v
       Run API Tests
              |
              v
     Integration Tests
              |
              v
       Pipeline Success
              |
              v
      Build Deployment
              |
              v
           Deploy
              |
              v
        Health Check
```

---

# 44. Architecture Decision Summary

| Decision              | Selected Technology / Approach | Reason                                        |
| --------------------- | ------------------------------ | --------------------------------------------- |
| Language              | Python 3.12+                   | Familiar, productive, strong ecosystem        |
| Backend               | FastAPI                        | Lightweight REST API framework                |
| Frontend              | HTML/CSS/JavaScript            | Keeps MVP simple                              |
| Templates             | Jinja2                         | Simple server-rendered UI where needed        |
| Database              | PostgreSQL                     | Reliable relational database                  |
| ORM                   | SQLAlchemy                     | Python database abstraction                   |
| Migration             | Alembic                        | Version-controlled schema changes             |
| Validation            | Pydantic                       | Strong request/data validation                |
| Application Server    | Uvicorn                        | Native ASGI server for FastAPI                |
| Reverse Proxy         | Nginx                          | Suitable Python deployment boundary           |
| Build/Dependency Tool | pip + requirements.txt         | Python-native and simple                      |
| Testing               | Pytest                         | Standard Python testing framework             |
| API Testing           | FastAPI TestClient / HTTPX     | API integration testing                       |
| File Storage          | Local filesystem               | Sufficient for MVP                            |
| Architecture          | Modular monolith               | Appropriate for small MVP                     |
| Authentication        | Token/session-based            | Simple MVP authentication                     |
| CI/CD                 | Git-based CI pipeline          | Automated validation and deployment           |
| Containerization      | Optional Docker                | Can be introduced for reproducible deployment |

---

# 45. Architecture Principles

The system will follow these principles:

### Principle 1 — Keep the MVP Simple

Do not introduce microservices, Kubernetes or distributed infrastructure without a demonstrated requirement.

### Principle 2 — Separate Responsibilities

API, business logic, database access and infrastructure concerns should remain separated.

### Principle 3 — Validate at the Backend

Frontend validation improves user experience, but backend validation is authoritative.

### Principle 4 — Make Workflow State Explicit

Nomination states and transitions must be controlled by the backend.

### Principle 5 — Make Changes Traceable

Important workflow actions should generate audit events.

### Principle 6 — Automate Repetitive Work

Build, testing and deployment should gradually become automated through CI/CD.

### Principle 7 — Design for Learning

The architecture should allow the team to understand every layer rather than hiding complexity behind unnecessary frameworks.

---

# 46. Initial Local Setup Checklist

Before development begins, the following should be available:

```text
[ ] Git installed
[ ] Python 3.12+ installed
[ ] PostgreSQL installed
[ ] Code editor configured
[ ] Python virtual environment created
[ ] Git repository cloned
[ ] requirements.txt created
[ ] Dependencies installed
[ ] PostgreSQL database created
[ ] Environment variables configured
[ ] Alembic configured
[ ] Initial database migration created
[ ] FastAPI application starts
[ ] Database connection verified
[ ] Basic API endpoint verified
[ ] Tests execute successfully
```

---

# 47. Initial Technical Milestone

The first technical milestone is not the complete application.

It is:

```text
Git Repository
      |
      v
Python Environment
      |
      v
FastAPI Application
      |
      v
PostgreSQL Connection
      |
      v
SQLAlchemy Models
      |
      v
Alembic Migration
      |
      v
Basic API
      |
      v
Automated Test
```

Once this foundation works, feature development can begin.

---

# 48. Final Architecture

The complete MVP architecture can be summarized as:

```text
                         USERS
                           |
                           v
                    +-------------+
                    |   Browser   |
                    +------+------+
                           |
                           | HTTP/HTTPS
                           v
                    +-------------+
                    |    Nginx    |
                    | Reverse     |
                    | Proxy       |
                    +------+------+
                           |
                           v
                    +-------------+
                    |   Uvicorn   |
                    +------+------+
                           |
                           v
              +-------------------------+
              |        FastAPI          |
              |                         |
              | Authentication          |
              | Authorization           |
              | API Routes              |
              | Validation              |
              | Business Logic          |
              | Workflow Management     |
              | Document Handling       |
              | Audit Management        |
              +-----------+-------------+
                          |
             +------------+------------+
             |                         |
             v                         v
      +-------------+           +-------------+
      | PostgreSQL  |           | File System |
      |             |           |             |
      | Users       |           | Documents   |
      | Roles       |           |             |
      | Nominations |           +-------------+
      | Documents   |
      | Audit       |
      +-------------+
```

---

# 49. Task 3 Deliverables Summary

| Deliverable                 | Status   |
| --------------------------- | -------- |
| SRS Summary                 | Defined  |
| Functional Requirements     | Defined  |
| Non-Functional Requirements | Defined  |
| Use-Case Diagram            | Defined  |
| Application Architecture    | Defined  |
| Technology Stack            | Selected |
| Database Model              | Defined  |
| Entity Relationships        | Defined  |
| API List                    | Defined  |
| Workflow State Model        | Defined  |
| Security Architecture       | Defined  |
| Document Validation Flow    | Defined  |
| Testing Architecture        | Defined  |
| Local Development Setup     | Defined  |
| Deployment Architecture     | Defined  |
| Project Structure           | Defined  |
| Build/Dependency Strategy   | Defined  |
| CI/CD Technical Flow        | Defined  |

---

# 50. Final Technical Definition

The **Training Nomination Workflow MVP** will be implemented as a **Python-based modular monolithic web application**.

The core stack is:

```text
Python 3.12+
      |
      v
FastAPI
      |
      +---- SQLAlchemy
      |
      +---- Pydantic
      |
      +---- Alembic
      |
      v
PostgreSQL

Deployment:

Client
  |
  v
Nginx
  |
  v
Uvicorn
  |
  v
FastAPI
  |
  +---- PostgreSQL
  |
  +---- Local File Storage
```

The system will support the complete MVP workflow:

```text
Employee
   |
   v
Create Training Nomination
   |
   v
Validate Data
   |
   v
Upload & Validate Document
   |
   v
Submit
   |
   v
SUBMITTED
   |
   v
Reviewer
   |
   v
UNDER_REVIEW
   |
   +----------------+
   |                |
Approve           Reject
   |                |
   v                v
APPROVED         REJECTED
   |                |
   +-------+--------+
           |
           v
      Status Tracking
           |
           v
      Audit History
```

This architecture provides the minimum technical foundation required to implement the approved 15-week MVP while also creating a practical environment for learning the complete DevOps lifecycle:

```text
Requirements
     ↓
Architecture
     ↓
Development
     ↓
Testing
     ↓
Build
     ↓
CI
     ↓
Deployment
     ↓
Operations
     ↓
Logging / Monitoring
     ↓
Feedback
     ↓
Backlog
     ↺
```

The system is intentionally designed as a **small, understandable and deployable MVP**, with complexity added only when a concrete requirement justifies it.
