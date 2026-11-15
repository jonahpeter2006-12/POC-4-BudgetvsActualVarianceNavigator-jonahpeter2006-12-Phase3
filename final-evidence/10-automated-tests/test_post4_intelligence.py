import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "test-results"
SCREENSHOTS = ROOT / "screenshots"
RESULTS.mkdir(exist_ok=True)
SCREENSHOTS.mkdir(exist_ok=True)

FRONTEND = "http://127.0.0.1:3002"
BACKEND = "http://127.0.0.1:8002"
TIMEOUT = 25
results = []


def record(name, passed, detail=""):
    results.append({
        "test": name,
        "status": "PASS" if passed else "FAIL",
        "detail": str(detail),
    })
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        # 1. Backend intelligence readiness
        health = requests.get(
            f"{BACKEND}/api/intelligence/health", timeout=10
        )
        health_data = health.json()
        record(
            "Intelligence API readiness",
            health.status_code == 200 and health_data.get("status") == "ready",
            f"HTTP {health.status_code}; findings={health_data.get('result_count')}",
        )

        # 2. Frontend route availability
        page_response = requests.get(
            f"{FRONTEND}/data-intelligence", timeout=10
        )
        record(
            "Data Intelligence route availability",
            page_response.status_code == 200,
            f"HTTP {page_response.status_code}",
        )

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, TIMEOUT)

        # 3. Page load and API-backed content
        driver.get(f"{FRONTEND}/data-intelligence")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        wait.until(
            lambda d: "Overall comparisons" in d.find_element(
                By.TAG_NAME, "body"
            ).text
        )
        body = driver.find_element(By.TAG_NAME, "body").text
        record(
            "Data Intelligence page and summary render",
            "Overall comparisons" in body
            and "Monthly findings" in body
            and "1,230" in body,
            "Summary cards and analytical validation are visible",
        )

        # 4. Overall findings
        overall_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Overall comparisons')]")
            )
        )
        overall_button.click()
        wait.until(
            lambda d: len(d.find_elements(By.XPATH, "//button[normalize-space()='View evidence']")) > 0
        )
        overall_rows = len(
            driver.find_elements(
                By.XPATH, "//button[normalize-space()='View evidence']"
            )
        )
        record(
            "Overall comparisons view",
            overall_rows == 16,
            f"{overall_rows} findings displayed; expected 16",
        )

        # 5. Monthly findings and evidence warning
        monthly_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Monthly findings')]")
            )
        )
        monthly_button.click()
        wait.until(
            lambda d: "Monthly findings are descriptive" in
            d.find_element(By.TAG_NAME, "body").text
        )
        monthly_rows = len(
            driver.find_elements(
                By.XPATH, "//button[normalize-space()='View evidence']"
            )
        )
        monthly_text = driver.find_element(By.TAG_NAME, "body").text
        record(
            "Monthly findings and limitation warning",
            monthly_rows == 48
            and "insufficient_evidence" in monthly_text,
            f"{monthly_rows} findings; insufficient-evidence warning visible",
        )

        # 6. Search interaction
        search = driver.find_element(
            By.CSS_SELECTOR, 'input[aria-label="Search findings"]'
        )
        search.clear()
        search.send_keys("Engineering")
        search_rows = len(
            driver.find_elements(
                By.XPATH, "//button[normalize-space()='View evidence']"
            )
        )
        record(
            "Finding search interaction",
            search_rows >= 1 and search_rows < monthly_rows,
            f"Search returned {search_rows} matching monthly findings",
        )
        search.click()
        search.send_keys(Keys.CONTROL, "a")
        search.send_keys(Keys.BACKSPACE)
        wait.until(
            lambda d: d.find_element(
                By.CSS_SELECTOR, 'input[aria-label="Search findings"]'
            ).get_attribute("value") == ""
        )
        # Return to overall view for evidence test
        overall_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Overall comparisons')]")
            )
        )
        driver.execute_script("arguments[0].click();", overall_button)
        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[contains(., 'Monthly findings are descriptive')]")
            )
        )
        evidence_buttons_after_switch = driver.find_elements(
            By.XPATH, "//button[normalize-space()='View evidence']"
        )
        search_value_after_switch = driver.find_element(
            By.CSS_SELECTOR, 'input[aria-label="Search findings"]'
        ).get_attribute("value")
        print(
            "[DEBUG] After switching to Overall:",
            "evidence_buttons=", len(evidence_buttons_after_switch),
            "search_value=", repr(search_value_after_switch),
            "monthly_warning_visible=",
            "Monthly findings are descriptive" in
            driver.find_element(By.TAG_NAME, "body").text,
            "overall_tab_class=", overall_button.get_attribute("class"),
        )
        wait.until(
            lambda d: len(d.find_elements(
                By.XPATH, "//button[normalize-space()='View evidence']"
            )) == 16
        )

        # 7. Evidence detail interaction
        first_evidence = driver.find_element(
            By.XPATH, "(//button[normalize-space()='View evidence'])[1]"
        )
        first_evidence.click()
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='Finding evidence']")
            )
        )
        evidence_text = driver.find_element(By.TAG_NAME, "body").text
        evidence_ok = (
            "Budget" in evidence_text
            and "Actual" in evidence_text
            and "Absolute variance" in evidence_text
            and "Source record IDs" in evidence_text
            and "Aggregation method" in evidence_text
        )
        record(
            "Finding evidence detail",
            evidence_ok,
            "Financial measures, source traceability and method details visible",
        )

        # 8. Close evidence detail
        driver.find_element(
            By.XPATH, "//button[normalize-space()='Close details']"
        ).click()
        wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='Finding evidence']")
            )
        )
        record("Evidence detail close interaction", True, "Details panel closed")

        # 9. Original operational dashboard route
        driver.get(FRONTEND)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        root_text = driver.find_element(By.TAG_NAME, "body").text
        record(
            "Operational dashboard regression",
            "Budget vs Actual Variance Navigator" in root_text
            and "Data Intelligence" in root_text,
            "Original dashboard and Data Intelligence navigation are present",
        )

        # 10. Mobile viewport / horizontal overflow
        driver.get(f"{FRONTEND}/data-intelligence")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        driver.set_window_size(390, 844)
        dimensions = driver.execute_script(
            "return {width: document.documentElement.clientWidth, "
            "scrollWidth: document.documentElement.scrollWidth}"
        )
        responsive_ok = dimensions["scrollWidth"] <= dimensions["width"] + 2
        record(
            "Mobile viewport overflow check",
            responsive_ok,
            json.dumps(dimensions),
        )
        # Capture screenshot only after intelligence data is fully rendered.
        driver.set_window_size(1440, 1000)
        driver.get(f"{FRONTEND}/data-intelligence")

        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )

        wait.until(
            lambda d: (
                "Overall comparisons" in d.find_element(
                    By.TAG_NAME, "body"
                ).text
                and "Monthly findings" in d.find_element(
                    By.TAG_NAME, "body"
                ).text
                and "1,230" in d.find_element(
                    By.TAG_NAME, "body"
                ).text
                and "64" in d.find_element(
                    By.TAG_NAME, "body"
                ).text
            )
        )

        driver.save_screenshot(
            str(SCREENSHOTS / "post4-intelligence.png")
        )

        record(
            "Post #4 screenshot evidence",
            (SCREENSHOTS / "post4-intelligence.png").exists(),
            "Completed Data Intelligence page screenshot captured",
        )
        record(
            "Post #4 screenshot evidence",
            (SCREENSHOTS / "post4-intelligence.png").exists(),
            "screenshots/post4-intelligence.png",
        )

    except Exception as exc:
        record(
            "Execution exception",
            False,
            f"{type(exc).__name__}: {exc}",
        )
        traceback.print_exc()
        if driver:
            try:
                driver.save_screenshot(
                    str(SCREENSHOTS / "post4-intelligence-failure.png")
                )
            except Exception:
                pass
    finally:
        if driver:
            driver.quit()

    passed = sum(item["status"] == "PASS" for item in results)
    failed = sum(item["status"] == "FAIL" for item in results)
    payload = {
        "project": "POC-4 Budget vs Actual Variance Navigator",
        "phase": "Phase 3 Post #4",
        "frontend_url": FRONTEND,
        "backend_url": BACKEND,
        "browser": "Google Chrome via Selenium WebDriver",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "passed": passed,
        "failed": failed,
        "result": "PASS" if results and failed == 0 else "FAIL",
        "tests": results,
    }
    output = RESULTS / "post4-results.json"
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nFINAL RESULT: {payload['result']} ({passed} passed, {failed} failed)")
    print(f"Report: {output}")
    sys.exit(0 if payload["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
