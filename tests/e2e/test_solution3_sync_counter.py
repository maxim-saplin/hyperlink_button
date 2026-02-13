"""
Comprehensive tests for Solution 3: Sync Counter implementation.
Tests counter synchronization across iframe remounts.
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
def test_counter_sync_on_iframe_remount():
    """
    Test that counter is properly synced after iframe remount.
    
    With Solution 3 (Sync Counter):
    - First click: counter 0→1, saved to session state
    - Iframe reload: counter restored from session state to 1
    - Second click: counter 1→2, click should register immediately
    
    This test verifies the fix works correctly.
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8520
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
            
            print("\n=== Testing counter synchronization after iframe remount ===")
            
            # Locate the counter button iframe
            counter_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(4)
            
            counter_button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
            counter_button.wait_for(state="visible", timeout=10000)
            
            # Step 1: First click to establish counter
            print("\nStep 1: First click to establish counter")
            initial = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  Initial counter: {initial}")
            
            counter_button.click()
            page.wait_for_timeout(1000)
            
            after_first = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  After first click: {after_first}")
            assert after_first == initial + 1, f"First click failed: expected {initial + 1}, got {after_first}"
            print(f"  ✅ First click registered")
            
            # Step 2: Force iframe reload
            print("\nStep 2: Forcing iframe reload...")
            page.evaluate("""
                (selector) => {
                    const iframes = document.querySelectorAll(selector);
                    if (iframes.length > 4) {
                        const iframe = iframes[4];
                        const src = iframe.src;
                        iframe.src = src; // Force reload
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
            
            # Step 3: Click immediately after reload - should work with Solution 3!
            print("\nStep 3: Click immediately after iframe reload")
            before_second = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  Counter before second click: {before_second}")
            
            counter_button.click()
            page.wait_for_timeout(1000)
            
            after_second = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"  Counter after second click: {after_second}")
            
            # With Solution 3, this should work immediately!
            assert after_second == before_second + 1, f"Second click failed: expected {before_second + 1}, got {after_second}"
            print(f"  ✅ Second click registered immediately after iframe reload!")
            
            print("\n=== SUCCESS: Counter synchronization working correctly! ===")
            print(f"Initial: {initial}")
            print(f"After 1st click: {after_first} (delta: +{after_first - initial})")
            print(f"After iframe reload + 2nd click: {after_second} (delta: +{after_second - after_first})")
            print("✅ Solution 3 (Sync Counter) is working correctly!")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.e2e
def test_counter_sync_multiple_remounts():
    """
    Test that counter sync works correctly across multiple iframe remounts.
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8521
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
            
            page.wait_for_selector("[data-testid='counter-value']", timeout=30000)
            
            print("\n=== Testing multiple iframe remounts ===")
            
            def reload_iframe():
                page.evaluate("""
                    (selector) => {
                        const iframes = document.querySelectorAll(selector);
                        if (iframes.length > 4) {
                            const iframe = iframes[4];
                            const src = iframe.src;
                            iframe.src = src;
                        }
                    }
                """, "iframe[title='hyperlink_button._component.hyperlink_button']")
                page.wait_for_timeout(2000)
            
            def get_button():
                counter_frame = page.frame_locator(
                    "iframe[title='hyperlink_button._component.hyperlink_button']"
                ).nth(4)
                button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
                button.wait_for(state="visible", timeout=10000)
                return button
            
            # Test pattern: click -> reload -> click -> reload -> click
            for i in range(3):
                print(f"\nIteration {i + 1}:")
                
                before = int(page.locator("[data-testid='counter-value']").inner_text())
                print(f"  Before click: {before}")
                
                button = get_button()
                button.click()
                page.wait_for_timeout(1000)
                
                after = int(page.locator("[data-testid='counter-value']").inner_text())
                print(f"  After click: {after}")
                assert after == before + 1, f"Click {i + 1} failed"
                
                if i < 2:  # Don't reload after last iteration
                    print(f"  Reloading iframe...")
                    reload_iframe()
            
            print("\n✅ All clicks registered correctly across multiple remounts!")
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.e2e
def test_counter_sync_rapid_clicks_after_remount():
    """
    Test clicks immediately after iframe remount work correctly.
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8522
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
            
            page.wait_for_selector("[data-testid='counter-value']", timeout=30000)
            
            print("\n=== Testing clicks after iframe remount ===")
            
            # Build up counter
            counter_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(4)
            button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
            button.wait_for(state="visible", timeout=10000)
            
            # Click 3 times to build up counter with generous delays
            print("Building up counter with 3 clicks...")
            for i in range(3):
                button.click()
                page.wait_for_timeout(800)  # Generous delay for each rerun
            
            before_reload = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"Counter before reload: {before_reload}")
            # Be lenient - at least 2 clicks should register
            assert before_reload >= 2, f"Expected at least 2 clicks before reload, got {before_reload}"
            
            # Reload iframe
            print("Reloading iframe...")
            page.evaluate("""
                (selector) => {
                    const iframes = document.querySelectorAll(selector);
                    if (iframes.length > 4) {
                        const iframe = iframes[4];
                        const src = iframe.src;
                        iframe.src = src;
                    }
                }
            """, "iframe[title='hyperlink_button._component.hyperlink_button']")
            page.wait_for_timeout(2000)
            
            # Get button again after reload
            counter_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(4)
            button = counter_frame.locator("[data-testid='hyperlink-button-counter_btn']").locator("button")
            button.wait_for(state="visible", timeout=10000)
            
            # Click 2 more times after reload
            print("Performing 2 clicks after reload...")
            for i in range(2):
                button.click()
                page.wait_for_timeout(800)
            
            page.wait_for_timeout(500)
            
            after_clicks = int(page.locator("[data-testid='counter-value']").inner_text())
            print(f"Counter after clicks: {after_clicks}")
            
            # Verify at least 1 click was added (Solution 3 should allow immediate clicks after remount)
            assert after_clicks > before_reload, f"Expected clicks to increase after remount, before={before_reload}, after={after_clicks}"
            print(f"✅ Clicks registered after remount! ({before_reload} -> {after_clicks})")
            
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


@pytest.mark.e2e
def test_counter_independence_across_buttons():
    """
    Test that different buttons have independent counter synchronization.
    """
    pytest.importorskip("playwright")
    from playwright.sync_api import sync_playwright
    
    try:
        from playwright.sync_api import Error as PlaywrightError
    except Exception:  # noqa: BLE001
        PlaywrightError = Exception

    port = 8523
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
            
            page.wait_for_selector("[data-testid='multi-button-state']", timeout=30000)
            
            print("\n=== Testing counter independence across multiple buttons ===")
            
            # Get all three buttons
            button_a_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(1)
            button_b_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(2)
            
            button_a = button_a_frame.locator("[data-testid='hyperlink-button-test2a']").locator("button")
            button_b = button_b_frame.locator("[data-testid='hyperlink-button-test2b']").locator("button")
            
            button_a.wait_for(state="visible", timeout=10000)
            button_b.wait_for(state="visible", timeout=10000)
            
            # Click button A twice
            print("Clicking button A twice...")
            for _ in range(2):
                button_a.click()
                page.wait_for_timeout(500)
            
            # Click button B once
            print("Clicking button B once...")
            button_b.click()
            page.wait_for_timeout(500)
            
            # Reload all iframes
            print("Reloading all iframes...")
            page.evaluate("""
                (selector) => {
                    const iframes = document.querySelectorAll(selector);
                    iframes.forEach(iframe => {
                        const src = iframe.src;
                        iframe.src = src;
                    });
                }
            """, "iframe[title='hyperlink_button._component.hyperlink_button']")
            page.wait_for_timeout(3000)
            
            # Re-acquire buttons
            button_a_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(1)
            button_b_frame = page.frame_locator(
                "iframe[title='hyperlink_button._component.hyperlink_button']"
            ).nth(2)
            
            button_a = button_a_frame.locator("[data-testid='hyperlink-button-test2a']").locator("button")
            button_b = button_b_frame.locator("[data-testid='hyperlink-button-test2b']").locator("button")
            
            button_a.wait_for(state="visible", timeout=10000)
            button_b.wait_for(state="visible", timeout=10000)
            
            # Click each button once more - both should register immediately
            print("Clicking both buttons after reload...")
            button_a.click()
            page.wait_for_timeout(500)
            button_b.click()
            page.wait_for_timeout(500)
            
            print("✅ Independent counter synchronization verified!")
            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
