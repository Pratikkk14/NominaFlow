# Task 1 — Problem Definition and Scope

## 1. Problem Statement

The Training Nomination Workflow currently relies heavily on manual coordination between employees, reviewers and training administrators. Training requests may be submitted through forms or email, supporting documents may be exchanged separately, validation may be performed manually, and approval decisions may not be reflected in a single source of truth.

This fragmented process can result in incomplete submissions, duplicated data entry, delayed approvals, unclear ownership, difficulty tracking request status and limited visibility into the overall training nomination pipeline.

The proposed Training Nomination Workflow MVP will provide a centralized web-based system through which employees can submit training nominations, validate required information and documents, reviewers can approve or reject requests, and users can track the current status of their requests.

The goal is not to build a complete enterprise Learning Management System, but to create a small, reliable and auditable workflow that demonstrates how software engineering, Agile practices and DevOps can improve a real organizational process.

---

## 2. Target Users

| User | Responsibilities |
|---|---|
| Employee / Nominee | Creates and submits training nominations and tracks their status |
| Reviewer / Manager | Reviews submitted nominations and approves or rejects requests |
| Training Administrator | Monitors nominations and overall workflow status |

---

## 3. Stakeholders

### Primary Stakeholders

1. Employees
2. Managers / Reviewers
3. Training / HR Administrators

### Secondary Stakeholders

4. IT / DevOps Team
5. Project Sponsor / Business Owner
6. Security / Compliance Stakeholders

### Development Stakeholders

7. Development Team
8. QA / Testing Team
9. DevOps / Deployment Team

---

## 4. Existing Pain Points

### P1 — Fragmented Submission
Training information and supporting documents may be submitted through different communication channels.

### P2 — Manual Validation
Required fields, supporting documents and submitted information may need to be manually checked.

### P3 — Approval Delays
Requests can remain pending without clear visibility into who is responsible for the next action.

### P4 — Poor Status Visibility
Employees may need to contact reviewers or administrators to determine the status of their training request.

### P5 — Duplicate Data Entry
Information may need to be copied between emails, spreadsheets and other records.

### P6 — Difficult Workflow Tracking
Administrators may not have a centralized view of requests and their current states.

### P7 — Limited Auditability
It may be difficult to determine who submitted, reviewed or modified a request and when those actions occurred.

---

## 5. Objectives

The MVP will have the following objectives:

1. **Centralize Training Nomination Submission**  
   Provide a single platform where employees can create and submit training requests.

2. **Validate Requests**  
   Validate required information and supporting documents before accepting a nomination.

3. **Digitize the Review Process**  
   Allow reviewers to view pending nominations and approve or reject them.

4. **Provide Status Visibility**  
   Allow employees and administrators to view the current status of training nominations.

5. **Maintain Basic Auditability**  
   Record important workflow actions, timestamps and decisions for traceability.

---

## 6. Measurable Success Criteria

| Metric | MVP Target |
|---|---:|
| Valid request submission completion | ≥ 95% of valid test submissions |
| Required-field validation | 100% of required fields validated |
| Invalid submission prevention | 100% of deliberately invalid test cases rejected |
| Status accuracy | 100% of workflow transitions correctly reflected |
| Reviewer decision recording | 100% of approval/rejection actions persisted |
| Request traceability | Every request has a unique ID and timestamps |
| Critical workflow tests | ≥ 90% pass rate |
| Local deployment | Application can be deployed using documented steps |
| Build reproducibility | Clean checkout results in a successful build |
| CI pipeline | Automated build and test execution |

> These targets represent MVP engineering success criteria and are not claims about an existing organization's current performance.

---

## 7. Constraints

### Time Constraint
- Total project duration: **15 weeks**

### Scope Constraint
- The system will focus only on the **Training Nomination Workflow**.
- It will not attempt to become a complete Learning Management System.

### User Constraint
The MVP will initially support three roles:

- Employee
- Reviewer
- Training Administrator

### Authentication Constraint
- Basic application-level authentication and role-based authorization will be implemented.
- Enterprise SSO is outside the initial MVP scope.

### Document Constraint
- The system will support basic document upload and validation.
- Advanced AI-based document understanding is outside the MVP.

### Deployment Constraint
- Development will initially be performed locally.
- Deployment will use a simple web-server/application-server setup.

### Security Constraint
The MVP will implement baseline security practices including:

