from __future__ import annotations

import hashlib
import inspect
import os
import re

import streamlit as st
import streamlit.components.v1 as components


_BUILD_DIR = os.path.join(os.path.dirname(__file__), "frontend", "build")
_DEV_URL = os.environ.get("HYPERLINK_BUTTON_DEV_SERVER_URL")


def _declare_component():
    # components.declare_component expects exactly one of url/path.
    if _DEV_URL:
        return components.declare_component("hyperlink_button", url=_DEV_URL)
    return components.declare_component("hyperlink_button", path=_BUILD_DIR)


_HB_COMPONENT = _declare_component()


def _safe_id(value: str) -> str:
    # For DOM/test ids.
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value)
    return value[:64] if value else "anon"


def _instance_id(label: str, user_key: str | None) -> str:
    # If user provided an explicit key, Streamlit already enforces uniqueness;
    # use it to make Playwright selectors stable.
    if user_key:
        return _safe_id(user_key)

    # Otherwise derive a stable id for a given callsite + label.
    # stack[0] = _instance_id, stack[1] = hyperlink_button, stack[2] = caller
    frame = inspect.stack()[2]
    payload = f"{frame.filename}:{frame.lineno}:{frame.function}:{label}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def hyperlink_button(
    label: str,
    key: str | None = None,
    help: str | None = None,
    on_click=None,
    args=None,
    kwargs=None,
    *,
    type: str = "secondary",
    icon: str | None = None,
    icon_position: str = "left",
    disabled: bool = False,
    use_container_width: bool | None = None,
    width="content",
    shortcut: str | None = None,
) -> bool:
    """Hyperlink-styled Streamlit button.

    Mirrors the current `st.button` API but renders as hyperlink-like text.
    """

    instance_id = _instance_id(label, key)
    component_key = (
        f"_hyperlink_button:{key}" if key else f"_hyperlink_button:{instance_id}"
    )
    state_key = f"_hyperlink_button_last_click:{component_key}"
    last_seen = int(st.session_state.get(state_key, 0) or 0)

    click_count = _HB_COMPONENT(
        key=component_key,
        label=label,
        instance_id=instance_id,
        testid=f"hyperlink-button-{instance_id}",
        help=help,
        disabled=disabled,
        type=type,
        icon=icon,
        icon_position=icon_position,
        use_container_width=use_container_width,
        width=width,
        shortcut=shortcut,
        default=0,
    )

    # Component returns an int counter; convert to ephemeral bool.
    try:
        click_count_int = int(click_count or 0)
    except Exception:
        click_count_int = 0

    clicked = click_count_int > last_seen
    # Mirror st.button's "trigger-like" behavior for users who rely on session_state.
    if key:
        st.session_state[key] = clicked

    if clicked:
        st.session_state[state_key] = click_count_int
        if on_click is not None:
            cb_args = args or ()
            cb_kwargs = kwargs or {}
            on_click(*cb_args, **cb_kwargs)
    return clicked
