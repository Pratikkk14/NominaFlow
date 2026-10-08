# Week 7 Deliverable Report — Jenkins CI Installation, Multibranch Pipeline & Ephemeral Agent Integration

> **Course**: DevOps Lab Mini Project  
> **Project**: NominaFlow — Training Nomination Workflow System  
> **Milestone**: Week 7 — Jenkins CI Multibranch Pipeline Setup, Ephemeral Docker Agent Orchestration, and Automated Test Execution  
> **Repository**: [https://github.com/Pratikkk14/NominaFlow](https://github.com/Pratikkk14/NominaFlow)  

---

## 1. Executive Summary

In **Week 7**, we designed, configured, and validated the **Continuous Integration (CI)** infrastructure for **NominaFlow**.

Rather than running monolithic builds directly on the Jenkins Controller, the architecture adopts modern enterprise DevOps practices:
1. **Jenkins Controller Containerization**: Jenkins LTS running on Docker with persistent home volume mapping (`D:/Jenkins/jenkins_home`).
2. **Docker-in-Docker Socket Communication**: The Jenkins controller orchestrates builds by communicating with the host Docker daemon via `/var/run/docker.sock`.
3. **Ephemeral Docker-Based Jenkins Agent (`nominaflow-ci-agent:python3`)**: On-demand provisioning of disposable agent containers that execute the pipeline and automatically self-terminate upon build completion (`DockerOnceRetentionStrategy`).
4. **Automated Pipeline Execution**: Automated checkout, environment verification, virtualenv creation, dependency installation, and Pytest test execution with JUnit XML and Coverage artifact publishing.

---

## 2. CI Architecture & Topology

```text
                           GitHub
                             │
                             ▼
                   Jenkins Multibranch
                        Pipeline
                             │
                             ▼
                    Jenkins Controller
                   (jenkins:lts-jdk21)
                             │
                             │ Docker API (/var/run/docker.sock)
                             ▼
                       Docker Daemon
                       (WSL2 Engine)
                             │
                             │ Spawns on build demand
                             ▼
                Ephemeral CI Agent Container
                (nominaflow-ci-agent:python3)
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
       Virtualenv Setup               Pytest Suite
     (Python 3.13, pip)            (28 Tests Passing)
              │                             │
              └──────────────┬──────────────┘
                             ▼
            Test & Coverage Artifacts Generated
           (reports/junit.xml, coverage.xml)
                             │
                             ▼
            Controller Archives Test Reports
                             │
                             ▼
           Agent Container Automatically Destroyed
```

---

## 3. Declarative Pipeline Configuration (`Jenkinsfile`)

The pipeline as code is version-controlled inside the repository root:

```groovy
pipeline {
    agent {
        label 'nominaflow-ci'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version
                    echo "Pip version:"
                    pip3 --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv /tmp/nominaflow-ci-venv
                    /tmp/nominaflow-ci-venv/bin/python -m pip install --upgrade pip
                    /tmp/nominaflow-ci-venv/bin/pip install ".[dev]"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    mkdir -p reports
                    /tmp/nominaflow-ci-venv/bin/pytest \
                        --junitxml=reports/junit.xml \
                        --cov=src \
                        --cov-report=xml:reports/coverage.xml \
                        --cov-report=term
                '''
            }
        }
    }

    post {
        always {
            junit 'reports/junit.xml'
            archiveArtifacts(
                artifacts: 'reports/coverage.xml',
                allowEmptyArchive: true
            )
        }
        cleanup {
            sh 'rm -rf /tmp/nominaflow-ci-venv'
        }
    }
}
```

---

## 4. Key Verification Metrics & Evidence

| Verification Area | Expected Behavior | Observed Result | Status |
|---|---|---|---|
| **Branch Discovery** | Multibranch scan detects `main`, `develop`, `feature/*` | All branches discovered dynamically | ✅ **Passed** |
| **Agent Provisioning** | Dynamic container creation from `nominaflow-ci-agent:python3` | Container spawned on demand | ✅ **Passed** |
| **Test Execution** | Run complete 28 Pytest test cases | 28 passed, 0 failed | ✅ **Passed** |
| **Artifact Publishing** | `reports/junit.xml` published to Jenkins Test Result table | Interactive test graphs generated | ✅ **Passed** |
| **Coverage Archiving** | `reports/coverage.xml` archived | Archived under build artifacts | ✅ **Passed** |
| **Container Lifecycle** | Destroy ephemeral container on completion | Container terminated and cleaned up | ✅ **Passed** |

---

## 5. Build Artifacts & Execution Screenshots

All execution evidence and test reports from the `develop` branch pipeline run have been archived locally under [`reports/develop-branch-report/`](../reports/develop-branch-report/):

1. **Jenkins Multibranch Dashboard**:
   - Screenshot: `reports/develop-branch-report/dashboard.png`
   - Evidence: Displays multibranch job status, branch discovery (`develop`, `main`), and green pipeline run indicator.
2. **Ephemeral Agent Container Execution**:
   - Screenshot: `reports/develop-branch-report/agent run on develop branch.png`
   - Evidence: Displays dynamic container provisioning of `nominaflow-ci-agent:python3`, virtual environment setup, and test execution.
3. **Automated Coverage Report**:
   - Artifact: `reports/develop-branch-report/coverage.xml`
   - Evidence: Detailed line-by-line statement coverage across models, services, API endpoints, and FSM state transitions.

---

## 6. Summary & Next Milestone
Week 7 successfully verified the commit-to-test automated pipeline with full ephemeral container orchestration. Week 8 will introduce static code quality analysis and parameterized deployment stages.