- Authentication
- Role-based authorization
- Input validation
- File validation
- Password protection
- Basic audit logging

Enterprise-level compliance and security infrastructure are outside the MVP.

---

# 8. Approved MVP Scope

## 8.1 Employee Features

The Employee / Nominee will be able to:

- Log in to the system
- Create a training nomination
- Enter required training details
- Upload supporting documents
- Submit a nomination
- View previously submitted nominations
- Track nomination status

---

## 8.2 Reviewer Features

The Reviewer / Manager will be able to:

- Log in to the system
- View pending nominations
- Open nomination details
- View supporting documents
- Approve a nomination
- Reject a nomination
- Add a review comment

---

## 8.3 Training Administrator Features

The Training Administrator will be able to:

- View all nominations
- Filter nominations by status
- View nomination details
- Monitor the workflow
- View basic request history and audit information

---

## 8.4 System Features

The system will provide:

- Authentication
- Role-based authorization
- Input validation
- Document validation
- Unique request ID generation
- Workflow state management
- Timestamp recording
- Audit history
- Database persistence

---

# 9. MVP Workflow

The core workflow will be:

```text
Employee
    |
    | Create Nomination
    v
+----------------------+
| Training Nomination  |
| Request              |
+----------+-----------+
           |
           v
    Data Validation
           |
           v
   Document Validation
           |
           v
       Submitted
           |
           v
      Under Review
           |
      +----+----+
      |         |
   Approve    Reject
      |         |
      v         v
  Approved   Rejected
      |         |
      +----+----+
           |
           v
    Status Tracking
```

# 10. MVP Workflow States

The initial workflow will use the following states:

```text
DRAFT
  |
  | Submit
  v
SUBMITTED
  |
  | Reviewer starts review
  v
UNDER_REVIEW
  |
  +----------------+
  |                |
Approve          Reject
  |                |
  v                v
APPROVED         REJECTED
```

State Definations:
| State        | Description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| DRAFT        | Nomination is being created and has not yet been submitted                 |
| SUBMITTED    | Nomination has passed initial validation and has been submitted for review |
| UNDER_REVIEW | Reviewer is currently reviewing the nomination                             |
| APPROVED     | Reviewer has approved the nomination                                       |
| REJECTED     | Reviewer has rejected the nomination                                       |


For the initial MVP, rejected nominations will remain in the `REJECTED` state. Resubmission will be considered as a future enhancement.

# 11. Core Use Cases

The MVP will contain the following primary use cases:

| ID    | Use Case                    |
| ----- | --------------------------- |
| UC-01 | User Login                  |
| UC-02 | Create Training Nomination  |
| UC-03 | Upload Supporting Document  |
| UC-04 | Submit Nomination           |
| UC-05 | Validate Nomination         |
| UC-06 | Review Nomination           |
| UC-07 | Approve / Reject Nomination |
| UC-08 | Track Nomination Status     |
| UC-09 | Monitor All Nominations     |

# 12. Out of Scope for MVP

The following features are explicitly excluded from the 15-week MVP:

- Complete Learning Management System
- Course delivery
- Online training
- Payment processing
- Training attendance tracking
- Certificate management
- AI-based training recommendations
- AI-based document interpretation
- Complex workflow designer
- Multi-level approval hierarchy
- Enterprise SSO
- Native mobile application
- Advanced analytics and BI dashboards
- Complex notification engine
- Microservices architecture
- Kubernetes-based deployment
- Multi-region deployment

These may be considered as future enhancements after the MVP.

13. 15-Week MVP Boundary

By the end of the 15-week project, the system should provide:
Working Web Application
        +
Database
        +
Authentication
        +
Role-Based Access
        +
Training Nomination Submission
        +
Data & Document Validation
        +
Reviewer Approval / Rejection
        +
Status Tracking
        +
Audit History
        +
Automated Tests
        +
CI Pipeline
        +
Deployment
        +
Basic Logging / Monitoring
        +
Technical Documentation

# 14. Final MVP Definition

The Training Nomination Workflow MVP is a centralized web application that enables an employee to submit a training nomination with supporting information, validates the submission, routes it to a reviewer, records an approval or rejection decision, and allows employees and administrators to track the request throughout its lifecycle.

The MVP is intentionally limited to the core nomination workflow so that the complete system can be designed, developed, tested, deployed and operated within a 15-week DevOps project.