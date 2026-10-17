"""
Insights & Visual Analytics View.
Provides:
1. Category spending distribution (interactive Plotly donut chart)
2. Monthly trend comparison (expenses vs income bar chart)
3. Breakdown summary table
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.db.connection import get_connection
from src.repositories.transaction_repo import (
    get_spending_by_category,
    get_monthly_trend,
    get_monthly_totals,
)
from src.repositories.settings_repo import get_user_settings
from src.utils.currency import format_cents, cents_to_float
from src.utils.date_helpers import get_current_month_str

def render_insights_view():
    conn = get_connection()
    settings = get_user_settings(conn)
    currency_symbol = settings.currency_symbol

    st.markdown("### 📊 Financial Insights")
    st.caption("Visual breakdowns of your spending habits and income trends.")

    # Month Selector for Breakdown
    current_month = get_current_month_str()
    selected_month = st.text_input("Analysis Month (YYYY-MM)", value=current_month, key="insights_month")

    # Fetch Category Breakdown
    cat_spending = get_spending_by_category(conn, selected_month)
    total_income_cents, total_expense_cents = get_monthly_totals(conn, selected_month)

    # Top metrics for the month
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Expenses", format_cents(total_expense_cents, symbol=currency_symbol))
    col2.metric("Total Income", format_cents(total_income_cents, symbol=currency_symbol))
    savings_cents = total_income_cents - total_expense_cents
    col3.metric("Net Savings", format_cents(savings_cents, symbol=currency_symbol))

    st.markdown("---")

    # 1. Spending by Category (Donut Chart)
    st.markdown("#### 🍩 Spending by Category")
    if cat_spending:
        chart_data = []
        for item in cat_spending:
            chart_data.append({
                "Category": f"{item['icon']} {item['category_name']}",
                "Amount": cents_to_float(item["total_spent"]),
                "Color": item["color"],
            })

        df_cat = pd.DataFrame(chart_data)

        fig_donut = px.pie(
            df_cat,
            values="Amount",
            names="Category",
            hole=0.55,
            color="Category",
            color_discrete_sequence=[item["color"] for item in cat_spending],
        )
        fig_donut.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>" + currency_symbol + "%{value:,.2f}<br>%{percent}",
        )
        fig_donut.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            height=320,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

        # Tabular breakdown
        st.markdown("**Category Breakdown Table**")
        breakdown_rows = []
        for item in cat_spending:
            spent_cents = item["total_spent"]
            pct = (spent_cents / total_expense_cents * 100) if total_expense_cents > 0 else 0
            breakdown_rows.append({
                "Category": f"{item['icon']} {item['category_name']}",
                "Amount": format_cents(spent_cents, currency_symbol),
                "Share": f"{pct:.1f}%",
            })
        st.dataframe(pd.DataFrame(breakdown_rows), use_container_width=True, hide_index=True)
    else:
        st.info(f"No expense transactions logged in {selected_month} yet to display a category breakdown.")

    st.markdown("---")

    # 2. Monthly Trend (Past 6 Months)
    st.markdown("#### 📈 Income vs Expenses Trend")
    trend_data = get_monthly_trend(conn, limit_months=6)

    if trend_data:
        months = [t["month"] for t in trend_data]
        expenses = [cents_to_float(t["total_expense"]) for t in trend_data]
        incomes = [cents_to_float(t["total_income"]) for t in trend_data]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=months,
            y=incomes,
            name="Income",
            marker_color="#10B981",
        ))
        fig_trend.add_trace(go.Bar(
            x=months,
            y=expenses,
            name="Expense",
            marker_color="#EF4444",
        ))

        fig_trend.update_layout(
            barmode="group",
            margin=dict(t=20, b=20, l=20, r=20),
            height=320,
            xaxis_title="Month",
            yaxis_title=f"Amount ({currency_symbol})",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Log transactions across different dates to see your trend analysis.")
