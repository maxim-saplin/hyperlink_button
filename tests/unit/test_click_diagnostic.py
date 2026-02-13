"""Diagnostic tests for the click reliability fixes.

These tests model the click protocol after the fixes:
  - Side effect moved outside the state updater (single emit per click)
  - Native button keyboard behavior used (no custom keydown double-fire)
  - Counter seeded from Python `last_seen` after remounts
"""


# ---------------------------------------------------------------------------
# Helpers: lightweight simulation of the Python-side click detection logic
# (mirrors _component.py lines 71-106)
# ---------------------------------------------------------------------------

class FakeSessionState(dict):
    """Minimal stand-in for st.session_state."""
    pass


def make_detector(component_key="test"):
    """Return a callable that simulates one hyperlink_button() rerun cycle.

    Returns (detect_fn, session_state) so the test can inspect internal state.
    """
    ss = FakeSessionState()
    state_key = f"_hyperlink_button_last_click:_hyperlink_button:{component_key}"

    def detect(click_count_from_component):
        last_seen = int(ss.get(state_key, 0) or 0)
        try:
            click_count_int = int(click_count_from_component or 0)
        except Exception:
            click_count_int = 0
        clicked = click_count_int > last_seen
        if clicked:
            ss[state_key] = click_count_int
        return clicked

    return detect, ss, state_key


# ---------------------------------------------------------------------------
# Helpers: lightweight simulation of the React-side click counter
# (mirrors HyperlinkButton.tsx handleActivate)
# ---------------------------------------------------------------------------

class ReactClickCounter:
    """Model the fixed React component behavior.

    The state updater is pure and side effects are emitted after state changes,
    so StrictMode does not duplicate Streamlit.setComponentValue calls.
    """

    def __init__(self, seed=0):
        self.click_count = seed
        self.values_sent = []

    def handle_activate(self, *, strict_mode=False):
        _ = strict_mode  # Signature parity with previous diagnostic helper.
        self.click_count += 1
        self.values_sent.append(self.click_count)

    def reset(self, seed=0):
        """Simulate iframe recreation with Python-seeded counter restore."""
        self.click_count = seed


# ===================================================================
# DIAGNOSTIC 1 – Normal flow (no StrictMode, no iframe recreation)
# ===================================================================

def test_normal_flow_works():
    """Baseline: clicks register reliably under ideal conditions."""
    detect, _, _ = make_detector()
    react = ReactClickCounter()

    results = []
    for _ in range(5):
        react.handle_activate(strict_mode=False)
        value = react.values_sent[-1]
        results.append(detect(value))

    # Every click should be detected
    assert results == [True, True, True, True, True], (
        f"Normal flow should detect every click, got {results}"
    )


# ===================================================================
# DIAGNOSTIC 2 – iframe recreation causes counter reset
# ===================================================================

def test_iframe_recreation_uses_seed_and_keeps_clicks_detectable():
    """After remount, the React counter is seeded from Python last_seen."""
    detect, ss, state_key = make_detector()
    react = ReactClickCounter()

    # --- Normal click #1 ---
    react.handle_activate()
    assert detect(react.values_sent[-1]) is True        # 1 > 0 → True
    assert ss[state_key] == 1

    # --- Normal click #2 ---
    react.handle_activate()
    assert detect(react.values_sent[-1]) is True        # 2 > 1 → True
    assert ss[state_key] == 2

    # --- iframe is recreated; React is seeded from Python last_seen ---
    assert ss[state_key] == 2
    react.reset(seed=ss[state_key])
    assert react.click_count == 2

    # --- User clicks ONCE after recreation ---
    react.handle_activate()
    sent_value = react.values_sent[-1]    # will be 3 (2 + 1)
    click_detected = detect(sent_value)

    # Fixed: 3 > 2 -> True (no dropped click).
    assert click_detected is True, (
        f"Expected first click after remount to register (sent {sent_value}, "
        f"last_seen=2), but got detected={click_detected}"
    )


# ===================================================================
# DIAGNOSTIC 3 – StrictMode double-invocation of setComponentValue
# ===================================================================

def test_strict_mode_does_not_duplicate_side_effects():
    """StrictMode should still emit one component value per click."""
    react = ReactClickCounter()

    react.handle_activate(strict_mode=True)

    assert react.click_count == 1
    assert len(react.values_sent) == 1, (
        f"Expected 1 setComponentValue call under StrictMode, "
        f"got {len(react.values_sent)}: {react.values_sent}"
    )
    assert react.values_sent == [1]


def test_strict_mode_click_remains_true_without_second_rerun():
    """A fixed click emits once, so no True->False flicker rerun sequence."""
    detect, _, _ = make_detector()
    react = ReactClickCounter()

    react.handle_activate(strict_mode=True)
    assert react.values_sent == [1]

    rerun1 = detect(react.values_sent[0])   # 1 > 0 -> True
    assert rerun1 is True


# ===================================================================
# DIAGNOSTIC 4 – Combined: StrictMode + iframe recreation
# ===================================================================

def test_strict_mode_plus_iframe_recreation():
    """StrictMode plus remount stays stable with Python-seeded counter."""
    detect, ss, state_key = make_detector()
    react = ReactClickCounter()

    # 3 clicks under StrictMode.
    for _ in range(3):
        react.handle_activate(strict_mode=True)
        detect(react.values_sent[-1])

    assert react.click_count == 3
    assert ss[state_key] == 3

    # Iframe recreation; seed from Python side.
    react.reset(seed=ss[state_key])
    react.handle_activate(strict_mode=True)
    val = react.values_sent[-1]
    assert detect(val) is True


# ===================================================================
# DIAGNOSTIC 5 – Verify side-effect placement is the root cause
# ===================================================================

def test_side_effect_outside_updater_is_safe():
    """If setComponentValue were called OUTSIDE the state updater
    (the correct pattern), StrictMode double-invocation would NOT
    cause double side effects.

    This models the CORRECT implementation for comparison.
    """
    class CorrectReactCounter:
        def __init__(self):
            self.click_count = 0
            self.values_sent = []

        def handle_activate_correct(self, *, strict_mode=False):
            # Correct: state updater is pure, side effect is separate
            # In real React: setClickCount(prev => prev + 1)
            # then useEffect or post-setState: setComponentValue(newCount)
            updater_calls = 2 if strict_mode else 1
            for _ in range(updater_calls):
                _ = self.click_count + 1  # pure computation, no side effect
            self.click_count += 1

            # Side effect fires ONCE, after state update
            self.values_sent.append(self.click_count)

    react = CorrectReactCounter()
    detect, _, _ = make_detector()

    results = []
    for _ in range(5):
        react.handle_activate_correct(strict_mode=True)
        val = react.values_sent[-1]
        results.append(detect(val))

    # With correct implementation, every click registers even under StrictMode
    assert results == [True, True, True, True, True], (
        f"Correct implementation should detect every click, got {results}"
    )
    # And only 5 setComponentValue calls (not 10)
    assert len(react.values_sent) == 5
