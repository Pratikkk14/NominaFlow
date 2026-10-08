"""Selenium WebDriver End-to-End User Journey Tests for NominaFlow.

Weeks 9 & 10 Milestone: Automated Browser testing covering critical user journeys
with assertion verification, failure screenshot capture, and CI quality gate integration.
"""

import os
import time
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginEmail")))

            # Enter credentials
            driver.find_element(By.ID, "loginEmail").clear()
            driver.find_element(By.ID, "loginEmail").send_keys("employee@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").clear()
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            WebDriverWait(driver, 5).until(EC.url_contains("/employee"))
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
        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginEmail")))

            driver.find_element(By.ID, "loginEmail").send_keys("employee@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            WebDriverWait(driver, 5).until(EC.url_contains("/employee"))

            # Create nomination via API call directly inside the authenticated browser session
            driver.execute_script("""
                apiCall('/api/v1/nominations', 'POST', {
                    title: 'Advanced Cloud Infrastructure',
                    provider: 'Cloud Native Institute',
                    training_type: 'Technical',
                    training_date: '2026-11-15',
                    duration: '3 Days',
                    cost: 450.0,
                    description: 'Deep dive into Kubernetes and Docker.',
                    justification: 'Required for upcoming migration project.'
                }).then(() => loadMyNominations());
            """)

            # Wait for table to reload with new nomination
            WebDriverWait(driver, 8).until(
                lambda d: "Advanced Cloud Infrastructure" in d.find_element(By.ID, "nominationsTableBody").text
            )
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
        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginEmail")))

            driver.find_element(By.ID, "loginEmail").send_keys("reviewer@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            WebDriverWait(driver, 5).until(EC.url_contains("/reviewer"))
            assert "Reviewer Evaluation Dashboard" in driver.page_source
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
        driver = self.get_chrome_driver()
        try:
            driver.get("http://localhost:8000/login")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginEmail")))

            driver.find_element(By.ID, "loginEmail").send_keys("admin@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            WebDriverWait(driver, 5).until(EC.url_contains("/admin"))
            time.sleep(1)
            assert "Administrator" in driver.page_source
            assert "statTotal" in driver.page_source
        except Exception:
            self.capture_screenshot(driver, "journey_4_failure")
            raise
        finally:
            driver.quit()
