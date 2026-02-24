from __future__ import annotations

import inspect
import os
from collections.abc import Callable, Mapping, Sequence
from typing import Any

import streamlit as st
from streamlit.components.v1 import declare_component
from streamlit.errors import StreamlitAPIException


def _component_path() -> str | None:
    base_dir = os.path.dirname(__file__)
    build_dir = os.path.join(base_dir, "frontend", "build")
    if os.path.isdir(build_dir):
        return build_dir
    return None


def _create_component() -> Callable[..., Any]:
    path = _component_path()
    if path is not None:
        return declare_component("hyperlink_button", path=path)
    return declare_component("hyperlink_button", url="http://localhost:3001")


_hyperlink_button_component = _create_component()


def _stable_auto_key() -> str:
    frame = inspect.currentframe()
    while frame is not None:
        frame = frame.f_back
        if frame is None:
            break
        module_name = frame.f_globals.get("__name__", "")
        if module_name.startswith("hyperlink_button"):
            continue
        filename = os.path.abspath(frame.f_code.co_filename)
        lineno = frame.f_lineno
        function = frame.f_code.co_name
        return f"hyperlink_button::{filename}:{lineno}:{function}"
    return "hyperlink_button::unknown"


def _build_args(args: Sequence[Any] | None) -> list[Any]:
    if args is None:
        return []
    return list(args)


def _build_kwargs(kwargs: Mapping[str, Any] | None) -> dict[str, Any]:
    if kwargs is None:
        return {}
    return dict(kwargs)


def hyperlink_button(
    label: str,
    key: str | None = None,
    help: str | None = None,
    on_click: Callable[..., Any] | None = None,
    args: Sequence[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
    disabled: bool = False,
    use_container_width: bool | None = None,
    type: str = "secondary",
    icon: str | None = None,
    icon_position: str = "left",
    width: int | str = "content",
    shortcut: str | None = None,
) -> bool:
    """A link-styled button with `st.button`-like semantics.

    Returns True only for the script run triggered by a new click.
    """

    resolved_key = key or _stable_auto_key()

    allowed_types = {"primary", "secondary", "tertiary"}
    if type not in allowed_types:
        raise StreamlitAPIException(
            "Invalid `type`. Expected one of: 'primary', 'secondary', 'tertiary'."
        )

    allowed_icon_positions = {"left", "right"}
    if icon_position not in allowed_icon_positions:
        raise StreamlitAPIException("Invalid `icon_position`. Expected 'left' or 'right'.")

    if width != "content" and width != "stretch" and not isinstance(width, int):
        raise StreamlitAPIException(
            "Invalid `width`. Expected 'content', 'stretch', or an int (pixels)."
        )

    result = _hyperlink_button_component(
        label=label,
        help=help,
        disabled=disabled,
        use_container_width=bool(use_container_width) if use_container_width is not None else False,
        type=type,
        icon=icon,
        icon_position=icon_position,
        width=width,
        shortcut=shortcut,
        key=resolved_key,
        default={"click_id": ""},
    )

    click_id = ""
    if isinstance(result, dict):
        click_id = str(result.get("click_id") or "")

    last_key = "__hyperlink_button_last_click_id__"
    last_click_map = st.session_state.get(last_key)
    if not isinstance(last_click_map, dict):
        last_click_map = {}
        st.session_state[last_key] = last_click_map

    last_click_id = str(last_click_map.get(resolved_key, ""))
    clicked = click_id != "" and click_id != last_click_id
    if clicked:
        last_click_map[resolved_key] = click_id
        st.session_state[last_key] = last_click_map
        if on_click is not None:
            on_click(*_build_args(args), **_build_kwargs(kwargs))

    return clicked
