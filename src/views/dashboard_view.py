"""
Home Dashboard View.
Renders:
1. Big 'Safe to spend today' hero metric
2. Monthly budget summary & progress
3. Category progress bars (green = safe, yellow = 80% of limit, red = over)
4. Recent 5 transactions
"""
import streamlit as st
from datetime import datetime
from src.db.connection import get_connection
from src.repositories.budget_repo import (
    get_budgets_for_month,
    get_total_budget_limit_for_month,
)
from src.repositories.transaction_repo import (
    get_monthly_totals,
    list_transactions,
)
from src.repositories.settings_repo import get_user_settings
from src.utils.safe_to_spend import calculate_safe_to_spend
from src.utils.currency import format_cents
from src.utils.date_helpers import (
    get_current_month_str,
    get_days_remaining_in_month,
    get_today_date,
)
from src.components.cards import render_hero_metric, render_summary_pills
from src.components.progress_bar import render_category_budget_bar

def render_dashboard_view():
    conn = get_connection()
    settings = get_user_settings(conn)
    currency_symbol = settings.currency_symbol

    current_month = get_current_month_str()
    today = get_today_date()
    days_left = get_days_remaining_in_month(today)
    month_name = today.strftime("%B %Y")

    # Fetch financial figures for current month
    total_income_cents, total_expense_cents = get_monthly_totals(conn, current_month)
    total_budget_limit = get_total_budget_limit_for_month(conn, current_month)

    # If no budget is set, fallback to monthly income if provided in onboarding
    effective_budget_limit = total_budget_limit if total_budget_limit > 0 else settings.monthly_income

    # Calculate safe to spend today
    safe_to_spend_cents = calculate_safe_to_spend(
        total_budget_limit=effective_budget_limit,
        total_spent_this_month=total_expense_cents,
        days_remaining=days_left,
    )

    remaining_budget_cents = effective_budget_limit - total_expense_cents

    # Hero Card: Safe to Spend Today
    if effective_budget_limit > 0:
        if remaining_budget_cents > 0:
            subtext = f"Based on {format_cents(remaining_budget_cents, currency_symbol)} remaining across {days_left} day{'s' if days_left != 1 else ''} left in {month_name}"
            color = "#10B981"  # Clean green
        else:
            subtext = f"⚠️ Monthly budget exceeded by {format_cents(abs(remaining_budget_cents), currency_symbol)}"
            color = "#EF4444"  # Red alert
    else:
        subtext = "Set your category limits in '🎯 Budgets' to unlock your daily safe spend guide."
        color = "#3B82F6"

    render_hero_metric(
        label="Safe to Spend Today",
        value_formatted=format_cents(safe_to_spend_cents, currency_symbol),
        subtext=subtext,
        color=color,
    )

    # Monthly Summary Row
    render_summary_pills(
        left_label="Total Budget",
        left_value=format_cents(effective_budget_limit, currency_symbol),
        right_label="Spent So Far",
        right_value=format_cents(total_expense_cents, currency_symbol),
    )

    # Category Progress Bars
    st.markdown("#### 🎯 Category Budgets")
    budgets = get_budgets_for_month(conn, current_month)
    active_budgets = [b for b in budgets if b.limit_amount > 0 or b.spent_amount > 0]

    if active_budgets:
        for b in active_budgets:
            render_category_budget_bar(
                category_name=b.category_name,
                category_icon=b.category_icon,
                spent_cents=b.spent_amount,
                limit_cents=b.limit_amount,
                currency_symbol=currency_symbol,
            )
    else:
        st.info("No category budgets configured yet. Visit the **🎯 Budgets** tab to set monthly limits.")

    # Recent Transactions Section
    st.markdown("#### 🕒 Recent Transactions")
    recent_txns = list_transactions(conn, limit=5)

    if recent_txns:
        for txn in recent_txns:
            is_expense = txn.type == "expense"
            amt_color = "#EF4444" if is_expense else "#10B981"
            sign = "-" if is_expense else "+"
            amt_display = f"{sign}{format_cents(txn.amount, currency_symbol)}"
            note_str = f" • <i>{txn.note}</i>" if txn.note else ""

            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: #FAFAFA; border: 1px solid #E2E8F0; border-radius: 10px; margin-bottom: 6px;">
                    <div>
                        <div style="font-weight: 600; font-size: 0.9rem;">
                            {txn.category_icon or '📁'} {txn.category_name or 'General'} {note_str}
                        </div>
                        <div style="font-size: 0.75rem; color: #64748B;">
                            {txn.date}
                        </div>
                    </div>
                    <div style="font-size: 1rem; font-weight: 700; color: {amt_color};">
                        {amt_display}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.caption("No recent transactions. Tap **➕ Add** to log your first expense!")
