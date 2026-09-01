# DevOps Workflow, Branching Strategy & Engineering Conventions

## 1. DevOps Lifecycle Flow

NominaFlow applies continuous integration and progressive delivery principles across its development lifecycle:

```text
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  GitHub Issue   ├────►│ Feature Branch  ├────►│  Local Testing  │
│ (User Story/Bug)│     │  (feat/issue-x) │     │ (Pytest/Linters)│
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Pull Request    │◄────┤  Git Commit     │◄────┤ Clean Working   │
│(Template/Checks)│     │ (Conventional)  │     │ Tree Validation │
└────────┬────────┘     └─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ CI Verification ├────►│  Code Review &  ├────►│ Merge to develop│
│ (Build & Tests) │     │    Approval     │     │ (or main)       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 2. Git Branching Strategy

The repository follows a structured branch model:

```text
main ───────────────────────────────────────────────────────────── (Production Releases)
  │
  └─► develop ─────────────────────────────────────────────────── (Integration)
        │
        ├─► feature/<short-description> ──────────────────────── (New Features)
        ├─► bugfix/<short-description> ───────────────────────── (Bug Fixes)
        ├─► docs/<short-description> ─────────────────────────── (Documentation)
        ├─► refactor/<short-description> ─────────────────────── (Refactoring)
        └─► test/<short-description> ─────────────────────────── (Testing Improvements)
```

### Branch Responsibilities

| Branch Type | Target Base | Purpose | Example |
|---|---|---|---|
| `main` | - | Stable, production-ready release branch | `main` |
| `develop` | `main` | Integration branch for actively developed features | `develop` |
| `feature/*` | `develop` | Implementation of new functional capabilities | `feature/auth-jwt-handler` |
| `bugfix/*` | `develop` | Remediation of defects discovered in testing | `bugfix/fix-null-date-validation` |
| `docs/*` | `develop` / `main` | Documentation updates, architecture notes | `docs/add-api-contract-specs` |
| `refactor/*`| `develop` | Code restructuring without behavior change | `refactor/modularize-db-session` |
| `test/*` | `develop` | Addition of test cases or test infrastructure | `test/add-workflow-fsm-tests` |

---

## 3. Conventional Commit Conventions

Commit messages must follow the Conventional Commits specification:

```text
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

### Allowed Types

* `feat`: A new user-facing or API feature
* `fix`: A bug fix
* `docs`: Documentation only changes
* `style`: Changes that do not affect the meaning of the code (white-space, formatting)
* `refactor`: A code change that neither fixes a bug nor adds a feature
* `perf`: A code change that improves performance
* `test`: Adding missing tests or correcting existing tests
* `chore`: Changes to the build process or auxiliary tools and libraries
* `ci`: Changes to CI configuration files and scripts

### Examples
* `feat(auth): implement jwt token generation and validation`
* `fix(validation): enforce maximum document file size of 5mb`
* `docs(readme): update local development setup instructions`
* `chore(deps): update fastapi and uvicorn dependencies`
* `test(nomination): add test cases for state machine transitions`
