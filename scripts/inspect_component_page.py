from __future__ import annotations

from playwright.sync_api import sync_playwright


def main() -> None:
    url = "http://localhost:8501/component/hyperlink_button._element.hyperlink_button/index.html?streamlitUrl=http%3A%2F%2Flocalhost%3A8501%2F"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        msgs: list[tuple[str, str]] = []
        reqs: list[tuple[str, str]] = []
        page.on("console", lambda m: msgs.append((m.type, m.text)))
        page.on("pageerror", lambda e: msgs.append(("pageerror", str(e))))
        page.on("request", lambda r: reqs.append((r.method, r.url)))

        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        print("requests:")
        for m, u in reqs[:20]:
            print(" ", m, u)

        print("messages:")
        for t, s in msgs[:50]:
            print(" ", t, s)

        print(
            "typeof window.__hyperlink_button_streamlit",
            page.evaluate("() => typeof window.__hyperlink_button_streamlit"),
        )
        print("root", page.locator("#root").evaluate("(el) => el.outerHTML"))
        print("button_count", page.locator("button").count())

        page.screenshot(path="/work/tmp_component_inspect.png", full_page=True)

        browser.close()


if __name__ == "__main__":
    main()
