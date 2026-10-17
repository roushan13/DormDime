"""
Category progress bar component with reactive color-coding:
- Green: < 80% of budget limit (Safe)
- Yellow: 80% - 100% of budget limit (Warning)
- Red: > 100% of budget limit (Exceeded)
"""
import streamlit as st
from src.utils.safe_to_spend import get_budget_status
from src.utils.currency import format_cents

STATUS_COLORS = {
    "safe": "#10B981",     # Clean green
    "warning": "#F59E0B",  # Warning yellow
    "danger": "#EF4444",   # Alert red
}

def render_category_budget_bar(
    category_name: str,
    category_icon: str,
    spent_cents: int,
    limit_cents: int,
    currency_symbol: str = "$"
):
    """
    Renders an individual category progress bar with status color and spent/limit labels.
    """
    status = get_budget_status(spent_cents, limit_cents)
    color = STATUS_COLORS[status]

    spent_str = format_cents(spent_cents, symbol=currency_symbol)
    limit_str = format_cents(limit_cents, symbol=currency_symbol)

    if limit_cents > 0:
        percent = min(100, int((spent_cents / limit_cents) * 100))
        ratio_label = f"{spent_str} of {limit_str} ({int((spent_cents / limit_cents) * 100)}%)"
        bar_fill_width = min(100, int((spent_cents / limit_cents) * 100))
    else:
        ratio_label = f"{spent_str} spent (No limit set)"
        bar_fill_width = 100 if spent_cents > 0 else 0
        if spent_cents > 0:
            color = "#94A3B8"

    # HTML progress bar
    st.markdown(
        f"""
        <div style="margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;">
                <span>{category_icon} {category_name}</span>
                <span style="color: {color}; font-weight: 700;">{ratio_label}</span>
            </div>
            <div style="width: 100%; height: 10px; background-color: #E2E8F0; border-radius: 999px; overflow: hidden;">
                <div style="width: {bar_fill_width}%; height: 100%; background-color: {color}; border-radius: 999px; transition: width 0.3s ease;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
