"""
Number pad and quick amount selector for ultra-fast logging (< 5s).
"""
import streamlit as st

def render_quick_amount_buttons(state_key: str = "txn_amount_str"):
    """
    Renders quick increment buttons: +$1, +$5, +$10, +$20, +$50.
    """
    st.write("**Quick Add Amounts**")
    cols = st.columns(5)
    increments = [1.0, 5.0, 10.0, 20.0, 50.0]
    
    current_val = float(st.session_state.get(state_key, 0.0) or 0.0)
    for col, inc in zip(cols, increments):
        if col.button(f"+${int(inc)}", key=f"btn_inc_{inc}", use_container_width=True):
            st.session_state[state_key] = round(current_val + inc, 2)
            st.rerun()
