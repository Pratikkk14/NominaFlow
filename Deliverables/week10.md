# Week 10 Deliverable Report — Continuous Acceptance Testing in Jenkins & Defect Gate Verification

> **Course**: DevOps Lab Mini Project  
> **Project**: NominaFlow — Training Nomination Workflow System  
> **Milestone**: Week 10 — Continuous Testing Gate in Jenkins, Test Trend Reporting, and Defect Detection Simulation  
> **Repository**: [https://github.com/Pratikkk14/NominaFlow](https://github.com/Pratikkk14/NominaFlow)  

---

## 1. Executive Summary

In **Week 10**, we established the **Continuous Acceptance Quality Gate** in Jenkins for **NominaFlow**.

This milestone demonstrates:
1. **Automated Test Reporting in CI**: Automated aggregation of Pytest test results into JUnit XML format with trend history tracking.
2. **Pipeline Quality Gate Threshold**: Build abortion mechanism ensuring any failing unit, integration, or E2E test halts downstream packaging and deployment.
3. **Defect Simulation & Recovery Demonstration**: Verification of pipeline behavior when a defect is introduced and corrected.

---

## 2. Continuous Testing Workflow in Jenkins

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CONTINUOUS TESTING PIPELINE LIFECYCLE                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Code Commit ➔ Trigger Jenkins Multibranch Build                          │
│ 2. Ephemeral Agent Spawns (`nominaflow-ci-agent:python3`)                   │
│ 3. Static Analysis Gate: `ruff check` + `flake8`                            │
│ 4. Unit & API Tests: 28 passing Pytest tests with 90% code coverage        │
│ 5. Selenium E2E Acceptance Gate: Headless browser journey validation        │
│ 6. Artifact Publishing: `reports/junit.xml`, `coverage.xml`, HTML reports   │
│ 7. Decision Gate:                                                           │
│      ├── IF Tests Pass ➔ Proceed to Packaging & Deployment                  │
│      └── IF Tests Fail ➔ STOP Pipeline & Notify Failure                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Defect Simulation & Recovery Case Study

To validate that the quality gate reliably blocks defective code from deploying:
1. **Defect Injected**: Introduced a simulated validation bypass in `state_machine.py` (allowing invalid transitions).
2. **Pipeline Trigger**: The Jenkins pipeline executed the `Unit Tests` stage.
3. **Gate Response**: `test_state_machine.py` failed with `AssertionError`.
4. **Action Taken**: The pipeline immediately halted execution, prevented artifact archiving for deployment, and marked the build status as **FAILED (Red)**.
5. **Defect Corrected**: Fixed the state machine invariant logic and pushed a clean commit.
6. **Recovery Verified**: The subsequent pipeline run executed cleanly with all 28 tests passing and build status restored to **SUCCESS (Blue/Green)**.

---

## 4. Key Verification Metrics

| Verification Area | Expected Result | Observed Result | Status |
|---|---|---|---|
| **Test Result Parsing** | JUnit XML parsed by Jenkins | Test Results trend dashboard rendered | ✅ **Passed** |
| **Coverage Threshold** | Minimum 80% line coverage | **90% coverage** achieved | ✅ **Passed** |
| **Defect Detection** | Pipeline halts on test failure | Build stops downstream stages on failure | ✅ **Verified** |
| **Clean Recovery** | Successful rerun on defect fix | Pipeline returns to green status | ✅ **Verified** |

---

## 5. Summary & Next Milestone
Weeks 9 & 10 complete the automated testing and continuous quality gate milestones. Next, **Weeks 11 & 12** implement **Docker multi-stage containerization, Docker Compose, and Continuous Deployment**.
