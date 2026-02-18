Implementation approaches for hyperlink_button

Objective
--------
Recommend an implementation approach for a `hyperlink_button` widget that matches Streamlit's `st.button` API and behavior but renders visually like an HTML hyperlink.

Scope and constraints
---------------------
- This is a design/spec doc only; no code changes are made.
- Allowed repo paths: `specs/**` (this file).
- Do not edit `st_docs/` (read-only). Document cites `st_docs/` files by path for justification and verification.

Summary recommendation
----------------------
Implement `hyperlink_button` as a small custom component (Streamlit Components) that mirrors `st.button`'s API and internal semantics but renders as an inline anchor-styled control. Use the components API (frontend React + minimal Python wrapper) rather than simply styling `st.button` output because matching callback semantics, return semantics, disabled handling, and key stability reliably requires control over event lifecycle and state serialization.

Rationale (short)
- A styling-wrapper around `st.button` is the lowest implementation effort but cannot reliably control internal Session State and rerun/callback semantics that `st.button` supports across different Streamlit versions and in headless/docker runs.
- A custom component gives full control over events and client-server messages and can reproduce `st.button` return/disabled/key behaviour; it requires more work (JS/TS + Python glue) and test harness but is the safest for correctness.

Approaches considered
--------------------

1) Style-wrapped `st.button` (pure-Python, CSS/HTML hacks)

- Description: Render a `st.button` but hide its default visual (or place it offscreen) and render a clickable <a> or <span> with hyperlink styles. Clicks trigger the underlying `st.button` element via DOM events or form submission.

- Ability to match API+behavior:
  - Callback semantics: Weak. `st.button` triggers a rerun with a True return for one-run when the underlying input is triggered. Programmatically synthesizing the click via JS may work in a browser session but is brittle across Streamlit internal changes and disabled states.
  - Return semantics: Partial. You can read the boolean from `st.button` on rerun. Synthetic events may not always produce identical timing/ordering as real clicks.
  - Disabled behavior: Difficult. If you keep an actual `st.button` in the DOM, disabled styling can be applied but synchronizing the visible hyperlink's appearance and preventing synthetic clicks requires careful JS that may not be supported via static markdown/HTML in Streamlit.
  - Key stability: Moderate. Because the wrapped `st.button` is still a native Streamlit widget, using `key` will work; but DOM shimming and offscreen placement can create unexpected widget ordering or focus differences when app layout changes.

- Pros:
  - Minimal Python-only changes; no build step.
  - Reuses Streamlit internals; likely smallest maintenance surface initially.

- Cons / Risks:
  - Brittle: relies on DOM structure and internal ids that Streamlit might change.
  - Hard to guarantee exact rerun timing and event ordering match `st.button` across environments (headless Docker, different browsers).
  - Accessibility and keyboard focus behavior may differ from native `st.button` usage.

2) Custom Streamlit Component (recommended)

- Description: Create a dedicated Streamlit Component (frontend in React or plain JS) that renders as a semantic anchor-styled element but implements the same client-server event contract as `st.button`. The Python wrapper exposes an `st.hyperlink_button(label, key=None, disabled=False, on_click=None, args=None, kwargs=None)` compatible signature and returns a boolean (clicked this run) like `st.button`.

- Ability to match API+behavior:
  - Callback semantics: Strong. Components can emit messages to the Python backend; the component can call `streamlit.setComponentValue(...)` (or the equivalent messaging API) to indicate a click, triggering the same rerun semantics. The wrapper can also accept `on_click` + args/kwargs and execute the callback server-side during the rerun.
  - Return semantics: Strong. On rerun the Python component wrapper can return True for the run immediately after the click and False otherwise, matching `st.button` contract.
  - Disabled behavior: Strong. The component can observe the `disabled` prop and render non-interactive anchor semantics (aria-disabled, prevent pointer events). It can also ensure `on_click` is not called when disabled.
  - Key stability: Strong. The component supports Streamlit widget keys; by matching the widget id serialization and stable props ordering the key will remain stable across rerenders.

