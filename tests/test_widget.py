import textwrap

from streamlit.testing.v1 import AppTest


def test_hyperlink_button_returns_true_once(tmp_path) -> None:
    script = tmp_path / "app.py"
    script.write_text(
        textwrap.dedent(
            """
            import streamlit as st
            from hyperlink_button import hyperlink_button

            if "count" not in st.session_state:
                st.session_state.count = 0

            def bump():
                st.session_state.count += 1

            clicked = hyperlink_button("Tap", key="tap", on_click=bump)
            st.write("clicked", clicked)
            st.write("count", st.session_state.count)
            """
        )
    )

    app = AppTest.from_file(str(script))
    app.run()
    # hyperlink_button injects a marker+style block as the first markdown element
    assert app.markdown[1].value == "clicked `False`"
    assert app.markdown[2].value == "count `0`"

    app.button[0].click()
    app.run()

    assert app.markdown[1].value == "clicked `True`"
    assert app.markdown[2].value == "count `1`"

    app.run()
    assert app.markdown[1].value == "clicked `False`"
    assert app.markdown[2].value == "count `1`"


def test_hyperlink_button_click_returns_true_then_false(tmp_path) -> None:
    script = tmp_path / "app.py"
    script.write_text(
        textwrap.dedent(
            """
            import streamlit as st
            from hyperlink_button import hyperlink_button

            clicked = hyperlink_button("Tap", key="tap")
            st.write("clicked", clicked)
            """
        )
    )

    app = AppTest.from_file(str(script))
    app.run()
    assert app.markdown[1].value == "clicked `False`"

    app.button[0].click()
    app.run()
    assert app.markdown[1].value == "clicked `True`"

    app.run()
    assert app.markdown[1].value == "clicked `False`"
