# Week 9 & 10 Deliverable Report — Selenium WebDriver Test Design, Local Execution & Continuous Testing Quality Gate

> **Course**: DevOps Lab Mini Project  
> **Project**: NominaFlow — Training Nomination Workflow System  
> **Milestone**: Weeks 9 & 10 — Selenium WebDriver E2E User Journeys, Failure Screenshot Capture, and Continuous Acceptance Testing  
> **Repository**: [https://github.com/Pratikkk14/NominaFlow](https://github.com/Pratikkk14/NominaFlow)  

---

## 1. Executive Summary

In **Weeks 9 and 10**, we implemented and verified the **End-to-End (E2E) Browser Acceptance Testing Suite** for **NominaFlow**.

This milestone delivers:
1. **4 Critical End-to-End User Journeys**: Automated browser journeys covering Employee login, Draft creation/incremental save, Reviewer decision queue, and Administrator governance metrics.
2. **Automated Failure Screenshot Engine**: Automatic full-page PNG capture saved into `reports/screenshots/` whenever an assertion or network error occurs.
3. **Headless Chrome WebDriver Integration**: High-performance headless execution with `--headless=new`, `--no-sandbox`, and containerized display emulation.
4. **CI Quality Gate Integration**: Ability to run browser-level regression testing inside Jenkins candidate builds.

---

## 2. Selenium Test Plan & Critical User Journeys (`tests/selenium/test_ui_e2e.py`)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AUTOMATED SELENIUM E2E SUITE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Journey 1: Employee Authentication & Navigation                             │
│   • Enters credentials on /login                                            │
│   • Verifies redirection to /employee and validates page headers            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Journey 2: Draft Creation & Incremental Saving in Form Text Boxes           │
│   • Opens "New Training Nomination" modal                                   │
│   • Fills Title, Provider, Description, and Justification text boxes        │
│   • Clicks "Save as Draft" and verifies table row persistence               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Journey 3: Reviewer Queue & Evaluation Interface                            │
│   • Logs in as Reviewer (reviewer@nominaflow.com)                           │
│   • Navigates to /reviewer and checks review queue presence                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Journey 4: Administrator Governance Dashboard & Audit Log                   │
│   • Logs in as Admin (admin@nominaflow.com)                                 │
│   • Validates KPI metric cards and immutable audit trail table              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Failure Screenshot Mechanism

```python
SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def capture_screenshot(self, driver, test_name: str) -> str:
    """Capture browser screenshot on failure or milestone."""
    timestamp = int(time.time())
    filepath = SCREENSHOT_DIR / f"{test_name}_{timestamp}.png"
    driver.save_screenshot(str(filepath))
    return str(filepath)
```

If an element is missing, assertion fails, or backend returns an error:
- The `except Exception:` block immediately captures the active DOM state to `reports/screenshots/<journey_name>_<timestamp>.png`.
- Re-raises the exception to ensure the test runner and Jenkins build record a failed status.

---

## 4. Key Verification Metrics

| User Journey | Verification Target | Assertion Strategy | Status |
|---|---|---|---|
| **Journey 1** | Employee Login | URL contains `/employee` & header text exists | ✅ **Implemented** |
| **Journey 2** | Draft Creation | Saved course title appears in DOM table | ✅ **Implemented** |
| **Journey 3** | Reviewer Queue | URL contains `/reviewer` & review queue rendered | ✅ **Implemented** |
| **Journey 4** | Admin Dashboard | URL contains `/admin` & Audit Trail rendered | ✅ **Implemented** |
| **Screenshots** | Failure Capture | PNG saved to `reports/screenshots/` | ✅ **Verified** |

---

## 5. Summary & Next Milestone
Weeks 9 & 10 establish automated browser quality gates for user journeys. Weeks 11 & 12 will implement **Multi-Stage Docker Containerization** and **Docker Compose Multi-Container Deployment**.
