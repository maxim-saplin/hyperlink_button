"""
Comprehensive e2e tests to diagnose sporadic click event firing issues.
These tests attempt to reproduce the double-click requirement and sporadic firing.
"""
import os
import subprocess
import time

import pytest
import requests


def _wait_http_ok(url: str, timeout_s: float = 30.0) -> None:
    start = time.time()
    last_err: Exception | None = None
    while time.time() - start < timeout_s:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code == 200:
                return
        except Exception as e:  # noqa: BLE001
            last_err = e
        time.sleep(0.3)
    raise RuntimeError(f"Server did not become ready: {url} ({last_err})")


@pytest.mark.e2e
def test_rapid_successive_clicks():
    """Test rapid successive clicks to see if events are dropped."""
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8512
    env = os.environ.copy()
    env.setdefault("STREAMLIT_SERVER_HEADLESS", "true")

    proc = subprocess.Popen(
        [
            "python",
            "-m",
            "streamlit",
            "run",
            "tests/fixtures/app_for_click_diagnostics.py",
            f"--server.port={port}",
            "--server.headless=true",
            "--server.address=127.0.0.1",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_http_ok(f"http://127.0.0.1:{port}")

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except PlaywrightError as e:
                msg = str(e)
                if "playwright install" in msg or "Executable doesn't exist" in msg:
                    pytest.skip(
                        "Playwright browsers not installed. Run: playwright install"
                    )
                raise
            
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}")
            
            # Wait for page to load
            page.wait_for_selector("[data-testid='test1-state']", timeout=30000)
            
            # Locate the counter button iframe (it's the 5th iframe, index 4)
            counter_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(4)
            
            counter_button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
            counter_button.wait_for(state="visible", timeout=10000)
            
            # Perform rapid successive clicks (10 clicks)
            print("\n=== Testing rapid successive clicks ===")
            initial_count = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"Initial counter: {initial_count}")
            
            for i in range(10):
                counter_button.click()
                # Very short delay to simulate rapid clicking
                page.wait_for_timeout(100)
                current_count = int(page.locator("[data-testid='counter-value']").inner_text())
                print(f"Click {i+1}: Counter = {current_count}, Expected = {initial_count + i + 1}")
            
            # Wait for all reloads to complete
            page.wait_for_timeout(1000)
            
            final_count = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"Final counter after 10 clicks: {final_count}")
            print(f"Expected: {initial_count + 10}, Got: {final_count}")
            
            # Check click history
            history_count = page.locator("[data-testid='history-count']").inner_text()
            print(f"Click history: {history_count}")
            
            # DIAGNOSTIC: Report findings
            if final_count != initial_count + 10:
                print(f"⚠️  ISSUE FOUND: Expected {initial_count + 10} but got {final_count}")
                print(f"   Missed clicks: {initial_count + 10 - final_count}")
            else:
                print("✅ All rapid clicks registered correctly")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.e2e
