"""
Diagnostic app to test click behavior with various scenarios.
This app includes counters and timing information to help diagnose sporadic click issues.
"""
import streamlit as st
import time
from datetime import datetime

from hyperlink_button import hyperlink_button

st.set_page_config(page_title="Click Diagnostics", layout="wide")

# Initialize session state for tracking clicks
if "click_history" not in st.session_state:
    st.session_state.click_history = []
if "total_clicks" not in st.session_state:
    st.session_state.total_clicks = 0

st.title("🔍 Hyperlink Button Click Diagnostics")

st.markdown("""
This app helps diagnose sporadic clicking issues by:
1. Tracking all click events with timestamps
2. Showing click history
3. Testing rapid successive clicks
4. Monitoring click count consistency
""")

# Test 1: Basic click tracking
st.header("Test 1: Basic Click Tracking")
col1, col2 = st.columns(2)

with col1:
    clicked1 = hyperlink_button(
        "Click Me (Test 1)",
        key="test1",
        help="Basic click test"
    )
    
with col2:
    st.markdown(f"<div data-testid='test1-state'>State: {clicked1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div data-testid='test1-count'>Count: {st.session_state.total_clicks}</div>", unsafe_allow_html=True)

if clicked1:
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    st.session_state.click_history.append(("test1", timestamp))
    st.session_state.total_clicks += 1
    st.success(f"✅ Click registered at {timestamp}")

# Test 2: Multiple buttons
st.header("Test 2: Multiple Buttons")
col3, col4, col5 = st.columns(3)

with col3:
    clicked2 = hyperlink_button("Button A", key="test2a", type="primary")
    if clicked2:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        st.session_state.click_history.append(("test2a", timestamp))
        st.write(f"A clicked: {timestamp}")

with col4:
    clicked3 = hyperlink_button("Button B", key="test2b", type="secondary")
    if clicked3:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        st.session_state.click_history.append(("test2b", timestamp))
        st.write(f"B clicked: {timestamp}")

with col5:
    clicked4 = hyperlink_button("Button C", key="test2c", type="tertiary")
    if clicked4:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        st.session_state.click_history.append(("test2c", timestamp))
        st.write(f"C clicked: {timestamp}")

st.markdown(f"""
<div data-testid='multi-button-state'>
A={clicked2}, B={clicked3}, C={clicked4}
</div>
""", unsafe_allow_html=True)

# Test 3: Click counter with visual feedback
st.header("Test 3: Click Counter")
if "counter" not in st.session_state:
    st.session_state.counter = 0

counter_clicked = hyperlink_button(
    f"Increment Counter (Current: {st.session_state.counter})",
    key="counter_btn",
    type="primary"
)

if counter_clicked:
    st.session_state.counter += 1
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    st.session_state.click_history.append(("counter", timestamp))
    st.info(f"Counter incremented to {st.session_state.counter} at {timestamp}")

st.markdown(f"<div data-testid='counter-value'>{st.session_state.counter}</div>", unsafe_allow_html=True)

# Click History
st.header("📊 Click History")
st.markdown(f"<div data-testid='history-count'>Total events: {len(st.session_state.click_history)}</div>", unsafe_allow_html=True)

if st.session_state.click_history:
    st.write("Recent clicks (last 10):")
    for i, (btn_id, ts) in enumerate(reversed(st.session_state.click_history[-10:])):
        st.text(f"{len(st.session_state.click_history) - i}. {btn_id} at {ts}")
else:
    st.info("No clicks recorded yet")

# Reset button
if st.button("🔄 Reset History"):
    st.session_state.click_history = []
    st.session_state.total_clicks = 0
    st.session_state.counter = 0
    st.rerun()
