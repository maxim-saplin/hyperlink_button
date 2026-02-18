import streamlit as st

from hyperlink_button import hyperlink_button


st.set_page_config(page_title="hyperlink_button demo", layout="centered")

st.title("hyperlink_button")
st.caption("A Streamlit button that looks like a hyperlink.")

clicked = hyperlink_button("Click me", key="demo")
st.write({"clicked": clicked})

col1, col2 = st.columns(2)

with col1:
    st.subheader("Disabled")
    st.write(
        {"clicked": hyperlink_button("Can't click", key="disabled", disabled=True)}
    )

with col2:
    st.subheader("With tooltip")
    st.write(
        {
            "clicked": hyperlink_button(
                "Hover me",
                key="help",
                help="This should look like a link.",
            )
        }
    )