def test_double_click_behavior():
    """Test if double-clicking has different behavior than single click."""
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8513
    env = os.environ.copy()
    env.setdefault("STREAMLIT_SERVER_HEADLESS", "true")

    proc = subprocess.Popen(
        [
            "python",
            "-m",
            "streamlit",
            "run",
            "tests/fixtures/app_for_click_diagnostics.py",
            f"--server.port={port}",
            "--server.headless=true",
            "--server.address=127.0.0.1",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_http_ok(f"http://127.0.0.1:{port}")

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except PlaywrightError as e:
                msg = str(e)
                if "playwright install" in msg or "Executable doesn't exist" in msg:
                    pytest.skip(
                        "Playwright browsers not installed. Run: playwright install"
                    )
                raise
            
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}")
            
            # Wait for page to load
            page.wait_for_selector("[data-testid='test1-state']", timeout=30000)
            
            # Test single click vs double click
            test1_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(0)
            
            test1_button = test1_frame.locator("[data-testid='hyperlink-button-test1']").locator("button")
            test1_button.wait_for(state="visible", timeout=10000)
            
            print("\n=== Testing single click ===")
            initial_state = page.locator("[data-testid='test1-state']").inner_text()
            print(f"Initial state: {initial_state}")
            
            test1_button.click()
            page.wait_for_timeout(800)  # Wait for rerun
            
            after_single = page.locator("[data-testid='test1-state']").inner_text()
            print(f"After single click: {after_single}")
            
            # Reload page for fresh state
            page.reload()
            page.wait_for_selector("[data-testid='test1-state']", timeout=10000)
            test1_button.wait_for(state="visible", timeout=10000)
            
            print("\n=== Testing double click ===")
            initial_state2 = page.locator("[data-testid='test1-state']").inner_text()
            print(f"Initial state: {initial_state2}")
            
            test1_button.dblclick()
            page.wait_for_timeout(800)
            
            after_double = page.locator("[data-testid='test1-state']").inner_text()
            print(f"After double click: {after_double}")
            
            # DIAGNOSTIC: Check if behavior differs
            print("\n=== Comparison ===")
            print(f"Single click result: {after_single}")
            print(f"Double click result: {after_double}")
            
            if "True" in after_single:
                print("✅ Single click registered")
            else:
                print("⚠️  Single click did NOT register")
            
            if "True" in after_double:
                print("✅ Double click registered")
            else:
                print("⚠️  Double click did NOT register")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.e2e
def test_click_with_different_delays():
    """Test clicks with various delays to identify timing issues."""
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8514
    env = os.environ.copy()
    env.setdefault("STREAMLIT_SERVER_HEADLESS", "true")

    proc = subprocess.Popen(
        [
            "python",
            "-m",
            "streamlit",
            "run",
            "tests/fixtures/app_for_click_diagnostics.py",
            f"--server.port={port}",
            "--server.headless=true",
            "--server.address=127.0.0.1",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        _wait_http_ok(f"http://127.0.0.1:{port}")

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
            except PlaywrightError as e:
                msg = str(e)
                if "playwright install" in msg or "Executable doesn't exist" in msg:
                    pytest.skip(
                        "Playwright browsers not installed. Run: playwright install"
                    )
                raise
            
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}")
            
            # Wait for page to load
            page.wait_for_selector("[data-testid='counter-value']", timeout=30000)
            
            counter_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(4)
            
            counter_button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
            counter_button.wait_for(state="visible", timeout=10000)
            
            # Test with different delays between clicks
            delays = [50, 100, 200, 500, 1000]
            results = {}
            
            for delay_ms in delays:
                # Reset by reloading
                page.reload()
                page.wait_for_selector("[data-testid='counter-value']", timeout=10000)
                counter_button.wait_for(state="visible", timeout=10000)
                
                print(f"\n=== Testing with {delay_ms}ms delay ===")
                initial = int(page.locator("[data-testid='counter-value']").inner_text())
                
                # Perform 5 clicks with the specified delay
                for i in range(5):
                    counter_button.click()
                    page.wait_for_timeout(delay_ms)
                
                # Wait for final rerun
                page.wait_for_timeout(500)
                
                final = int(page.locator("[data-testid='counter-value']").inner_text())
                expected = initial + 5
                success_rate = (final - initial) / 5 * 100
                
                results[delay_ms] = {
                    "expected": expected,
                    "actual": final,
                    "missed": expected - final,
                    "success_rate": success_rate
                }
                
                print(f"Expected: {expected}, Got: {final}, Success rate: {success_rate}%")
            
            # DIAGNOSTIC: Report findings
            print("\n=== DIAGNOSTIC SUMMARY ===")
            for delay_ms, data in results.items():
                status = "✅" if data["missed"] == 0 else "⚠️"
                print(f"{status} {delay_ms}ms delay: {data['success_rate']}% success rate ({data['missed']} missed)")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
