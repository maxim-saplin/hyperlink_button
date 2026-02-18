from __future__ import annotations

from pathlib import Path
from typing import Literal

import streamlit.components.v1 as components


_RELEASE = True


def _component() -> components.CustomComponent:
    if not _RELEASE:
        return components.declare_component(
            "hyperlink_button",
            url="http://localhost:5173",
        )

    build_dir = Path(__file__).parent / "frontend" / "dist"
    return components.declare_component(
        "hyperlink_button",
        path=str(build_dir),
    )


_hyperlink_button = _component()


ButtonType = Literal["primary", "secondary", "tertiary"]


def hyperlink_button(
    label: str,
    key: str | int | None = None,
    help: str | None = None,
    on_click=None,
    args=None,
    kwargs=None,
    *,
    type: ButtonType = "secondary",
    icon: str | None = None,
    icon_position: Literal["left", "right"] = "left",
    disabled: bool = False,
    use_container_width: bool | None = None,
    width: Literal["content", "stretch"] | int = "content",
    shortcut: str | None = None,
) -> bool:
    """A Streamlit button widget that looks like a hyperlink.

    This aims to mirror the public API of `st.button` while rendering as a
    link-styled control.
    """

    if use_container_width is not None:
        width = "stretch" if use_container_width else "content"

    if type not in {"primary", "secondary", "tertiary"}:
        raise ValueError(
            'The type argument to hyperlink_button must be "primary", "secondary", or "tertiary".'
        )

    # We intentionally do not attempt to participate in Streamlit's internal
    # element ID computation. Custom components always register as
    # "component_instance" widgets.
    value = _hyperlink_button(
        label=label,
        help=help,
        type=type,
        icon=icon,
        icon_position=icon_position,
        disabled=disabled,
        width=width,
        shortcut=shortcut,
        default=False,
        key=None if key is None else str(key),
        on_change=on_click,
    )

    # Our frontend returns a boolean 'true' on click (a trigger).
    return bool(value)
