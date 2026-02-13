import streamlit as st

from hyperlink_button import hyperlink_button


def main():
    st.title("Hyperlink Button Demo")
    st.write("This is a simple demo showing the hyperlink_button API.")

    # Initialize or get the current click counter from session state
    if "click_count" not in st.session_state:
        st.session_state.click_count = 0

    # Basic usage: looks like a link but acts as a button
    clicked = hyperlink_button("Click me", key="hb1", help="This is a demo tooltip")
    if clicked:
        st.session_state.click_count += 1

    st.write("Click count:", st.session_state.click_count)

    # Disabled state
    disabled_clicked = hyperlink_button("Disabled", key="hb2", disabled=True)
    st.write("Disabled clicked? ", disabled_clicked)


if __name__ == "__main__":
    main()
