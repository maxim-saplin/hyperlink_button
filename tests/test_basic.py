import inspect

import streamlit as st

from hyperlink_button import hyperlink_button


def test_hyperlink_button_signature_matches_streamlit() -> None:
    assert inspect.signature(hyperlink_button) == inspect.signature(st.button)


def test_hyperlink_button_forwards_arguments_to_st_button() -> None:
    class StreamlitStub:
        def __init__(self) -> None:
            self.calls: list[tuple[str, tuple[object, ...], dict[str, object]]] = []

        def markdown(self, *args: object, **kwargs: object) -> None:
            self.calls.append(("markdown", args, kwargs))

        def html(self, *args: object, **kwargs: object) -> None:
            self.calls.append(("html", args, kwargs))

        def button(self, *args: object, **kwargs: object) -> bool:
            self.calls.append(("button", args, kwargs))
            return True

    def handle_click() -> None:
        return None

    stub = StreamlitStub()
    original = hyperlink_button.__globals__["st"]
    hyperlink_button.__globals__["st"] = stub
    try:
        result = hyperlink_button(
            "Docs",
            key="a",
            help="help",
            on_click=handle_click,
            args=("one", 2),
            kwargs={"alpha": 1},
            type="primary",
            icon=":material/link:",
            icon_position="right",
            disabled=True,
            use_container_width=True,
            width=200,
            shortcut="CTRL+K",
        )
    finally:
        hyperlink_button.__globals__["st"] = original

    assert result is True
    # We expect a single marker+style emission before the button
    assert len(stub.calls) == 2
    # We now emit the marker+style via `markdown` with unsafe HTML
    assert stub.calls[0][0] == "markdown"
    assert stub.calls[1] == (
        "button",
        ("Docs",),
        {
            "key": "a",
            "help": "help",
            "on_click": handle_click,
            "args": ("one", 2),
            "kwargs": {"alpha": 1},
            "type": "primary",
            "icon": ":material/link:",
            "icon_position": "right",
            "disabled": True,
            "use_container_width": True,
            "width": 200,
            "shortcut": "CTRL+K",
        },
    )
