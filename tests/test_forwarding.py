from __future__ import annotations

from contextlib import contextmanager
from typing import Any

import hyperlink_button._widget as widget


class _DummyStreamlit:
    def __init__(self) -> None:
        self.markdown_calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        self.button_calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def markdown(self, *args: Any, **kwargs: Any) -> None:
        self.markdown_calls.append((args, kwargs))

    def button(self, *args: Any, **kwargs: Any) -> bool:
        self.button_calls.append((args, kwargs))
        return True


def test_forwards_all_params(monkeypatch) -> None:
    dummy = _DummyStreamlit()
    monkeypatch.setattr(widget, "st", dummy)

    def _cb() -> None:
        return None

    out = widget.hyperlink_button(
        "Label",
        key="k",
        help="help",
        on_click=_cb,
        args=(1, 2),
        kwargs={"x": 3},
        type="primary",
        icon=":material/link:",
        icon_position="right",
        disabled=True,
        use_container_width=None,
        width="stretch",
        shortcut="Ctrl+K",
    )

    assert out is True
    assert len(dummy.markdown_calls) == 1
    assert len(dummy.button_calls) == 1

    (call_args, call_kwargs) = dummy.button_calls[0]
    assert call_args == ("Label",)
    assert call_kwargs["key"] == "k"
    assert call_kwargs["help"] == "help"
    assert call_kwargs["on_click"] is _cb
    assert call_kwargs["args"] == (1, 2)
    assert call_kwargs["kwargs"] == {"x": 3}
    assert call_kwargs["type"] == "primary"
    assert call_kwargs["icon"] == ":material/link:"
    assert call_kwargs["icon_position"] == "right"
    assert call_kwargs["disabled"] is True
    assert call_kwargs["use_container_width"] is None
    assert call_kwargs["width"] == "stretch"
    assert call_kwargs["shortcut"] == "Ctrl+K"
