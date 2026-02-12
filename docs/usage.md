# Hyperlink Button Usage

- API mirrors `st.button`:
  - `hyperlink_button(label, key=None, help=None, on_click=None, args=None, kwargs=None, *, type='secondary', icon=None, icon_position='left', disabled=False, use_container_width=None, width='content', shortcut=None)`
- Visually a hoverable text link; click triggers a Streamlit rerun.
- Returns `True` only on the click-run, otherwise `False`.
