import inspect

import streamlit as st

from hyperlink_button import hyperlink_button
from hyperlink_button import _component as hb_comp  # type: ignore


def test_signature_matches_st_button():
    sig = inspect.signature(hyperlink_button)
    st_sig = inspect.signature(st.button)
    assert list(sig.parameters.keys()) == list(st_sig.parameters.keys())


def test_forwarding_calls(monkeypatch):
    # Patch internal component to a dummy function to verify forwarding
    calls = {}

    def fake_component(*args, **kwargs):
        calls["args"] = args
        calls["kwargs"] = kwargs
        return 2

    monkeypatch.setattr(hb_comp, "_HB_COMPONENT", fake_component)
    # click_count 2 > last_seen 0
    res = hyperlink_button("Link", key="hb1")
    assert res is True
    assert "kwargs" in calls
