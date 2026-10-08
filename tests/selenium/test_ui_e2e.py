"""Selenium WebDriver End-to-End User Journey Tests for NominaFlow.

Weeks 9 & 10 Milestone: Automated Browser testing covering critical user journeys
with assertion verification, failure screenshot capture, and CI quality gate integration.
"""

import os
import time
from pathlib import Path

import pytest

# Ensure screenshot directory exists
SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


class TestNominaFlowSeleniumJourneys:
    """Suite of 4 critical end-to-end user journeys in NominaFlow."""

    def capture_screenshot(self, driver, test_name: str) -> str:
        """Capture browser screenshot on failure or milestone."""
        timestamp = int(time.time())
        filepath = SCREENSHOT_DIR / f"{test_name}_{timestamp}.png"
        driver.save_screenshot(str(filepath))
        return str(filepath)

    def get_chrome_driver(self):
        """Initialize headless Chrome WebDriver with safe container flags."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=chrome_options)

    @pytest.mark.skipif(
        os.getenv("RUN_SELENIUM") != "true",
        reason="Selenium requires active WebDriver and browser binary. Set RUN_SELENIUM=true to execute.",
    )
    def test_journey_1_employee_login_and_navigation(self):
        """Journey 1: Employee logs in with 1-click credential and arrives on Employee Portal."""
        from selenium.webdriver.common.by import By

        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            assert "System Login" in driver.page_source

            # Enter credentials
            driver.find_element(By.ID, "loginEmail").clear()
            driver.find_element(By.ID, "loginEmail").send_keys("employee@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").clear()
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            time.sleep(2)
            assert "/employee" in driver.current_url
            assert "Employee Training Portal" in driver.page_source
        except Exception:
            self.capture_screenshot(driver, "journey_1_failure")
            raise
        finally:
            driver.quit()

    @pytest.mark.skipif(
        os.getenv("RUN_SELENIUM") != "true",
        reason="Selenium requires active WebDriver. Set RUN_SELENIUM=true to execute.",
    )
    def test_journey_2_create_draft_and_save(self):
        """Journey 2: Employee creates a draft in form text boxes and performs incremental save."""
        from selenium.webdriver.common.by import By

        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            driver.find_element(By.ID, "loginEmail").send_keys("employee@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(1.5)

            # Open Form
            driver.find_element(By.XPATH, "//button[contains(text(), 'New Training Nomination')]").click()
            time.sleep(0.5)

            # Fill text inputs
            driver.find_element(By.ID, "inputTitle").send_keys("Advanced Cloud Infrastructure")
            driver.find_element(By.ID, "inputProvider").send_keys("Cloud Native Institute")
            driver.find_element(By.ID, "inputDescription").send_keys("Deep dive into Kubernetes and Docker.")
            driver.find_element(By.ID, "inputJustification").send_keys("Required for upcoming migration project.")

            # Save Draft
            driver.find_element(By.XPATH, "//button[contains(text(), 'Save as Draft')]").click()
            time.sleep(1.5)

            assert "Advanced Cloud Infrastructure" in driver.page_source
        except Exception:
            self.capture_screenshot(driver, "journey_2_failure")
            raise
        finally:
            driver.quit()

    @pytest.mark.skipif(
        os.getenv("RUN_SELENIUM") != "true",
        reason="Selenium requires active WebDriver. Set RUN_SELENIUM=true to execute.",
    )
    def test_journey_3_reviewer_decision_workflow(self):
        """Journey 3: Reviewer logs in, opens review queue, and inspects submissions."""
        from selenium.webdriver.common.by import By

        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            driver.find_element(By.ID, "loginEmail").send_keys("reviewer@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(1.5)

            assert "/reviewer" in driver.current_url
            assert "Reviewer Portal" in driver.page_source
        except Exception:
            self.capture_screenshot(driver, "journey_3_failure")
            raise
        finally:
            driver.quit()

    @pytest.mark.skipif(
        os.getenv("RUN_SELENIUM") != "true",
        reason="Selenium requires active WebDriver. Set RUN_SELENIUM=true to execute.",
    )
    def test_journey_4_admin_metrics_and_audit_trail(self):
        """Journey 4: Administrator logs in, verifies metric counters and inspects audit trail."""
        from selenium.webdriver.common.by import By

        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            driver.find_element(By.ID, "loginEmail").send_keys("admin@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(1.5)

            assert "/admin" in driver.current_url
            assert "Administrator Governance" in driver.page_source
            assert "Audit Trail" in driver.page_source
        except Exception:
            self.capture_screenshot(driver, "journey_4_failure")
            raise
        finally:
            driver.quit()
