from __future__ import annotations

from playwright.sync_api import sync_playwright


def main() -> None:
    url = "http://localhost:8501"
    screenshot_path = "/work/tmp_inspect.png"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="networkidle")

        btn = page.get_by_role("button", name="A default")
        btn.wait_for(state="visible", timeout=10_000)

        handle = btn.element_handle()
        if handle is None:
            raise RuntimeError("Could not get element_handle for button")

        outer = handle.evaluate("(el) => el.outerHTML")
        print("button outerHTML:\n", outer)

        # Dump ancestry with ids and data attributes to find a stable selector.
        ancestors = handle.evaluate(
            """
            (el) => {
              const out = [];
              let n = el;
              for (let i = 0; i < 12 && n; i++) {
                const attrs = {};
                for (const a of n.attributes || []) {
                  if (a.name === 'id' || a.name.startsWith('data-') || a.name === 'class') {
                    attrs[a.name] = a.value;
                  }
                }
                out.push({ tag: n.tagName, ...attrs });
                n = n.parentElement;
              }
              return out;
            }
            """
        )
        print("ancestry:")
        for row in ancestors:
            print(" ", row)

        html = page.content()
        print("page contains $$ID?", "$$ID" in html)
        if "$$ID" in html:
            idx = html.index("$$ID")
            print("snippet around $$ID:\n", html[max(0, idx - 120) : idx + 240])

        btn.click()
        page.wait_for_timeout(1000)

        page.get_by_text("clicked_a", exact=False).wait_for(timeout=10_000)

        page.screenshot(path=screenshot_path, full_page=True)

        stbtn = handle.evaluate_handle(
            "(el) => el.closest('[data-testid=\\\"stButton\\\"]')"
        )
        st_outer = stbtn.evaluate("(el) => (el ? el.outerHTML : null)")
        print("closest stButton outerHTML:\n", st_outer)

        browser.close()

    print(f"saved {screenshot_path}")


if __name__ == "__main__":
    main()
