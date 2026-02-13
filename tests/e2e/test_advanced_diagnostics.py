"""
Advanced diagnostic tests for race conditions and edge cases.
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
def test_race_condition_on_rerun():
    """
    Test potential race condition: clicking while a rerun is in progress.
    This could be the root cause of sporadic click issues.
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8516
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
            
            print("\n=== Testing clicks during rerun (race condition) ===")
            
            # Strategy: Click rapidly and check if any clicks are lost
            # This simulates clicking before the previous rerun completes
            results = []
            for attempt in range(5):
                page.reload()
                page.wait_for_selector("[data-testid='counter-value']", timeout=10000)
                counter_button.wait_for(state="visible", timeout=10000)
                
                initial = int(page.locator("[data-testid='counter-value']").inner_text())
                
                # Click very rapidly - don't wait for rerun to complete
                for i in range(3):
                    counter_button.click()
                    # Only 20ms delay - likely triggers race condition
                    page.wait_for_timeout(20)
                
                # Now wait for all reruns to complete
                page.wait_for_timeout(2000)
                
                final = int(page.locator("[data-testid='counter-value']").inner_text())
                missed = 3 - (final - initial)
                results.append(missed)
                
                print(f"Attempt {attempt + 1}: Expected 3, got {final - initial}, missed: {missed}")
            
            print(f"\n=== DIAGNOSTIC RESULTS ===")
            total_missed = sum(results)
            if total_missed > 0:
                print(f"⚠️  RACE CONDITION DETECTED!")
                print(f"   Total clicks missed across 5 attempts: {total_missed}/15")
                print(f"   Success rate: {((15 - total_missed) / 15) * 100:.1f}%")
                print(f"   This confirms sporadic click event firing issue")
            else:
                print(f"✅ No race condition detected (0 missed clicks)")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.e2e
def test_component_state_persistence():
    """
    Test if component internal state persists correctly across reruns.
    State management issues could cause sporadic click registration.
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8517
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
            
            print("\n=== Testing component state persistence ===")
            
            # Click multiple times with sufficient delay for reruns
            for i in range(5):
                before = int(page.locator("[data-testid='counter-value']").inner_text())
                counter_button.click()
                
                # Wait for rerun
                page.wait_for_timeout(800)
                
                after = int(page.locator("[data-testid='counter-value']").inner_text())
                increment = after - before
                
                print(f"Click {i+1}: Before={before}, After={after}, Increment={increment}")
                
                if increment != 1:
                    print(f"⚠️  State inconsistency! Expected +1, got +{increment}")
            
            final = int(page.locator("[data-testid='counter-value']").inner_text())
            if final == 5:
                print(f"✅ State persistence correct: {final}/5")
            else:
                print(f"⚠️  State persistence issue: {final}/5")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.e2e  
def test_click_while_streamlit_reconnecting():
    """
    Test clicking behavior during network issues or reconnection.
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8518
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
            
            print("\n=== Testing clicks with simulated network latency ===")
            
            # Simulate slow network by adding artificial latency
            page.route("**/*", lambda route: (
                time.sleep(0.1),  # 100ms latency
                route.continue_()
            ))
            
            initial = int(page.locator("[data-testid='counter-value']").inner_text())
            
            # Click multiple times with latency
            for i in range(3):
                counter_button.click()
                page.wait_for_timeout(100)
            
            # Wait for all requests to complete
            page.wait_for_timeout(2000)
            
            final = int(page.locator("[data-testid='counter-value']").inner_text())
            missed = 3 - (final - initial)
            
            print(f"With network latency: Expected 3, got {final - initial}, missed: {missed}")
            
            if missed > 0:
                print(f"⚠️  Network latency causes click loss")
            else:
                print(f"✅ Clicks handled correctly despite network latency")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
