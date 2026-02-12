import streamlit as st

from hyperlink_button import hyperlink_button


def main():
    st.title("Hyperlink Button Demo")
    st.write("This is a simple demo showing the hyperlink_button API.")

    # Basic usage: looks like a link but acts as a button
    clicked = hyperlink_button("Click me", key="hb1", help="This is a demo tooltip")
    st.write("Clicked? ", clicked)

    # Disabled state
    disabled_clicked = hyperlink_button("Disabled", key="hb2", disabled=True)
    st.write("Disabled clicked? ", disabled_clicked)


if __name__ == "__main__":
    main()
