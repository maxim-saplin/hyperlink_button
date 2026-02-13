"""
Test to try to reproduce iframe remount scenario.
This test attempts to simulate component remounting without full page reload.
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
def test_iframe_remount_scenario():
    """
    Attempt to reproduce the iframe remount issue.
    
    This test:
    1. Clicks button to increment counter
    2. Attempts to force iframe reload
    3. Checks if next click registers
    
    Expected behavior with bug:
    - First click: counter 0→1, last_seen=1
    - Iframe reload: counter resets to 0, last_seen still 1
    - Second click: counter 0→1, but 1 !> 1, so NOT registered (BUG!)
    - Third click: counter 1→2, and 2 > 1, so registered
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8519
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
            
            # Enable console logging to see component lifecycle
            page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
            
            page.goto(f"http://127.0.0.1:{port}")
            
            # Wait for page to load
            page.wait_for_selector("[data-testid='counter-value']", timeout=30000)
            
            print("\n=== Testing iframe remount scenario ===")
            
            # Step 1: First click to establish baseline
            counter_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(4)
            
            counter_button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
            counter_button.wait_for(state="visible", timeout=10000)
            
            print("\nStep 1: First click to establish counter")
            initial = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  Initial counter: {initial}")
            
            counter_button.click()
            page.wait_for_timeout(1000)
            
            after_first = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  After first click: {after_first}")
            print(f"  ✅ First click registered: {after_first > initial}")
            
            # Step 2: Try to reload just the iframe (not the whole page)
            print("\nStep 2: Attempting to reload iframe...")
            
            # Get the iframe element
            iframe_element = page.locator("iframe[title='hyperlink_button._component.hyperlink_button']").nth(4)
            
            # Try to reload iframe using JavaScript
            # This simulates what might happen when Streamlit remounts the component
            page.evaluate("""
                (selector) => {
                    const iframes = document.querySelectorAll(selector);
                    if (iframes.length > 4) {
                        const iframe = iframes[4];
                        const src = iframe.src;
                        iframe.src = src; // Force reload
                        console.log('Iframe reloaded');
                    }
                }
            """, "iframe[title='hyperlink_button._component.hyperlink_button']")
            
            # Wait for iframe to reload
            page.wait_for_timeout(2000)
            
            # Re-acquire frame locator after reload
            counter_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(4)
            counter_button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
            counter_button.wait_for(state="visible", timeout=10000)
            
            print("  Iframe reloaded")
            
            # Step 3: Try to click again
            print("\nStep 3: Click after iframe reload")
            before_second = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  Counter before second click: {before_second}")
            
            counter_button.click()
            page.wait_for_timeout(1000)
            
            after_second = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  Counter after second click: {after_second}")
            
            if after_second > before_second:
                print(f"  ✅ Second click registered immediately")
            else:
                print(f"  ⚠️  Second click did NOT register!")
                
                # Try third click
                print("\nStep 4: Third click (testing double-click requirement)")
                counter_button.click()
                page.wait_for_timeout(1000)
                
                after_third = int(page.locator("[data-testid='counter-value']").inner_text())
                print(f"  Counter after third click: {after_third}")
                
                if after_third > after_second:
                    print(f"  ⚠️  BUG REPRODUCED! Required double-click after iframe reload")
                    print(f"  This confirms the iframe remount hypothesis!")
                else:
                    print(f"  ❌ Even third click didn't work - different issue")
            
            print("\n=== DIAGNOSTIC SUMMARY ===")
            print(f"Initial: {initial}")
            print(f"After 1st click: {after_first} (delta: +{after_first - initial})")
            print(f"After iframe reload + 2nd click: {after_second} (delta: +{after_second - after_first})")
            if after_second == before_second:
                print(f"After 3rd click: {after_third} (delta: +{after_third - after_second})")
                if after_third > after_second:
                    print("\n⚠️  CONFIRMED: Iframe remount causes double-click requirement!")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