- Pros:
  - Precise control over message lifecycle and event ordering.
  - Can match `st.button` behavior closely including accessibility attributes, keyboard activation (Enter/Space), focus/active states, and disabled semantics.
  - Testable in headless environments (JS unit tests + Docker verification).

- Cons / Costs:
  - Higher implementation cost (frontend + build + JS toolchain) and extra CI steps.
  - Need to maintain component build and ensure compatibility across Streamlit releases.

3) Hybrid: Use `st.markdown` with a link + server-side URL parameter handling

- Description: Render an anchor tag that links to the current app URL but includes query params (or fragment) that indicate the 'button' was clicked. On app load, Python inspects query params (via `st.experimental_get_query_params()` or similar) to detect clicks.

- Ability to match API+behavior:
  - Callback semantics: Weak/Workaround. Detecting click on load is possible, but this approach triggers a full page navigation (not the simple rerun semantic) and requires manual query param management and cleanup.
  - Return semantics: Weak. Returning a boolean that is True only for the run immediately after the click is possible by clearing the param after detection, but race conditions / browser history interactions make the semantics fragile.
  - Disabled behavior: Moderate. You can render non-clickable anchor or set href to `javascript:void(0)` but disabling needs to be enforced client-side.
  - Key stability: N/A (no Streamlit widget key semantics) — the approach doesn't integrate with the widget registry.

- Pros:
  - No JS build step; very simple to implement.
  - Works with plain Markdown/HTML in Streamlit.

- Cons / Risks:
  - Loses widget registry integration: callbacks, session state, and `key` behavior will diverge from `st.button`.
  - Browser history and deep-linking side-effects.

Evaluation vs `st.button` API & behavior
-------------------------------------
We evaluate four key features requested in the work order: callback semantics, return semantics, disabled behavior, key stability.

- Callback semantics (callable `on_click`) — how easily a click triggers server-side callback with same timing:
  1. Style-wrapped `st.button`: Medium/Fragile. Works when DOM events map to the real `st.button`, but injecting/synthesizing events is brittle.
  2. Custom Component: High. Components intentionally send messages to server; callbacks can be invoked server-side during rerun.
  3. Query-param link: Low. Requires navigation and manual server-side logic.

- Return semantics (function returns boolean True only on the immediate run following click):
  1. Style-wrapped `st.button`: Medium. Likely achievable but edge cases (timing, race) exist.
  2. Custom Component: High. Wrapper can mirror `st.button` behavior exactly by returning value from component state.
  3. Query-param link: Low/Workaround.

- Disabled behavior (widget disabled state prevents activation and is visually represented):
  1. Style-wrapped `st.button`: Medium. Possible if real `st.button` used, syncing visual link state is error-prone.
  2. Custom Component: High. The component enforces disabled state in the frontend and does not emit click events when disabled.
  3. Query-param link: Medium. Needs client-side handling to prevent navigation.

- Key stability (ability to provide `key=` and preserve widget identity across reruns):
  1. Style-wrapped `st.button`: High. Because `st.button` is used, keys map naturally.
  2. Custom Component: High. Components support `key` via Streamlit's widget registry if the Python wrapper integrates properly.
  3. Query-param link: Low. Not part of widget registry.

Recommendation (detail)
---------------------
Recommendation: Build a small custom Streamlit Component (frontend JS/React + Python wrapper) that intentionally reproduces `st.button` API and returns, while rendering visually as a hyperlink.

Key reasons:
- Deterministic control: Components provide explicit client-to-server messaging channels so we can precisely reproduce rerun semantics and when the Python-side callback runs.
- Accessibility and keyboard parity: The frontend can implement keyboard activation (Enter/Space), proper aria attributes, and focus ring behavior so hyperlink-button works for keyboard users like `st.button` does.
- Disabled & key correctness: The component can implement `disabled` as a first-class prop, and the Python wrapper can participate in the widget registry to maintain stable keys.

