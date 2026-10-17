"""
Theme tokens and CSS styles for the Student Budget Tracker.
Provides color constants, spacing, typography, and injects clean modern styling.
"""

# Color Palette (Minimal, friendly, high contrast)
COLORS = {
    "primary": "#3B82F6",         # Clean energetic blue
    "primary_hover": "#2563EB",
    "success": "#10B981",         # Green: safe budget (<80%)
    "warning": "#F59E0B",         # Yellow: budget warning (80-100%)
    "danger": "#EF4444",          # Red: budget exceeded (>100%)
    "income": "#10B981",          # Green for income
    "expense": "#EF4444",         # Red for expense
    "background_card": "#FFFFFF",
    "background_card_dark": "#1E293B",
    "text_primary": "#0F172A",
    "text_secondary": "#64748B",
    "border": "#E2E8F0",
}

CUSTOM_CSS = """
<style>
/* Responsive layout container */
.main .block-container {
    max-width: 680px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Card container for dashboard & stats */
.metric-card {
    background: var(--background-color, #ffffff);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.hero-number {
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin-top: 0.25rem;
    margin-bottom: 0.25rem;
}

.hero-subtext {
    font-size: 0.9rem;
    color: #64748B;
    margin-bottom: 0;
}

/* Large thumb-friendly buttons */
.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    transition: all 0.15s ease-in-out;
}

/* Number pad buttons */
div[data-testid="column"] button {
    min-height: 52px;
    font-size: 1.2rem;
    font-weight: 700;
}

/* Category chips */
.category-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 600;
    background: #EFF6FF;
    color: #1D4ED8;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* Progress bar labels */
.progress-meta {
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 4px;
}
</style>
"""

def inject_theme():
    """Inject custom CSS into Streamlit page."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
