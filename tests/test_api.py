import inspect

import streamlit as st
from streamlit.testing.v1 import AppTest

import hyperlink_button as hb
from hyperlink_button import component


def test_signature_matches_streamlit_button_defaults() -> None:
    sig = inspect.signature(hb.button)
    param_names = list(sig.parameters.keys())
    assert param_names == [
        "label",
        "key",
        "help",
        "on_click",
        "args",
        "kwargs",
        "type",
        "icon",
        "disabled",
        "use_container_width",
    ]

    defaults = {name: p.default for name, p in sig.parameters.items()}
    assert defaults["key"] is None
    assert defaults["help"] is None
    assert defaults["on_click"] is None
    assert defaults["args"] is None
    assert defaults["kwargs"] is None
    assert defaults["type"] == "secondary"
    assert defaults["icon"] is None
    assert defaults["disabled"] is False
    assert defaults["use_container_width"] is False


def _app() -> None:
    import hyperlink_button as hb
    import streamlit as st

    clicked = hb.button("Click me")
    st.session_state["clicked"] = clicked


def test_click_behavior_fallback(monkeypatch) -> None:
    monkeypatch.setattr(component, "_component_func", None)

    at = AppTest.from_function(_app).run()
    assert at.session_state["clicked"] is False
    at.button[0].click().run()
    assert at.session_state["clicked"] is True


def test_click_behavior_edge_trigger(monkeypatch) -> None:
    values = iter([None, 1, 1, 2])

    def _fake_component(**_kwargs):
        return next(values)

    monkeypatch.setattr(component, "_component_func", _fake_component)

    def _edge_app() -> None:
        import hyperlink_button as hb
        import streamlit as st

        if "callback_calls" not in st.session_state:
            st.session_state["callback_calls"] = 0

        def _on_click() -> None:
            st.session_state["callback_calls"] += 1

        clicked = hb.button("Edge", on_click=_on_click)
        st.session_state["clicked"] = clicked

    at = AppTest.from_function(_edge_app).run()
    assert at.session_state["clicked"] is False
    assert at.session_state["callback_calls"] == 0

    at.run()
    assert at.session_state["clicked"] is True
    assert at.session_state["callback_calls"] == 1

    at.run()
    assert at.session_state["clicked"] is False
    assert at.session_state["callback_calls"] == 1

    at.run()
    assert at.session_state["clicked"] is True
    assert at.session_state["callback_calls"] == 2
