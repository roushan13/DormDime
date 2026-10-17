"""
Budgets View.
Set and edit monthly limits per category with immediate comparison against actual spending.
"""
import streamlit as st
from src.db.connection import get_connection
from src.repositories.budget_repo import (
    get_budgets_for_month,
    set_category_budget,
    get_total_budget_limit_for_month,
)
from src.repositories.settings_repo import get_user_settings
from src.utils.currency import format_cents, parse_to_cents, cents_to_float
from src.utils.date_helpers import get_current_month_str
from src.components.progress_bar import render_category_budget_bar

def render_budgets_view():
    conn = get_connection()
    settings = get_user_settings(conn)
    currency_symbol = settings.currency_symbol

    st.markdown("### 🎯 Monthly Budgets")
    st.caption("Plan spending targets per category. Budgets reset each calendar month.")

    # Month Selector
    current_month = get_current_month_str()
    selected_month = st.text_input("Budget Month (YYYY-MM)", value=current_month)

    # Fetch budgets and current spending for selected month
    budgets = get_budgets_for_month(conn, selected_month)
    total_budget_limit = get_total_budget_limit_for_month(conn, selected_month)
    total_spent_this_month = sum(b.spent_amount for b in budgets)

    # Summary Row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Budget", format_cents(total_budget_limit, symbol=currency_symbol))
    col2.metric("Total Spent", format_cents(total_spent_this_month, symbol=currency_symbol))
    remaining = total_budget_limit - total_spent_this_month
    col3.metric("Remaining", format_cents(remaining, symbol=currency_symbol))

    st.markdown("---")
    st.markdown("#### Set Limits by Category")

    with st.form("budget_form"):
        new_limits = {}
        for b in budgets:
            col_info, col_input = st.columns([2, 1])
            with col_info:
                st.markdown(f"**{b.category_icon} {b.category_name}**")
                st.caption(f"Spent so far: {format_cents(b.spent_amount, symbol=currency_symbol)}")
            with col_input:
                current_limit_dollars = cents_to_float(b.limit_amount)
                val = st.number_input(
                    f"Limit ({currency_symbol})",
                    min_value=0.0,
                    max_value=50000.0,
                    value=float(current_limit_dollars),
                    step=10.0,
                    key=f"budget_input_{b.category_id}_{selected_month}",
                    label_visibility="collapsed",
                )
                new_limits[b.category_id] = val

        submit_budgets = st.form_submit_button("💾 Save All Budgets", type="primary", use_container_width=True)
        if submit_budgets:
            for cat_id, dollar_val in new_limits.items():
                cents_val = parse_to_cents(dollar_val)
                set_category_budget(conn, category_id=cat_id, month=selected_month, limit_amount=cents_val)
            st.success(f"✅ Budgets saved successfully for {selected_month}!")
            st.rerun()

    # Visual preview of progress bars
    st.markdown("---")
    st.markdown("#### Current Budget Progress")
    for b in budgets:
        if b.limit_amount > 0 or b.spent_amount > 0:
            render_category_budget_bar(
                category_name=b.category_name,
                category_icon=b.category_icon,
                spent_cents=b.spent_amount,
                limit_cents=b.limit_amount,
                currency_symbol=currency_symbol,
            )
