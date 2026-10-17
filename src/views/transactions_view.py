"""
Transactions List View.
Provides searchable, filterable transaction history with date, category, and type filters,
summary statistics, and quick deletion.
"""
import streamlit as st
from datetime import date, timedelta
from src.db.connection import get_connection
from src.repositories.category_repo import get_all_categories
from src.repositories.transaction_repo import list_transactions, delete_transaction
from src.repositories.settings_repo import get_user_settings
from src.utils.currency import format_cents
from src.utils.date_helpers import get_today_date

def render_transactions_view():
    conn = get_connection()
    settings = get_user_settings(conn)
    currency_symbol = settings.currency_symbol

    st.markdown("### 📋 Transaction History")

    # Search Bar
    search_query = st.text_input("🔍 Search transactions", placeholder="Filter by note or category name...")

    # Filter Controls
    col_type, col_cat, col_date = st.columns([1, 1, 1])

    with col_type:
        type_options = ["all", "expense", "income"]
        selected_type = st.selectbox(
            "Type",
            options=type_options,
            format_func=lambda x: "All Types" if x == "all" else x.capitalize(),
        )

    with col_cat:
        all_cats = get_all_categories(conn)
        cat_choices = {"All Categories": None}
        for c in all_cats:
            cat_choices[f"{c.icon} {c.name}"] = c.id
        selected_cat_label = st.selectbox("Category", options=list(cat_choices.keys()))
        selected_cat_id = cat_choices[selected_cat_label]

    with col_date:
        date_filter_preset = st.selectbox(
            "Date Range",
            options=["This Month", "Last 30 Days", "This Year", "All Time", "Custom"],
        )

    # Resolve date boundaries
    today = get_today_date()
    start_date = None
    end_date = None

    if date_filter_preset == "This Month":
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif date_filter_preset == "Last 30 Days":
        start_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif date_filter_preset == "This Year":
        start_date = today.replace(month=1, day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif date_filter_preset == "Custom":
        col_s, col_e = st.columns(2)
        with col_s:
            s_val = st.date_input("Start Date", value=today - timedelta(days=7))
            start_date = s_val.strftime("%Y-%m-%d")
        with col_e:
            e_val = st.date_input("End Date", value=today)
            end_date = e_val.strftime("%Y-%m-%d")

    # Query filtered transactions
    txns = list_transactions(
        conn=conn,
        search_query=search_query if search_query.strip() else None,
        category_id=selected_cat_id,
        type_filter=selected_type,
        start_date=start_date,
        end_date=end_date,
    )

    # Summary Stats for Current Filter
    total_spent_cents = sum(t.amount for t in txns if t.type == "expense")
    total_income_cents = sum(t.amount for t in txns if t.type == "income")
    net_cents = total_income_cents - total_spent_cents

    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Items Found", len(txns))
    col_s2.metric("Total Spent", format_cents(total_spent_cents, symbol=currency_symbol))
    col_s3.metric("Net Flow", format_cents(net_cents, symbol=currency_symbol))

    st.markdown("---")

    if not txns:
        st.info("No transactions found matching your criteria. Try adjusting the filters or adding one!")
        return

    # Render Transaction Cards
    for txn in txns:
        is_expense = txn.type == "expense"
        color = "#EF4444" if is_expense else "#10B981"
        sign = "-" if is_expense else "+"
        amt_str = f"{sign}{format_cents(txn.amount, symbol=currency_symbol)}"

        card_col, del_col = st.columns([5, 1])

        with card_col:
            cat_icon = txn.category_icon or "📁"
            cat_name = txn.category_name or "Unknown"
            note_str = f" • <i>{txn.note}</i>" if txn.note else ""
            acc_str = f"<span style='background: #F1F5F9; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; color: #475569;'>{txn.account_name or 'Cash'}</span>"

            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: #FAFAFA; border: 1px solid #E2E8F0; border-radius: 12px; margin-bottom: 8px;">
                    <div>
                        <div style="font-weight: 700; font-size: 0.95rem;">
                            {cat_icon} {cat_name} {note_str}
                        </div>
                        <div style="font-size: 0.75rem; color: #64748B; margin-top: 2px;">
                            {txn.date} &nbsp;{acc_str}
                        </div>
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 800; color: {color};">
                        {amt_str}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with del_col:
            # Delete button
            if st.button("🗑️", key=f"del_txn_{txn.id}", help="Delete transaction"):
                delete_transaction(conn, txn.id)
                st.rerun()
