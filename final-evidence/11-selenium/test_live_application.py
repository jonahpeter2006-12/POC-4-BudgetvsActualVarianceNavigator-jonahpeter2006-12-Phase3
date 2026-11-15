"""
POC-4 live Selenium E2E test.
Targets the deployed Render frontend; never defaults to localhost.
"""
import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOTS = ROOT / "screenshots"
RESULTS = ROOT / "test-results"
SCREENSHOTS.mkdir(exist_ok=True)
RESULTS.mkdir(exist_ok=True)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL", "https://poc4-budget-frontend.onrender.com"
).rstrip("/")
BACKEND_URL = os.getenv(
    "BACKEND_URL", "https://poc4-budget-backend.onrender.com"
).rstrip("/")
EXPECTED_NAME = os.getenv("EXPECTED_NAME", "Jona Peter")
TIMEOUT = int(os.getenv("SELENIUM_TIMEOUT", "35"))

results = []

def record(name, passed, detail=""):
    results.append({
        "test": name,
        "status": "PASS" if passed else "FAIL",
        "detail": str(detail)
    })
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")

def wait_for(driver, condition, timeout=TIMEOUT):
    return WebDriverWait(driver, timeout).until(condition)

def main():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = None
    try:
        driver = webdriver.Chrome(options=options)

        # 1. Live application availability and page load
        response = requests.get(FRONTEND_URL, timeout=25)
        record("Live frontend availability", response.status_code == 200,
               f"HTTP {response.status_code} at {FRONTEND_URL}")

        driver.get(FRONTEND_URL)
        wait_for(driver, EC.presence_of_element_located((By.TAG_NAME, "main")))
        wait_for(driver, lambda d: d.execute_script("return document.readyState") == "complete")
        record("Page load", "Budget vs Actual Variance Navigator" in driver.title
               or "Budget vs Actual Variance Navigator" in driver.page_source,
               f"title={driver.title}")

        # Wait until data has rendered; a visible error state is not accepted.
        wait_for(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "main button")) > 0)
        body_text = driver.find_element(By.TAG_NAME, "body").text
        no_error = "Unable to connect to the backend" not in body_text
        record("Data rendered", no_error and len(body_text.strip()) > 100,
               "Dashboard text is present" if no_error else "Backend connection error is visible")

        # 2. Core visualization: Recharts SVGs are the rendered chart surfaces.
        wait_for(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "main svg.recharts-surface")) > 0)
        charts = driver.find_elements(By.CSS_SELECTOR, "main svg.recharts-surface")
        record("Visualization rendering", len(charts) > 0,
               f"{len(charts)} Recharts chart surface(s) found")

        # 3. Frontend-to-backend handshake: check deployed API health + summary.
        health = requests.get(f"{BACKEND_URL}/api/health", timeout=20)
        summary = requests.get(f"{BACKEND_URL}/api/summary", timeout=20)
        api_ok = health.ok and summary.ok and bool(summary.content)
        record("Frontend/backend API handshake", api_ok,
               f"health={health.status_code}, summary={summary.status_code}, backend={BACKEND_URL}")

        # 4. Department filter interaction
        department_filter = wait_for(
            driver, EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'select[aria-label="Filter by department"]')
            )
        )
        department_options = Select(department_filter).options
        if len(department_options) > 1:
            before = department_filter.get_attribute("value")
            Select(department_filter).select_by_index(1)
            wait_for(driver, lambda d: d.find_element(
                By.CSS_SELECTOR, 'select[aria-label="Filter by department"]'
            ).get_attribute("value") != before)
            record("Filter interaction", True,
                   f"Selected {department_filter.get_attribute('value')}")
        else:
            record("Filter interaction", False, "No department options available")

        # 5. Intelligence panel via a KPI card (actual dashboard click path).
        kpi = wait_for(driver, EC.element_to_be_clickable(
            (By.XPATH, "//button[.//*[contains(normalize-space(), 'Approved budget')]]")
        ))
        kpi.click()
        panel = wait_for(driver, EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[role="dialog"][aria-label="Financial insights"]')
        ))
        record("Intelligence panel interaction", panel.is_displayed(),
               "Financial insights dialog opened from Approved budget KPI")
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close insights panel"]').click()
        wait_for(driver, EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, '[role="dialog"][aria-label="Financial insights"]')
        ))

        # 6. Signature: info icon opens metadata and expected intern name is present.
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Open application metadata"]').click()
        metadata = wait_for(driver, EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[role="dialog"][aria-labelledby="metadata-title"]')
        ))
        metadata_text = metadata.text
        record("Info icon / signature", metadata.is_displayed() and EXPECTED_NAME in metadata_text,
               f"Expected '{EXPECTED_NAME}' in metadata; modal text: {metadata_text[:300]}")
        driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close metadata"]').click()

        # 7. Responsive layout: use mobile viewport and verify no horizontal overflow.
        driver.set_window_size(390, 844)
        wait_for(driver, EC.presence_of_element_located((By.TAG_NAME, "main")))
        dimensions = driver.execute_script(
            "return {width: document.documentElement.clientWidth, "
            "scrollWidth: document.documentElement.scrollWidth}"
        )
        responsive_ok = dimensions["scrollWidth"] <= dimensions["width"] + 2
        record("Responsive layout", responsive_ok, json.dumps(dimensions))

        driver.set_window_size(1440, 1000)
        driver.save_screenshot(str(SCREENSHOTS / "selenium-live-dashboard.png"))
        record("Screenshot evidence", True, "screenshots/selenium-live-dashboard.png")

    except Exception as exc:
        record("Execution exception", False, f"{type(exc).__name__}: {exc}")
        if driver:
            try:
                driver.save_screenshot(str(SCREENSHOTS / "selenium-failure.png"))
            except Exception:
                pass
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

    passed = sum(r["status"] == "PASS" for r in results)
    failed = sum(r["status"] == "FAIL" for r in results)
    overall = "PASS" if results and failed == 0 else "FAIL"
    timestamp = datetime.now(timezone.utc).isoformat()
    payload = {
        "project": "POC-4 Budget vs Actual Variance Navigator",
        "frontend_url": FRONTEND_URL,
        "backend_url": BACKEND_URL,
        "browser": "Google Chrome via Selenium WebDriver",
        "executed_at_utc": timestamp,
        "passed": passed,
        "failed": failed,
        "result": overall,
        "tests": results,
    }
    (RESULTS / "results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "POC-4 SELENIUM E2E TEST REPORT",
        f"Executed (UTC): {timestamp}",
        f"Frontend URL: {FRONTEND_URL}",
        f"Backend URL: {BACKEND_URL}",
        "Browser: Google Chrome / Selenium WebDriver",
        "",
    ]
    lines += [f"{r['status']}: {r['test']} — {r['detail']}" for r in results]
    lines += ["", f"TOTAL: {passed} PASS, {failed} FAIL", f"FINAL RESULT: {overall}"]
    (ROOT / "Test_Report.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nFINAL RESULT: {overall} ({passed} passed, {failed} failed)")
    sys.exit(0 if overall == "PASS" else 1)

if __name__ == "__main__":
    main()
