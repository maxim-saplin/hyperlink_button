from hyperlink_button.core import build_hyperlink_html
from hyperlink_button.widget import _style_block


def test_build_style_block_scopes_to_marker() -> None:
    style = _style_block("marker-123")
    assert "marker-123" in style


def test_build_hyperlink_html_escapes_content() -> None:
    html = build_hyperlink_html("Click <me>", "https://example.com?q=1&x=2")
    assert "Click &lt;me&gt;" in html
    assert "https://example.com?q=1&amp;x=2" in html


def test_build_hyperlink_html_disabled_markup() -> None:
    html = build_hyperlink_html("Click", "https://example.com", disabled=True)
    assert "hb-disabled" in html
    assert "aria-disabled=\"true\"" in html
