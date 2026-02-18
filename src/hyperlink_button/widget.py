from __future__ import annotations

import inspect
import re
from collections.abc import Callable
from uuid import uuid4

import streamlit as st


def _marker_id(key: str | None) -> str:
    if key is None:
        token = uuid4().hex
    else:
        token = re.sub(r"[^a-zA-Z0-9_-]", "-", str(key)).strip("-")
        if not token:
            token = uuid4().hex
    return f"hb-link-{token}"


def _style_block(marker_id: str) -> str:
    # Target the Streamlit element container that contains our inline marker
    # and the following element container that holds the button. This scopes
    # the styles to only the button that immediately follows the marker.
    selector = (
        f"div[data-testid=\"stElementContainer\"]:has(#{marker_id}) + "
        "div[data-testid=\"stElementContainer\"] div[data-testid=\"stButton\"] button"
    )
    return (
        "<style>"
        f"{selector} {{"
        "background: none;"
        "border: none;"
        "padding: 0;"
        "cursor: pointer;"
        "color: var(--primary-color, #1a0dab);"
        "text-decoration: underline;"
        "text-underline-offset: 2px;"
        "font-weight: 500;"
        "}"
        f"{selector}:hover {{"
        "text-decoration-thickness: 2px;"
        "}"
        f"{selector}:focus-visible {{"
        "outline: 2px solid currentColor;"
        "outline-offset: 2px;"
        "}"
        f"{selector}:disabled {{"
        "color: var(--text-color, #6b6b6b);"
        "text-decoration: none;"
        "cursor: not-allowed;"
        "opacity: 0.6;"
        "}"
        "</style>"
    )


def hyperlink_button(
    label: str,
    key: str | None = None,
    help: str | None = None,
    on_click: Callable[..., object] | None = None,
    args: tuple[object, ...] | None = None,
    kwargs: dict[str, object] | None = None,
    *,
    type: str = "secondary",
    icon: str | None = None,
    icon_position: str = "left",
    disabled: bool = False,
    use_container_width: bool | None = None,
    width: int | str = "content",
    shortcut: str | None = None,
) -> bool:
    marker_id = _marker_id(key)
    # Emit the marker span and the scoped style together so the style
    # appears immediately before the button in the DOM. Use `st.markdown`
    # with `unsafe_allow_html=True` so the marker is placed inline in the
    # real Streamlit DOM (not inside an iframe-like HTML element).
    st.markdown(
        f"<span id=\"{marker_id}\"></span>" + _style_block(marker_id),
        unsafe_allow_html=True,
    )

    result = st.button(
        label,
        key=key,
        help=help,
        on_click=on_click,
        args=args,
        kwargs=kwargs,
        type=type,
        icon=icon,
        icon_position=icon_position,
        disabled=disabled,
        use_container_width=use_container_width,
        width=width,
        shortcut=shortcut,
    )
    return result


setattr(hyperlink_button, "__signature__", inspect.signature(st.button))
