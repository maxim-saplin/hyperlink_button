from __future__ import annotations

import uuid
from collections.abc import Callable, Mapping, Sequence
from typing import Any, Literal

import streamlit as st


ButtonType = Literal["primary", "secondary", "tertiary"]
IconPosition = Literal["left", "right"]
Width = Literal["content", "stretch"] | int


def _scoped_style_block(scope_id: str) -> str:
    scope_container = (
        f'div[data-testid="stElementContainer"]:has(span[data-hyperlink-button-scope="{scope_id}"])'
    )
    target_button = (
        f'{scope_container} + div[data-testid="stElementContainer"] '
        f'div[data-testid="stButton"] button'
    )
    return f"""
<span data-hyperlink-button-scope=\"{scope_id}\" style=\"display:none\"></span>
<style>
{scope_container} {{
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}}

{target_button} {{
  background: transparent !important;
  border: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  min-height: auto !important;
  height: auto !important;
  line-height: 1.2 !important;
  color: var(--primary-color, #0066cc) !important;
  text-decoration: none !important;
}}

{target_button}:hover:not(:disabled) {{
  text-decoration: underline !important;
  text-underline-offset: 2px !important;
}}

{target_button}:focus-visible {{
  outline: 2px solid var(--primary-color, #0066cc) !important;
  outline-offset: 2px !important;
  border-radius: 3px !important;
  text-decoration: none !important;
}}

{target_button}:disabled {{
  opacity: 0.45 !important;
  cursor: not-allowed !important;
  text-decoration: none !important;
}}
</style>
""".strip()


def hyperlink_button(
    label: str,
    key: str | int | None = None,
    help: str | None = None,
    on_click: Callable[..., Any] | None = None,
    args: Sequence[Any] | None = None,
    kwargs: Mapping[str, Any] | None = None,
    *,
    type: ButtonType = "secondary",
    icon: str | None = None,
    icon_position: IconPosition = "left",
    disabled: bool = False,
    use_container_width: bool | None = None,
    width: Width = "content",
    shortcut: str | None = None,
) -> bool:
    """Drop-in replacement for `st.button` that renders like a text link.

    This intentionally keeps the same call signature as Streamlit's `st.button`.
    """
    scope_id = uuid.uuid4().hex
    st.markdown(_scoped_style_block(scope_id), unsafe_allow_html=True)
    return st.button(
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
