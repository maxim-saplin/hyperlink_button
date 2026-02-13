"""
Simple demo showing Solution 3: Sync Counter working correctly.
This demonstrates that clicks register immediately after iframe remount.
"""
import streamlit as st
from hyperlink_button import hyperlink_button

st.title("Solution 3: Sync Counter - Demo")

st.markdown("""
### Test Instructions

1. Click the button below several times
2. Note the counter value
3. **Reload the page** (Ctrl+R or F5)
4. Click the button again
5. Notice that the click registers **immediately** (no double-click needed!)

This demonstrates that Solution 3 correctly syncs the counter across iframe remounts.
""")

# Counter to track total clicks
if "click_count" not in st.session_state:
    st.session_state.click_count = 0

# Button with counter
if hyperlink_button("Click Me!", key="test_button"):
    st.session_state.click_count += 1
    st.success(f"Button clicked! Total clicks: {st.session_state.click_count}")

# Display current count
st.metric("Total Clicks", st.session_state.click_count)

st.markdown("""
---
### How Solution 3 Works

**Before the fix (Bug):**
- Click button 5 times → counter reaches 5
- Page reload → React counter resets to 0, Python last_seen stays at 5
- Next click → counter goes 0→1, but 1 !> 5, so click is **ignored** ❌
- Had to click 5 more times to get past the threshold

**After the fix (Solution 3):**
- Click button 5 times → counter reaches 5, saved to session state
- Page reload → React counter restored from session state to 5
- Next click → counter goes 5→6, and 6 > 5, so click **registers immediately** ✅
- Single click works every time!

The key is that the counter value is persisted in Python's session state and
restored to the React component on mount, keeping both sides in perfect sync.
""")