Implementation sketch
--------------------
- Python API surface (wrapper):

  def hyperlink_button(label: str, key: Optional[str] = None, disabled: bool = False, on_click: Optional[callable] = None, args: Optional[tuple] = None, kwargs: Optional[dict] = None) -> bool:
      """Return True on the run immediately after the user clicks the hyperlink.
      If `on_click` is provided, call it during that run (same semantics as `st.button`)."""

- Frontend behavior:
  - Render an inline element with anchor styling (blue, underline, pointer cursor).
  - Support `role="button"`, `tabindex=0`, keydown handlers for Enter/Space.
  - When activated and not disabled, call `Streamlit.setComponentValue({clicked: true})` (or the current components messaging API).

- Python wrapper behavior:
  - On component value True, return True for that run and call `on_click` if provided, passing args/kwargs.
  - Ensure the returned boolean resets on subsequent runs (store ephemeral state in widget value semantics).

- Testing and verification:
  - Unit tests for Python wrapper (simulate component return values).
  - JS tests for keyboard and pointer events.
  - Docker headless verification in Chrome (playwright/selenium) to validate focus, keyboard activation, disabled behavior, and callback timing in a containerized environment.

Unknowns and empirical verifications (Docker-only)
------------------------------------------------
The following items must be verified empirically in the Docker environment because they depend on how Streamlit's runtime serializes widget state and how headless browsers behave in the CI container.

1. Exact component messaging API and lifecycle details in the target Streamlit runtime (confirm `setComponentValue` behavior and on-rerun ordering). Verify with `st_docs/components.md` and real tests.

2. Keyboard activation parity: ensure Enter and Space produce the same rerun ordering and focus behavior as `st.button` in headless Chrome inside Docker.

3. Interaction with `st.form` and other input wrappers: does the component behave identically to `st.button` when used inside `st.form`? See `st_docs/elements/form.md`.

4. Widget registry behavior and key collisions: confirm the component's widget id generation and `key` handling exactly match expectations and do not break session state across reruns. See `st_docs/widgets.md` or `st_docs/elements/widgets.md`.

5. Accessibility semantics: confirm screen reader behavior in containerized test (manual or automated a11y checks) to ensure parity with `st.button`.

Relevant `st_docs/` files to consult (by path)
------------------------------------------
- `st_docs/elements/button.md` — describes `st.button` API and behavior
- `st_docs/components.md` — describes the Streamlit Components API and lifecycle
- `st_docs/elements/form.md` — describes forms and how `st.button` behaves inside forms
- `st_docs/elements/widget_behavior.md` — (widget lifecycle, return semantics)
- `st_docs/elements/keyboard_accessibility.md` — keyboard and accessibility expectations for interactive widgets

If any of these files are in slightly different paths under `st_docs/`, consult the local tree; these entries are the canonical topics to cite when implementing.

Risks, mitigations, and tradeoffs
--------------------------------
- Risk: Component maintenance burden across Streamlit releases. Mitigation: keep component minimal, rely on standard messaging API, and add CI integration tests pinned to the Docker image used for verification.
- Risk: Slight behavioral drift from `st.button` over time. Mitigation: include a test suite that verifies return boolean semantics, disabled behavior, and keyboard activation in CI against the target Streamlit version.
- Tradeoff: More upfront work (JS build) vs correctness and robustness. This is acceptable because the acceptance criteria require matching `st.button` API+behavior.

Next steps
----------
1. Confirm exact `st_docs/` paths in the repo and copy authoritative snippets or examples needed for the component wrapper.

Handoff note for implementer
---------------------------
- Changed paths: `specs/implementation_approach.md` (this file)
- Why: Provide a decision and implementation plan for `hyperlink_button` that meets `st.button` parity requirements.
- Verification: doc-only; implementation will include tests and Docker verification steps described above.
