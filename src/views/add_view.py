"""
Add Transaction View.
Optimized for rapid logging in under 5 seconds:
1. Amount input (number pad / quick addition buttons)
2. Category selector with visual icons
3. Optional note
4. One-tap save
"""
import streamlit as st
from datetime import date
from src.db.connection import get_connection
from src.repositories.category_repo import get_all_categories
from src.repositories.account_repo import get_all_accounts, get_default_account
from src.repositories.transaction_repo import create_transaction
from src.repositories.settings_repo import get_user_settings
from src.utils.currency import parse_to_cents, format_cents
from src.utils.date_helpers import get_today_date
from src.components.numpad import render_quick_amount_buttons

def render_add_view():
    conn = get_connection()
    settings = get_user_settings(conn)
    currency_symbol = settings.currency_symbol

    st.markdown("### ➕ Log a Transaction")
    st.caption("Fast expense or income entry — designed to take under 5 seconds.")

    # Transaction Type Toggle
    txn_type = st.radio(
        "Transaction Type",
        options=["expense", "income"],
        format_func=lambda x: "💸 Expense" if x == "expense" else "💰 Income",
        horizontal=True,
        label_visibility="collapsed",
    )

    # Initialize session state for amount if needed
    if "txn_amount_input" not in st.session_state:
        st.session_state["txn_amount_input"] = 0.0

    # Quick Amount Buttons
    render_quick_amount_buttons(state_key="txn_amount_input")

    # Main Amount Input
    amount_val = st.number_input(
        f"Amount ({currency_symbol})",
        min_value=0.0,
        max_value=100000.0,
        value=float(st.session_state["txn_amount_input"]),
        step=1.0,
        format="%.2f",
        key="amount_widget",
    )
    # Sync with session state
    st.session_state["txn_amount_input"] = amount_val

    # Clear amount quick button
    col_clear, _ = st.columns([1, 3])
    if col_clear.button("🔄 Clear Amount"):
        st.session_state["txn_amount_input"] = 0.0
        st.rerun()

    # Category Selection
    categories = get_all_categories(conn, type_filter=txn_type)
    if not categories:
        st.warning("No categories found for this type. Please check settings.")
        return

    category_labels = {f"{c.icon} {c.name}": c.id for c in categories}
    selected_cat_label = st.selectbox(
        "Choose Category",
        options=list(category_labels.keys()),
        index=0,
    )
    selected_cat_id = category_labels[selected_cat_label]

    # Date and Account selection (collapsible / secondary for speed)
    col_date, col_acc = st.columns(2)
    with col_date:
        txn_date = st.date_input("Date", value=get_today_date())
    with col_acc:
        accounts = get_all_accounts(conn)
        acc_labels = {a.name: a.id for a in accounts}
        selected_acc_name = st.selectbox("Account", options=list(acc_labels.keys()), index=0)
        selected_acc_id = acc_labels[selected_acc_name]

    # Optional Note
    note = st.text_input("Note (optional)", placeholder="e.g. Boba with friends, Textbook, Groceries")

    # Save Button
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.button("💾 Save Transaction", type="primary", use_container_width=True):
        cents = parse_to_cents(st.session_state["txn_amount_input"])
        if cents <= 0:
            st.error("Please enter an amount greater than 0.")
            return

        date_str = txn_date.strftime("%Y-%m-%d")
        txn_id = create_transaction(
            conn=conn,
            account_id=selected_acc_id,
            category_id=selected_cat_id,
            amount=cents,
            type=txn_type,
            date=date_str,
            note=note,
        )

        formatted_amt = format_cents(cents, symbol=currency_symbol)
        st.success(f"✅ Saved {formatted_amt} for {selected_cat_label}!")
        # Reset amount for next transaction
        st.session_state["txn_amount_input"] = 0.0
        st.rerun()
