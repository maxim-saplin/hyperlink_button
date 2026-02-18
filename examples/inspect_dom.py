import streamlit as st

from hyperlink_button import hyperlink_button


st.set_page_config(page_title="Inspect DOM", layout="centered")

st.write("Inspect DOM for st.button and hyperlink_button.")

st.header("Buttons")

clicked_a = st.button("A default", key="a_default")
st.write({"clicked_a": clicked_a})

clicked_b = st.button("B tertiary", key="b_tertiary", type="tertiary")
st.write({"clicked_b": clicked_b})

clicked_c = st.button("C tertiary 2", key="c_tertiary", type="tertiary", help="tooltip")
st.write({"clicked_c": clicked_c})

st.header("hyperlink_button")

clicked_h = hyperlink_button("H hyperlink", key="h")
st.write({"clicked_h": clicked_h})
