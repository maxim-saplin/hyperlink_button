from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, Sequence

import streamlit as st
import streamlit.components.v1 as components

_COMPONENT_NAME = "hyperlink_button"
_LAST_SEEN_PREFIX = "_hyperlink_button_last_seen_"
_FRONTEND_DIR = Path(__file__).resolve().parent / "frontend" / "build"
_DEV_URL = os.environ.get("HYPERLINK_BUTTON_DEV_URL")

if _DEV_URL:
    _component_func = components.declare_component(_COMPONENT_NAME, url=_DEV_URL)
elif (_FRONTEND_DIR / "index.html").exists():
    _component_func = components.declare_component(
        _COMPONENT_NAME, path=str(_FRONTEND_DIR)
    )
else:
    _component_func = None


def _state_key(label: str, key: str | None) -> str:
    identity = key if key is not None else label
    return f"{_LAST_SEEN_PREFIX}{identity}"


def _edge_triggered(token: Any, state_key: str) -> bool:
    if token is None:
        return False

    last_seen = st.session_state.get(state_key)
    try:
        token_value = int(token)
    except (TypeError, ValueError):
        st.session_state[state_key] = token
        return token != last_seen

    try:
        baseline = int(last_seen)
    except (TypeError, ValueError):
        baseline = 0

    st.session_state[state_key] = token_value
    return token_value > baseline


def button(
    label: str,
    key: str | None = None,
    help: str | None = None,
    on_click: Callable[..., Any] | None = None,
    args: Sequence[Any] | None = None,
    kwargs: dict[str, Any] | None = None,
    type: str = "secondary",
    icon: str | None = None,
    disabled: bool = False,
    use_container_width: bool = False,
) -> bool:
    if _component_func is None:
        return st.button(
            label=label,
            key=key,
            help=help,
            on_click=on_click,
            args=args,
            kwargs=kwargs,
            type=type,
            icon=icon,
            disabled=disabled,
            use_container_width=use_container_width,
        )

    call_args = [] if args is None else list(args)
    call_kwargs = {} if kwargs is None else dict(kwargs)

    click_count = _component_func(
        label=label,
        key=key,
        help=help,
        type=type,
        icon=icon,
        disabled=disabled,
        use_container_width=use_container_width,
        default=0,
    )

    clicked = _edge_triggered(click_count, _state_key(label, key))

    if clicked and on_click is not None:
        on_click(*call_args, **call_kwargs)

    return bool(clicked)
