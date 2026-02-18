from __future__ import annotations

from html import escape

STYLE_BLOCK = """
<style>
:root {
  --hb-primary: #25425f;
  --hb-primary-text: #f7f2e8;
  --hb-border: #25425f;
  --hb-shadow: rgba(18, 31, 43, 0.18);
}

.hb-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.65rem 1.1rem;
  border-radius: 999px;
  border: 1px solid var(--hb-border);
  font-weight: 600;
  text-decoration: none;
  letter-spacing: 0.01em;
  transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
  box-shadow: 0 10px 18px -16px var(--hb-shadow);
}

.hb-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 16px 22px -16px var(--hb-shadow);
}

.hb-primary {
  background: var(--hb-primary);
  color: var(--hb-primary-text);
}

.hb-ghost {
  background: transparent;
  color: var(--hb-primary);
}

.hb-disabled {
  opacity: 0.5;
  pointer-events: none;
}
</style>
""".strip()


def build_style_block() -> str:
    return STYLE_BLOCK


def build_hyperlink_html(
    label: str,
    url: str,
    *,
    variant: str = "primary",
    disabled: bool = False,
) -> str:
    safe_label = escape(label)
    safe_url = escape(url, quote=True)
    safe_variant = escape(variant)
    disabled_attr = " aria-disabled=\"true\"" if disabled else ""
    disabled_class = " hb-disabled" if disabled else ""
    disabled_tab = " tabindex=\"-1\"" if disabled else ""
    return (
        "<a class=\"hb-button hb-"
        + safe_variant
        + disabled_class
        + "\" href=\""
        + safe_url
        + "\" target=\"_blank\" rel=\"noopener noreferrer\""
        + disabled_attr
        + disabled_tab
        + ">"
        + safe_label
        + "</a>"
    )


def render_hyperlink_button(
    label: str,
    url: str,
    *,
    variant: str = "primary",
) -> None:
    import streamlit as st

    st.markdown(build_style_block(), unsafe_allow_html=True)
    st.markdown(build_hyperlink_html(label, url, variant=variant), unsafe_allow_html=True)
