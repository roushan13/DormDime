"""
Reusable UI card components.
"""
import streamlit as st

def render_hero_metric(label: str, value_formatted: str, subtext: str, color: str = "#10B981"):
    """
    Renders the prominent 'Safe to spend today' or summary hero card.
    """
    st.markdown(
        f"""
        <div class="metric-card">
            <span style="font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B;">
                {label}
            </span>
            <div class="hero-number" style="color: {color};">
                {value_formatted}
            </div>
            <p class="hero-subtext">{subtext}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_summary_pills(left_label: str, left_value: str, right_label: str, right_value: str):
    """
    Renders two compact summary cards side-by-side.
    """
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card" style="padding: 1rem;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B;">{left_label}</div>
                <div style="font-size: 1.3rem; font-weight: 700;">{left_value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card" style="padding: 1rem;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #64748B;">{right_label}</div>
                <div style="font-size: 1.3rem; font-weight: 700;">{right_value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
