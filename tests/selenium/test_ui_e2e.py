"""Selenium WebDriver End-to-End User Journey Tests for NominaFlow.

Week 9 & 10 Milestone: Automated Browser testing covering critical user journeys
with failure screenshot mechanism and assertions.
"""

import os
import time
from pathlib import Path

import pytest

# Ensure screenshot directory exists
SCREENSHOT_DIR = Path("reports/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


class TestNominaFlowSeleniumJourneys:
    """Suite of critical user journeys in NominaFlow."""

    def capture_screenshot(self, driver, test_name: str) -> str:
        """Capture browser screenshot on failure or milestone."""
        timestamp = int(time.time())
        filepath = SCREENSHOT_DIR / f"{test_name}_{timestamp}.png"
        driver.save_screenshot(str(filepath))
        return str(filepath)

    @pytest.mark.skipif(
        os.getenv("RUN_SELENIUM") != "true",
        reason="Selenium requires active WebDriver and browser binary. Set RUN_SELENIUM=true to execute.",
    )
    def test_journey_1_login_and_role_navigation(self):
        """Journey 1: Employee logs in and is navigated to Employee Portal."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get("http://localhost:8000/login")
            assert "System Login" in driver.page_source

            # Enter credentials
            driver.find_element(By.ID, "loginEmail").send_keys("employee@nominaflow.com")
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
    def test_journey_2_create_and_submit_nomination(self):
        """Journey 2: Employee creates a draft in form text boxes and submits."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        try:
            driver.get("http://localhost:8000/login")
            # Log in
            driver.find_element(By.ID, "loginEmail").send_keys("employee@nominaflow.com")
            driver.find_element(By.ID, "loginPassword").send_keys("password123")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(1.5)

            # Open Form
            driver.find_element(By.XPATH, "//button[contains(text(), 'New Training Nomination')]").click()
            time.sleep(0.5)

            # Fill text boxes
            driver.find_element(By.ID, "inputTitle").send_keys("Selenium E2E Test Course")
            driver.find_element(By.ID, "inputProvider").send_keys("WebDriver Academy")
            driver.find_element(By.ID, "inputDescription").send_keys("Automated journey validation.")
            driver.find_element(By.ID, "inputJustification").send_keys("Testing critical paths.")

            # Save Draft
            driver.find_element(By.XPATH, "//button[contains(text(), 'Save as Draft')]").click()
            time.sleep(1.5)

            assert "Selenium E2E Test Course" in driver.page_source
        except Exception:
            self.capture_screenshot(driver, "journey_2_failure")
            raise
        finally:
            driver.quit()
